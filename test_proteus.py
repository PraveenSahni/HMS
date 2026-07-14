#!/usr/bin/env python3
"""Test Proteus and Tryton auth on VM."""
import sys

# Test Proteus
try:
    from proteus import config, Model
    config.set_url("http://127.0.0.1:8000/")
    config.set_database("gnuhealth")
    config.set_user("admin")
    config.set_password("IstHealth@2026!Admin")
    User = Model.get("res.user")
    users = User.find([("login", "=", "admin")])
    print("Proteus OK:", users[0].id if users else "no user")
except Exception as e:
    print("Proteus FAILED:", e)

# Test alternate passwords
import requests
url = "http://127.0.0.1:8000/gnuhealth/"
for pw in ["admin", "IstHealth@2026!Admin", "gnuhealth"]:
    r = requests.post(
        url,
        json={
            "jsonrpc": "2.0",
            "method": "common.authenticate",
            "params": ["gnuhealth", "admin", {"password": pw}, "en"],
            "id": 1,
        },
        timeout=30,
    )
    print(f"auth pw={pw!r} -> {r.status_code} {r.text[:150]}")
