#!/usr/bin/env python3
"""Import entry for 17_accounting.

Default is dry-run plan JSON. Live CoA/FY/company write uses the on-VM Proteus
uploader (not HTTP JSON-RPC from laptop).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from generator import generate

REPO_ROOT = Path(__file__).resolve().parents[2]
UPLOADER = REPO_ROOT / "scripts" / "accounting" / "upload_ist_health_accounting.py"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", default=True)
    ap.add_argument(
        "--execute",
        action="store_true",
        help="Print live-upload instructions / invoke local uploader if on HIS VM",
    )
    ap.add_argument(
        "--run-uploader",
        action="store_true",
        help="If on HIS VM with trytond.conf, run upload_ist_health_accounting.py",
    )
    args = ap.parse_args()
    dry = not args.execute
    plan = generate(dry_run=dry)
    print(json.dumps(plan, indent=2))

    if args.run_uploader:
        if not UPLOADER.is_file():
            print(f"Uploader missing: {UPLOADER}", file=sys.stderr)
            sys.exit(2)
        cmd = [sys.executable, str(UPLOADER)]
        cmd.append("--execute" if args.execute else "--dry-run")
        raise SystemExit(subprocess.call(cmd))


if __name__ == "__main__":
    main()
