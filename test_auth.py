#!/usr/bin/env python3
import requests

url = "http://34.18.116.146/gnuhealth/"
password = "IstHealth@2026!Admin"
tests = [
    ("common.authenticate", ["gnuhealth", "admin", {"password": password}, "en"]),
    ("common.login", ["gnuhealth", "admin", password]),
    ("common.db.login", ["gnuhealth", "admin", password]),
    ("common.db.login", ["gnuhealth", "admin", {"password": password}]),
]
for method, params in tests:
    r = requests.post(
        url,
        json={"jsonrpc": "2.0", "method": method, "params": params, "id": 1},
        timeout=30,
    )
    print(f"{method} -> {r.status_code} {r.text[:300]}")
