#!/bin/bash
for mod in health_lab health_nursing health_surgery health_imaging health_inpatient; do
  echo "==== $mod ===="
  dir="/opt/gnuhealth/his-50/venv/lib/python3.11/site-packages/$mod"
  if [ ! -d "$dir" ]; then echo missing; continue; fi
  grep -rh "__name__ = " "$dir" --include='*.py' 2>/dev/null | head -40
  echo "--- tryton.cfg deps ---"
  sed -n '1,40p' "$dir/tryton.cfg" 2>/dev/null
done
echo "==== activation status ===="
tail -25 /tmp/module_activate.log
pgrep -af trytond-admin | grep -v 'bash -c' || echo no-admin
sudo -u postgres psql -d gnuhealth -c "SELECT state, count(1) FROM ir_module GROUP BY state ORDER BY state;"
