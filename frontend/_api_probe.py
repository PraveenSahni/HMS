import json, urllib.request, base64
base = "http://127.0.0.1/api/tryton/gnuhealth/"
user = "admin"
password = "IstHealth@2026!Admin"

def rpc(method, params, auth=None):
    payload = json.dumps({"id": 1, "method": method, "params": params}).encode()
    headers = {"Content-Type": "application/json"}
    if auth:
        headers["Authorization"] = auth
    req = urllib.request.Request(base, data=payload, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read().decode()
    print("RAW", method, raw[:300])
    body = json.loads(raw)
    if isinstance(body, dict) and body.get("error"):
        raise RuntimeError(body["error"])
    if isinstance(body, dict):
        return body.get("result")
    return body

login = rpc("common.db.login", [user, {"password": password}])
print("LOGIN_OK", login)
uid, session = login[0], login[1]
token = base64.b64encode(("%s:%s:%s" % (user, uid, session)).encode()).decode()
auth = "Session " + token
count = rpc("model.gnuhealth.patient.search_count", [[], {}], auth=auth)
print("PATIENT_SEARCH_COUNT", count)
print("API_PROBE_OK")
