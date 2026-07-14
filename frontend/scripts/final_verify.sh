#!/bin/bash
echo "=== trytond ==="
pgrep -af '/venv/bin/trytond' | grep -v admin | head -3
curl -s -o /dev/null -w 'trytond=%{http_code}\n' http://127.0.0.1:8000/
curl -s -o /dev/null -w 'react=%{http_code}\n' http://127.0.0.1/
echo "=== assets ==="
ls /var/www/ist-health/frontend/dist/assets/
echo "=== module counts ==="
sudo -u postgres psql -d gnuhealth -c "SELECT state, count(1) FROM ir_module WHERE name LIKE 'health%' GROUP BY state;"
sudo -u postgres psql -d gnuhealth -c "SELECT count(1) AS activated_health FROM ir_module WHERE state='activated' AND name LIKE 'health%';"
echo "=== login test ==="
python3 - <<'PY'
import json, urllib.request
req = urllib.request.Request(
    'http://127.0.0.1:8000/',
    data=json.dumps({
        'jsonrpc':'2.0','id':1,'method':'common.db.login',
        'params':['admin','IstHealth@2026!Admin',None]
    }).encode(),
    headers={'Content-Type':'application/json'},
)
# Tryton 7 often uses database in URL path or params differently
# Try both styles
for params in [
    ['admin','IstHealth@2026!Admin', None],
    ['gnuhealth', 'admin','IstHealth@2026!Admin'],
]:
    payload = {'id':1,'method':'common.db.login','params':params}
    try:
        r = urllib.request.urlopen(urllib.request.Request(
            'http://127.0.0.1:8000/',
            data=json.dumps(payload).encode(),
            headers={'Content-Type':'application/json'},
        ), timeout=20)
        print('params', params, '->', r.read()[:200])
    except Exception as e:
        print('params', params, 'ERR', e)

# Also via nginx proxy path
for url in ['http://127.0.0.1/gnuhealth/', 'http://127.0.0.1:8000/']:
    try:
        payload = {'id':1,'method':'common.db.login','params':['admin','IstHealth@2026!Admin', None]}
        r = urllib.request.urlopen(urllib.request.Request(
            url,
            data=json.dumps(payload).encode(),
            headers={'Content-Type':'application/json'},
        ), timeout=20)
        print('url', url, '->', r.read()[:300])
    except Exception as e:
        print('url', url, 'ERR', e)
PY
