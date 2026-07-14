#!/usr/bin/env bash
set +e
PID=$(pgrep -f 'venv/bin/trytond' | head -1)
echo "trytond pid=$PID"
if [ -n "$PID" ]; then
  sudo tr '\0' '\n' < /proc/$PID/environ | sort
fi
echo "==== RPC list direct ===="
curl -sS -X POST http://127.0.0.1:8000/ \
  -H 'Content-Type: application/json' \
  --data-binary '{"id":1,"method":"common.db.list","params":[]}'
echo
echo "==== RPC list via https proxy ===="
curl -skS -X POST https://127.0.0.1/api/tryton/ \
  -H 'Content-Type: application/json' \
  --data-binary '{"id":1,"method":"common.db.list","params":[]}'
echo
echo "==== SPA https ===="
curl -skS -o /dev/null -w "spa=%{http_code}\n" https://127.0.0.1/
curl -sS -o /dev/null -w "http=%{http_code}\n" http://127.0.0.1/
echo "==== systemd ===="
systemctl is-active trytond
ss -tlnp | grep -E ':443|:80|:8000'
