#!/usr/bin/env python3
"""Assess accounting master data on a GNU Health / Tryton DB (Proteus/trytond).

Run on the HIS VM:
  export GNUHEALTH_TRYTOND_CONF=/opt/gnuhealth/his-50/etc/trytond.conf
  /opt/gnuhealth/his-50/venv/bin/python assess_accounting.py [--database isthealth]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import date


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database", default="isthealth")
    parser.add_argument("--user", default="admin")
    parser.add_argument(
        "--config-file",
        default=os.environ.get(
            "GNUHEALTH_TRYTOND_CONF", "/opt/gnuhealth/his-50/etc/trytond.conf"
        ),
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    from proteus import Model, config as proteus_config

    proteus_config.set_trytond(
        database=args.database,
        user=args.user,
        config_file=args.config_file,
    )

    report: dict = {
        "database": args.database,
        "assessed_on": date.today().isoformat(),
        "companies": [],
        "currencies": [],
        "counts": {},
        "fiscalyears": [],
        "journals": [],
        "sample_accounts": [],
        "invoice_states": {},
        "moves_posted": 0,
        "account_templates": 0,
        "modules_hint": {},
        "safety": {},
    }

    Company = Model.get("company.company")
    Currency = Model.get("currency.currency")
    Party = Model.get("party.party")

    for c in Company.find([]):
        party = c.party
        cur = c.currency
        report["companies"].append(
            {
                "id": c.id,
                "party_name": party.name if party else None,
                "party_code": getattr(party, "code", None) if party else None,
                "currency": cur.code if cur else None,
                "code": getattr(c, "code", None),
            }
        )

    for cur in Currency.find(
        [("code", "in", ["AED", "QAR", "USD", "EUR", "GBP"])]
    ):
        report["currencies"].append(
            {
                "id": cur.id,
                "code": cur.code,
                "name": cur.name,
                "symbol": cur.symbol,
            }
        )

    def count(model: str) -> int:
        try:
            M = Model.get(model)
            return len(M.find([]))
        except Exception as exc:  # noqa: BLE001
            report["modules_hint"][model] = str(exc)
            return -1

    for model in (
        "account.account",
        "account.account.type",
        "account.account.template",
        "account.fiscalyear",
        "account.period",
        "account.journal",
        "account.invoice",
        "account.move",
        "account.tax",
        "account.configuration",
        "party.party",
    ):
        report["counts"][model] = count(model)

    try:
        FY = Model.get("account.fiscalyear")
        for fy in FY.find([]):
            periods = []
            try:
                Period = Model.get("account.period")
                for p in Period.find([("fiscalyear", "=", fy.id)]):
                    periods.append(
                        {
                            "id": p.id,
                            "name": p.name,
                            "start_date": str(p.start_date),
                            "end_date": str(p.end_date),
                            "state": p.state,
                            "type": getattr(p, "type", None),
                        }
                    )
            except Exception as exc:  # noqa: BLE001
                periods = [{"error": str(exc)}]
            report["fiscalyears"].append(
                {
                    "id": fy.id,
                    "name": fy.name,
                    "company": fy.company.party.name if fy.company else None,
                    "start_date": str(fy.start_date),
                    "end_date": str(fy.end_date),
                    "state": fy.state,
                    "periods": len(periods),
                    "period_sample": periods[:3],
                }
            )
    except Exception as exc:  # noqa: BLE001
        report["modules_hint"]["account.fiscalyear"] = str(exc)

    try:
        Journal = Model.get("account.journal")
        for j in Journal.find([]):
            report["journals"].append(
                {
                    "id": j.id,
                    "name": j.name,
                    "code": getattr(j, "code", None),
                    "type": j.type,
                }
            )
    except Exception as exc:  # noqa: BLE001
        report["modules_hint"]["account.journal"] = str(exc)

    try:
        Account = Model.get("account.account")
        for a in Account.find([], limit=30):
            report["sample_accounts"].append(
                {
                    "id": a.id,
                    "code": a.code,
                    "name": a.name,
                    "type": a.type.name if a.type else None,
                    "company": a.company.party.name if a.company else None,
                }
            )
    except Exception as exc:  # noqa: BLE001
        report["modules_hint"]["account.account"] = str(exc)

    try:
        Invoice = Model.get("account.invoice")
        states: dict[str, int] = {}
        for inv in Invoice.find([]):
            states[inv.state] = states.get(inv.state, 0) + 1
        report["invoice_states"] = states
    except Exception as exc:  # noqa: BLE001
        report["modules_hint"]["account.invoice"] = str(exc)

    try:
        Move = Model.get("account.move")
        report["moves_posted"] = len(Move.find([("state", "=", "posted")]))
        report["counts"]["account.move.posted"] = report["moves_posted"]
        report["counts"]["account.move.draft"] = len(
            Move.find([("state", "=", "draft")])
        )
    except Exception as exc:  # noqa: BLE001
        report["modules_hint"]["account.move"] = str(exc)

    try:
        Template = Model.get("account.account.template")
        report["account_templates"] = len(Template.find([]))
        roots = Template.find([("parent", "=", None)], limit=20)
        report["template_roots"] = [
            {"id": t.id, "name": t.name, "code": getattr(t, "code", None)}
            for t in roots
        ]
    except Exception as exc:  # noqa: BLE001
        report["modules_hint"]["account.account.template"] = str(exc)

    # Party receivable/payable sample for company parties
    try:
        party_acct = []
        for c in report["companies"]:
            code = c.get("party_code")
            if not code:
                continue
            parties = Party.find([("code", "=", code)], limit=1)
            if not parties:
                continue
            p = parties[0]
            party_acct.append(
                {
                    "party": p.name,
                    "code": p.code,
                    "account_receivable": (
                        p.account_receivable.code
                        if getattr(p, "account_receivable", None)
                        else None
                    ),
                    "account_payable": (
                        p.account_payable.code
                        if getattr(p, "account_payable", None)
                        else None
                    ),
                }
            )
        report["company_party_accounts"] = party_acct
    except Exception as exc:  # noqa: BLE001
        report["modules_hint"]["party_accounts"] = str(exc)

    n_accounts = report["counts"].get("account.account", 0)
    n_moves = report["counts"].get("account.move", 0)
    posted = report.get("moves_posted", 0)
    report["safety"] = {
        "coa_exists": n_accounts > 0,
        "posted_moves_exist": posted > 0,
        "any_moves": n_moves > 0,
        "safe_to_create_coa_from_scratch": n_accounts <= 0 and posted <= 0,
        "safe_to_recreate_coa": False,  # never drop blindly
        "recommendation": (
            "Create CoA / FY / journals via Proteus (no posted moves)."
            if n_accounts <= 0 and posted <= 0
            else (
                "CoA exists with posted moves — align labels/defaults only; do NOT drop CoA."
                if posted > 0
                else "CoA and/or moves exist — update idempotently; do NOT drop CoA."
            )
        ),
    }

    if args.json:
        print(json.dumps(report, indent=2, default=str))
    else:
        print("=== IST Health accounting assessment ===")
        print(f"database: {args.database}")
        print("companies:")
        for c in report["companies"]:
            print(f"  {c}")
        print("currencies:", report["currencies"])
        print("counts:", report["counts"])
        print("fiscalyears:", report["fiscalyears"])
        print("journals:", report["journals"])
        print("invoice_states:", report["invoice_states"])
        print("template_roots:", report.get("template_roots"))
        print("safety:", report["safety"])
        print("modules_hint:", report["modules_hint"])

    return 0


if __name__ == "__main__":
    sys.exit(main())
