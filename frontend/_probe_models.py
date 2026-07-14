import base64, json, urllib.request, urllib.error, re, os, sys

URLS = [
    "http://127.0.0.1/api/tryton/",
    "http://127.0.0.1/api/tryton/gnuhealth/",
    "http://127.0.0.1:8000/gnuhealth/",
]
USER = "admin"
PASSWORD = "IstHealth@2026!Admin"

def rpc(url, method, params, auth=None):
    payload = json.dumps({"id": 1, "method": method, "params": params}).encode()
    headers = {"Content-Type": "application/json"}
    if auth:
        headers["Authorization"] = auth
    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode()
            body = json.loads(raw)
    except urllib.error.HTTPError as e:
        raw = e.read().decode(errors="replace")
        print("HTTP", e.code, url, method, raw[:300])
        try:
            body = json.loads(raw)
        except Exception:
            raise RuntimeError("HTTP %s: %s" % (e.code, raw[:200])) from e
    if isinstance(body, dict) and body.get("error") is not None:
        err = body["error"]
        if isinstance(err, list):
            msg = " | ".join(str(x) for x in err if x)
        elif isinstance(err, dict):
            msg = err.get("message") or err.get("data") or json.dumps(err)
        else:
            msg = str(err)
        raise RuntimeError(msg)
    if isinstance(body, dict) and "result" in body:
        return body["result"]
    return body

URL = None
auth = None
for u in URLS:
    for params in (
        [USER, {"password": PASSWORD}, "en"],
        [USER, {"password": PASSWORD}],
        [USER, PASSWORD],
    ):
        try:
            login = rpc(u, "common.db.login", params)
            if isinstance(login, dict) and "result" in login:
                login = login["result"]
            uid, session = login[0], login[1]
            auth = "Session " + base64.b64encode(("%s:%s:%s" % (USER, uid, session)).encode()).decode()
            URL = u
            print("LOGIN OK url=%s uid=%s params=%s" % (u, uid, params))
            break
        except Exception as e:
            print("LOGIN FAIL url=%s params=%s err=%s" % (u, params, e))
    if URL:
        break

if not URL:
    sys.exit(2)

MODELS = [
    ("party.party", ["id", "name", "code", "active", "is_patient", "is_healthprof"]),
    ("company.company", ["id", "rec_name", "party"]),
    ("product.template", ["id", "name", "code", "active", "list_price", "type"]),
    ("product.product", ["id", "rec_name", "code", "active"]),
    ("stock.location", ["id", "rec_name", "code", "type"]),
    ("stock.move", ["id", "rec_name", "product", "quantity", "from_location", "to_location", "state"]),
    ("account.invoice", ["id", "rec_name", "number", "party", "invoice_date", "total_amount", "state", "type"]),
    ("currency.currency", ["id", "rec_name", "name", "code", "symbol"]),
    ("calendar.calendar", ["id", "rec_name", "name", "description"]),
    ("calendar.event", ["id", "rec_name", "summary", "dtstart", "dtend", "status"]),
    ("res.user", ["id", "rec_name", "name", "login", "active"]),
    ("ir.module", ["id", "rec_name", "name", "state"]),
    ("country.country", ["id", "rec_name", "name", "code"]),
]

rows = []
for model, fields in MODELS:
    try:
        ids = rpc(URL, "model.%s.search" % model, [[], 0, 3, None, {}], auth)
        if ids:
            rpc(URL, "model.%s.read" % model, [ids, fields, {}], auth)
        rows.append((model, "OK", ""))
        print("OK  %s" % model)
    except Exception as e:
        msg = str(e).replace("\n", " ")[:180]
        rows.append((model, "FAIL", msg))
        print("FAIL %s: %s" % (model, msg))

print("--- INDEX ---")
candidates = [
    "/var/www/html/index.html",
    "/var/www/ist-health/index.html",
    "/usr/share/nginx/html/index.html",
    "/home/gnuhealth/ist-health/index.html",
    "/opt/ist-health/index.html",
]
found = None
for p in candidates:
    if os.path.isfile(p):
        found = p
        break
if not found:
    for root in ["/var/www", "/usr/share/nginx", "/home/gnuhealth", "/opt"]:
        if not os.path.isdir(root):
            continue
        for dirpath, _, files in os.walk(root):
            if "index.html" in files:
                found = os.path.join(dirpath, "index.html")
                break
        if found:
            break

index_status = "FAIL"
index_detail = "index.html not found"
if found:
    with open(found, "r", encoding="utf-8", errors="replace") as f:
        html = f.read()
    has = "index-CJvn5vvO.js" in html
    index_status = "OK" if has else "FAIL"
    scripts = re.findall(r'src=["\']([^"\']+)["\']', html)
    index_detail = "%s refs=%s has_CJvn5vvO=%s" % (found, scripts, has)
    print(index_detail)

print("--- TABLE ---")
print("URL used: %s" % URL)
print("%-22s %-6s %s" % ("model", "status", "detail"))
print("-" * 80)
for m, s, d in rows:
    print("%-22s %-6s %s" % (m, s, d))
print("%-22s %-6s %s" % ("index.html bundle", index_status, index_detail))
