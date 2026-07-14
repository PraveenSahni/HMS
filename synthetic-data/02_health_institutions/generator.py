#!/usr/bin/env python3
"""Synthetic generator stub for pack 02_health_institutions.

Integrates with existing synthetic_data package; does not bypass prod refuse / dry-run.
"""
from __future__ import annotations

SYNTHETIC_DATA = True
SYNTHETIC_BATCH_ID = "ISTHIS-DEMO-20260714"
SYNTHETIC_SEED = 20260714
PACK = "02_health_institutions"
MODULES = ['health']
MODELS = ['gnuhealth.institution']


def generate(dry_run: bool = True) -> dict:
    """Return planned records; refuse production unless caller overrides safely."""
    return {
        "pack": PACK,
        "dry_run": dry_run,
        "synthetic_data": SYNTHETIC_DATA,
        "synthetic_batch_id": SYNTHETIC_BATCH_ID,
        "synthetic_seed": SYNTHETIC_SEED,
        "modules": MODULES,
        "models": MODELS,
        "records": [],
        "status": "stub-ready",
    }


if __name__ == "__main__":
    import json
    print(json.dumps(generate(dry_run=True), indent=2))
