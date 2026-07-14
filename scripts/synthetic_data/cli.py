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
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Load sibling module without requiring scripts/ to be a package
import importlib.util

_gen_path = Path(__file__).resolve().parent / "max_demo_generator.py"
_spec = importlib.util.spec_from_file_location("max_demo_generator", _gen_path)
assert _spec and _spec.loader
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
build_max_demo_dataset = _mod.build_max_demo_dataset
write_dataset = _mod.write_dataset

REPORT_DIR = ROOT / "docs" / "testing" / "evidence"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

CHANGE_ME = frozenset({"", "CHANGE_ME", "CHANGEME", "TODO", "XXX"})


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
    # Also refuse when options flag set and URL matches production_hosts
    opts = cfg.get("options") or {}
    if opts.get("refuse_production_without_override") and not allow:
        server = cfg.get("server") or {}
        url = str(server.get("url", "")).lower()
        for h in server.get("production_hosts") or []:
            if h and h.lower() in url and not dry_run:
                # environment may be test/demo but host is listed prod — require override
                raise SystemExit(
                    "REFUSED: server URL matches production_hosts. "
                    "Use --dry-run, or --allow-production after explicit demo/CAB approval."
                )


def password_configured(cfg: dict[str, Any]) -> bool:
    pwd = str((cfg.get("server") or {}).get("password", "")).strip()
    return pwd.upper() not in {p.upper() for p in CHANGE_ME} and bool(pwd)


def cmd_validate(cfg: dict[str, Any], config_path: Path) -> dict[str, Any]:
    errors: list[str] = []
    if not cfg.get("synthetic_data", False):
        errors.append("synthetic_data must be true")
    seed = cfg.get("seed")
    if seed is None and "seed" not in (cfg.get("data") or {}):
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
    facilities = cfg.get("facilities") or []
    entities = cfg.get("entities") or []
    if not entities:
        errors.append("entities org tree required")
    if not facilities:
        errors.append("facilities list required")
    report = {
        "command": "validate",
        "config": str(config_path),
        "ok": not errors,
        "errors": errors,
        "patients": patients,
        "staff": int(data.get("staff", 0)),
        "entities": len(entities),
        "facilities": len(facilities),
        "seed": seed if seed is not None else (data.get("seed")),
        "synthetic_data": cfg.get("synthetic_data"),
        "synthetic_batch_id": cfg.get("synthetic_batch_id"),
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


def _is_max_profile(cfg: dict[str, Any], config_path: Path) -> bool:
    name = config_path.name.lower()
    if "max_demo" in name or "max-demo" in name:
        return True
    return bool(cfg.get("packs")) and int((cfg.get("data") or {}).get("patients", 0)) >= 500


def cmd_generate(cfg: dict[str, Any], config_path: Path) -> dict[str, Any]:
    seed = int(cfg.get("seed") or (cfg.get("data") or {}).get("seed") or 42)
    data = cfg.get("data") or {}
    n_patients = int(data.get("patients", 50))
    n_staff = int(data.get("staff", 10))

    if _is_max_profile(cfg, config_path):
        dataset = build_max_demo_dataset(cfg)
        paths = write_dataset(dataset, REPORT_DIR, write_full=True)
        # Also mirror under synthetic-data/generated for pack consumers
        mirror = ROOT / "synthetic-data" / "generated"
        write_dataset(dataset, mirror, write_full=True)
        payload = {
            "command": "generate_synthetic",
            "profile": "max_demo",
            "config": str(config_path),
            "seed": seed,
            "synthetic_batch_id": cfg.get("synthetic_batch_id"),
            "counts": dataset["counts"],
            "paths": {k: str(v) for k, v in paths.items()},
            "packs": dataset["meta"].get("packs"),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        (REPORT_DIR / "generate-synthetic-report.json").write_text(
            json.dumps(payload, indent=2), encoding="utf-8"
        )
        print(
            f"GENERATE OK (max demo) patients={dataset['counts']['patients']} "
            f"staff={dataset['counts']['health_professionals']} "
            f"appointments={dataset['counts']['appointments']} seed={seed}"
        )
        print(f"Summary: {paths['summary']}")
        print(f"Full dataset: {paths.get('full')}")
        return payload

    # Small demo path (uae_qatar_demo.yaml)
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
    dataset = REPORT_DIR / "synthetic-demo-dataset.json"
    dataset.write_text(
        json.dumps({"patients": patients, "staff": staff, "seed": seed}, indent=2),
        encoding="utf-8",
    )
    print(f"GENERATE OK patients={len(patients)} staff={len(staff)} seed={seed}")
    print(f"Report: {out}")
    return payload


def cmd_import_data(
    cfg: dict[str, Any], config_path: Path, dry_run: bool, allow_prod: bool
) -> dict[str, Any]:
    refuse_production(cfg, allow_prod, dry_run=dry_run)
    plan = {
        "entities": len(cfg.get("entities") or []),
        "facilities": len(cfg.get("facilities") or []),
        "patients": int((cfg.get("data") or {}).get("patients", 0)),
        "staff": int((cfg.get("data") or {}).get("staff", 0)),
        "packs": list((cfg.get("packs") or {}).keys()),
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

    (REPORT_DIR / "import-data-report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    print("import_data recorded (master-data apply uses Excel + GH tools).")
    return report


def _merge_engine_config(cfg: dict[str, Any]) -> dict[str, Any]:
    """Map demo/max yaml into run_synthetic_data.py shape."""
    data = dict(cfg.get("data") or {})
    if "seed" not in data:
        data["seed"] = cfg.get("seed", 42)
    options = {
        "idempotent": cfg.get("idempotent", True),
        **(cfg.get("options") or {}),
    }
    # Engine uses inpatient_beds (total), not per-hospital
    if "inpatient_beds" not in options and "inpatient_beds_per_hospital" in options:
        hospitals = [
            f
            for f in (cfg.get("facilities") or [])
            if f.get("type") == "hospital"
        ]
        n_h = max(len(hospitals), 1)
        options["inpatient_beds"] = int(options["inpatient_beds_per_hospital"]) * n_h
    return {
        "company": cfg.get("company"),
        "server": cfg.get("server"),
        "data": data,
        "options": options,
    }


def cmd_import_synthetic(
    cfg: dict[str, Any],
    config_path: Path,
    dry_run: bool,
    allow_prod: bool,
    force: bool,
) -> dict[str, Any]:
    report: dict[str, Any] = {
        "command": "import_synthetic",
        "dry_run": dry_run,
        "config": str(config_path),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "seed": cfg.get("seed"),
        "synthetic_batch_id": cfg.get("synthetic_batch_id"),
    }

    if dry_run:
        # Dry-run never writes; skip prod refuse
        report["status"] = "dry-run-ok"
        report["would_call"] = "run_synthetic_data.py"
        report["engine_steps"] = [
            "company",
            "staff",
            "patients",
            "appointments",
            "laboratory",
            "pharmacy",
            "inpatient",
            "evaluations",
        ]
        report["local_only_packs"] = [
            k
            for k, v in (cfg.get("packs") or {}).items()
            if (v or {}).get("mode") in {"local_connected", "stub_marker"}
        ]
        report["plan_counts"] = {
            "patients": int((cfg.get("data") or {}).get("patients", 0)),
            "staff": int((cfg.get("data") or {}).get("staff", 0)),
            "entities": len(cfg.get("entities") or []),
            "facilities": len(cfg.get("facilities") or []),
        }
        report["password_configured"] = password_configured(cfg)
        report["production_host_match"] = is_production(cfg) or any(
            h and h.lower() in str((cfg.get("server") or {}).get("url", "")).lower()
            for h in ((cfg.get("server") or {}).get("production_hosts") or [])
        )
        print("DRY-RUN import_synthetic — would call run_synthetic_data engine")
        print(json.dumps(report, indent=2))
        (REPORT_DIR / "import-synthetic-dry-run.json").write_text(
            json.dumps(report, indent=2), encoding="utf-8"
        )
        return report

    if not password_configured(cfg):
        report["status"] = "skipped-no-credentials"
        report["reason"] = (
            "server.password is CHANGE_ME / empty; generated local dataset only"
        )
        cmd_generate(cfg, config_path)
        (REPORT_DIR / "import-synthetic-report.json").write_text(
            json.dumps(report, indent=2), encoding="utf-8"
        )
        print("SKIP live import (no credentials); local generate completed.")
        print(
            "Next: set server.password in a local override (never commit), then:\n"
            f"  python scripts/synthetic_data/cli.py import_synthetic "
            f"--config {config_path} --allow-production\n"
            "Or: python run_synthetic_data.py --config <merged.yaml> --dry-run"
        )
        return report

    # Live write path — enforce prod gates
    refuse_production(cfg, allow_prod, dry_run=False)

    merged = _merge_engine_config(cfg)
    if force:
        merged.setdefault("options", {})["idempotent"] = False
    tmp = REPORT_DIR / "_runtime_synthetic_config.yaml"
    tmp.write_text(yaml.safe_dump(merged, sort_keys=False), encoding="utf-8")

    cmd = [sys.executable, str(ROOT / "run_synthetic_data.py"), "--config", str(tmp)]
    if force:
        cmd.append("--force")
    print(f"Delegating to engine: {' '.join(cmd)}")
    proc = subprocess.run(cmd, cwd=str(ROOT), check=False)
    report["status"] = "delegated-to-run_synthetic_data"
    report["engine_rc"] = proc.returncode
    report["runtime_config"] = str(tmp)
    (REPORT_DIR / "import-synthetic-report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    print(json.dumps(report, indent=2))
    if proc.returncode != 0:
        raise SystemExit(proc.returncode)
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
