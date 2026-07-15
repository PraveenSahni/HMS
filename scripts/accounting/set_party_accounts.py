#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Set party AR/AP + account.configuration defaults per company context."""
from __future__ import annotations

import os

from proteus import Model, config as pc

pc.set_trytond(
    database="isthealth",
    user="admin",
    config_file=os.environ.get(
        "GNUHEALTH_TRYTOND_CONF", "/opt/gnuhealth/his-50/etc/trytond.conf"
    ),
)

User = Model.get("res.user")
Company = Model.get("company.company")
Party = Model.get("party.party")
Config = Model.get("account.configuration")
Account = Model.get("account.account")

from trytond.modules.account.tests.tools import get_accounts

admin = User.find([("login", "=", "admin")])[0]
for cid in (1, 2):
    c = Company(cid)
    if c.id not in {x.id for x in admin.companies}:
        admin.companies.append(c)
admin.save()

for cid, code in ((1, "IST-HC-QA"), (2, "IST-HC-AE")):
    company = Company(cid)
    admin.company = company
    admin.save()
    pc._context = User.get_preferences(True, {})
    print("===", code, "ctx company", pc._context.get("company"), "===")

    accs = get_accounts(company)
    print("accounts", {k: (v.id, v.name) for k, v in accs.items()})

    # Configuration defaults (company-scoped MultiValue)
    cfg = Config(1)
    if accs.get("receivable"):
        cfg.default_account_receivable = accs["receivable"]
    if accs.get("payable"):
        cfg.default_account_payable = accs["payable"]
    try:
        cfg.save()
        print("configuration defaults saved")
    except Exception as exc:
        print("configuration save:", exc)

    party = Party.find([("code", "=", code)])[0]
    # Reload party in current context
    party = Party(party.id)
    try:
        if accs.get("receivable"):
            party.account_receivable = accs["receivable"]
        if accs.get("payable"):
            party.account_payable = accs["payable"]
        party.save()
        print(
            "party AR/AP set",
            party.account_receivable.name if party.account_receivable else None,
            party.account_payable.name if party.account_payable else None,
        )
    except Exception as exc:
        print("party AR/AP via proteus failed:", type(exc).__name__, exc)
        # Fallback: write party.party.account MultiValue model directly
        try:
            PartyAccount = Model.get("party.party.account")
            rows = PartyAccount.find(
                [("party", "=", party.id), ("company", "=", company.id)]
            )
            if rows:
                row = rows[0]
            else:
                row = PartyAccount()
                row.party = party
                row.company = company
            if accs.get("receivable"):
                row.account_receivable = accs["receivable"]
            if accs.get("payable"):
                row.account_payable = accs["payable"]
            row.save()
            print("party.party.account row saved id=", row.id)
        except Exception as exc2:
            print("party.party.account fallback failed:", type(exc2).__name__, exc2)

admin.company = Company(1)
admin.save()
print("DONE")
