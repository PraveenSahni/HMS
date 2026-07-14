#!/usr/bin/env python3
"""docs_sync CLI — discover, download, verify, compare, traceability, drift."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / "docs" / "upstream"
IST = ROOT / "docs" / "ist-his"
MANIFEST = UPSTREAM / "source-manifest.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def cmd_discover(args: argparse.Namespace) -> int:
    baseline = UPSTREAM / "UPSTREAM_BASELINE.yaml"
    print(json.dumps({
        "baseline_exists": baseline.exists(),
        "manifest_exists": MANIFEST.exists(),
        "ist_docs": IST.exists(),
        "original": str(UPSTREAM / "original"),
    }, indent=2))
    return 0


def cmd_download(args: argparse.Namespace) -> int:
    print(
        "Download is performed by scripts/upstream_sync/build_all.py.\n"
        "Refusing to auto-overwrite docs/upstream/original/. "
        f"Requested version={args.version}"
    )
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    errors = []
    for entry in data.get("files", []):
        path = ROOT / entry["path"]
        if not path.exists():
            errors.append(f"MISSING {entry['path']}")
            continue
        digest = sha256(path)
        if digest != entry["sha256"]:
            errors.append(f"HASH_MISMATCH {entry['path']}")
    if errors:
        print("FAIL")
        for e in errors:
            print(e)
        return 1
    print(f"OK {len(data.get('files', []))} files")
    return 0


def cmd_compare(args: argparse.Namespace) -> int:
    upstream = Path(args.upstream)
    ist = Path(args.ist_docs)
    print(json.dumps({
        "upstream_files": sum(1 for p in upstream.rglob('*') if p.is_file()) if upstream.exists() else 0,
        "ist_files": sum(1 for p in ist.rglob('*') if p.is_file()) if ist.exists() else 0,
        "note": "Never auto-overwrite approved IST docs",
    }, indent=2))
    return 0


def cmd_traceability(args: argparse.Namespace) -> int:
    xlsx = IST / "IST_HIS_Documentation_Traceability.xlsx"
    print(json.dumps({"traceability": str(xlsx), "exists": xlsx.exists()}, indent=2))
    return 0


def cmd_drift(args: argparse.Namespace) -> int:
    report = UPSTREAM / "upstream-drift-report.md"
    print(report.read_text(encoding="utf-8") if report.exists() else "No drift report yet")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="docs_sync")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("discover_upstream", aliases=["discover"])
    p.set_defaults(func=cmd_discover)

    p = sub.add_parser("download")
    p.add_argument("--version", required=True)
    p.set_defaults(func=cmd_download)

    p = sub.add_parser("verify_checksums", aliases=["verify"])
    p.set_defaults(func=cmd_verify)

    p = sub.add_parser("compare")
    p.add_argument("--upstream", default=str(UPSTREAM / "original"))
    p.add_argument("--ist-docs", default=str(IST))
    p.set_defaults(func=cmd_compare)

    p = sub.add_parser("generate_traceability", aliases=["traceability"])
    p.set_defaults(func=cmd_traceability)

    p = sub.add_parser("report_drift", aliases=["drift"])
    p.set_defaults(func=cmd_drift)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
