#!/usr/bin/env python3
"""Regenerate all framework docs, Excel, Word, and help content."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = [
    "scripts/implementation/generate_research_docs.py",
    "scripts/implementation/generate_excel_artifacts.py",
    "scripts/implementation/generate_word_and_guides.py",
    "scripts/implementation/generate_help_content.py",
]


def main() -> int:
    for rel in SCRIPTS:
        path = ROOT / rel
        print(f"=== {rel} ===")
        proc = subprocess.run([sys.executable, str(path)], cwd=str(ROOT))
        if proc.returncode != 0:
            return proc.returncode
    print("ALL GENERATORS OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
