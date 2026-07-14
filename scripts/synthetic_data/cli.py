#!/usr/bin/env python3
"""
IST Health synthetic / master-data CLI.

Commands:
  validate
  import_data --dry-run
  generate_synthetic
  import_synthetic
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

REPORT_DIR = ROOT / "docs" / "testing" / "evidence"
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    if not isinstance(data, dict):
        raise SystemExit(f"Config must be a mapping: {path}")
    return data


def is_production(cfg: dict[str, Any]) -> bool:
    env = str(cfg.get("environment", "dev")).lower()
    if env in {"dev", "test", "uat", "demo"}:
        return False
    if env == "production":
        return True
    server = cfg.get("server") or {}
    url = str(server.get("url", "")).lower()
    hosts = server.get("production_hosts") or []
    for h in hosts:
        if h and h.lower() in url:
            return True
    return False


def refuse_production(cfg: dict[str, Any], allow: bool, *, dry_run: bool = False) -> None:
    if dry_run:
        return
    if is_production(cfg) and not allow:
        raise SystemExit(
            "REFUSED: production target detected. "
            "Re-run with --allow-production after CAB approval."
        )


def cmd_validate(cfg: dict[str, Any], config_path: Path) -> dict[str, Any]:
    errors: list[str] = []
    if not cfg.get("synthetic_data", False):
        errors.append("synthetic_data must be true")
    if "seed" not in cfg and "seed" not in (cfg.get("data") or {}):
        # allow seed at top or nested via company configs
        if cfg.get("seed") is None:
            errors.append("seed is required for determinism")
    data = cfg.get("data") or {}
    patients = int(data.get("patients", 0))
    if patients <= 0:
        errors.append("data.patients must be > 0")
    if patients > 5000 and cfg.get("environment") == "test":
        errors.append("test environment patient volume suspiciously high (>5000)")
    idf = cfg.get("id_formats") or {}
    for key in ("national_id_qa", "national_id_ae"):
        val = str(idf.get(key, ""))
        if val and not val.startswith("SYN-"):
            errors.append(f"{key} must use SYN- prefix")
    report = {
        "command": "validate",
        "config": str(config_path),
        "ok": not errors,
        "errors": errors,
        "patients": patients,
        "seed": cfg.get("seed"),
        "synthetic_data": cfg.get("synthetic_data"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    out = REPORT_DIR / "validate-report.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    if errors:
        print("VALIDATE FAIL")
        for e in errors:
            print(f" - {e}")
        raise SystemExit(1)
    print("VALIDATE OK")
    print(json.dumps(report, indent=2))
    return report


def cmd_generate(cfg: dict[str, Any], config_path: Path) -> dict[str, Any]:
    seed = int(cfg.get("seed", 42))
    data = cfg.get("data") or {}
    n_patients = int(data.get("patients", 50))
    n_staff = int(data.get("staff", 10))
    code = (cfg.get("company") or {}).get("code", "IST")
    patients = [
        {
            "code": f"{code}-P-{i:05d}",
            "national_id_synthetic": f"SYN-QA-{i:08d}" if i % 2 else f"SYN-AE-{i:08d}",
            "synthetic_data": True,
            "country": "QA" if i % 2 else "AE",
        }
        for i in range(1, n_patients + 1)
    ]
    staff = [
        {"code": f"{code}-ST-{i:04d}", "synthetic_data": True}
        for i in range(1, n_staff + 1)
    ]
    payload = {
        "command": "generate_synthetic",
        "config": str(config_path),
        "seed": seed,
        "counts": {"patients": len(patients), "staff": len(staff)},
        "sample_patients": patients[:5],
        "sample_staff": staff[:5],
        "entities": cfg.get("entities"),
        "facilities": cfg.get("facilities"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    out = REPORT_DIR / "generate-synthetic-report.json"
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    # also write a small dataset file for tests
    dataset = REPORT_DIR / "synthetic-demo-dataset.json"
    dataset.write_text(
        json.dumps({"patients": patients, "staff": staff, "seed": seed}, indent=2),
        encoding="utf-8",
    )
    print(f"GENERATE OK patients={len(patients)} staff={len(staff)} seed={seed}")
    print(f"Report: {out}")
    return payload


def cmd_import_data(cfg: dict[str, Any], config_path: Path, dry_run: bool, allow_prod: bool) -> dict[str, Any]:
    refuse_production(cfg, allow_prod, dry_run=dry_run)
    plan = {
        "entities": len(cfg.get("entities") or []),
        "facilities": len(cfg.get("facilities") or []),
        "patients": int((cfg.get("data") or {}).get("patients", 0)),
        "staff": int((cfg.get("data") or {}).get("staff", 0)),
    }
    report = {
        "command": "import_data",
        "dry_run": dry_run,
        "config": str(config_path),
        "plan": plan,
        "writes": 0 if dry_run else "delegated",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    if dry_run:
        print("DRY-RUN import_data — no writes")
        print(json.dumps(report, indent=2))
        (REPORT_DIR / "import-data-dry-run.json").write_text(
            json.dumps(report, indent=2), encoding="utf-8"
        )
        return report

    # Non-dry-run master-data import is a stub that records intent; live GH write uses import_synthetic
    (REPORT_DIR / "import-data-report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    print("import_data recorded (master-data apply uses Excel + GH tools).")
    return report


def cmd_import_synthetic(
    cfg: dict[str, Any],
    config_path: Path,
    dry_run: bool,
    allow_prod: bool,
    force: bool,
) -> dict[str, Any]:
    refuse_production(cfg, allow_prod, dry_run=dry_run)
    report: dict[str, Any] = {
        "command": "import_synthetic",
        "dry_run": dry_run,
        "config": str(config_path),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    if dry_run:
        report["status"] = "dry-run-ok"
        print("DRY-RUN import_synthetic — would call run_synthetic_data engine")
        (REPORT_DIR / "import-synthetic-dry-run.json").write_text(
            json.dumps(report, indent=2), encoding="utf-8"
        )
        return report

    # Bridge to existing engine when server password is real
    server = cfg.get("server") or {}
    if str(server.get("password", "")).upper() in {"", "CHANGE_ME"}:
        report["status"] = "skipped-no-credentials"
        report["reason"] = "server.password not configured; generated local dataset only"
        cmd_generate(cfg, config_path)
        (REPORT_DIR / "import-synthetic-report.json").write_text(
            json.dumps(report, indent=2), encoding="utf-8"
        )
        print("SKIP live import (no credentials); local generate completed.")
        return report

    # Map demo yaml into temporary config for run_synthetic_data
    from run_synthetic_data import load_config, run  # type: ignore

    # Build merged config compatible with existing engine
    merged = {
        "company": cfg.get("company"),
        "server": server,
        "data": cfg.get("data"),
        "options": {
            "idempotent": cfg.get("idempotent", True) and not force,
            **(cfg.get("options") or {}),
        },
    }
    tmp = REPORT_DIR / "_runtime_synthetic_config.yaml"
    tmp.write_text(yaml.safe_dump(merged, sort_keys=False), encoding="utf-8")
    # Use argparse-like namespace
    class NS:
        pass

    args = NS()
    args.config = str(tmp)
    args.force = force
    args.dry_run = False
    args.only = ""
    args.verbose = False
    # run() expects parsed args — call underlying carefully
    import run_synthetic_data as engine

    engine.setup_logging(False)
    config = load_config(tmp)
    # Manual step execution via engine.main pattern — invoke CLI subprocess-like
    sys.argv = ["run_synthetic_data.py", "--config", str(tmp)]
    if force:
        sys.argv.append("--force")
    rc = engine.main() if hasattr(engine, "main") else None
    report["status"] = "delegated-to-run_synthetic_data"
    report["engine_rc"] = rc
    (REPORT_DIR / "import-synthetic-report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    print(json.dumps(report, indent=2))
    return report


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="IST synthetic / import CLI")
    p.add_argument(
        "command",
        choices=["validate", "import_data", "generate_synthetic", "import_synthetic"],
    )
    p.add_argument(
        "--config",
        default=str(ROOT / "config" / "synthetic" / "uae_qatar_demo.yaml"),
    )
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--allow-production", action="store_true")
    p.add_argument("--force", action="store_true", help="Disable idempotency")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = (Path.cwd() / config_path).resolve()
    cfg = load_yaml(config_path)

    if args.command == "validate":
        cmd_validate(cfg, config_path)
    elif args.command == "generate_synthetic":
        cmd_validate(cfg, config_path)
        cmd_generate(cfg, config_path)
    elif args.command == "import_data":
        cmd_validate(cfg, config_path)
        cmd_import_data(
            cfg,
            config_path,
            dry_run=bool(args.dry_run),
            allow_prod=args.allow_production,
        )
    elif args.command == "import_synthetic":
        cmd_validate(cfg, config_path)
        cmd_import_synthetic(
            cfg,
            config_path,
            dry_run=args.dry_run,
            allow_prod=args.allow_production,
            force=args.force,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
