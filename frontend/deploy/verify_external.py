import json, urllib.request, ssl
ctx = ssl._create_unverified_context()

def get(url, https=False):
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=15, context=ctx if https else None) as r:
            print(f"GET {url} -> {r.status}")
    except Exception as e:
        print(f"GET {url} -> FAIL {e}")

def post(url, method, params, https=False):
    body = json.dumps({"jsonrpc":"2.0","id":1,"method":method,"params":params}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type":"application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30, context=ctx if https else None) as r:
            print(f"POST {url} {method} -> {r.status} {r.read()[:120].decode()}")
    except Exception as e:
        err = e.read()[:120].decode() if hasattr(e, 'read') else str(e)
        print(f"POST {url} {method} -> FAIL {err}")

get('http://34.18.116.146/login')
get('http://34.18.116.146/sao/')
get('https://34.18.116.146/login', https=True)
get('https://34.18.116.146/sao/', https=True)
post('http://34.18.116.146/api/tryton/', 'common.db.list', [])
post('http://34.18.116.146/api/tryton/gnuhealth/', 'common.db.login', ['admin', {'password': 'IstHealth@2026!Admin'}, 'en'])
get('http://34.18.116.146:8000/')
