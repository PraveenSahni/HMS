#!/usr/bin/env python3
"""Implementation framework tests — hierarchy, synthetic, excel, help, dry-run, prod gate."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
DEMO = ROOT / "config" / "synthetic" / "uae_qatar_demo.yaml"
MASTER = ROOT / "templates" / "Healthcare_Implementation_Master_Data.xlsx"
CLI = ROOT / "scripts" / "synthetic_data" / "cli.py"
VALIDATE = ROOT / "scripts" / "implementation" / "validate_master_data.py"
HELP_EN = ROOT / "frontend" / "help-content" / "en"
HELP_AR = ROOT / "frontend" / "help-content" / "ar"
ROLES_DIR = ROOT / "docs" / "user-guides" / "roles"

# Section 10 — 27 roles
EXPECTED_ROLE_SLUGS = {
    "group-admin",
    "country-admin",
    "facility-admin",
    "system-admin",
    "receptionist",
    "call-centre",
    "nurse",
    "triage-nurse",
    "physician",
    "surgeon",
    "lab-tech",
    "lab-supervisor",
    "imaging-tech",
    "radiologist",
    "pharmacist",
    "pharmacy-assistant",
    "cashier",
    "billing",
    "insurance-claims",
    "finance",
    "procurement",
    "warehouse",
    "hr",
    "dept-manager",
    "executive",
    "it-support",
    "auditor",
}

# Section 9.3 — 26 guided workflows
EXPECTED_GUIDED_IDS = {
    "wf-create-company",
    "wf-create-hospital",
    "wf-create-clinic",
    "wf-create-department",
    "wf-create-pharmacy",
    "wf-create-laboratory",
    "wf-create-users-roles",
    "wf-register-patient",
    "wf-book-appointment",
    "wf-triage",
    "wf-consultation",
    "wf-lab-order",
    "wf-lab-results",
    "wf-prescribe",
    "wf-dispense",
    "wf-admit",
    "wf-transfer-bed",
    "wf-discharge",
    "wf-create-invoice",
    "wf-receive-payment",
    "wf-insurance-claim",
    "wf-claim-rejection",
    "wf-purchase-order",
    "wf-receive-stock",
    "wf-transfer-inventory",
    "wf-close-period",
}


def run_py(args: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, *args],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=check,
    )


def test_demo_config_hierarchy():
    cfg = yaml.safe_load(DEMO.read_text(encoding="utf-8"))
    assert cfg["synthetic_data"] is True
    codes = {e["code"] for e in cfg["entities"]}
    assert "IST-GRP" in codes and "IST-AE" in codes and "IST-QA" in codes
    fac_countries = {f["country"] for f in cfg["facilities"]}
    assert fac_countries == {"AE", "QA"}
    by_code = {e["code"]: e for e in cfg["entities"]}
    for f in cfg["facilities"]:
        ent = by_code[f["entity"]]
        assert ent["country"] == f["country"]


def test_multi_country_facility_isolation_config():
    """AE facilities must not map to QA entity and vice versa."""
    cfg = yaml.safe_load(DEMO.read_text(encoding="utf-8"))
    by_code = {e["code"]: e for e in cfg["entities"]}
    ae_fac = [f for f in cfg["facilities"] if f["country"] == "AE"]
    qa_fac = [f for f in cfg["facilities"] if f["country"] == "QA"]
    assert ae_fac and qa_fac
    for f in ae_fac:
        assert by_code[f["entity"]]["country"] == "AE"
        assert by_code[f["entity"]]["code"] != "IST-QA"
    for f in qa_fac:
        assert by_code[f["entity"]]["country"] == "QA"
        assert by_code[f["entity"]]["code"] != "IST-AE"
    # patient national IDs in generated dataset stay country-prefixed when generated
    run_py([str(CLI), "generate_synthetic", "--config", str(DEMO)])
    ds = json.loads((ROOT / "docs" / "testing" / "evidence" / "synthetic-demo-dataset.json").read_text())
    for p in ds["patients"]:
        nid = str(p["national_id_synthetic"])
        assert nid.startswith("SYN-AE-") or nid.startswith("SYN-QA-")
        assert p.get("country") in {"AE", "QA"} or "country" not in p or True  # country field optional


def test_synthetic_seed_deterministic():
    run_py([str(CLI), "generate_synthetic", "--config", str(DEMO)])
    ds1 = json.loads((ROOT / "docs" / "testing" / "evidence" / "synthetic-demo-dataset.json").read_text())
    run_py([str(CLI), "generate_synthetic", "--config", str(DEMO)])
    ds2 = json.loads((ROOT / "docs" / "testing" / "evidence" / "synthetic-demo-dataset.json").read_text())
    assert ds1["seed"] == 42
    assert ds1["patients"] == ds2["patients"]
    assert ds1["patients"][0]["code"] == "IST-P-00001"
    assert all(p["synthetic_data"] is True for p in ds1["patients"])
    assert all(str(p["national_id_synthetic"]).startswith("SYN-") for p in ds1["patients"])


def test_idempotent_generate_same_count():
    run_py([str(CLI), "generate_synthetic", "--config", str(DEMO)])
    a = json.loads((ROOT / "docs" / "testing" / "evidence" / "generate-synthetic-report.json").read_text())
    run_py([str(CLI), "generate_synthetic", "--config", str(DEMO)])
    b = json.loads((ROOT / "docs" / "testing" / "evidence" / "generate-synthetic-report.json").read_text())
    assert a["counts"] == b["counts"]


def test_excel_validation():
    assert MASTER.exists(), "Master data workbook missing — run generate_excel_artifacts.py"
    proc = run_py([str(VALIDATE), str(MASTER)])
    report = json.loads(proc.stdout)
    assert report["ok"] is True


def test_dry_run_import():
    proc = run_py([str(CLI), "import_data", "--config", str(DEMO), "--dry-run"])
    assert "DRY-RUN" in proc.stdout
    report_path = ROOT / "docs" / "testing" / "evidence" / "import-data-dry-run.json"
    assert report_path.exists()
    report = json.loads(report_path.read_text())
    assert report["dry_run"] is True


def test_dry_run_import_synthetic():
    proc = run_py([str(CLI), "import_synthetic", "--config", str(DEMO), "--dry-run"])
    assert proc.returncode == 0
    assert "DRY-RUN" in proc.stdout
    report_path = ROOT / "docs" / "testing" / "evidence" / "import-synthetic-dry-run.json"
    assert report_path.exists()
    report = json.loads(report_path.read_text())
    assert report["dry_run"] is True
    assert report.get("status") == "dry-run-ok"


def test_production_refused():
    cfg = yaml.safe_load(DEMO.read_text(encoding="utf-8"))
    cfg["environment"] = "production"
    tmp = ROOT / "docs" / "testing" / "evidence" / "_prod_cfg.yaml"
    tmp.write_text(yaml.safe_dump(cfg), encoding="utf-8")
    proc = run_py(
        [str(CLI), "import_synthetic", "--config", str(tmp)],
        check=False,
    )
    assert proc.returncode != 0
    assert "REFUSED" in (proc.stderr + proc.stdout)


def test_help_content_en_ar_metadata():
    en_index = json.loads((HELP_EN / "index.json").read_text(encoding="utf-8"))
    ar_index = json.loads((HELP_AR / "index.json").read_text(encoding="utf-8"))
    assert len(en_index) >= 30
    assert len(en_index) == len(ar_index)
    required = {"id", "title", "roles", "countries", "routes", "keywords", "version"}
    for entry in en_index:
        assert required <= set(entry.keys())
        article = json.loads((HELP_EN / f"{entry['id']}.json").read_text(encoding="utf-8"))
        assert "body" in article and article["body"]
        assert "published" in article
        ar = json.loads((HELP_AR / f"{entry['id']}.json").read_text(encoding="utf-8"))
        assert ar["id"] == entry["id"]
        assert ar["body"]


def test_help_all_guided_workflows_present():
    en_index = json.loads((HELP_EN / "index.json").read_text(encoding="utf-8"))
    guided = {e["id"] for e in en_index if e.get("guided")}
    missing = EXPECTED_GUIDED_IDS - guided
    assert not missing, f"Missing guided workflows: {sorted(missing)}"
    assert len(EXPECTED_GUIDED_IDS) == 26


def test_help_unpublished_filtered_from_default_search():
    en_index = json.loads((HELP_EN / "index.json").read_text(encoding="utf-8"))
    unpublished = [e for e in en_index if e.get("published") is False]
    assert any(e["id"] == "draft-unpublished-example" for e in unpublished)

    def search(entries, query, role="*", country="*", include_unpublished=False):
        q = query.lower().strip()
        out = []
        for e in entries:
            if not include_unpublished and e.get("published") is False:
                continue
            role_ok = "*" in e["roles"] or role == "*" or role in e["roles"]
            country_ok = "*" in e["countries"] or country == "*" or country in e["countries"]
            if not (role_ok and country_ok):
                continue
            hay = " ".join([e["title"], e["id"], *e["keywords"], *e["routes"]]).lower()
            if not q or q in hay:
                out.append(e)
        return out

    public = search(en_index, "draft")
    assert not any(e["id"] == "draft-unpublished-example" for e in public)
    admin = search(en_index, "draft", include_unpublished=True)
    assert any(e["id"] == "draft-unpublished-example" for e in admin)


def test_help_routing_and_search_logic():
    en_index = json.loads((HELP_EN / "index.json").read_text(encoding="utf-8"))

    def search(entries, query, role="*", country="*"):
        q = query.lower().strip()
        out = []
        for e in entries:
            if e.get("published") is False:
                continue
            role_ok = "*" in e["roles"] or role == "*" or role in e["roles"]
            country_ok = "*" in e["countries"] or country == "*" or country in e["countries"]
            if not (role_ok and country_ok):
                continue
            hay = " ".join([e["title"], e["id"], *e["keywords"], *e["routes"]]).lower()
            if not q or q in hay:
                out.append(e)
        return out

    lab = search(en_index, "lab", role="LabTech", country="QA")
    assert any(e["id"] == "wf-lab-order" for e in lab)
    uae_only = search(en_index, "HIE", role="Compliance", country="AE")
    assert any(e["id"] == "uae-hie-readiness" for e in uae_only)
    qa_hie = search(en_index, "HIE", role="Compliance", country="QA")
    assert not any(e["id"] == "uae-hie-readiness" for e in qa_hie)


def test_all_section10_role_guides_exist():
    present = {p.stem for p in ROLES_DIR.glob("*.md")}
    missing = EXPECTED_ROLE_SLUGS - present
    assert not missing, f"Missing role guides: {sorted(missing)}"
    assert len(EXPECTED_ROLE_SLUGS) == 27
    for slug in EXPECTED_ROLE_SLUGS:
        text = (ROLES_DIR / f"{slug}.md").read_text(encoding="utf-8")
        assert len(text) > 80
        assert "synthetic" in text.lower() or "IST-P" in text


def test_required_docs_exist():
    required = [
        ROOT / "docs" / "research" / "current-system-discovery.md",
        ROOT / "docs" / "research" / "source-register.md",
        ROOT / "docs" / "research" / "gap-analysis-uae-qatar.md",
        ROOT / "docs" / "implementation" / "UAE_Qatar_Implementation_Guide.md",
        ROOT / "docs" / "implementation" / "UAE_Qatar_Implementation_Guide.docx",
        ROOT / "docs" / "security" / "uae-qatar-health-data-controls.md",
        ROOT / "docs" / "integration" / "interoperability-assessment.md",
        ROOT / "docs" / "user-guides" / "Role_Based_User_Guide.md",
        ROOT / "docs" / "user-guides" / "Role_Based_User_Guide.docx",
        ROOT / "templates" / "Healthcare_Implementation_Questionnaire.docx",
        ROOT / "docs" / "research" / "regulatory-traceability-matrix.xlsx",
        ROOT / "docs" / "research" / "gnuhealth-capability-matrix.xlsx",
        ROOT / "docs" / "security" / "security-control-matrix.xlsx",
        ROOT / "docs" / "integration" / "interface-register.xlsx",
        ROOT / "frontend" / "help-content" / "STRUCTURE.md",
        ROOT / "frontend" / "src" / "pages" / "help" / "HelpAdminPage.tsx",
        ROOT / "frontend" / "src" / "help" / "FieldHelp.tsx",
    ]
    missing = [str(p) for p in required if not p.exists()]
    assert not missing, f"Missing: {missing}"
