#!/bin/bash
set -e
HIS=/opt/gnuhealth/his-50
CONF=$HIS/etc/trytond.conf
VENV=$HIS/venv/bin
PW='IstHealth@2026!Admin'

echo "=== trytond-admin help ==="
$VENV/trytond-admin --help 2>&1 | head -30

echo ""
echo "=== Reset admin password ==="
$VENV/trytond-admin -c "$CONF" -d gnuhealth --user admin --password "$PW" 2>&1 || \
$VENV/trytond-admin -c "$CONF" -d gnuhealth --email admin --password "$PW" 2>&1 || \
echo "trytond-admin failed, trying alternate..."

echo ""
echo "=== Test auth after reset ==="
$VENV/python -c "
import requests
url='http://127.0.0.1:8000/gnuhealth/'
pw='$PW'
r=requests.post(url,json={'jsonrpc':'2.0','method':'common.authenticate','params':['gnuhealth','admin',{'password':pw},'en'],'id':1},timeout=30)
print('auth ->', r.status_code, r.text[:200])
"
