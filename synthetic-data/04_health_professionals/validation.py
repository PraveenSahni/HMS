#!/usr/bin/env python3
"""Validation rules for pack 04_health_professionals."""
from __future__ import annotations

FORBIDDEN_PREFIXES = ()  # real national IDs never generated
REQUIRED_MARKERS = ("synthetic_data", "synthetic_batch_id", "synthetic_seed")


def validate_record(rec: dict) -> list[str]:
    errors = []
    for k in REQUIRED_MARKERS:
        if k not in rec:
            errors.append(f"missing {k}")
    for key in ("emirates_id", "qatar_id", "national_id"):
        val = str(rec.get(key, ""))
        if val and not (val.startswith("SYN-AE-") or val.startswith("SYN-QA-") or val.startswith("IST-")):
            errors.append(f"non-synthetic identifier in {key}: {val}")
    return errors
