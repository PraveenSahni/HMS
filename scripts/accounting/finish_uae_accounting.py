#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Finish UAE fiscal year + party AR/AP after partial accounting upload."""
from __future__ import annotations

import os
from datetime import date

from proteus import Model, Wizard, config as pc

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
FiscalYear = Model.get("account.fiscalyear")
Period = Model.get("account.period")

admin = User.find([("login", "=", "admin")])[0]
qa = Company(1)
uae = Company(2)
for c in (qa, uae):
    if c.id not in {x.id for x in admin.companies}:
        admin.companies.append(c)
admin.company = uae
admin.save()
pc._context = User.get_preferences(True, {})
print(
    "context company=",
    pc._context.get("company"),
    "companies=",
    pc._context.get("companies"),
)

from trytond.modules.account.tests.tools import create_fiscalyear, get_accounts
from trytond.modules.account_invoice.tests.tools import (
    set_fiscalyear_invoice_sequences,
)

existing = FiscalYear.find([("company", "=", uae.id)], limit=1)
if existing:
    fy = existing[0]
    print("UAE FY exists", fy.id, fy.name)
else:
    fy = create_fiscalyear(uae, today=(date(2026, 1, 1), date(2026, 12, 31)))
    fy.name = "2026 - IST Healthcare UAE (ISTHIS-ACCT-20260715)"
    fy = set_fiscalyear_invoice_sequences(fy)
    for s in fy.invoice_sequences:
        if not s.company:
            s.company = uae
    fy.save()
    print("UAE FY created", fy.id)

n_periods = len(Period.find([("fiscalyear", "=", fy.id)]))
if n_periods == 0:
    w = Wizard("account.fiscalyear.create_periods", [fy])
    w.form.frequency = "monthly"
    w.form.interval = 1
    w.form.end_day = 31
    w.execute("create_periods")
    n_periods = len(Period.find([("fiscalyear", "=", fy.id)]))
print("UAE periods", n_periods)

# Brand Qatar FY name if still plain
qa_fy = FiscalYear.find([("company", "=", qa.id)], limit=1)
if qa_fy and qa_fy[0].name == "2026":
    qa_fy[0].name = "2026 - IST Healthcare Qatar (ISTHIS-ACCT-20260715)"
    qa_fy[0].save()
    print("Renamed Qatar FY")

for code, company in (("IST-HC-QA", qa), ("IST-HC-AE", uae)):
    admin.company = company
    admin.save()
    pc._context = User.get_preferences(True, {})
    p = Party.find([("code", "=", code)])[0]
    accs = get_accounts(company)
    changed = False
    if accs.get("receivable") and p.account_receivable != accs["receivable"]:
        p.account_receivable = accs["receivable"]
        changed = True
    if accs.get("payable") and p.account_payable != accs["payable"]:
        p.account_payable = accs["payable"]
        changed = True
    if changed:
        p.save()
    print(
        code,
        "AR=",
        p.account_receivable.name if p.account_receivable else None,
        "AP=",
        p.account_payable.name if p.account_payable else None,
        "changed=",
        changed,
    )

# Ensure admin has both companies; primary Qatar for demo
admin = User.find([("login", "=", "admin")])[0]
for c in (qa, uae):
    if c.id not in {x.id for x in admin.companies}:
        admin.companies.append(c)
admin.company = qa
admin.save()
print("admin companies OK; primary=Qatar")
print("DONE")
