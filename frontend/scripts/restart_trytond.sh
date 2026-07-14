#!/bin/bash
set -e
echo "Stopping trytond..."
sudo pkill -f '/opt/gnuhealth/his-50/venv/bin/trytond' || true
sleep 3
# ensure dead
if pgrep -f '/opt/gnuhealth/his-50/venv/bin/trytond' >/dev/null; then
  sudo pkill -9 -f '/opt/gnuhealth/his-50/venv/bin/trytond' || true
  sleep 2
fi
cd /opt/gnuhealth/his-50
sudo -u "$(stat -c %U start_gnuhealth 2>/dev/null || echo PraveenSAHNI)" bash -c 'cd /opt/gnuhealth/his-50 && nohup ./start_gnuhealth > /tmp/trytond_start.log 2>&1 &' || true
# fallback: run as current user with sudo redirect
sleep 1
if ! pgrep -f '/opt/gnuhealth/his-50/venv/bin/trytond' >/dev/null; then
  echo "fallback start as current user"
  rm -f /tmp/trytond_start.log
  nohup sudo -u PraveenSAHNI /opt/gnuhealth/his-50/start_gnuhealth > /home/PraveenSAHNI/trytond_start.log 2>&1 &
fi
sleep 5
pgrep -af trytond | head -5
echo "=== model check via RPC-ish pool ==="
/opt/gnuhealth/his-50/venv/bin/python - <<'PY'
from trytond.config import config
config.update_etc('/opt/gnuhealth/his-50/etc/trytond.conf')
from trytond.pool import Pool
from trytond.transaction import Transaction
Pool.start()
pool = Pool('gnuhealth')
with Transaction().start('gnuhealth', 0, readonly=True):
    pool.init()
    for m in [
      'gnuhealth.patient.lab.test','gnuhealth.lab','gnuhealth.lab.test_type',
      'gnuhealth.inpatient.registration','gnuhealth.hospital.bed',
      'gnuhealth.surgery','gnuhealth.operation','gnuhealth.patient.procedure',
      'gnuhealth.imaging.test.request','gnuhealth.imaging.test','gnuhealth.imaging.test.result',
      'gnuhealth.patient.rounding','gnuhealth.patient.ambulatory_care',
      'account.invoice',
    ]:
        try:
            Model = pool.get(m)
            print(f'OK {m} count={Model.search([], count=True)}')
        except Exception as e:
            print(f'MISS {m}: {type(e).__name__}: {e}')
PY
curl -s -o /dev/null -w 'trytond_http=%{http_code}\n' http://127.0.0.1:8000/ || true
curl -s -o /dev/null -w 'react_http=%{http_code}\n' http://127.0.0.1/ || true
