#!/usr/bin/env python3
"""Ensure docs/upstream/original files match source-manifest.json SHA-256 digests."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "docs" / "upstream" / "source-manifest.json"
ORIGINAL = ROOT / "docs" / "upstream" / "original"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def test_manifest_exists():
    assert MANIFEST.exists()


def test_original_immutable_checksums():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data.get("file_count", 0) > 0
    for entry in data["files"]:
        path = ROOT / entry["path"]
        assert path.exists(), entry["path"]
        assert sha256(path) == entry["sha256"], entry["path"]


def test_no_empty_original():
    files = [p for p in ORIGINAL.rglob("*") if p.is_file()]
    assert files, "original/ should contain acquired upstream files"


def test_baseline_yaml_exists():
    assert (ROOT / "docs" / "upstream" / "UPSTREAM_BASELINE.yaml").exists()


def test_module_registry_exists():
    assert (ROOT / "docs" / "upstream" / "module-registry.json").exists()


def test_docs_sync_verify():
    from docs_sync.cli import cmd_verify
    class A:
        pass
    assert cmd_verify(A()) == 0
