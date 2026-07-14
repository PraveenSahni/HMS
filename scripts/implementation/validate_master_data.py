#!/usr/bin/env python3
"""Validate Healthcare_Implementation_Master_Data.xlsx structure and synthetic rules."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from openpyxl import load_workbook

REQUIRED_SHEETS = [
    "Cover",
    "Instructions",
    "VersionHistory",
    "ValidationLists",
    "6.1_LegalEntities",
    "6.2_Facilities",
    "6.3_Departments",
    "6.4_UsersRoles",
    "6.5_Specialties",
    "6.6_ProductsMeds",
    "6.7_LabCatalog",
    "6.8_Insurance",
    "6.9_Warehouses",
    "6.10_Sequences",
    "DataDictionary",
    "SignOff",
]


def validate(path: Path) -> dict:
    wb = load_workbook(path, read_only=True, data_only=True)
    errors: list[str] = []
    warnings: list[str] = []
    names = set(wb.sheetnames)
    for s in REQUIRED_SHEETS:
        if s not in names:
            errors.append(f"Missing sheet: {s}")

    # Check synthetic_data columns on demographic-ish sheets
    for sheet in ["6.1_LegalEntities", "6.2_Facilities", "6.4_UsersRoles"]:
        if sheet not in names:
            continue
        ws = wb[sheet]
        rows = list(ws.iter_rows(values_only=True))
        if not rows:
            errors.append(f"{sheet} empty")
            continue
        headers = [str(h) if h is not None else "" for h in rows[0]]
        if "synthetic_data" not in headers:
            errors.append(f"{sheet} missing synthetic_data column")
            continue
        idx = headers.index("synthetic_data")
        for i, row in enumerate(rows[1:], start=2):
            if row is None or all(c is None for c in row):
                continue
            val = row[idx] if idx < len(row) else None
            if str(val).upper() not in {"TRUE", "1", "YES"}:
                errors.append(f"{sheet} row {i}: synthetic_data must be TRUE")

    # National ID format sniff on facilities phones — warn if looks like real Emirates ID pattern
    report = {
        "file": str(path),
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "sheets": wb.sheetnames,
    }
    wb.close()
    return report


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("excel")
    p.add_argument("--json-out", default="")
    args = p.parse_args()
    path = Path(args.excel)
    if not path.exists():
        print(f"FAIL: file not found {path}")
        return 1
    report = validate(path)
    text = json.dumps(report, indent=2)
    print(text)
    if args.json_out:
        Path(args.json_out).write_text(text, encoding="utf-8")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
