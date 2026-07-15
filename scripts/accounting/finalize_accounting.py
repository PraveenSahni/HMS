#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Complete UAE CoA properties, demo labels, party AR/AP; verify both companies."""
from __future__ import annotations

import json
import os

from proteus import Model, Wizard, config as pc

pc.set_trytond(
    database="isthealth",
    user="admin",
    config_file=os.environ.get(
        "GNUHEALTH_TRYTOND_CONF", "/opt/gnuhealth/his-50/etc/trytond.conf"
    ),
)

MARKER = "IST Health demo"
User = Model.get("res.user")
Company = Model.get("company.company")
Party = Model.get("party.party")
Account = Model.get("account.account")
FiscalYear = Model.get("account.fiscalyear")
Period = Model.get("account.period")
Config = Model.get("account.configuration")
Journal = Model.get("account.journal")

from trytond.modules.account.tests.tools import get_accounts


def switch(company):
    admin = User.find([("login", "=", "admin")])[0]
    if company.id not in {c.id for c in admin.companies}:
        admin.companies.append(company)
    admin.company = company
    admin.save()
    pc._context = User.get_preferences(True, {})


report = {"companies": []}

for cid, code in ((1, "IST-HC-QA"), (2, "IST-HC-AE")):
    company = Company(cid)
    switch(company)
    print("===", company.party.name, "===")

    # Demo labels
    for acc in Account.find([("company", "=", company.id)]):
        if MARKER not in (acc.name or ""):
            acc.name = f"{acc.name} ({MARKER})"
            acc.save()

    accounts = get_accounts(company)
    print("kinds", {k: v.name for k, v in accounts.items()})

    # Ensure create_chart properties if defaults missing
    cfg = Config(1)
    need_props = not cfg.default_account_receivable or not cfg.default_account_payable
    if need_props and accounts.get("receivable") and accounts.get("payable"):
        try:
            # Re-run only properties via setting config directly with matching company accounts
            cfg.default_account_receivable = accounts["receivable"]
            cfg.default_account_payable = accounts["payable"]
            cfg.save()
            print("config defaults OK")
        except Exception as exc:
            print("config defaults failed:", exc)
            # Try category accounts if present on config
            for fname, key in (
                ("default_category_account_revenue", "revenue"),
                ("default_category_account_expense", "expense"),
            ):
                if fname in Config._fields and accounts.get(key):
                    try:
                        setattr(cfg, fname, accounts[key])
                    except Exception:
                        pass

    party = Party(Party.find([("code", "=", code)])[0].id)
    try:
        if accounts.get("receivable"):
            party.account_receivable = accounts["receivable"]
        if accounts.get("payable"):
            party.account_payable = accounts["payable"]
        party.save()
        print("party AR/AP OK")
    except Exception as exc:
        print("party AR/AP failed:", exc)
        # Inspect receivable domain-ish fields
        if accounts.get("receivable"):
            r = accounts["receivable"]
            print(
                "receivable detail",
                "type=",
                r.type.name if r.type else None,
                "party_required=",
                getattr(r, "party_required", None),
                "closed=",
                getattr(r, "closed", None),
                "company=",
                r.company.id,
            )

    # Reload party to read MultiValue in context
    party = Party(party.id)
    fys = FiscalYear.find([("company", "=", company.id)])
    ent = {
        "company_id": company.id,
        "party": company.party.name,
        "party_code": code,
        "currency": company.currency.code,
        "accounts": len(Account.find([("company", "=", company.id)])),
        "account_names": [a.name for a in Account.find([("company", "=", company.id)])],
        "fiscalyears": [
            {
                "id": fy.id,
                "name": fy.name,
                "state": fy.state,
                "periods": len(Period.find([("fiscalyear", "=", fy.id)])),
            }
            for fy in fys
        ],
        "party_receivable": (
            party.account_receivable.name if party.account_receivable else None
        ),
        "party_payable": party.account_payable.name if party.account_payable else None,
        "default_receivable": (
            cfg.default_account_receivable.name
            if cfg.default_account_receivable
            else None
        ),
        "default_payable": (
            cfg.default_account_payable.name if cfg.default_account_payable else None
        ),
    }
    report["companies"].append(ent)

report["journals"] = [
    {"code": j.code, "name": j.name, "type": j.type} for j in Journal.find([])
]
report["taxes"] = 0
try:
    report["taxes"] = len(Model.get("account.tax").find([]))
except Exception:
    pass
report["invoices"] = len(Model.get("account.invoice").find([]))
report["posted_moves"] = len(
    Model.get("account.move").find([("state", "=", "posted")])
)

# Primary company back to Qatar
switch(Company(1))
print(json.dumps(report, indent=2))
