#!/usr/bin/env python3
"""Probe IST parties/institutions and CoA wizard models on isthealth."""
from __future__ import annotations

import os
from proteus import Model, Wizard, config as proteus_config

proteus_config.set_trytond(
    database="isthealth",
    user="admin",
    config_file=os.environ.get(
        "GNUHEALTH_TRYTOND_CONF", "/opt/gnuhealth/his-50/etc/trytond.conf"
    ),
)

Party = Model.get("party.party")
print("=== IST-related parties (sample) ===")
for p in Party.find([("name", "ilike", "%IST%")], limit=40):
    print(f"  id={p.id} code={getattr(p,'code',None)!r} name={p.name!r}")

print("=== Iris / Healthcare / Technologies parties ===")
for domain in [
    [("name", "ilike", "%Iris%")],
    [("name", "ilike", "%Healthcare%")],
    [("name", "ilike", "%Technologies%")],
    [("code", "ilike", "IST%")],
]:
    rows = Party.find(domain, limit=20)
    print(f"  domain={domain} count={len(rows)}")
    for p in rows[:10]:
        print(f"    id={p.id} code={getattr(p,'code',None)!r} name={p.name!r}")

try:
    Inst = Model.get("gnuhealth.institution")
    print("=== Institutions ===")
    for i in Inst.find([], limit=30):
        print(
            f"  id={i.id} code={i.code!r} name={i.name if hasattr(i,'name') else i.party.name!r}"
        )
except Exception as e:
    print("institution err", e)

print("=== Company model fields ===")
Company = Model.get("company.company")
print("fields sample:", [f for f in sorted(Company._fields.keys()) if f in (
    "party", "currency", "code", "header", "footer", "timezone", "employee"
)] )

print("=== Account template tree ===")
Template = Model.get("account.account.template")
for t in Template.find([]):
    parent = t.parent.id if t.parent else None
    print(f"  id={t.id} code={getattr(t,'code',None)!r} name={t.name!r} parent={parent}")

print("=== Account type templates ===")
try:
    ATT = Model.get("account.account.type.template")
    for t in ATT.find([], limit=30):
        print(f"  id={t.id} name={t.name!r} parent={t.parent.id if t.parent else None}")
except Exception as e:
    print("type template err", e)

print("=== CreateChart wizard availability ===")
for wiz_name in (
    "account.create_chart",
    "account.create_chart.start",
    "account.create_chart.account",
    "account.create_chart.properties",
):
    try:
        w = Wizard(wiz_name) if wiz_name == "account.create_chart" else None
        if wiz_name == "account.create_chart":
            print(f"  Wizard({wiz_name}) form={w.form_state} states={list(w._states) if hasattr(w,'_states') else 'n/a'}")
            print(f"    form fields: {list(w.form._fields.keys()) if hasattr(w,'form') else w}")
        else:
            M = Model.get(wiz_name)
            print(f"  Model {wiz_name} ok fields={list(M._fields.keys())[:20]}")
    except Exception as e:
        print(f"  {wiz_name}: {e}")

print("=== FiscalYear create_period wizard ===")
for wiz_name in ("account.fiscalyear.create_periods", "account.fiscalyear.create_periods.start"):
    try:
        if wiz_name.endswith("start"):
            M = Model.get(wiz_name)
            print(f"  Model {wiz_name} fields={list(M._fields.keys())}")
        else:
            w = Wizard(wiz_name)
            print(f"  Wizard {wiz_name} form_state={w.form_state}")
    except Exception as e:
        print(f"  {wiz_name}: {e}")

print("=== account.configuration ===")
Config = Model.get("account.configuration")
for c in Config.find([]):
    print(f"  id={c.id}")
    for f in ("default_account_receivable", "default_account_payable", "default_customer_tax_rule", "default_supplier_tax_rule"):
        if f in Config._fields:
            val = getattr(c, f, None)
            print(f"    {f}={val.id if val else None}")
