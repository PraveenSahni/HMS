#!/usr/bin/env python3
"""Test login through nginx /api/tryton/ proxy."""
import base64
import json
import urllib.error
import urllib.request

PROXY_URL = "http://127.0.0.1/api/tryton/"
USER = "admin"
PASSWORD = "IstHealth@2026!Admin"


def rpc(url: str, method: str, params: list, auth: str | None = None) -> dict:
    payload = {"method": method, "params": params, "id": 1}
    headers = {"Content-Type": "application/json"}
    if auth:
        headers["Authorization"] = auth
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


if __name__ == "__main__":
    print("=== Login via nginx proxy ===")
    result = rpc(PROXY_URL, "common.db.login", [USER, {"password": PASSWORD}, "en"])
    print("login:", result)
    uid, token = result["result"]
    auth = f"Session {base64.b64encode(f'{USER}:{uid}:{token}'.encode()).decode()}"
    print("=== Search patients via proxy ===")
    search = rpc(
        PROXY_URL,
        "model.party.party.search",
        [[], 0, 5, None, {}],
        auth=auth,
    )
    print("search:", search)
