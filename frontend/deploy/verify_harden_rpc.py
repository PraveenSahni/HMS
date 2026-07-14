import json, urllib.request
def post(url, method, params):
    body = json.dumps({"jsonrpc":"2.0","id":1,"method":method,"params":params}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type":"application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print(url, method, r.status, r.read()[:300].decode())
    except Exception as e:
        if hasattr(e, 'read'):
            print(url, method, 'ERR', e.read()[:300].decode())
        else:
            print(url, method, type(e).__name__, e)

post('http://127.0.0.1:8000/', 'common.db.list', [])
post('http://127.0.0.1/api/tryton/', 'common.db.list', [])
post('http://127.0.0.1:8000/gnuhealth/', 'common.db.login', ['admin', {'password': 'IstHealth@2026!Admin'}, 'en'])
post('http://127.0.0.1/api/tryton/gnuhealth/', 'common.db.login', ['admin', {'password': 'IstHealth@2026!Admin'}, 'en'])
