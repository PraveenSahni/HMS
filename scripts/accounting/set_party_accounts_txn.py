#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Set party AR/AP using trytond Transaction with correct company context."""
from __future__ import annotations

import os

from proteus import Model, config as pc

DATABASE = "isthealth"
CONF = os.environ.get(
    "GNUHEALTH_TRYTOND_CONF", "/opt/gnuhealth/his-50/etc/trytond.conf"
)

pc.set_trytond(database=DATABASE, user="admin", config_file=CONF)

from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.modules.account.tests.tools import get_accounts

User = Model.get("res.user")
Company = Model.get("company.company")
Party = Model.get("party.party")
Account = Model.get("account.account")
FiscalYear = Model.get("account.fiscalyear")
Period = Model.get("account.period")


def switch(cid: int) -> None:
    admin = User.find([("login", "=", "admin")])[0]
    c = Company(cid)
    if c.id not in {x.id for x in admin.companies}:
        admin.companies.append(c)
    admin.company = c
    admin.save()
    pc._context = User.get_preferences(True, {})


admin_id = User.find([("login", "=", "admin")])[0].id
pool = Pool(DATABASE)

# Inspect existing
with Transaction().start(DATABASE, admin_id, context={"company": 1, "companies": [1, 2]}):
    PartyAccount = pool.get("party.party.account")
    rows = PartyAccount.search([])
    print(
        "existing",
        [
            (
                r.id,
                r.party.id,
                r.company.id if r.company else None,
                r.account_receivable.id if r.account_receivable else None,
                r.account_payable.id if r.account_payable else None,
            )
            for r in rows
        ],
    )

for cid, code in ((1, "IST-HC-QA"), (2, "IST-HC-AE")):
    switch(cid)
    company = Company(cid)
    for a in Account.find([("company", "=", cid)]):
        if "IST Health demo" not in (a.name or ""):
            a.name = f"{a.name} (IST Health demo)"
            a.save()
    accs = get_accounts(company)
    party_id = Party.find([("code", "=", code)])[0].id
    print(code, "accs", {k: v.id for k, v in accs.items()})

    ctx = {"company": cid, "companies": [1, 2]}
    with Transaction().start(DATABASE, admin_id, context=ctx) as txn:
        PartyAccount = pool.get("party.party.account")
        Config = pool.get("account.configuration")
        existing = PartyAccount.search(
            [("party", "=", party_id), ("company", "=", cid)]
        )
        vals = {
            "account_receivable": accs["receivable"].id,
            "account_payable": accs["payable"].id,
        }
        try:
            if existing:
                PartyAccount.write(existing, vals)
                print(code, "updated", [e.id for e in existing])
            else:
                rec = PartyAccount(
                    party=party_id,
                    company=cid,
                    account_receivable=vals["account_receivable"],
                    account_payable=vals["account_payable"],
                )
                rec.save()
                print(code, "created", rec.id)
        except Exception as exc:
            print(code, "PartyAccount failed:", type(exc).__name__, exc)

        try:
            confs = Config.search([])
            conf = confs[0]
            Config.write(
                [conf],
                {
                    "default_account_receivable": accs["receivable"].id,
                    "default_account_payable": accs["payable"].id,
                },
            )
            print(code, "config OK")
        except Exception as exc:
            print(code, "config failed:", type(exc).__name__, exc)
        txn.commit()

report = []
for cid, code in ((1, "IST-HC-QA"), (2, "IST-HC-AE")):
    switch(cid)
    p = Party(Party.find([("code", "=", code)])[0].id)
    row = {
        "code": code,
        "company": Company(cid).party.name,
        "currency": Company(cid).currency.code,
        "accounts": len(Account.find([("company", "=", cid)])),
        "fiscalyears": len(FiscalYear.find([("company", "=", cid)])),
        "periods": len(Period.find([])),
        "AR": p.account_receivable.name if p.account_receivable else None,
        "AP": p.account_payable.name if p.account_payable else None,
    }
    report.append(row)
    print("VERIFY", row)

switch(1)
print("DONE")
