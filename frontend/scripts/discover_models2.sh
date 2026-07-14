#!/bin/bash
set -e
echo "=== package locations ==="
/opt/gnuhealth/his-50/venv/bin/python - <<'PY'
import health_lab, health_nursing, health_surgery, health_imaging, health_inpatient, os
for m in [health_lab, health_nursing, health_surgery, health_imaging, health_inpatient]:
    print(m.__name__, '->', os.path.dirname(m.__file__))
PY

echo "=== model __name__ ==="
for pkg in health_lab health_nursing health_surgery health_imaging health_inpatient; do
  echo "---- $pkg ----"
  dir=$(/opt/gnuhealth/his-50/venv/bin/python -c "import $pkg,os; print(os.path.dirname($pkg.__file__))")
  grep -rh "__name__ = " "$dir" --include='*.py' | head -40
done

echo "=== activated health ==="
sudo -u postgres psql -d gnuhealth -c "SELECT name, state FROM ir_module WHERE state = 'activated' AND name LIKE 'health%' ORDER BY name;"

echo "=== activation tail ==="
tail -20 /tmp/module_activate.log
pgrep -af trytond-admin | grep -v 'bash -c' || echo no-admin
