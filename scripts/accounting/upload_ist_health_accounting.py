#!/usr/bin/env python3
"""Align and upload IST Health accounting master data into a GNU Health DB.

Idempotent Proteus/trytond uploader for demo DB ``isthealth`` (or --database).

Creates / aligns (per legal company):
  - Currencies AED + QAR (symbols)
  - Parties + company.company for IST Healthcare Qatar (QAR) and UAE (AED)
  - Chart of Accounts from Tryton Minimal Account Chart template
  - Fiscal year + monthly periods for the current calendar year
  - Default receivable/payable on company parties + account.configuration
  - Journal presence check (Cash / Expense / Revenue / … — shared Tryton journals)

Taxes: NOT invented. Leaves tax config unset; optional --demo-tax-zero creates a
clearly marked synthetic 0% tax (still needs counsel confirmation for real rates).

Safety:
  - Refuses to drop / recreate CoA when posted account.move rows exist for a company
  - Skips create_chart when accounts already exist for that company

Run on HIS VM (same pattern as max-demo):
  export GNUHEALTH_TRYTOND_CONF=/opt/gnuhealth/his-50/etc/trytond.conf
  /opt/gnuhealth/his-50/venv/bin/python upload_ist_health_accounting.py --dry-run
  /opt/gnuhealth/his-50/venv/bin/python upload_ist_health_accounting.py --execute

Synthetic markers: party codes IST-HC-QA / IST-HC-AE; account name suffix
\"(IST Health demo)\"; batch note in fiscal year name.
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from datetime import date
from typing import Any

logger = logging.getLogger("ist_health_accounting")

BATCH_ID = "ISTHIS-ACCT-20260715"
SYNTHETIC_MARKER = "IST Health demo"
YEAR = date.today().year

# Legal entities for UAE + Qatar side-by-side multi-company demo
ENTITIES = [
    {
        "party_code": "IST-HC-QA",
        "party_name": "IST Healthcare Qatar",
        "party_aliases": ("IST-CO", "IST Technologies LLC", "IST Healthcare Group"),
        "currency": "QAR",
        "currency_name": "Qatari Rial",
        "currency_symbol": "QR",
        "country_hint": "QA",
        "legal_note": (
            f"Synthetic/{SYNTHETIC_MARKER}. Legal/tech brands: "
            "Iris Star / IST Technologies / IST Health. Batch {batch}."
        ),
        "reuse_existing_codes": ("IST-CO",),  # align existing demo party if present
    },
    {
        "party_code": "IST-HC-AE",
        "party_name": "IST Healthcare UAE",
        "party_aliases": (),
        "currency": "AED",
        "currency_name": "UAE Dirham",
        "currency_symbol": "AED",
        "country_hint": "AE",
        "legal_note": (
            f"Synthetic/{SYNTHETIC_MARKER}. IST Healthcare UAE (AED). "
            "Iris Star / IST Technologies. Batch {batch}."
        ),
        "reuse_existing_codes": (),
    },
]


def _connect(database: str, user: str, config_file: str):
    from proteus import Model, Wizard, config as proteus_config

    proteus_config.set_trytond(
        database=database,
        user=user,
        config_file=config_file,
    )
    return Model, Wizard, proteus_config


def _refresh_user_context(Model, proteus_config) -> None:
    User = Model.get("res.user")
    proteus_config._context = User.get_preferences(True, {})


def ensure_currency(Model, code: str, name: str, symbol: str, dry_run: bool) -> Any:
    Currency = Model.get("currency.currency")
    found = Currency.find([("code", "=", code)], limit=1)
    if found:
        cur = found[0]
        changed = False
        if not cur.symbol and symbol:
            cur.symbol = symbol
            changed = True
        if dry_run:
            logger.info("[dry-run] currency %s exists id=%s (symbol update=%s)", code, cur.id, changed)
            return cur
        if changed:
            cur.save()
            logger.info("Updated currency %s symbol=%s", code, symbol)
        else:
            logger.info("Currency %s already OK id=%s", code, cur.id)
        return cur

    if dry_run:
        logger.info("[dry-run] would create currency %s", code)
        return None

    cur = Currency(name=name, code=code, symbol=symbol)
    if hasattr(cur, "digits") and cur.digits is None:
        cur.digits = 2
    if hasattr(cur, "rounding") and not cur.rounding:
        cur.rounding = 0.01
    cur.save()
    logger.info("Created currency %s id=%s", code, cur.id)
    return cur


def find_or_align_party(Model, entity: dict, dry_run: bool) -> Any:
    Party = Model.get("party.party")
    code = entity["party_code"]
    name = entity["party_name"]

    found = Party.find([("code", "=", code)], limit=1)
    if found:
        party = found[0]
        if party.name != name and not dry_run:
            party.name = name
            party.save()
            logger.info("Aligned party name %s → %s", code, name)
        else:
            logger.info("Party %s exists id=%s name=%r", code, party.id, party.name)
        return party

    # Reuse legacy demo party (e.g. IST-CO) for Qatar company
    for legacy in entity.get("reuse_existing_codes") or ():
        legacy_hits = Party.find([("code", "=", legacy)], limit=1)
        if not legacy_hits:
            continue
        party = legacy_hits[0]
        if dry_run:
            logger.info(
                "[dry-run] would realign party id=%s code %s→%s name %r→%r",
                party.id,
                party.code,
                code,
                party.name,
                name,
            )
            return party
        old_code, old_name = party.code, party.name
        party.code = code
        party.name = name
        # Keep institution linkage; note brands in a free-text field if present
        note = entity["legal_note"].format(batch=BATCH_ID)
        for field in ("comment", "extra_info"):
            if field in Party._fields:
                existing = getattr(party, field, None) or ""
                if BATCH_ID not in existing:
                    setattr(party, field, (existing + "\n" + note).strip())
                break
        party.save()
        logger.info(
            "Realigned party id=%s %s/%s → %s/%s",
            party.id,
            old_code,
            old_name,
            code,
            name,
        )
        return party

    if dry_run:
        logger.info("[dry-run] would create party %s %r", code, name)
        return None

    party = Party(name=name, code=code)
    if "is_institution" in Party._fields:
        party.is_institution = True
    if "is_person" in Party._fields:
        party.is_person = False
    note = entity["legal_note"].format(batch=BATCH_ID)
    for field in ("comment", "extra_info"):
        if field in Party._fields:
            setattr(party, field, note)
            break
    party.save()
    logger.info("Created party %s id=%s", code, party.id)
    return party


def ensure_company(Model, Wizard, proteus_config, party, currency, dry_run: bool) -> Any:
    Company = Model.get("company.company")
    if party is None or currency is None:
        logger.info("[dry-run] skip company create (party/currency pending)")
        return None

    existing = Company.find([("party", "=", party.id)], limit=1)
    if existing:
        company = existing[0]
        if company.currency and company.currency.id != currency.id and not dry_run:
            company.currency = currency
            company.save()
            logger.info("Updated company currency for %s → %s", party.name, currency.code)
        else:
            logger.info(
                "Company exists id=%s party=%r currency=%s",
                company.id,
                party.name,
                company.currency.code if company.currency else None,
            )
        return company

    if dry_run:
        logger.info("[dry-run] would create company for %r / %s", party.name, currency.code)
        return None

    # Prefer company.company.config wizard (sets employee/user links properly)
    company_config = Wizard("company.company.config")
    company_config.execute("company")
    form = company_config.form
    form.party = party
    form.currency = currency
    company_config.execute("add")
    _refresh_user_context(Model, proteus_config)

    companies = Company.find([("party", "=", party.id)], limit=1)
    if not companies:
        raise RuntimeError(f"company.company not created for party {party.id}")
    company = companies[0]
    logger.info("Created company id=%s party=%r currency=%s", company.id, party.name, currency.code)
    return company


def assign_user_companies(Model, companies: list, dry_run: bool) -> None:
    if not companies:
        return
    User = Model.get("res.user")
    admin = User.find([("login", "=", "admin")], limit=1)[0]
    if dry_run:
        logger.info("[dry-run] would assign admin to %s companies", len(companies))
        return
    # proteus Many2Many: assign companies then set primary
    current_ids = {c.id for c in admin.companies}
    for company in companies:
        if company.id not in current_ids:
            admin.companies.append(company)
    if not admin.company:
        admin.company = companies[0]
    admin.save()
    logger.info(
        "Admin user companies=%s primary=%s",
        [c.party.name for c in admin.companies],
        admin.company.party.name if admin.company else None,
    )


def switch_company_context(Model, proteus_config, company) -> None:
    """Ensure admin can create company-scoped records (sequences, CoA, FY)."""
    if company is None:
        return
    User = Model.get("res.user")
    admin = User.find([("login", "=", "admin")], limit=1)[0]
    current_ids = {c.id for c in admin.companies}
    if company.id not in current_ids:
        admin.companies.append(company)
    admin.company = company
    admin.save()
    _refresh_user_context(Model, proteus_config)
    logger.info("Switched admin context to company %s (%s)", company.id, company.party.name)


def company_has_accounts(Model, company) -> bool:
    Account = Model.get("account.account")
    return bool(Account.find([("company", "=", company.id)], limit=1))


def company_has_posted_moves(Model, company) -> bool:
    Move = Model.get("account.move")
    return bool(
        Move.find([("company", "=", company.id), ("state", "=", "posted")], limit=1)
    )


def create_chart_for_company(Model, Wizard, company, dry_run: bool) -> dict[str, Any]:
    result = {"company": company.party.name, "action": "skip", "accounts": 0}
    if company_has_accounts(Model, company):
        Account = Model.get("account.account")
        n = len(Account.find([("company", "=", company.id)]))
        result["action"] = "already_exists"
        result["accounts"] = n
        if company_has_posted_moves(Model, company):
            result["note"] = "posted moves exist — CoA left untouched"
        logger.info("CoA already exists for %s (%s accounts)", company.party.name, n)
        return result

    if dry_run:
        result["action"] = "would_create"
        logger.info("[dry-run] would create Minimal CoA for %s", company.party.name)
        return result

    AccountTemplate = Model.get("account.account.template")
    ModelData = Model.get("ir.model.data")
    data = ModelData.find(
        [("module", "=", "account"), ("fs_id", "=", "account_template_root_en")],
        limit=1,
    )[0]
    account_template = AccountTemplate(data.db_id)

    create_chart = Wizard("account.create_chart")
    create_chart.execute("account")
    create_chart.form.account_template = account_template
    create_chart.form.company = company
    create_chart.execute("create_account")

    from trytond.modules.account.tests.tools import get_accounts

    accounts = get_accounts(company)
    try:
        if accounts.get("receivable") and getattr(
            accounts["receivable"], "party_required", False
        ):
            create_chart.form.account_receivable = accounts["receivable"]
        if accounts.get("payable") and getattr(accounts["payable"], "party_required", False):
            create_chart.form.account_payable = accounts["payable"]
        create_chart.execute("create_properties")
    except Exception as exc:  # noqa: BLE001
        logger.warning("create_properties for %s: %s", company.party.name, exc)

    # Demo-friendly labels (idempotent suffix)
    Account = Model.get("account.account")
    for acc in Account.find([("company", "=", company.id)]):
        if SYNTHETIC_MARKER not in (acc.name or ""):
            acc.name = f"{acc.name} ({SYNTHETIC_MARKER})"
            acc.save()

    n = len(Account.find([("company", "=", company.id)]))
    if n == 0:
        result["action"] = "failed_empty"
        result["note"] = (
            "create_chart returned 0 accounts — check admin company context / ACL"
        )
        logger.error("CoA empty after wizard for %s", company.party.name)
        return result

    result["action"] = "created"
    result["accounts"] = n
    result["kinds"] = {
        k: (v.code if getattr(v, "code", None) else v.name) for k, v in accounts.items()
    }
    logger.info("Created CoA for %s — %s accounts", company.party.name, n)
    return result


def ensure_fiscalyear(Model, Wizard, company, year: int, dry_run: bool) -> dict[str, Any]:
    FiscalYear = Model.get("account.fiscalyear")
    Period = Model.get("account.period")

    name = f"{year} — {company.party.name} ({BATCH_ID})"
    existing = FiscalYear.find(
        [
            ("company", "=", company.id),
            ("start_date", ">=", date(year, 1, 1)),
            ("end_date", "<=", date(year, 12, 31)),
        ],
        limit=1,
    )
    # Also match create_fiscalyear default name = str(year)
    if not existing:
        existing = FiscalYear.find(
            [("company", "=", company.id), ("name", "ilike", f"%{year}%")],
            limit=1,
        )
    if existing:
        fy = existing[0]
        n_periods = len(Period.find([("fiscalyear", "=", fy.id)]))
        if n_periods == 0 and not dry_run:
            create_periods = Wizard("account.fiscalyear.create_periods", [fy])
            create_periods.form.frequency = "monthly"
            if "interval" in create_periods.form._fields:
                create_periods.form.interval = 1
            if "end_day" in create_periods.form._fields:
                create_periods.form.end_day = 31
            create_periods.execute("create_periods")
            n_periods = len(Period.find([("fiscalyear", "=", fy.id)]))
            logger.info("Created missing periods for FY id=%s → %s", fy.id, n_periods)
            return {"action": "periods_added", "id": fy.id, "periods": n_periods, "name": fy.name}
        logger.info("Fiscal year exists id=%s periods=%s", fy.id, n_periods)
        return {"action": "already_exists", "id": fy.id, "periods": n_periods, "name": fy.name}

    if dry_run:
        logger.info("[dry-run] would create FY %s for %s", year, company.party.name)
        return {"action": "would_create", "name": name}

    from trytond.modules.account.tests.tools import create_fiscalyear
    from trytond.modules.account_invoice.tests.tools import (
        set_fiscalyear_invoice_sequences,
    )

    fy = create_fiscalyear(company, today=(date(year, 1, 1), date(year, 12, 31)))
    # Prefer IST-branded name once company is attached
    fy.name = name
    fy = set_fiscalyear_invoice_sequences(fy)
    for seq in getattr(fy, "invoice_sequences", []) or []:
        if not getattr(seq, "company", None):
            seq.company = company
    fy.save()

    create_periods = Wizard("account.fiscalyear.create_periods", [fy])
    create_periods.form.frequency = "monthly"
    if "interval" in create_periods.form._fields:
        create_periods.form.interval = 1
    if "end_day" in create_periods.form._fields:
        create_periods.form.end_day = 31
    create_periods.execute("create_periods")

    n_periods = len(Period.find([("fiscalyear", "=", fy.id)]))
    logger.info("Created FY %s id=%s with %s periods", name, fy.id, n_periods)
    return {"action": "created", "id": fy.id, "periods": n_periods, "name": name}


def set_party_accounts(Model, company, party, dry_run: bool) -> dict[str, Any]:
    from trytond.modules.account.tests.tools import get_accounts
    from trytond.pool import Pool
    from trytond.transaction import Transaction

    accounts = get_accounts(company)
    receivable = accounts.get("receivable")
    payable = accounts.get("payable")
    out = {
        "party": party.name,
        "receivable": receivable.name if receivable else None,
        "payable": payable.name if payable else None,
    }
    if dry_run:
        out["action"] = "would_set"
        return out
    if not receivable or not payable:
        out["action"] = "skip_missing_accounts"
        return out

    # MultiValue party.party.account is unreliable via Proteus write under some
    # company contexts — use trytond Transaction with explicit company context.
    db_name = os.environ.get("GNUHEALTH_DATABASE", "isthealth")
    try:
        from proteus import config as proteus_config

        db_name = proteus_config.get_config().database_name
    except Exception:  # noqa: BLE001
        pass

    User = Model.get("res.user")
    uid = User.find([("login", "=", "admin")])[0].id
    pool = Pool(db_name)
    ctx = {"company": company.id, "companies": [company.id]}
    # Include sibling companies if present on admin
    admin = User.find([("login", "=", "admin")])[0]
    sibling_ids = [c.id for c in admin.companies] or [company.id]
    ctx["companies"] = sibling_ids

    with Transaction().start(db_name, uid, context=ctx) as txn:
        PartyAccount = pool.get("party.party.account")
        Config = pool.get("account.configuration")
        existing = PartyAccount.search(
            [("party", "=", party.id), ("company", "=", company.id)]
        )
        vals = {
            "account_receivable": receivable.id,
            "account_payable": payable.id,
        }
        if existing:
            PartyAccount.write(existing, vals)
            out["action"] = "updated"
            out["party_account_ids"] = [e.id for e in existing]
        else:
            # Delete mismatched company rows for this party (demo hygiene)
            mismatched = PartyAccount.search(
                [
                    ("party", "=", party.id),
                    ("company", "!=", company.id),
                    ("account_receivable", "=", None),
                    ("account_payable", "=", None),
                ]
            )
            if mismatched:
                PartyAccount.delete(mismatched)
            rec = PartyAccount(
                party=party.id,
                company=company.id,
                account_receivable=receivable.id,
                account_payable=payable.id,
            )
            rec.save()
            out["action"] = "created"
            out["party_account_ids"] = [rec.id]
        try:
            confs = Config.search([])
            if confs:
                Config.write(
                    confs,
                    {
                        "default_account_receivable": receivable.id,
                        "default_account_payable": payable.id,
                    },
                )
                out["configuration"] = "updated"
        except Exception as exc:  # noqa: BLE001
            out["configuration"] = f"skip: {exc}"
        txn.commit()
    return out


def ensure_journals(Model, dry_run: bool) -> dict[str, Any]:
    """Journals are global in Tryton account; verify required set for invoice posting."""
    Journal = Model.get("account.journal")
    required = {
        "CASH": ("Cash", "cash"),
        "EXP": ("Expense", "expense"),
        "REV": ("Revenue", "revenue"),
        "MISC": ("Miscellaneous", "general"),
    }
    present = {j.code: j for j in Journal.find([])}
    created = []
    missing = []
    for code, (name, jtype) in required.items():
        if code in present:
            continue
        missing.append(code)
        if dry_run:
            continue
        j = Journal(name=name, code=code, type=jtype)
        j.save()
        created.append(code)
        present[code] = j
    return {
        "existing": sorted(present.keys()),
        "created": created,
        "missing_before": missing,
        "action": "ok" if not missing or created else ("would_create" if dry_run else "partial"),
    }


def maybe_demo_tax_zero(Model, company, dry_run: bool, enabled: bool) -> dict[str, Any]:
    if not enabled:
        return {
            "action": "skipped",
            "note": "Taxes left unset — VAT/healthcare rates need confirmation (no invented rates).",
        }
    Tax = Model.get("account.tax")
    name = f"DEMO 0% — SYNTHETIC — needs confirmation ({BATCH_ID})"
    existing = Tax.find([("name", "=", name), ("company", "=", company.id)], limit=1)
    if existing:
        return {"action": "already_exists", "id": existing[0].id, "name": name}
    if dry_run:
        return {"action": "would_create", "name": name}
    tax = Tax(name=name, company=company)
    # Minimal fields — rate 0; type/kind vary by Tryton version
    if "rate" in Tax._fields:
        tax.rate = 0
    if "type" in Tax._fields:
        tax.type = "percentage"
    if "description" in Tax._fields:
        tax.description = (
            "SYNTHETIC/DEMO placeholder only. Not a legal VAT rate. "
            "Replace after counsel/finance confirmation."
        )
    tax.save()
    return {"action": "created", "id": tax.id, "name": name}


def run(args: argparse.Namespace) -> dict[str, Any]:
    dry_run = not args.execute
    Model, Wizard, proteus_config = _connect(args.database, args.user, args.config_file)

    report: dict[str, Any] = {
        "database": args.database,
        "batch_id": BATCH_ID,
        "dry_run": dry_run,
        "year": YEAR,
        "entities": [],
        "journals": {},
        "taxes_policy": "unset_unless_demo_tax_zero",
        "safety": {},
    }

    # Global safety
    Move = Model.get("account.move")
    posted_all = len(Move.find([("state", "=", "posted")]))
    report["safety"] = {
        "posted_moves_total": posted_all,
        "coa_drop_forbidden": True,
    }

    report["journals"] = ensure_journals(Model, dry_run)

    companies_created = []
    for entity in ENTITIES:
        ent_report: dict[str, Any] = {"spec": entity["party_code"], "currency": entity["currency"]}
        currency = ensure_currency(
            Model,
            entity["currency"],
            entity["currency_name"],
            entity["currency_symbol"],
            dry_run,
        )
        party = find_or_align_party(Model, entity, dry_run)
        company = ensure_company(Model, Wizard, proteus_config, party, currency, dry_run)
        ent_report["party_id"] = party.id if party else None
        ent_report["company_id"] = company.id if company else None

        if company:
            companies_created.append(company)
            if not dry_run:
                switch_company_context(Model, proteus_config, company)
            if company_has_posted_moves(Model, company):
                ent_report["coa"] = {
                    "action": "blocked",
                    "note": "Posted moves exist — refusing CoA recreate; align labels/defaults only.",
                }
                # Still ensure FY if missing
                ent_report["fiscalyear"] = ensure_fiscalyear(Model, Wizard, company, YEAR, dry_run)
                if party and company_has_accounts(Model, company):
                    ent_report["party_accounts"] = set_party_accounts(
                        Model, company, party, dry_run
                    )
            else:
                ent_report["coa"] = create_chart_for_company(Model, Wizard, company, dry_run)
                ent_report["fiscalyear"] = ensure_fiscalyear(Model, Wizard, company, YEAR, dry_run)
                if party and (
                    dry_run or company_has_accounts(Model, company)
                ):
                    ent_report["party_accounts"] = set_party_accounts(
                        Model, company, party, dry_run
                    )
            ent_report["tax"] = maybe_demo_tax_zero(
                Model, company, dry_run, enabled=args.demo_tax_zero
            )
        report["entities"].append(ent_report)

    assign_user_companies(Model, [c for c in companies_created if c], dry_run)
    _refresh_user_context(Model, proteus_config)

    # Post-counts
    def _count(model: str, domain=None) -> int:
        try:
            return len(Model.get(model).find(domain or []))
        except Exception:  # noqa: BLE001
            return -1

    report["counts_after"] = {
        "company.company": _count("company.company"),
        "account.account": _count("account.account"),
        "account.fiscalyear": _count("account.fiscalyear"),
        "account.period": _count("account.period"),
        "account.journal": _count("account.journal"),
        "account.tax": _count("account.tax"),
        "account.invoice": _count("account.invoice"),
        "account.move.posted": _count("account.move", [("state", "=", "posted")]),
    }
    report["sao_remainder"] = [
        "Confirm CoA template suitability with finance (Minimal Account Chart used for demo).",
        "Configure real VAT/tax rates only after counsel confirmation (left unset by default).",
        "Payment terms / invoice sequences per facility policy (SAO).",
        "Post/pay sample invoice in SAO after draft from React /financial.",
        "Period close policy — needs confirmation before wf-close-period UAT.",
        "Multi-company record rules / user company ACL beyond admin — SAO / CAB.",
    ]
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", default="isthealth")
    parser.add_argument("--user", default="admin")
    parser.add_argument(
        "--config-file",
        default=os.environ.get(
            "GNUHEALTH_TRYTOND_CONF", "/opt/gnuhealth/his-50/etc/trytond.conf"
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Plan only (default)",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Write changes to the database",
    )
    parser.add_argument(
        "--demo-tax-zero",
        action="store_true",
        help="Create clearly marked synthetic 0%% tax (still not a legal rate)",
    )
    parser.add_argument("--json-out", default="", help="Write report JSON path")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    report = run(args)
    text = json.dumps(report, indent=2, default=str)
    print(text)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            fh.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
