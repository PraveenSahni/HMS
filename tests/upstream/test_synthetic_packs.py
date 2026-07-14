#!/usr/bin/env python3
from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SYN = ROOT / "synthetic-data"


def test_packs_00_20_exist():
    for i in range(0, 21):
        name = f"{i:02d}_" 
        matches = [p for p in SYN.iterdir() if p.is_dir() and p.name.startswith(f"{i:02d}_")]
        assert matches, f"missing pack {i:02d}_*"


def test_model_registry():
    reg = SYN / "schema" / "ist_his_model_registry.json"
    assert reg.exists()
