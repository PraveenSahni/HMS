#!/usr/bin/env python3
"""Probe ir.ui.menu + act_window for React tree menu."""
from __future__ import annotations

import base64
import json
import urllib.request

PROXY = "http://34.18.116.146/api/tryton/gnuhealth/"
USER = "admin"
PASSWORD = "IstHealth@2026!Admin"
rid = 0
auth = None


def rpc(method, params, use_auth=True):
    global rid, auth
    rid += 1
    headers = {"Content-Type": "application/json"}
    if use_auth and auth:
        headers["Authorization"] = auth
    req = urllib.request.Request(
        PROXY,
        data=json.dumps({"id": rid, "method": method, "params": params}).encode(),
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        body = json.loads(resp.read().decode())
    if body.get("error"):
        raise RuntimeError(body["error"])
    return body.get("result")


def main():
    global auth
    login = rpc("common.db.login", [USER, {"password": PASSWORD}, "en"], use_auth=False)
    uid, sess = login[0], login[1]
    auth = "Session " + base64.b64encode(f"{USER}:{uid}:{sess}".encode()).decode()
    print("LOGIN OK", uid)

    n = rpc("model.ir.ui.menu.search_count", [[["active", "=", True]], {}])
    print("ACTIVE MENUS", n)

    rows = rpc(
        "model.ir.ui.menu.search_read",
        [
            [["active", "=", True]],
            0,
            15,
            [["sequence", "ASC"], ["id", "ASC"]],
            ["id", "name", "parent", "childs", "action", "active", "sequence", "icon"],
            {},
        ],
    )
    print("SAMPLE ROWS:")
    for r in rows or []:
        print(" ", r)

    with_action = rpc(
        "model.ir.ui.menu.search_read",
        [
            [["active", "=", True], ["action", "!=", None]],
            0,
            8,
            None,
            ["id", "name", "action"],
            {},
        ],
    )
    print("WITH ACTION:")
    for r in with_action or []:
        print(" ", r)
        action = r.get("action")
        if isinstance(action, str) and "," in action:
            model, aid = action.split(",", 1)
            if model == "ir.action.act_window":
                aw = rpc(
                    "model.ir.action.act_window.read",
                    [[int(aid)], ["id", "name", "res_model", "domain", "type"], {}],
                )
                print("   ->", aw)

    roots = rpc(
        "model.ir.ui.menu.search_read",
        [
            [["active", "=", True], ["parent", "=", None]],
            0,
            None,
            [["sequence", "ASC"]],
            ["id", "name", "sequence", "childs"],
            {},
        ],
    )
    print("ROOTS:")
    for r in roots or []:
        print(" ", r["id"], r["name"], "children=", len(r.get("childs") or []))

    # lab fields probe
    for model, fields in [
        ("gnuhealth.patient.lab.test", ["id", "rec_name", "state", "date", "patient_id", "name"]),
        ("gnuhealth.lab", ["id", "rec_name", "name", "date_analysis", "patient", "state"]),
    ]:
        try:
            ids = rpc(f"model.{model}.search", [[], 0, 1, None, {}])
            if ids:
                row = rpc(f"model.{model}.read", [ids, fields, {}])
                print(f"LAB {model}", row)
            else:
                print(f"LAB {model} empty")
        except Exception as e:
            print(f"LAB {model} ERR", e)


if __name__ == "__main__":
    main()
