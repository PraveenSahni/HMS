#!/bin/bash
# Quick JSON-RPC login + modelExists checks
set -e
BASE=http://127.0.0.1:8000
# Tryton login
LOGIN=$(curl -s -X POST "$BASE/" -H 'Content-Type: application/json' -d '{
  "jsonrpc":"2.0","id":1,"method":"common.db.login",
  "params":["gnuhealth","admin","IstHealth@2026!Admin",null]
}')
echo "LOGIN=$LOGIN"
SESSION=$(python3 - <<PY
import json
r=json.loads('''$LOGIN''')
print(r.get('result'))
PY
)
# result is typically [user_id, session]
USER=$(python3 - <<PY
import json
r=json.loads('''$LOGIN''')
print(r['result'][0])
PY
)
SID=$(python3 - <<PY
import json
r=json.loads('''$LOGIN''')
print(r['result'][1])
PY
)
echo "user=$USER session_ok=${#SID}"

check() {
  local model="$1"
  RESP=$(curl -s -X POST "$BASE/" -H 'Content-Type: application/json' -d "{
    \"jsonrpc\":\"2.0\",\"id\":2,\"method\":\"model.$model.search_count\",
    \"params\":[[], {}, {\"client\": \"$SID\"}]
  }")
  # Tryton 7 auth is different - use session list form
  RESP=$(curl -s -X POST "$BASE/" -H 'Content-Type: application/json' -d "{
    \"id\":2,\"method\":\"model.$model.search_count\",
    \"params\":[\"gnuhealth\", $USER, \"$SID\", [], {}]
  }")
  echo "$model -> $RESP"
}
check gnuhealth.lab.test_type
check gnuhealth.patient.lab.test
check gnuhealth.surgery
check gnuhealth.imaging.test.request
check gnuhealth.inpatient.registration
check gnuhealth.patient.ambulatory_care
