#!/bin/bash
VENV=/opt/gnuhealth/his-50/venv
echo "=== find modules ==="
ls "$VENV"/lib/python3.11/site-packages | grep -iE 'health|gnuhealth' | head -60
echo "=== trytond modules path ==="
$VENV/bin/python - <<'PY'
from trytond.modules import get_module_list, get_module_info
import trytond.modules as tm
import os
print('modules pkg', os.path.dirname(tm.__file__))
for name in ['health_lab','health_nursing','health_surgery','health_imaging','health_inpatient']:
    try:
        info = get_module_info(name)
        print(name, 'OK', info.get('directory') or info)
    except Exception as e:
        print(name, 'ERR', e)
# locate health_lab files
import glob
paths = glob.glob('/opt/gnuhealth/his-50/venv/lib/python3.11/site-packages/**/health_lab/**/*.py', recursive=True)[:10]
print('sample paths', paths[:5])
# also egg-link / dist-info
for p in glob.glob('/opt/gnuhealth/his-50/venv/lib/python3.11/site-packages/*lab*'):
    print('lab path', p)
PY

echo "=== activated ==="
sudo -u postgres psql -d gnuhealth -c "SELECT name, state FROM ir_module WHERE state = 'activated' ORDER BY name;"
echo "=== log tail ==="
tail -30 /tmp/module_activate.log
pgrep -af trytond-admin | grep -v 'bash -c' || echo no-admin
