#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Final verification JSON for IST Health accounting upload (Proteus only)."""
from __future__ import annotations

import json
import os

from proteus import Model, config as pc

DATABASE = "isthealth"
CONF = os.environ.get(
    "GNUHEALTH_TRYTOND_CONF", "/opt/gnuhealth/his-50/etc/trytond.conf"
)
pc.set_trytond(database=DATABASE, user="admin", config_file=CONF)

User = Model.get("res.user")
Company = Model.get("company.company")
Party = Model.get("party.party")
Account = Model.get("account.account")
FiscalYear = Model.get("account.fiscalyear")
Period = Model.get("account.period")
Journal = Model.get("account.journal")
Invoice = Model.get("account.invoice")
Move = Model.get("account.move")
Currency = Model.get("currency.currency")
Tax = Model.get("account.tax")


def switch(cid: int) -> None:
    admin = User.find([("login", "=", "admin")])[0]
    c = Company(cid)
    ids = {x.id for x in admin.companies}
    if c.id not in ids:
        admin.companies.append(c)
    admin.company = c
    admin.save()
    pc._context = User.get_preferences(True, {})


admin = User.find([("login", "=", "admin")])[0]
for c in Company.find([]):
    if c.id not in {x.id for x in admin.companies}:
        admin.companies.append(c)
admin.company = Company(1)
admin.save()
pc._context = User.get_preferences(True, {})

report = {
    "database": DATABASE,
    "batch_id": "ISTHIS-ACCT-20260715",
    "companies": [],
    "journals": [
        {"code": j.code, "name": j.name, "type": j.type} for j in Journal.find([])
    ],
    "currencies": [],
    "totals": {
        "companies": 0,
        "accounts": 0,
        "fiscalyears": 0,
        "periods": 0,
        "journals": 0,
        "invoices": len(Invoice.find([])),
        "posted_moves": 0,
        "taxes": 0,
    },
}

for code in ("AED", "QAR"):
    cur = Currency.find([("code", "=", code)])[0]
    report["currencies"].append(
        {"code": cur.code, "name": cur.name, "symbol": cur.symbol}
    )

n_accounts = n_fy = n_periods = n_posted = n_taxes = 0
for cid, code in ((1, "IST-HC-QA"), (2, "IST-HC-AE")):
    switch(cid)
    company = Company(cid)
    party = Party(Party.find([("code", "=", code)])[0].id)
    accounts = list(Account.find([("company", "=", cid)]))
    fys = list(FiscalYear.find([("company", "=", cid)]))
    periods = 0
    for fy in fys:
        periods += len(Period.find([("fiscalyear", "=", fy.id)]))
    posted = len(Move.find([("company", "=", cid), ("state", "=", "posted")]))
    taxes = len(Tax.find([("company", "=", cid)])) if "company" in Tax._fields else len(Tax.find([]))
    n_accounts += len(accounts)
    n_fy += len(fys)
    n_periods += periods
    n_posted += posted
    n_taxes += taxes
    report["companies"].append(
        {
            "id": cid,
            "party_code": code,
            "party_name": party.name,
            "currency": company.currency.code,
            "account_count": len(accounts),
            "accounts": [
                {"id": a.id, "name": a.name, "type": a.type.name if a.type else None}
                for a in accounts
            ],
            "fiscalyears": [
                {
                    "id": fy.id,
                    "name": fy.name,
                    "state": fy.state,
                    "periods": len(Period.find([("fiscalyear", "=", fy.id)])),
                }
                for fy in fys
            ],
            "account_receivable": (
                party.account_receivable.name if party.account_receivable else None
            ),
            "account_payable": (
                party.account_payable.name if party.account_payable else None
            ),
        }
    )

report["totals"].update(
    {
        "companies": len(Company.find([])),
        "accounts": n_accounts,
        "fiscalyears": n_fy,
        "periods": n_periods,
        "journals": len(Journal.find([])),
        "posted_moves": n_posted,
        "taxes": n_taxes,
    }
)

switch(1)
out = "/opt/gnuhealth/synthetic-data/accounting/upload_report.json"
with open(out, "w", encoding="utf-8") as fh:
    json.dump(report, fh, indent=2)
print(json.dumps(report, indent=2))
print("Wrote", out)
