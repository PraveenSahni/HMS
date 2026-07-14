#!/bin/bash
/opt/gnuhealth/his-50/venv/bin/pip list 2>/dev/null | grep -iE 'proteus|tryton'
echo "--- admin user ---"
sudo -u postgres psql gnuhealth -c "SELECT id, login, active FROM res_user WHERE login='admin';"
echo "--- auth localhost ---"
/opt/gnuhealth/his-50/venv/bin/python /opt/gnuhealth/synthetic-data/test_auth.py
echo "--- auth localhost:8000 ---"
/opt/gnuhealth/his-50/venv/bin/python -c "
import requests
url='http://127.0.0.1:8000/gnuhealth/'
pw='IstHealth@2026!Admin'
for method,params in [
  ('common.authenticate',['gnuhealth','admin',{'password':pw},'en']),
  ('common.login',['gnuhealth','admin',pw]),
]:
  r=requests.post(url,json={'jsonrpc':'2.0','method':method,'params':params,'id':1},timeout=30)
  print(method,r.status_code,r.text[:200])
"
