#!/bin/bash
BASE=/opt/gnuhealth/his-50/venv/lib/python3.11/site-packages/trytond/modules
echo "=== inpatient failure context ==="
sed -n '39,75p' /tmp/module_activate.log

echo "=== model names ==="
for mod in health_lab health_nursing health_surgery health_imaging health_inpatient; do
  echo "---- $mod ----"
  grep -rh "__name__ = " "$BASE/$mod" --include='*.py' | grep -v sequences | head -30
done

echo "=== lab fields (PatientLabTest / Lab) ==="
# Extract class field definitions roughly
python3 - <<'PY'
import re, pathlib
base = pathlib.Path('/opt/gnuhealth/his-50/venv/lib/python3.11/site-packages/trytond/modules')
for mod, files in {
  'health_lab': ['health_lab.py'],
  'health_nursing': ['health_nursing.py'],
  'health_surgery': ['health_surgery.py'],
  'health_imaging': ['health_imaging.py'],
  'health_inpatient': ['health_inpatient.py'],
}.items():
  print('####', mod)
  for f in files:
    text = (base/mod/f).read_text(errors='ignore')
    # find ModelSQL classes and their __name__
    for m in re.finditer(r"class (\w+)\(.*?\):(.*?)(?=\nclass |\Z)", text, re.S):
      body = m.group(2)
      nm = re.search(r"__name__\s*=\s*'([^']+)'", body)
      if not nm: continue
      fields = re.findall(r"^    (\w+)\s*=\s*fields\.", body, re.M)
      print(nm.group(1), '->', ', '.join(fields[:20]))
PY

echo "=== progress ==="
tail -15 /tmp/module_activate.log
sudo -u postgres psql -d gnuhealth -c "SELECT name FROM ir_module WHERE state='activated' AND name LIKE 'health%' ORDER BY 1;"
