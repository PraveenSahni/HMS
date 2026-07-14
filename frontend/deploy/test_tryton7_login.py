#!/usr/bin/env python3
"""Test Tryton 7 common.db.login on GNU Health VM."""
import json
import urllib.error
import urllib.request

BASE = "http://127.0.0.1:8000"
DB = "gnuhealth"
USER = "admin"
PASSWORD = "IstHealth@2026!Admin"


def rpc(url: str, method: str, params: list) -> None:
    payload = {"method": method, "params": params, "id": 1}
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode()
            print(f"OK  {url} {method} {params!r}")
            print(f"    => {body[:500]}")
    except urllib.error.HTTPError as e:
        print(f"ERR {url} {method} => HTTP {e.code}: {e.read().decode()[:400]}")


if __name__ == "__main__":
    url = f"{BASE}/{DB}/"
    # Tryton 7: params are [user, parameters] — database is in URL path
    rpc(url, "common.db.login", [USER, {"password": PASSWORD}])
    rpc(url, "common.db.login", [USER, PASSWORD])
    rpc(url, "common.db.login", [USER, {"password": PASSWORD}, "en"])
