#!/bin/bash
# Retry modules that failed due to dep order once lifestyle/etc are ready
CONF=/opt/gnuhealth/his-50/etc/trytond.conf
DB=gnuhealth
export PATH=/opt/gnuhealth/his-50/venv/bin:$PATH
LOG=/tmp/module_retry.log
exec > >(tee -a "$LOG") 2>&1

# Wait until the main activate script finishes
echo "Waiting for main activator to finish..."
while pgrep -f '/tmp/activate_modules.sh' >/dev/null; do
  sleep 15
done
echo "Main activator done at $(date -Is)"

activate_one() {
  local mod="$1"
  st=$(sudo -u postgres psql -d "$DB" -t -A -c "SELECT state FROM ir_module WHERE name='$mod';")
  if [ "$st" = "activated" ]; then
    echo "already OK $mod"
    return 0
  fi
  echo "===== RETRY $mod $(date -Is) ====="
  sudo -u postgres psql -d "$DB" -c "UPDATE ir_module SET state='to activate' WHERE name='$mod' AND state='not activated';"
  if trytond-admin -c "$CONF" -d "$DB" --all; then
    echo "OK $mod"
  else
    echo "FAIL $mod"
    sudo -u postgres psql -d "$DB" -c "UPDATE ir_module SET state='not activated' WHERE state='to activate';"
  fi
}

# Priority clinical deps first, then dependents
for m in health_inpatient health_surgery health_icu health_stock health_services \
  health_services_lab health_services_imaging health_stock_inpatient health_stock_nursing \
  health_stock_surgery health_surgery_protocols health_imaging_worklist health_inpatient_calendar \
  health_insurance health_crypto health_crypto_lab health_calendar health_qrcodes health_reporting \
  health_dentistry health_disability health_ems health_genetics health_ophthalmology health_icd10 \
  health_icd11 health_icd9procs health_icpm health_icd10pcs health_who_essential_medicines \
  health_mdg6 health_ntd health_ntd_chagas health_ntd_dengue health_contact_tracing \
  health_archives health_federation health_orthanc health_caldav health_webdav3_server \
  health_genetics_uniprot health_pediatrics_growth_charts health_pediatrics_growth_charts_who \
  health_iss; do
  activate_one "$m"
done

echo "===== FINAL $(date -Is) ====="
sudo -u postgres psql -d "$DB" -c "SELECT state, count(1) FROM ir_module WHERE name LIKE 'health%' OR name IN ('account','account_invoice','account_product','stock','stock_lot') GROUP BY state ORDER BY 1;"
sudo -u postgres psql -d "$DB" -c "SELECT name, state FROM ir_module WHERE name LIKE 'health%' OR name IN ('account','account_invoice','account_product','stock','stock_lot') ORDER BY state, name;"

# Verify key models
/opt/gnuhealth/his-50/venv/bin/python - <<'PY'
from trytond.pool import Pool
from trytond.config import config
config.update_etc('/opt/gnuhealth/his-50/etc/trytond.conf')
from trytond.transaction import Transaction
Pool.start()
pool = Pool('gnuhealth')
with Transaction().start('gnuhealth', 0, readonly=True):
    pool.init()
    models = [
      'gnuhealth.patient.lab.test','gnuhealth.lab','gnuhealth.lab.test_type',
      'gnuhealth.inpatient.registration','gnuhealth.hospital.bed',
      'gnuhealth.surgery','gnuhealth.operation','gnuhealth.patient.procedure',
      'gnuhealth.imaging.test.request','gnuhealth.imaging.test','gnuhealth.imaging.test.result',
      'gnuhealth.patient.rounding','gnuhealth.patient.ambulatory_care',
    ]
    for m in models:
        try:
            Model = pool.get(m)
            n = Model.search([], count=True)
            print(f'OK {m} count={n}')
        except Exception as e:
            print(f'MISSING {m}: {e}')
PY

echo "Restarting trytond..."
pkill -f '/opt/gnuhealth/his-50/venv/bin/trytond' || true
sleep 3
cd /opt/gnuhealth/his-50 && nohup ./start_gnuhealth > /tmp/trytond.log 2>&1 &
sleep 4
pgrep -af trytond | head -5
echo DONE
