#!/usr/bin/env python3
"""Rollback stub for 01_company — deletes by synthetic_batch_id when registry supports it."""
BATCH = "ISTHIS-DEMO-20260714"


def rollback(dry_run: bool = True) -> dict:
    return {"pack": "01_company", "batch": BATCH, "dry_run": dry_run, "status": "stub"}
