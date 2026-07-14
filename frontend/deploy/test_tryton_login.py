#!/usr/bin/env python3
"""Test Tryton JSON-RPC auth on GNU Health VM."""
import json
import urllib.error
import urllib.request

URL = "http://127.0.0.1:8000/"


def rpc(method: str, params: list) -> None:
    payload = {"method": method, "params": params, "id": 1}
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        URL, data=data, headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode()
            print(f"OK  {method} => {body[:400]}")
    except urllib.error.HTTPError as e:
        print(f"ERR {method} => HTTP {e.code}: {e.read().decode()[:400]}")


if __name__ == "__main__":
    rpc("common.db.list", [])
    rpc("common.server.version", [])
    rpc(
        "common.authenticate",
        ["gnuhealth", "admin", {"password": "IstHealth@2026!Admin"}, "en"],
    )
    rpc("common.db.login", ["gnuhealth", "admin", "IstHealth@2026!Admin"])
    rpc("common.login", ["gnuhealth", "admin", "IstHealth@2026!Admin"])
