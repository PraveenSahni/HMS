#!/usr/bin/env python3
"""Probe Tryton login + Session auth via nginx proxy and direct trytond."""
from __future__ import annotations

import base64
import json
import urllib.error
import urllib.request

PROXY = "http://127.0.0.1/api/tryton/"
DIRECT = "http://127.0.0.1:8000/gnuhealth/"
USER = "admin"
PASSWORD = "IstHealth@2026!Admin"


def rpc(url: str, method: str, params: list, auth: str | None = None, req_id: int = 1):
    headers = {"Content-Type": "application/json"}
    if auth:
        headers["Authorization"] = auth
    body = json.dumps({"id": req_id, "method": method, "params": params}).encode()
    req = urllib.request.Request(url, data=body, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode()
            return resp.status, raw, json.loads(raw)
    except urllib.error.HTTPError as e:
        raw = e.read().decode(errors="replace")
        try:
            parsed = json.loads(raw)
        except Exception:
            parsed = None
        return e.code, raw, parsed


def extract_login(parsed):
    """Handle {result:[uid,tok]}, bare [uid,tok], or Tryton [id,[uid,tok]]."""
    if isinstance(parsed, dict) and "result" in parsed:
        r = parsed["result"]
        if isinstance(r, (list, tuple)) and len(r) >= 2:
            return r[0], r[1]
    if isinstance(parsed, list) and len(parsed) >= 2:
        # bare [uid, token]
        if not isinstance(parsed[1], (list, tuple)):
            return parsed[0], parsed[1]
        # classic [id, [uid, token]]
        inner = parsed[1]
        if isinstance(inner, (list, tuple)) and len(inner) >= 2:
            return inner[0], inner[1]
    raise ValueError(f"Cannot parse login response: {parsed!r}")


def main():
    print("=== LOGIN via proxy ===")
    status, raw, parsed = rpc(PROXY, "common.db.login", [USER, {"password": PASSWORD}, "en"])
    print(f"HTTP {status}")
    print(f"raw={raw[:400]}")
    print(f"type={type(parsed).__name__}")
    uid, token = extract_login(parsed)
    print(f"uid={uid} token_len={len(str(token))}")
    auth = "Session " + base64.b64encode(f"{USER}:{uid}:{token}".encode()).decode()
    print(f"auth={auth[:60]}...")

    calls = [
        ("party.search_count", "model.party.party.search_count", [[], {}]),
        ("patient.search_count", "model.gnuhealth.patient.search_count", [[], {}]),
        ("appt.search_count", "model.gnuhealth.appointment.search_count", [[], {}]),
        ("hp.search_count", "model.gnuhealth.healthprofessional.search_count", [[], {}]),
        ("party.search", "model.party.party.search", [[], 0, 3, None, {}]),
        ("company.search", "model.company.company.search", [[], 0, 5, None, {}]),
        ("menu.search", "model.ir.ui.menu.search", [["active", "=", True], 0, 20, None, {}]),
    ]
    print("\n=== AUTHENTICATED via proxy ===")
    for label, method, params in calls:
        st, raw2, parsed2 = rpc(PROXY, method, params, auth=auth)
        print(f"\n[{label}] HTTP {st}")
        print(f"  raw={raw2[:350]}")
        print(f"  type={type(parsed2).__name__}")

    print("\n=== NO AUTH party.search_count ===")
    st, raw2, _ = rpc(PROXY, "model.party.party.search_count", [[], {}])
    print(f"HTTP {st} raw={raw2[:300]}")

    print("\n=== AUTHENTICATED via direct :8000 ===")
    st, raw2, parsed2 = rpc(DIRECT, "model.party.party.search_count", [[], {}], auth=auth)
    print(f"HTTP {st} raw={raw2[:300]}")

    print("\n=== trytond version ===")
    try:
        import trytond

        print("trytond", getattr(trytond, "__version__", "?"))
    except Exception as e:
        print("import trytond failed:", e)


if __name__ == "__main__":
    main()
