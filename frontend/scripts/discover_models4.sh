#!/bin/bash
VENV=/opt/gnuhealth/his-50/venv
SITE=$VENV/lib/python3.11/site-packages
echo "=== locate health_lab code ==="
find "$SITE" -type d -name 'health_lab' 2>/dev/null
find "$SITE" -path '*health_lab*lab.py' 2>/dev/null | head
# dist-info RECORD
grep -h 'health_lab' "$SITE"/gnuhealth_lab-5.0.4.dist-info/RECORD 2>/dev/null | head -20

echo "=== entry points ==="
cat "$SITE"/gnuhealth_lab-5.0.4.dist-info/entry_points.txt 2>/dev/null
cat "$SITE"/gnuhealth_nursing-5.0.4.dist-info/entry_points.txt 2>/dev/null

# modules often live under trytond.modules via namespace packages
ls -la "$SITE"/trytond/modules/ 2>/dev/null | head -40

echo "=== grep models ==="
for d in "$SITE"/trytond/modules/health_lab "$SITE"/health_lab; do
  if [ -d "$d" ]; then
    echo "DIR $d"
    grep -rh "__name__ = " "$d" --include='*.py' | head -40
  fi
done

# Some installs use zip/egg
$VENV/bin/python - <<'PY'
import importlib.metadata as md
for name in ['gnuhealth-lab','gnuhealth-nursing','gnuhealth-surgery','gnuhealth-imaging','gnuhealth-inpatient']:
    try:
        dist = md.distribution(name)
        print(name, 'files sample:')
        files = list(dist.files or [])[:15]
        for f in files:
            print(' ', f)
        # locate module root
        for f in dist.files or []:
            if str(f).endswith('__init__.py') and 'health_' in str(f):
                print(' init', f, '->', dist.locate_file(f))
                break
    except Exception as e:
        print(name, e)
PY

echo "=== inpatient in log ==="
grep -n "health_inpatient\|health_lab\|FAIL\|OK " /tmp/module_activate.log | head -60
echo "=== current ==="
tail -10 /tmp/module_activate.log
sudo -u postgres psql -d gnuhealth -t -A -c "SELECT count(1) FROM ir_module WHERE state='activated';"
