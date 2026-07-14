#!/usr/bin/env python3
"""Rollback stub for 02_health_institutions — deletes by synthetic_batch_id when registry supports it."""
BATCH = "ISTHIS-DEMO-20260714"


def rollback(dry_run: bool = True) -> dict:
    return {"pack": "02_health_institutions", "batch": BATCH, "dry_run": dry_run, "status": "stub"}
