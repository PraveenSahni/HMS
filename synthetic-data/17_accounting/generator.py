#!/usr/bin/env python3
"""Synthetic generator for pack 17_accounting — accounting master + draft invoice markers.

Does not invent tax rates. CoA/FY/journals are applied on the HIS VM via
``scripts/accounting/upload_ist_health_accounting.py`` (Proteus), not this stub alone.
"""
from __future__ import annotations

from datetime import date

SYNTHETIC_DATA = True
SYNTHETIC_BATCH_ID = "ISTHIS-ACCT-20260715"
SYNTHETIC_SEED = 20260715
PACK = "17_accounting"
MODULES = ["account", "account_invoice", "health_services"]
MODELS = [
    "company.company",
    "currency.currency",
    "account.account",
    "account.fiscalyear",
    "account.period",
    "account.journal",
    "account.invoice",
]

ENTITIES = [
    {
        "model": "company.company",
        "party_code": "IST-HC-QA",
        "party_name": "IST Healthcare Qatar",
        "currency": "QAR",
        "brands": ["IST Health", "IST Technologies", "Iris Star"],
    },
    {
        "model": "company.company",
        "party_code": "IST-HC-AE",
        "party_name": "IST Healthcare UAE",
        "currency": "AED",
        "brands": ["IST Health", "IST Technologies", "Iris Star"],
    },
]


def generate(dry_run: bool = True) -> dict:
    """Return planned accounting master records + upload hook metadata."""
    year = date.today().year
    records = []
    for ent in ENTITIES:
        records.append(
            {
                **ent,
                "synthetic_data": True,
                "synthetic_batch_id": SYNTHETIC_BATCH_ID,
                "coa_template": "account.account_template_root_en (Minimal Account Chart)",
                "fiscal_year": year,
                "periods": "monthly",
                "taxes": "unset — needs confirmation (no invented VAT rates)",
            }
        )
    records.append(
        {
            "model": "account.journal",
            "codes": ["CASH", "EXP", "REV", "MISC", "EXC", "STO"],
            "note": "Shared Tryton journals; verify presence for invoice posting",
        }
    )
    return {
        "pack": PACK,
        "dry_run": dry_run,
        "synthetic_data": SYNTHETIC_DATA,
        "synthetic_batch_id": SYNTHETIC_BATCH_ID,
        "synthetic_seed": SYNTHETIC_SEED,
        "modules": MODULES,
        "models": MODELS,
        "records": records,
        "status": "master-data-ready",
        "live_upload": {
            "script": "scripts/accounting/upload_ist_health_accounting.py",
            "assess": "scripts/accounting/assess_accounting.py",
            "deploy": "scripts/accounting/deploy-and-run-accounting.sh",
            "path": "On-VM Proteus/trytond (same as max-demo)",
            "database": "isthealth",
        },
        "docs": [
            "docs/implementation/ist-health-accounting-upload.md",
            "docs/implementation/financial-setup.md",
        ],
    }


if __name__ == "__main__":
    import json

    print(json.dumps(generate(dry_run=True), indent=2))
