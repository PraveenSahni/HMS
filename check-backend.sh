#!/bin/bash
set -e

HIS=/opt/gnuhealth/his-50

echo "=== DATABASES ==="
sudo -u postgres psql -lqt

echo ""
echo "=== TRYTON PROCESSES ==="
ps aux | grep -E 'tryton|gnuhealth' | grep -v grep || echo "none running"

echo ""
echo "=== PORTS ==="
sudo ss -tlnp | grep -E '8000|80' || echo "8000 not listening"

echo ""
echo "=== trytond.conf (non-comment) ==="
grep -E '^[^#]' "$HIS/etc/trytond.conf" 2>/dev/null | head -25 || echo "not found"

echo ""
echo "=== gnuhealthrc files ==="
for f in /home/sahni_ps/.gnuhealthrc "$HIS/.gnuhealthrc" /opt/gnuhealth/.gnuhealthrc; do
  if [ -f "$f" ]; then
    echo "--- $f ---"
    cat "$f"
  fi
done
[ ! -f /home/sahni_ps/.gnuhealthrc ] && [ ! -f "$HIS/.gnuhealthrc" ] && echo "(no gnuhealthrc found)"

echo ""
echo "=== local/ directory ==="
ls -la "$HIS/local/" 2>/dev/null || echo "local/ missing or empty"

echo ""
echo "=== ghcontrol / install logs (recent) ==="
ls -lt "$HIS/log/" 2>/dev/null | head -5 || true
if [ -f "$HIS/log/packages.log" ]; then
  echo "--- last 15 lines packages.log ---"
  tail -15 "$HIS/log/packages.log"
fi

echo ""
for DB in gnuhealth isthealth; do
  if sudo -u postgres psql -lqt | cut -d'|' -f1 | tr -d ' ' | grep -qx "$DB"; then
    echo "=== DB EXISTS: $DB ==="
    TABLE_CHECK=$(sudo -u postgres psql -d "$DB" -tAc "SELECT to_regclass('public.ir_module');" 2>/dev/null || echo "")
    if [ "$TABLE_CHECK" = "ir_module" ]; then
      echo "Tryton schema: YES (ir_module table present)"
      sudo -u postgres psql -d "$DB" -c "SELECT count(*) AS activated_modules FROM ir_module WHERE state='activated';"
      sudo -u postgres psql -d "$DB" -c "SELECT count(*) AS total_modules FROM ir_module;"
      echo "--- users ---"
      sudo -u postgres psql -d "$DB" -c "SELECT id, login, active FROM res_user ORDER BY id LIMIT 10;"
    else
      echo "Tryton schema: NO (database empty or not initialized)"
    fi
  else
    echo "=== DB NOT FOUND: $DB ==="
  fi
  echo ""
done

echo "=== GNU Health pip packages ==="
if [ -x "$HIS/ghis_env/bin/pip" ]; then
  "$HIS/ghis_env/bin/pip" list 2>/dev/null | grep -i gnuhealth | wc -l | xargs echo "gnuhealth package count:"
  "$HIS/ghis_env/bin/pip" list 2>/dev/null | grep -i gnuhealth | head -15
else
  echo "ghis_env pip not found"
fi

echo ""
echo "=== start_gnuhealth (first 20 lines) ==="
head -20 "$HIS/start_gnuhealth" 2>/dev/null || echo "start script not found"

echo ""
echo "=== nginx sites ==="
ls -la /etc/nginx/sites-enabled/ 2>/dev/null || true
grep -r "8000\|tryton\|gnuhealth" /etc/nginx/ 2>/dev/null | head -10 || echo "no tryton proxy in nginx"
