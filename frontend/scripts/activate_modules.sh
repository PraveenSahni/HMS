#!/bin/bash
set -u
CONF=/opt/gnuhealth/his-50/etc/trytond.conf
DB=gnuhealth
VENV=/opt/gnuhealth/his-50/venv
LOG=/tmp/module_activate.log
REPORT=/tmp/module_activate_report.txt
export PATH="$VENV/bin:$PATH"

exec > >(tee -a "$LOG") 2>&1
echo "===== START $(date -Is) ====="

mark() {
  local mods="$1"
  sudo -u postgres psql -d "$DB" -v ON_ERROR_STOP=1 -c "
    UPDATE ir_module SET state = 'to activate'
    WHERE state = 'not activated' AND name = ANY(string_to_array('$mods', ','));
  "
}

activate_batch() {
  local name="$1"
  local mods="$2"
  echo ""
  echo "===== BATCH: $name ($(date -Is)) ====="
  echo "Modules: $mods"
  mark "$mods" || { echo "FAIL mark $name"; echo "$name|MARK_FAIL|$mods" >> "$REPORT"; return 1; }
  if trytond-admin -c "$CONF" -d "$DB" --all; then
    echo "OK batch $name"
    echo "$name|OK|$mods" >> "$REPORT"
    return 0
  else
    echo "FAIL batch $name — resetting leftover to activate"
    sudo -u postgres psql -d "$DB" -c "UPDATE ir_module SET state='not activated' WHERE state='to activate';"
    echo "$name|FAIL|$mods" >> "$REPORT"
    return 1
  fi
}

activate_one() {
  local mod="$1"
  echo ""
  echo "===== ONE: $mod ($(date -Is)) ====="
  mark "$mod" || return 1
  if trytond-admin -c "$CONF" -d "$DB" --all; then
    echo "OK $mod"
    echo "one|$mod|OK" >> "$REPORT"
    return 0
  else
    echo "FAIL $mod"
    sudo -u postgres psql -d "$DB" -c "UPDATE ir_module SET state='not activated' WHERE state='to activate';"
    echo "one|$mod|FAIL" >> "$REPORT"
    return 1
  fi
}

: > "$REPORT"

# Phase 0: Tryton deps for stock/billing
activate_batch "tryton_deps" "account,account_product,account_invoice,stock,stock_lot" || true

# Phase 1: Core clinical for React UI
CORE="health_lab,health_nursing,health_inpatient,health_surgery,health_imaging,health_icu,health_gyneco,health_pediatrics,health_lifestyle,health_socioeconomics,health_history,health_disability,health_ophthalmology,health_dentistry,health_ems,health_genetics,health_qrcodes,health_reporting,health_calendar,health_crypto,health_services,health_services_lab,health_services_imaging,health_stock,health_stock_inpatient,health_stock_nursing,health_stock_surgery,health_surgery_protocols,health_imaging_worklist,health_inpatient_calendar,health_insurance,health_crypto_lab"
if ! activate_batch "core_clinical" "$CORE"; then
  echo "Core batch failed — activating one by one"
  IFS=',' read -ra ARR <<< "$CORE"
  for m in "${ARR[@]}"; do
    st=$(sudo -u postgres psql -d "$DB" -t -A -c "SELECT state FROM ir_module WHERE name='$m';")
    if [ "$st" = "activated" ]; then
      echo "already activated $m"
      continue
    fi
    activate_one "$m" || true
  done
fi

# Phase 2: ICD / catalogs / remaining health_*
REST=$(sudo -u postgres psql -d "$DB" -t -A -c "SELECT string_agg(name, ',' ORDER BY name) FROM ir_module WHERE name LIKE 'health_%' AND state='not activated';")
if [ -n "$REST" ] && [ "$REST" != "" ]; then
  echo "Remaining modules: $REST"
  if ! activate_batch "remaining" "$REST"; then
    IFS=',' read -ra ARR <<< "$REST"
    for m in "${ARR[@]}"; do
      activate_one "$m" || true
    done
  fi
fi

echo ""
echo "===== FINAL STATE $(date -Is) ====="
sudo -u postgres psql -d "$DB" -c "SELECT state, count(*) FROM ir_module WHERE name LIKE 'health%' OR name IN ('account','account_invoice','account_product','stock','stock_lot') GROUP BY state ORDER BY state;"
sudo -u postgres psql -d "$DB" -c "SELECT name, state FROM ir_module WHERE name LIKE 'health%' OR name IN ('account','account_invoice','account_product','stock','stock_lot') ORDER BY state, name;"

echo "Restarting trytond..."
pkill -f '/opt/gnuhealth/his-50/venv/bin/trytond' || true
sleep 3
cd /opt/gnuhealth/his-50
nohup ./start_gnuhealth > /tmp/trytond.log 2>&1 &
sleep 4
pgrep -af trytond | head -5 || true
echo "===== DONE $(date -Is) ====="
