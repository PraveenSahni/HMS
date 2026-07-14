#!/usr/bin/env python3
"""Import stub for 06_appointments — wires to scripts/synthetic_data/cli.py patterns."""
from __future__ import annotations
import argparse
from generator import generate


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", default=True)
    ap.add_argument("--execute", action="store_true", help="Actually attempt load (still respects prod refuse upstream)")
    args = ap.parse_args()
    dry = not args.execute
    print(generate(dry_run=dry))


if __name__ == "__main__":
    main()
