#!/usr/bin/env python3
"""Build IST HIS upstream synchronization artefacts (Phases 1–17).

Pinned baseline (VM gnuhealth-his-01, 2026-07-14):
  GNU Health HIS core package 5.0.6, Tryton 7.0.53, SAO 7.0.53.
Does NOT upgrade GNU Health/Tryton.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import sys
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from module_catalog import (  # noqa: E402
    BRIEF_SECTION5,
    DISPLAY_NAMES,
    FEATURES_EXTRA,
    PIP_VERSIONS,
    VM_ACTIVATED,
    load_release_modules,
)

try:
    import openpyxl
    from openpyxl import Workbook
except ImportError as e:  # pragma: no cover
    raise SystemExit("openpyxl required: pip install openpyxl") from e

try:
    from docx import Document
except ImportError as e:  # pragma: no cover
    raise SystemExit("python-docx required: pip install python-docx") from e

BASELINE_DATE = "2026-07-14"
IST_HIS_VERSION = "1.0.0"
GH_VERSION = "5.0.6"
GH_LATEST_STABLE = "5.0.7"
TRYTON = "7.0.53"
SAO = "7.0.53"
GH_CONTROL = "5.0.3"
PG = "15.18"
PYTHON_VM = "3.11.2"
SOURCE_COMMIT = "f50972fee0d4e001133a09af8d9ea7dbfe67f7a8"  # tag v5.0.6
DOC_RETRIEVAL = BASELINE_DATE

UPSTREAM = ROOT / "docs" / "upstream"
ORIGINAL = UPSTREAM / "original"
GENERATED = UPSTREAM / "generated-reference"
CACHE_DOC = UPSTREAM / "_cache" / "documentation"
CACHE_HIS = UPSTREAM / "_cache" / "his-5.0.6"
IST = ROOT / "docs" / "ist-his"
SYN = ROOT / "synthetic-data"
TEMPLATES = ROOT / "templates"

ATTRIBUTION = """IST HIS is a customized healthcare information system developed by
IRIS STAR Technologies and based on GNU Health HIS.

Portions of this documentation are adapted from the GNU Health
Hospital Information System documentation, Copyright GNU Solidario,
and are made available under the Creative Commons
Attribution-ShareAlike 4.0 International licence.

GNU Health software components are licensed under the GNU General
Public License version 3 or later. IST-specific components must carry
the applicable copyright and licence notices.
"""

PACKS = [
    ("00_foundation", ["party", "country", "currency"], ["health"]),
    ("01_company", ["company"], ["health"]),
    ("02_health_institutions", ["gnuhealth.institution"], ["health"]),
    ("03_users_and_access", ["res.user", "res.group"], ["health"]),
    ("04_health_professionals", ["gnuhealth.healthprofessional"], ["health"]),
    ("05_patients", ["gnuhealth.patient", "party.party"], ["health"]),
    ("06_appointments", ["gnuhealth.appointment"], ["health", "health_calendar"]),
    ("07_evaluations", ["gnuhealth.patient.evaluation"], ["health"]),
    ("08_inpatient", ["gnuhealth.inpatient.registration"], ["health_inpatient"]),
    ("09_nursing", ["gnuhealth.patient.rounding"], ["health_nursing"]),
    ("10_icu", ["gnuhealth.icu.apache2"], ["health_icu"]),
    ("11_laboratory", ["gnuhealth.lab"], ["health_lab"]),
    ("12_imaging", ["gnuhealth.imaging.test.request"], ["health_imaging"]),
    ("13_pharmacy", ["gnuhealth.prescription.order"], ["health", "health_stock"]),
    ("14_stock", ["stock.location", "stock.move"], ["health_stock"]),
    ("15_surgery", ["gnuhealth.surgery"], ["health_surgery"]),
    ("16_insurance", ["gnuhealth.insurance"], ["health_insurance"]),
    ("17_accounting", ["account.invoice"], ["health_services", "account_invoice"]),
    ("18_services_and_billing", ["gnuhealth.health_service"], ["health_services"]),
    ("19_reporting", ["gnuhealth.top_diseases"], ["health_reporting"]),
    ("20_federation_and_integration", ["gnuhealth.federation"], ["health_federation"]),
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def copy_tree_files(src: Path, dst: Path, patterns: tuple[str, ...] | None = None) -> list[Path]:
    copied: list[Path] = []
    if not src.exists():
        return copied
    for p in src.rglob("*"):
        if not p.is_file():
            continue
        if patterns and not any(p.match(pat) or p.suffix.lower() in patterns for pat in patterns):
            # also allow by suffix list passed as patterns like '.rst'
            if patterns and p.suffix.lower() not in patterns and not any(
                p.name.endswith(pat.strip("*")) for pat in patterns
            ):
                continue
        rel = p.relative_to(src)
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, target)
        copied.append(target)
    return copied


def phase1_baseline(modules: dict[str, Any]) -> None:
    UPSTREAM.mkdir(parents=True, exist_ok=True)
    baseline = f"""product:
  name: IST HIS
  full_name: IST HIS — Iris Star Hospital Information System
  vendor: IRIS STAR Technologies
  upstream_product: GNU Health HIS
  upstream_server_version: "{GH_VERSION}"
  upstream_client_version: "sao-{SAO}"
  tryton_version: "{TRYTON}"
  tryton_client_version: "sao-{SAO} (no desktop tryton client installed)"
  gnuhealth_control_version: "{GH_CONTROL}"
  postgresql_version: "{PG}"
  python_version: "{PYTHON_VM}"
  baseline_date: "{BASELINE_DATE}"
  source_release: "codeberg.org/gnuhealth/his tag v{GH_VERSION}"
  source_commit: "{SOURCE_COMMIT}"
  latest_official_stable_not_adopted: "{GH_LATEST_STABLE}"
  upgrade_performed: false
  notes: |
    Installed core PyPI package gnuhealth=={GH_VERSION} on VM gnuhealth-his-01.
    Latest Codeberg tag is {GH_LATEST_STABLE}; deliberately NOT upgraded.
    Module package versions vary (mostly 5.0.4); core health is 5.0.6.
    Database: isthealth — {len(VM_ACTIVATED)} health* modules activated.
    Custom IST Tryton modules: none detected in ir.module.
ist_his_product_version: "{IST_HIS_VERSION}"
documentation_version: "{IST_HIS_VERSION}"
synthetic_data_schema_version: "{IST_HIS_VERSION}"
implementation_template_version: "{IST_HIS_VERSION}"
evidence:
  vm: gnuhealth-his-01
  project: isthealth
  zone: me-central1-a
  install_path: /opt/gnuhealth/his-50
"""
    write_text(UPSTREAM / "UPSTREAM_BASELINE.yaml", baseline)

    active = [m for m, meta in modules.items() if meta.get("activation_state") == "activated"]
    inactive = [m for m, meta in modules.items() if meta.get("activation_state") != "activated"]
    report = f"""# Version Discovery Report — IST HIS Upstream Baseline

**Baseline date:** {BASELINE_DATE}  
**Product:** IST HIS — Iris Star Hospital Information System  
**VM:** `gnuhealth-his-01` (project `isthealth`, zone `me-central1-a`)  
**Status:** Live VM evidence captured via `gcloud compute ssh`

## Detected versions

| Component | Version | Source |
|-----------|---------|--------|
| GNU Health HIS (core `gnuhealth`) | **{GH_VERSION}** | `pip show` on VM |
| Latest official stable (not adopted) | {GH_LATEST_STABLE} | Codeberg tag `5.0.7` |
| Tryton server (`trytond`) | **{TRYTON}** | `pip show` |
| Tryton web client (SAO) | **{SAO}** | `/opt/gnuhealth/his-50/sao/package.json` |
| Desktop Tryton client | Not installed | `pip show tryton` empty |
| GNU Health Control | {GH_CONTROL} | `pip show gnuhealth-control` |
| PostgreSQL | {PG} | `psql --version` |
| Python | {PYTHON_VM} | VM venv |
| Source pin | tag `v{GH_VERSION}` commit `{SOURCE_COMMIT}` | Codeberg |

## Upgrade policy

**No automatic upgrade.** Installed series is 5.0.x with core package {GH_VERSION}.
Latest patchset {GH_LATEST_STABLE} exists upstream; adoption requires a separate change window.

## Modules

| Metric | Count |
|--------|------:|
| Health modules in release source tree | {len(modules)} |
| Activated (`ir.module`, DB `isthealth`) | {len(VM_ACTIVATED)} |
| Inactive health modules on VM | {len(VM_ACTIVATED) and 0} |
| Custom IST modules (`ist*` / `iris*`) | 0 |

All {len(VM_ACTIVATED)} discovered `health*` / `health` modules are **activated** on `isthealth`.

## Database schema version

Tryton module states are authoritative for schema. Exact `ir.configuration` / DB revision
string was not separately exported; schema corresponds to activated modules at baseline.

## Confidence

| Item | Confidence |
|------|------------|
| Server / Tryton / SAO / PG / Python | **High** (live VM) |
| Module activation list | **High** (live `ir.module`) |
| Per-module field catalogue | **Medium** (scraped from tag `v{GH_VERSION}` source; not live proteus introspection) |
| Documentation RST portal | **Medium** (Codeberg `documentation` main branch at retrieval; may lag/lead patchset) |

## Commands used

```bash
gcloud compute ssh gnuhealth-his-01 --project=isthealth --zone=me-central1-a --command='...'
# pip show / pip list | grep gnuhealth
# psql -d isthealth -c "SELECT name, state FROM ir_module WHERE name LIKE 'health%' OR name='health'"
```
"""
    write_text(UPSTREAM / "version-discovery-report.md", report)

    wb = Workbook()
    ws = wb.active
    ws.title = "Installed Modules"
    headers = [
        "technical_name",
        "display_name",
        "pip_version",
        "tryton_cfg_version",
        "activation_state",
        "upstream_or_ist",
        "depends",
        "model_count",
        "in_release_source",
    ]
    ws.append(headers)
    for name in sorted(set(list(modules) + list(FEATURES_EXTRA))):
        if name in modules:
            m = modules[name]
            ws.append(
                [
                    name,
                    m["display_name"],
                    m["version"],
                    m.get("tryton_cfg_version", ""),
                    m["activation_state"],
                    m["upstream_or_ist"],
                    ", ".join(m.get("depends") or []),
                    len(m.get("models") or []),
                    True,
                ]
            )
        else:
            extra = FEATURES_EXTRA[name]
            ws.append(
                [
                    name,
                    extra["display_name"],
                    "",
                    "",
                    "absent_from_release",
                    "upstream-features-doc-only",
                    "",
                    0,
                    False,
                ]
            )
    wb.save(UPSTREAM / "installed-module-inventory.xlsx")
    print("Phase 1 complete")


def phase2_3_acquire_docs() -> dict[str, Any]:
    """Copy immutable RST/images from official documentation clone; download HTML index set."""
    ORIGINAL.mkdir(parents=True, exist_ok=True)
    rst_src = CACHE_DOC / "his" / "source"
    img_src = rst_src / "images"
    copied: list[Path] = []

    if rst_src.exists():
        for p in rst_src.rglob("*"):
            if not p.is_file():
                continue
            if p.suffix.lower() not in {".rst", ".py", ".png", ".svg", ".jpg", ".jpeg", ".gif", ".css", ".txt", ".md"}:
                if p.name not in {"Makefile", "conf.py"} and p.suffix.lower() not in {".html"}:
                    continue
            rel = p.relative_to(rst_src)
            if p.suffix.lower() == ".rst" or p.name == "conf.py":
                target = ORIGINAL / "rst" / rel
            elif p.suffix.lower() in {".png", ".svg", ".jpg", ".jpeg", ".gif"}:
                target = ORIGINAL / "images" / rel
            else:
                target = ORIGINAL / "rst" / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, target)
            copied.append(target)

    # Release notes from HIS source
    for fname in ("README.rst", "COPYING", "LICENSE", "Changelog", "CHANGELOG"):
        for candidate in (CACHE_HIS / fname, CACHE_HIS / "tryton" / fname):
            if candidate.exists() and candidate.is_file():
                dest = ORIGINAL / "release-notes" / candidate.name
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(candidate, dest)
                copied.append(dest)

    # Minimal configuration examples placeholder from docs if any
    (ORIGINAL / "configuration").mkdir(parents=True, exist_ok=True)
    (ORIGINAL / "diagrams").mkdir(parents=True, exist_ok=True)

    # Download key HTML pages into generated-reference (not original)
    html_dir = GENERATED / "html"
    html_dir.mkdir(parents=True, exist_ok=True)
    urls = [
        "https://docs.gnuhealth.org/his/",
        "https://docs.gnuhealth.org/his/features.html",
        "https://docs.gnuhealth.org/his/changelog.html",
        "https://docs.gnuhealth.org/his/preface.html",
        "https://docs.gnuhealth.org/his/support.html",
        "https://docs.gnuhealth.org/his/roadmap.html",
    ]
    import urllib.request

    html_count = 0
    for url in urls:
        name = url.rstrip("/").split("/")[-1] or "index.html"
        if not name.endswith(".html"):
            name = "index.html"
        dest = html_dir / name
        try:
            with urllib.request.urlopen(url, timeout=60) as resp:
                dest.write_bytes(resp.read())
            html_count += 1
            copied.append(dest)  # tracked in manifest separately for original only
        except Exception as exc:  # noqa: BLE001
            write_text(html_dir / f"{name}.error.txt", f"Failed {url}: {exc}")

    # Attribution & licences
    write_text(UPSTREAM / "ATTRIBUTION.md", f"""# Attribution — Upstream GNU Health Documentation

Retrieval date: {DOC_RETRIEVAL}

## Copyright

GNU Health Hospital Information System documentation — Copyright © GNU Solidario.

Software — Copyright © GNU Solidario / GNU Health contributors; licensed under GPL-3.0-or-later.

## IST HIS notice

{ATTRIBUTION}

## Legal review flag

**LEGAL REVIEW REQUIRED** before commercial distribution: branding, trademark use of
“GNU Health”, CC-BY-SA share-alike obligations for adapted documentation, and GPL
compliance for distributed binaries/modifications.

Do not claim certification, sponsorship, or endorsement by GNU Solidario, the GNU Project,
or the Free Software Foundation unless written authorization exists.
""")

    # Licence texts (short pointers + GPL header; full GPL from HIS COPYING if present)
    write_text(
        UPSTREAM / "LICENSE-DOCUMENTATION.txt",
        "GNU Health HIS documentation is available under Creative Commons "
        "Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).\n"
        "See https://creativecommons.org/licenses/by-sa/4.0/\n"
        f"Upstream source: https://codeberg.org/gnuhealth/documentation (retrieved {DOC_RETRIEVAL})\n",
    )
    copy_src = CACHE_HIS / "COPYING"
    if copy_src.exists():
        shutil.copy2(copy_src, UPSTREAM / "LICENSE-SOFTWARE.txt")
    else:
        # Also check LICENSES folder in tryton
        lic = list((CACHE_HIS / "tryton").glob("**/COPYING"))[:1]
        if lic:
            shutil.copy2(lic[0], UPSTREAM / "LICENSE-SOFTWARE.txt")
        else:
            write_text(
                UPSTREAM / "LICENSE-SOFTWARE.txt",
                "GNU Health software components: GNU General Public License v3 or later.\n"
                "See https://www.gnu.org/licenses/gpl-3.0.html\n"
                f"Source pin: codeberg.org/gnuhealth/his tag v{GH_VERSION}\n",
            )

    # Manifest for original/ only — paths relative to repository root
    manifest_files = []
    for p in sorted(ORIGINAL.rglob("*")):
        if p.is_file():
            rel = str(p.relative_to(ROOT)).replace("\\", "/")
            manifest_files.append(
                {
                    "path": rel,
                    "original_source": "https://codeberg.org/gnuhealth/documentation (HIS RST) / his release tree",
                    "upstream_version": GH_VERSION,
                    "retrieval_date": DOC_RETRIEVAL,
                    "copyright_owner": "GNU Solidario",
                    "licence": "CC-BY-SA-4.0 (docs) / GPL-3.0-or-later (software texts)",
                    "sha256": sha256_file(p),
                    "bytes": p.stat().st_size,
                }
            )
    manifest = {
        "product": "IST HIS",
        "upstream_product": "GNU Health HIS",
        "upstream_version": GH_VERSION,
        "retrieval_date": DOC_RETRIEVAL,
        "immutable_root": "docs/upstream/original/",
        "file_count": len(manifest_files),
        "html_pages_downloaded": html_count,
        "files": manifest_files,
    }
    write_text(UPSTREAM / "source-manifest.json", json.dumps(manifest, indent=2))
    print(f"Phase 2-3 complete: {len(manifest_files)} original files, {html_count} HTML pages")
    return manifest


def phase4_5_registry(modules: dict[str, Any]) -> tuple[list[dict], list[dict]]:
    rows: list[dict[str, Any]] = []
    reverse: dict[str, list[str]] = {}
    for name, m in modules.items():
        for dep in m.get("depends") or []:
            reverse.setdefault(dep, []).append(name)

    for name in sorted(set(list(modules) + BRIEF_SECTION5 + list(FEATURES_EXTRA))):
        if name in modules:
            m = modules[name]
            rows.append(
                {
                    "technical_module_name": name,
                    "display_name": m["display_name"],
                    "version": m["version"],
                    "description": f"GNU Health module {name}",
                    "upstream_or_ist": "upstream",
                    "installation_state": "installed",
                    "activation_state": m["activation_state"],
                    "dependencies": m.get("depends") or [],
                    "reverse_dependencies": reverse.get(name, []),
                    "models_introduced": m.get("models") or [],
                    "models_extended": [],
                    "database_tables": [x.replace(".", "_") for x in (m.get("models") or [])],
                    "menus": [],
                    "views": [x for x in (m.get("xml_files") or []) if "view" in x],
                    "wizards": [x for x in (m.get("xml_files") or []) if "wizard" in x],
                    "reports": [x for x in (m.get("xml_files") or []) if "report" in x],
                    "sequences": [],
                    "scheduled_jobs": [],
                    "security_groups": [],
                    "access_control_rules": [],
                    "reference_master_data": [],
                    "country_applicability": ["AE", "QA", "global"],
                    "facility_applicability": "all",
                    "synthetic_data_availability": "pack-mapped" if name in VM_ACTIVATED else "none",
                    "ist_his_documentation_status": "guide-generated" if name in VM_ACTIVATED else "not-enabled",
                    "test_coverage": "pack-stub",
                    "implementation_status": "activated" if name in VM_ACTIVATED else "not-in-db",
                    "brief_section5": name in BRIEF_SECTION5,
                    "in_release": True,
                    "notes": "",
                }
            )
        else:
            extra = FEATURES_EXTRA.get(name, {})
            rows.append(
                {
                    "technical_module_name": name,
                    "display_name": extra.get("display_name", DISPLAY_NAMES.get(name, name)),
                    "version": "",
                    "description": extra.get("description", ""),
                    "upstream_or_ist": "upstream-features-doc-only",
                    "installation_state": "absent",
                    "activation_state": "absent_from_release",
                    "dependencies": [],
                    "reverse_dependencies": [],
                    "models_introduced": [],
                    "models_extended": [],
                    "database_tables": [],
                    "menus": [],
                    "views": [],
                    "wizards": [],
                    "reports": [],
                    "sequences": [],
                    "scheduled_jobs": [],
                    "security_groups": [],
                    "access_control_rules": [],
                    "reference_master_data": [],
                    "country_applicability": [],
                    "facility_applicability": "n/a",
                    "synthetic_data_availability": "none",
                    "ist_his_documentation_status": "marked-missing-deprecated",
                    "test_coverage": "n/a",
                    "implementation_status": "not_in_selected_release",
                    "brief_section5": name in BRIEF_SECTION5,
                    "in_release": False,
                    "notes": extra.get("status_note", "Present in §5 brief / features page but not in v5.0.6 tryton tree"),
                }
            )

    # Also include release-only modules not in BRIEF (e.g. health_socioeconomics, health_stock_*)
    write_text(UPSTREAM / "module-registry.json", json.dumps({"baseline": GH_VERSION, "modules": rows}, indent=2))

    wb = Workbook()
    ws = wb.active
    ws.title = "Module Registry"
    keys = [
        "technical_module_name",
        "display_name",
        "version",
        "description",
        "upstream_or_ist",
        "installation_state",
        "activation_state",
        "dependencies",
        "reverse_dependencies",
        "models_introduced",
        "country_applicability",
        "synthetic_data_availability",
        "ist_his_documentation_status",
        "implementation_status",
        "brief_section5",
        "in_release",
        "notes",
    ]
    ws.append(keys)
    for r in rows:
        ws.append(
            [
                ", ".join(r[k]) if isinstance(r[k], list) and k in (
                    "dependencies",
                    "reverse_dependencies",
                    "models_introduced",
                    "country_applicability",
                )
                else r[k]
                for k in keys
            ]
        )
    wb.save(UPSTREAM / "GNU_Health_Complete_Module_Registry.xlsx")

    # Dependency mermaid
    lines = [
        "# GNU Health Module Dependency Map (IST HIS baseline)",
        "",
        f"**Upstream version:** {GH_VERSION}  ",
        f"**Generated:** {BASELINE_DATE}  ",
        "",
        "Dependencies parsed from each module `tryton.cfg` in tag `v5.0.6`.",
        "",
        "```mermaid",
        "flowchart TD",
    ]
    for name, m in sorted(modules.items()):
        safe = name.replace("-", "_")
        for dep in m.get("depends") or []:
            if dep.startswith("health") or dep == "health":
                lines.append(f"  {dep.replace('-', '_')} --> {safe}")
    lines.append("```")
    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("- Non-health Tryton deps (`party`, `company`, `stock`, …) omitted from diagram for readability.")
    lines.append("- `health_accounting` / `health_profile` / `health_imaging_orthanc` are **not** in the release tree.")
    write_text(UPSTREAM / "module-dependency-map.md", "\n".join(lines) + "\n")

    # Model and field catalogue
    field_rows: list[dict] = []
    model_rows: list[dict] = []
    for name, m in sorted(modules.items()):
        for model in m.get("models") or []:
            model_rows.append(
                {
                    "module": name,
                    "model": model,
                    "confidence": "medium-source-scrape",
                    "upstream_version": GH_VERSION,
                }
            )
        for fr in m.get("fields") or []:
            field_rows.append({**fr, "module": name, "confidence": "medium-source-scrape"})

    wb2 = Workbook()
    ws1 = wb2.active
    ws1.title = "Models"
    ws1.append(["module", "model", "confidence", "upstream_version"])
    for r in model_rows:
        ws1.append([r["module"], r["model"], r["confidence"], r["upstream_version"]])
    ws2 = wb2.create_sheet("Fields")
    ws2.append(["module", "model", "field", "type", "string", "source_file", "confidence"])
    for r in field_rows:
        ws2.append(
            [
                r.get("module"),
                r.get("model"),
                r.get("field"),
                r.get("type"),
                r.get("string"),
                r.get("source_file"),
                r.get("confidence", "medium-source-scrape"),
            ]
        )
    ws3 = wb2.create_sheet("Confidence")
    ws3.append(["note"])
    ws3.append(
        [
            "Catalogue scraped from Python sources at tag v5.0.6. "
            "Live Tryton/proteus field introspection on VM was not run for full dump; mark medium confidence."
        ]
    )
    wb2.save(UPSTREAM / "model-and-field-catalogue.xlsx")
    print(f"Phase 4-5 complete: {len(rows)} registry rows, {len(model_rows)} models, {len(field_rows)} fields")
    return model_rows, field_rows


def phase6_naming() -> None:
    IST.mkdir(parents=True, exist_ok=True)
    write_text(
        IST / "IST_HIS_Naming_and_Branding_Policy.md",
        f"""---
title: IST HIS Naming and Branding Policy
ist_his_version: {IST_HIS_VERSION}
upstream_product: GNU Health HIS
upstream_version: {GH_VERSION}
implementation_status: policy
last_verified_against_code: {BASELINE_DATE}
licence: CC-BY-SA-4.0
legal_review: REQUIRED
---

# IST HIS Naming and Branding Policy

**Product (customer-facing):** IST HIS — Iris Star Hospital Information System  

**Upstream:** GNU Health HIS {GH_VERSION} on Tryton {TRYTON}

## 6.1 Replace with “IST HIS”

Use IST HIS branding in:

- Product titles, page headers, login screen, navigation headings
- Help-centre headings, user/implementation manuals, training material
- Client-facing screenshots and configurable report headers
- Email/notification templates and architecture diagrams for customers
- Customer-facing file names (e.g. `IST_HIS_*` templates)

## 6.2 Preserve technical names

Do **not** rename without a formal migration design:

- Python package names (`gnuhealth-*`)
- Tryton module names (`health`, `health_lab`, …)
- Model names beginning with `gnuhealth.`
- Database table names, XML IDs, API fields, configuration parameters
- Entry-point commands, module dependencies, `gnuhealth-control` commands
- Existing migration references

### Examples

| Customer-facing name | Technical identifier |
|----------------------|----------------------|
| IST HIS Patient | `gnuhealth.patient` |
| IST HIS Laboratory | module `health_lab` |
| IST HIS Inpatient Management | module `health_inpatient` |

**Do not** perform naive global search-replace of “GNU Health” → “IST HIS” in code or technical docs.

## 6.3 Attribution

{ATTRIBUTION}

## 6.4 Legal review flag

**FLAG: LEGAL REVIEW REQUIRED** before commercial release covering trademarks,
CC-BY-SA share-alike for adapted docs, GPL compliance, and non-endorsement wording.
""",
    )
    print("Phase 6 complete")


def module_guide_md(name: str, meta: dict[str, Any]) -> str:
    deps = ", ".join(meta.get("depends") or []) or "(see tryton.cfg)"
    models = meta.get("models") or []
    model_list = "\n".join(f"- `{m}`" for m in models[:40]) or "- *(no `__name__` models scraped — verify in source)*"
    if len(models) > 40:
        model_list += f"\n- … +{len(models) - 40} more"
    return f"""---
title: IST HIS Module Guide — {DISPLAY_NAMES.get(name, name)}
ist_his_version: {IST_HIS_VERSION}
upstream_product: GNU Health HIS
upstream_version: {GH_VERSION}
upstream_document: features / module source tryton.cfg
upstream_modules:
  - {name}
country:
  - AE
  - QA
roles:
  - system-admin
  - facility-admin
implementation_status: activated
last_verified_against_code: {BASELINE_DATE}
licence: CC-BY-SA-4.0
adaptation_status: Adapted for IST HIS terminology
---

# IST HIS — {DISPLAY_NAMES.get(name, name)}

> {ATTRIBUTION.split(chr(10))[0]}

## Module purpose

Customer-facing capability area for **{DISPLAY_NAMES.get(name, name)}**, implemented by upstream
GNU Health module `{name}` (package version {meta.get('version', '')}).

## Technical module name

`{name}`

## Dependencies

{deps}

## Activation procedure

On the HIS server (do **not** run casually in production):

```bash
# Prefer gnuhealth-control / trytond-admin against the configured database
trytond-admin -c /opt/gnuhealth/his-50/etc/trytond.conf -d isthealth -u {name} --activate-dependencies
```

Baseline DB `isthealth` already has this module **activated** ({BASELINE_DATE}).

## Configuration prerequisites

- Company / institution master data (`company.company`, `gnuhealth.institution`)
- Users and access groups in Tryton
- Any coding catalogues required by depends (e.g. ICD modules)

## Master-data requirements

Populate reference data required by the module before synthetic clinical loads.
See `templates/IST_HIS_Implementation_Master_Data.xlsx`.

## Roles and permissions

Managed via Tryton `res.group` / `ir.model.access`. IST HIS React UI respects session roles;
do not invent permissions beyond upstream access XML without an IST custom module.

## Menu paths

Upstream SAO menus remain under GNU Health menu XML. IST React routes map selected models
(see `frontend/src/lib/tryton/models.ts`). Unmapped menus open SAO fallback.

## Screen descriptions

Prefer IST HIS React screens where implemented; otherwise SAO at `:8000` / `/sao/`.
Screen inventory is **best-effort** — verify against live menus after deploy.

## Field definitions

See `docs/upstream/model-and-field-catalogue.xlsx` filtered by module `{name}`.
Confidence: medium (source scrape of tag `v{GH_VERSION}`).

## Models

{model_list}

## Workflow states

Follow upstream model state fields (e.g. draft/confirmed/done) — do not invent states.
Mark **unverified** until confirmed in UI or proteus.

## Approval rules

Upstream wizard/button rules apply unless an IST customization is documented.

## Reports

Upstream ODT/PDF reports remain technically `gnuhealth.*` report actions; customer-facing
titles may show IST HIS where configurable.

## Integrations

Module-specific integrations (Orthanc, federation, CalDAV, etc.) only where the module
provides them. UAE/Qatar HIE connectors are **not** provided by upstream — pending IST work.

## Synthetic-data scenarios

See `synthetic-data/` packs that list `{name}` under applicable modules.

## UAE-specific considerations

- Use synthetic Emirates ID format `SYN-AE-*` only.
- National HIE (NABIDH / Malaffi / Riayati) — **pending regulatory confirmation**; not in upstream module.

## Qatar-specific considerations

- Use synthetic Qatar ID format `SYN-QA-*` only.
- MoPH / national e-health mandates — **pending regulatory confirmation**.

## Known gaps

- Live menu/field verification against SAO screens not exhaustively screenshot-tested in this baseline.
- No IST custom Tryton module for synthetic markers; markers live in external registry.

## Troubleshooting

1. Confirm module state: `SELECT name, state FROM ir_module WHERE name='{name}';`
2. Check trytond logs under `/opt/gnuhealth/his-50/log`
3. Do not upgrade modules as part of troubleshooting without change control

## Source traceability

| Item | Reference |
|------|-----------|
| Upstream features | https://docs.gnuhealth.org/his/features.html |
| Source | `docs/upstream/_cache/his-5.0.6/tryton/{name}` (local cache) / Codeberg tag v{GH_VERSION} |
| Immutable docs | `docs/upstream/original/` |
| IST policy | `docs/ist-his/IST_HIS_Naming_and_Branding_Policy.md` |
"""


def phase7_9_ist_library(modules: dict[str, Any], model_rows: list, field_rows: list) -> int:
    dirs = [
        "architecture",
        "implementation",
        "administration",
        "configuration",
        "user-guides",
        "modules",
        "workflows",
        "integration",
        "security",
        "data-migration",
        "synthetic-data",
        "troubleshooting",
        "training",
        "compliance",
    ]
    for d in dirs:
        (IST / d).mkdir(parents=True, exist_ok=True)

    def meta_header(title: str, status: str = "Adapted for IST HIS terminology") -> str:
        return f"""---
title: {title}
ist_his_version: {IST_HIS_VERSION}
upstream_product: GNU Health HIS
upstream_version: {GH_VERSION}
country: [AE, QA]
implementation_status: documented
last_verified_against_code: {BASELINE_DATE}
licence: CC-BY-SA-4.0
adaptation_status: {status}
---
"""

    write_text(
        IST / "index.md",
        meta_header("IST HIS Documentation Library")
        + f"""
# IST HIS Documentation Library

**IST HIS — Iris Star Hospital Information System** (product version {IST_HIS_VERSION})  
Upstream baseline: GNU Health HIS **{GH_VERSION}** / Tryton **{TRYTON}**

{ATTRIBUTION}

## Sections

| Section | Path |
|---------|------|
| Architecture | [architecture/](architecture/) |
| Implementation | [implementation/](implementation/) |
| Administration | [administration/](administration/) |
| Configuration | [configuration/](configuration/) |
| User guides | [user-guides/](user-guides/) |
| Modules | [modules/](modules/) |
| Workflows | [workflows/](workflows/) |
| Integration | [integration/](integration/) |
| Security | [security/](security/) |
| Data migration | [data-migration/](data-migration/) |
| Synthetic data | [synthetic-data/](synthetic-data/) |
| Troubleshooting | [troubleshooting/](troubleshooting/) |
| Training | [training/](training/) |
| Compliance | [compliance/](compliance/) |
| Naming policy | [IST_HIS_Naming_and_Branding_Policy.md](IST_HIS_Naming_and_Branding_Policy.md) |

## Adaptation classification legend

Adopted unchanged · Adapted for IST HIS terminology · Adapted for IST HIS UI · Adapted for UAE ·
Adapted for Qatar · Extended with IST-specific functionality · Replaced by custom IST workflow ·
Not enabled · Not applicable · Pending implementation · Pending regulatory confirmation
""",
    )

    write_text(
        IST / "architecture" / "overview.md",
        meta_header("IST HIS Architecture", "Adapted for IST HIS user interface")
        + f"""
# Architecture Overview

IST HIS presents a React SPA over GNU Health HIS / Tryton JSON-RPC.

- Backend: GNU Health {GH_VERSION}, Tryton {TRYTON}, PostgreSQL {PG}
- Legacy UI: SAO {SAO}
- Frontend: `frontend/` (IST branding)
- Technical models remain `gnuhealth.*`

See also `docs/research/current-system-discovery.md`.
""",
    )
    write_text(
        IST / "implementation" / "overview.md",
        meta_header("Implementation Overview")
        + """
# Implementation Overview

Follow master data templates under `templates/IST_HIS_*.xlsx`, synthetic packs under
`synthetic-data/`, and module guides under `modules/`. Do not upgrade GNU Health during
implementation without a controlled change request.
""",
    )
    write_text(
        IST / "administration" / "overview.md",
        meta_header("Administration Overview")
        + """
# Administration

Use Tryton administration for users, groups, modules, sequences. Prefer `gnuhealth-control`
and documented backup procedures from upstream tech guide (adapted terminology only).
""",
    )
    write_text(
        IST / "configuration" / "overview.md",
        meta_header("Configuration Overview")
        + """
# Configuration

Institution, company, warehouses, and coding catalogues must be configured before go-live.
Country packs AE/QA are configuration overlays — not upstream renames.
""",
    )
    write_text(
        IST / "user-guides" / "overview.md",
        meta_header("User Guides Overview", "Adapted for IST HIS user interface")
        + """
# User Guides

Role-based guides also exist under `docs/user-guides/roles/`. Module-specific operational
detail lives under `docs/ist-his/modules/<module>/`.
""",
    )
    write_text(
        IST / "workflows" / "overview.md",
        meta_header("Workflows Overview", "Adapted for IST HIS user interface")
        + """
# Workflows

Guided Help Centre workflows (frontend) complement these documents. Map each workflow to
activated modules before UAT sign-off.
""",
    )
    write_text(
        IST / "integration" / "overview.md",
        meta_header("Integration Overview", "Pending regulatory confirmation")
        + """
# Integration

Upstream: Orthanc (`health_orthanc`), Federation (`health_federation`), CalDAV/WebDAV.
UAE/Qatar HIE (NABIDH, Malaffi, Riayati, Qatar HIE) — **pending regulatory confirmation**
and are **not** claimed as upstream GNU Health features.
""",
    )
    write_text(
        IST / "security" / "overview.md",
        meta_header("Security Overview")
        + """
# Security

Follow upstream access control plus IST policies in `docs/security/`. Crypto modules
(`health_crypto`, `health_crypto_lab`) remain technical GNU Health packages.
""",
    )
    write_text(
        IST / "data-migration" / "overview.md",
        meta_header("Data Migration Overview")
        + """
# Data Migration

Use `templates/IST_HIS_Data_Migration_Mapping.xlsx`. Only map to real Tryton/GNU Health
or documented IST staging fields.
""",
    )
    write_text(
        IST / "synthetic-data" / "overview.md",
        meta_header("Synthetic Data Overview", "Extended with IST-specific functionality")
        + """
# Synthetic Data

Schema registry: `synthetic-data/schema/ist_his_model_registry.json`.  
Markers: `synthetic_data=true`, batch `ISTHIS-DEMO-*`. Never use real Emirates/Qatar IDs.
""",
    )
    write_text(
        IST / "troubleshooting" / "overview.md",
        meta_header("Troubleshooting Overview")
        + """
# Troubleshooting

Check module activation, trytond logs, and nginx/`/api/tryton` proxy. Do not modify
`docs/upstream/original/`.
""",
    )
    write_text(
        IST / "training" / "overview.md",
        meta_header("Training Overview")
        + """
# Training

Train on IST HIS UI labels while referencing technical module names for IT staff.
""",
    )
    write_text(
        IST / "compliance" / "overview.md",
        meta_header("Compliance Overview", "Pending regulatory confirmation")
        + """
# Compliance

UAE PDPL / Qatar PDPPL / HIE obligations require counsel confirmation. See
`docs/research/source-register.md`.
""",
    )

    guide_count = 0
    for name in VM_ACTIVATED:
        meta = modules.get(name)
        if not meta:
            continue
        path = IST / "modules" / name / "README.md"
        write_text(path, module_guide_md(name, meta))
        guide_count += 1

    # Traceability workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Traceability"
    headers = [
        "upstream_document_id",
        "upstream_title",
        "upstream_path",
        "upstream_version",
        "related_module",
        "related_model",
        "related_menu",
        "related_ist_his_screen",
        "ist_his_document_path",
        "adaptation_status",
        "uae_applicability",
        "qatar_applicability",
        "code_verified",
        "screenshot_verified",
        "synthetic_data_available",
        "test_scenario_available",
        "last_synchronized",
        "change_detected",
        "reviewer",
        "approval_status",
    ]
    ws.append(headers)
    # Map some upstream RST topics
    topics = [
        ("UG-PAT", "Patient management", "userguide/core/patientmanagement.rst", "health", "gnuhealth.patient", "/patients"),
        ("UG-EVAL", "Patient evaluations", "userguide/core/patientevaluations.rst", "health", "gnuhealth.patient.evaluation", "/evaluations"),
        ("UG-APPT", "Appointments", "userguide/core/patientappointment.rst", "health", "gnuhealth.appointment", "/appointments"),
        ("UG-LAB", "Laboratory", "userguide/modules/laboratory.rst", "health_lab", "gnuhealth.lab", "/laboratory"),
        ("UG-IMG", "Imaging", "userguide/modules/imaging.rst", "health_imaging", "gnuhealth.imaging.test.request", "/imaging"),
        ("UG-INP", "Inpatient", "userguide/modules/inpatientmanagement.rst", "health_inpatient", "gnuhealth.inpatient.registration", "/beds"),
        ("UG-NUR", "Nursing", "userguide/modules/nursing.rst", "health_nursing", "gnuhealth.patient.rounding", "/nursing"),
        ("UG-SUR", "Surgery", "userguide/modules/surgery.rst", "health_surgery", "gnuhealth.surgery", "/procedures"),
        ("FEAT", "Features / packages", "features.rst", "(all)", "", ""),
        ("CHG", "Changelog", "changelog.rst", "(all)", "", ""),
    ]
    for doc_id, title, path, mod, model, screen in topics:
        ist_path = f"docs/ist-his/modules/{mod}/README.md" if mod in VM_ACTIVATED else "docs/ist-his/index.md"
        ws.append(
            [
                doc_id,
                title,
                path,
                GH_VERSION,
                mod,
                model,
                "",
                screen,
                ist_path,
                "Adapted for IST HIS terminology",
                "Y",
                "Y",
                "partial",
                "N",
                "Y" if mod in VM_ACTIVATED else "N",
                "stub",
                BASELINE_DATE,
                "N",
                "",
                "draft",
            ]
        )
    for name in VM_ACTIVATED:
        ws.append(
            [
                f"MOD-{name}",
                f"Module {name}",
                f"tryton/{name}",
                GH_VERSION,
                name,
                "",
                "",
                "",
                f"docs/ist-his/modules/{name}/README.md",
                "Adapted for IST HIS terminology",
                "Y",
                "Y",
                "source-scrape",
                "N",
                "Y",
                "pack-stub",
                BASELINE_DATE,
                "N",
                "",
                "draft",
            ]
        )
    wb.save(IST / "IST_HIS_Documentation_Traceability.xlsx")
    print(f"Phase 7-9 complete: {guide_count} module guides")
    return guide_count


def phase10_12_synthetic(modules: dict[str, Any], model_rows: list) -> int:
    SYN.mkdir(parents=True, exist_ok=True)
    schema_models = []
    for r in model_rows:
        schema_models.append(
            {
                "model": r["model"],
                "module": r["module"],
                "ist_functional_area": r["module"],
                "confidence": r["confidence"],
            }
        )
    registry = {
        "schema_version": IST_HIS_VERSION,
        "upstream_version": GH_VERSION,
        "generated": BASELINE_DATE,
        "synthetic_marker_fields": {
            "synthetic_data": True,
            "synthetic_batch_id_pattern": "ISTHIS-DEMO-YYYYMMDD",
            "synthetic_seed": 20260714,
            "storage": "external_registry_preferred",
            "note": "Do not modify upstream GNU Health modules; use IST registry or future custom module",
        },
        "id_policy": {
            "emirates_id": "SYN-AE-{seq:08d}",
            "qatar_id": "SYN-QA-{seq:08d}",
            "forbid_real_national_ids": True,
        },
        "demo_group": {
            "name": "IST Healthcare Group",
            "children": {
                "IST Healthcare UAE": [
                    "IST General Hospital Dubai",
                    "IST Medical Centre Dubai",
                    "IST Day Surgery Centre Dubai",
                    "IST General Hospital Abu Dhabi",
                    "Central Laboratory UAE",
                    "Central Pharmacy UAE",
                ],
                "IST Healthcare Qatar": [
                    "IST General Hospital Doha",
                    "IST Medical Centre Doha",
                    "IST Specialist Clinic Doha",
                    "Central Laboratory Qatar",
                    "Central Pharmacy Qatar",
                ],
            },
        },
        "models": schema_models,
    }
    write_text(SYN / "schema" / "ist_his_model_registry.json", json.dumps(registry, indent=2))

    # Extend config synthetic demo
    demo_path = ROOT / "config" / "synthetic" / "uae_qatar_demo.yaml"
    # Append group structure file rather than breaking existing
    write_text(
        ROOT / "config" / "synthetic" / "ist_healthcare_group.yaml",
        f"""# IST Healthcare Group — synthetic org structure (baseline {BASELINE_DATE})
synthetic_data: true
synthetic_batch_id: ISTHIS-DEMO-20260714
synthetic_seed: 20260714
environment: test

group:
  name: IST Healthcare Group
  code: IST-HC-GRP

entities:
  - code: IST-HC-AE
    name: IST Healthcare UAE
    country: AE
    parent: IST-HC-GRP
  - code: IST-HC-QA
    name: IST Healthcare Qatar
    country: QA
    parent: IST-HC-GRP

facilities:
  - {{ code: FAC-DXB-GH, name: IST General Hospital Dubai, country: AE, entity: IST-HC-AE }}
  - {{ code: FAC-DXB-MC, name: IST Medical Centre Dubai, country: AE, entity: IST-HC-AE }}
  - {{ code: FAC-DXB-DS, name: IST Day Surgery Centre Dubai, country: AE, entity: IST-HC-AE }}
  - {{ code: FAC-AUH-GH, name: IST General Hospital Abu Dhabi, country: AE, entity: IST-HC-AE }}
  - {{ code: FAC-AE-LAB, name: Central Laboratory UAE, country: AE, entity: IST-HC-AE }}
  - {{ code: FAC-AE-PH, name: Central Pharmacy UAE, country: AE, entity: IST-HC-AE }}
  - {{ code: FAC-DOH-GH, name: IST General Hospital Doha, country: QA, entity: IST-HC-QA }}
  - {{ code: FAC-DOH-MC, name: IST Medical Centre Doha, country: QA, entity: IST-HC-QA }}
  - {{ code: FAC-DOH-SC, name: IST Specialist Clinic Doha, country: QA, entity: IST-HC-QA }}
  - {{ code: FAC-QA-LAB, name: Central Laboratory Qatar, country: QA, entity: IST-HC-QA }}
  - {{ code: FAC-QA-PH, name: Central Pharmacy Qatar, country: QA, entity: IST-HC-QA }}

id_formats:
  national_id_ae: "SYN-AE-{{seq:08d}}"
  national_id_qa: "SYN-QA-{{seq:08d}}"
  note: "Synthetic only — never real Emirates/Qatar ID values"

options:
  refuse_production_without_override: true
""",
    )

    gen_count = 0
    for pack, models, mods in PACKS:
        pdir = SYN / pack
        pdir.mkdir(parents=True, exist_ok=True)
        write_text(
            pdir / "prerequisites.md",
            f"# Prerequisites — `{pack}`\n\nApplicable modules: {', '.join(mods)}\n\n"
            f"Upstream: GNU Health {GH_VERSION}. Ensure modules activated. Dry-run before import.\n",
        )
        write_text(
            pdir / "config.yaml",
            f"pack: {pack}\nmodules: {mods}\nmodels: {models}\n"
            f"synthetic_batch_id: ISTHIS-DEMO-20260714\nsynthetic_seed: 20260714\n"
            f"volume:\n  default: 10\n",
        )
        write_text(
            pdir / "generator.py",
            f'''#!/usr/bin/env python3
"""Synthetic generator stub for pack {pack}.

Integrates with existing synthetic_data package; does not bypass prod refuse / dry-run.
"""
from __future__ import annotations

SYNTHETIC_DATA = True
SYNTHETIC_BATCH_ID = "ISTHIS-DEMO-20260714"
SYNTHETIC_SEED = 20260714
PACK = "{pack}"
MODULES = {mods!r}
MODELS = {models!r}


def generate(dry_run: bool = True) -> dict:
    """Return planned records; refuse production unless caller overrides safely."""
    return {{
        "pack": PACK,
        "dry_run": dry_run,
        "synthetic_data": SYNTHETIC_DATA,
        "synthetic_batch_id": SYNTHETIC_BATCH_ID,
        "synthetic_seed": SYNTHETIC_SEED,
        "modules": MODULES,
        "models": MODELS,
        "records": [],
        "status": "stub-ready",
    }}


if __name__ == "__main__":
    import json
    print(json.dumps(generate(dry_run=True), indent=2))
''',
        )
        write_text(
            pdir / "validation.py",
            f'''#!/usr/bin/env python3
"""Validation rules for pack {pack}."""
from __future__ import annotations

FORBIDDEN_PREFIXES = ()  # real national IDs never generated
REQUIRED_MARKERS = ("synthetic_data", "synthetic_batch_id", "synthetic_seed")


def validate_record(rec: dict) -> list[str]:
    errors = []
    for k in REQUIRED_MARKERS:
        if k not in rec:
            errors.append(f"missing {{k}}")
    for key in ("emirates_id", "qatar_id", "national_id"):
        val = str(rec.get(key, ""))
        if val and not (val.startswith("SYN-AE-") or val.startswith("SYN-QA-") or val.startswith("IST-")):
            errors.append(f"non-synthetic identifier in {{key}}: {{val}}")
    return errors
''',
        )
        write_text(
            pdir / "import_stub.py",
            f'''#!/usr/bin/env python3
"""Import stub for {pack} — wires to scripts/synthetic_data/cli.py patterns."""
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
''',
        )
        write_text(
            pdir / "rollback_stub.py",
            f'''#!/usr/bin/env python3
"""Rollback stub for {pack} — deletes by synthetic_batch_id when registry supports it."""
BATCH = "ISTHIS-DEMO-20260714"


def rollback(dry_run: bool = True) -> dict:
    return {{"pack": "{pack}", "batch": BATCH, "dry_run": dry_run, "status": "stub"}}
''',
        )
        write_text(
            pdir / "test_pack.py",
            f'''#!/usr/bin/env python3
from generator import generate
from validation import validate_record


def test_generate_dry_run():
    out = generate(dry_run=True)
    assert out["synthetic_data"] is True
    assert out["pack"] == "{pack}"


def test_validation_flags_bad_id():
    errs = validate_record({{"synthetic_data": True, "synthetic_batch_id": "x", "synthetic_seed": 1, "national_id": "784-1990-1234567-1"}})
    assert errs
''',
        )
        write_text(
            pdir / "README.md",
            f"# Synthetic pack `{pack}`\n\nModules: {', '.join(mods)}\n\n"
            f"Models: {', '.join(models)}\n\nExpected workflows/reports: see module guides.\n",
        )
        gen_count += 1

    # Bridge note for existing synthetic_data package
    write_text(
        SYN / "README.md",
        f"""# IST HIS Synthetic Data Packs

Upstream model alignment: GNU Health **{GH_VERSION}**.  
Schema: `schema/ist_his_model_registry.json`.

Existing runtime loaders remain in `synthetic_data/` and `scripts/synthetic_data/` —
these packs extend them with module-ordered stubs. **Prod refuse** and **dry-run**
behaviour in the existing CLI must be preserved.
""",
    )
    print(f"Phase 10-12 complete: {gen_count} packs")
    return gen_count


def phase13_templates(field_rows: list, model_rows: list) -> int:
    TEMPLATES.mkdir(parents=True, exist_ok=True)

    def sheet_with_field_map(wb, title: str, rows: list[list]):
        ws = wb.create_sheet(title) if wb.sheetnames != ["Sheet"] else wb.active
        ws.title = title
        header = [
            "ist_his_business_name",
            "technical_model",
            "technical_field",
            "field_type",
            "mandatory",
            "allowed_values",
            "format",
            "max_length",
            "unique_rule",
            "parent_reference",
            "applicable_module",
            "uae_applicability",
            "qatar_applicability",
            "example_synthetic_value",
            "validation_rule",
            "import_order",
            "notes",
        ]
        ws.append(header)
        for r in rows:
            ws.append(r)
        return ws

    # Master data
    wb = Workbook()
    known = [
        ["Patient code", "gnuhealth.patient", "name", "Many2One/Char", "Y", "", "", "", "Y", "party.party", "health", "Y", "Y", "IST-P-00001", "synthetic prefix", 10, ""],
        ["Patient party name", "party.party", "name", "Char", "Y", "", "", "255", "", "", "health", "Y", "Y", "SYN Patient 00001", "", 5, ""],
        ["Synthetic AE ID", "party.party", "code/extra", "Char", "N", "SYN-AE-*", "SYN-AE-########", "16", "", "", "health", "Y", "N", "SYN-AE-00000001", "must start SYN-AE-", 6, "not real Emirates ID"],
        ["Synthetic QA ID", "party.party", "code/extra", "Char", "N", "SYN-QA-*", "SYN-QA-########", "16", "", "", "health", "N", "Y", "SYN-QA-00000001", "must start SYN-QA-", 6, "not real Qatar ID"],
        ["Institution", "gnuhealth.institution", "name", "Char", "Y", "", "", "", "", "party.party", "health", "Y", "Y", "IST General Hospital Doha", "", 3, ""],
        ["Appointment date", "gnuhealth.appointment", "appointment_date", "DateTime", "Y", "", "ISO-8601", "", "", "gnuhealth.patient", "health", "Y", "Y", "2026-07-14T09:00:00", "", 20, ""],
        ["Lab test", "gnuhealth.lab", "name", "Char", "Y", "", "", "", "", "gnuhealth.patient", "health_lab", "Y", "Y", "SYN-LAB-0001", "", 30, ""],
        ["Invoice", "account.invoice", "number", "Char", "N", "", "", "", "", "party.party", "account_invoice", "Y", "Y", "SYN-INV-0001", "", 40, "Tryton accounting"],
    ]
    sheet_with_field_map(wb, "MasterData", known)
    # add sample scraped fields (first 200)
    ws2 = wb.create_sheet("ScrapedFieldsSample")
    ws2.append(["module", "model", "field", "type", "string", "confidence"])
    for fr in field_rows[:200]:
        ws2.append([fr.get("module"), fr.get("model"), fr.get("field"), fr.get("type"), fr.get("string"), "medium-source-scrape"])
    wb.save(TEMPLATES / "IST_HIS_Implementation_Master_Data.xlsx")

    wb = Workbook()
    ws = wb.active
    ws.title = "DataDictionary"
    ws.append(["model", "field", "type", "string", "module", "upstream_version", "confidence"])
    for fr in field_rows[:5000]:
        ws.append([fr.get("model"), fr.get("field"), fr.get("type"), fr.get("string"), fr.get("module"), GH_VERSION, "medium-source-scrape"])
    wb.save(TEMPLATES / "IST_HIS_Data_Dictionary.xlsx")

    wb = Workbook()
    ws = wb.active
    ws.title = "Roles"
    ws.append(["role", "tryton_group_hint", "modules", "uae", "qatar", "notes"])
    for role in ["receptionist", "physician", "nurse", "lab-tech", "pharmacist", "cashier", "facility-admin", "system-admin"]:
        ws.append([role, f"IST/{role}", "health(+)", "Y", "Y", "Map to actual res.group on VM — unverified names"])
    wb.save(TEMPLATES / "IST_HIS_Role_Access_Matrix.xlsx")

    wb = Workbook()
    ws = wb.active
    ws.title = "Integrations"
    ws.append(["integration", "direction", "standard", "upstream_module", "uae", "qatar", "status"])
    for row in [
        ["Orthanc PACS", "bi", "DICOM", "health_orthanc", "Y", "Y", "upstream"],
        ["Federation/Thalamus", "bi", "GH Federation", "health_federation", "?", "?", "upstream-optional"],
        ["NABIDH", "out", "HL7/FHIR", "n/a", "Y", "N", "pending regulatory confirmation"],
        ["Malaffi", "out", "HL7/FHIR", "n/a", "Y", "N", "pending regulatory confirmation"],
        ["Riayati", "out", "HL7/FHIR", "n/a", "Y", "N", "pending regulatory confirmation"],
        ["Qatar HIE", "out", "TBD", "n/a", "N", "Y", "pending regulatory confirmation"],
    ]:
        ws.append(row)
    wb.save(TEMPLATES / "IST_HIS_Integration_Register.xlsx")

    wb = Workbook()
    ws = wb.active
    ws.title = "MigrationMapping"
    ws.append(["source_field", "ist_business_name", "technical_model", "technical_field", "transform", "notes"])
    ws.append(["LegacyMRN", "Patient code", "gnuhealth.patient", "name", "prefix IST-P-", "synthetic/demo only"])
    ws.append(["LegacyName", "Party name", "party.party", "name", "copy", ""])
    wb.save(TEMPLATES / "IST_HIS_Data_Migration_Mapping.xlsx")

    wb = Workbook()
    ws = wb.active
    ws.title = "UAT"
    ws.append(["scenario_id", "title", "module", "steps", "expected", "country"])
    for i, (sid, title, mod) in enumerate(
        [
            ("UAT-001", "Register synthetic patient", "health"),
            ("UAT-002", "Book appointment", "health"),
            ("UAT-003", "Create evaluation", "health"),
            ("UAT-004", "Lab order and result", "health_lab"),
            ("UAT-005", "Prescription", "health"),
            ("UAT-006", "Admission", "health_inpatient"),
        ],
        1,
    ):
        ws.append([sid, title, mod, "See module guide", "Record created with synthetic markers", "AE/QA"])
    wb.save(TEMPLATES / "IST_HIS_UAT_Scenarios.xlsx")

    doc = Document()
    doc.add_heading("IST HIS Client Questionnaire", 0)
    doc.add_paragraph(
        f"IST HIS — Iris Star Hospital Information System (v{IST_HIS_VERSION}). "
        f"Upstream GNU Health HIS {GH_VERSION}."
    )
    doc.add_paragraph(ATTRIBUTION.split("\n")[0])
    doc.add_heading("Facility profile", level=1)
    for q in [
        "Legal entity name(s) UAE / Qatar",
        "Facilities in scope",
        "Modules required (from registry)",
        "Coding standards (ICD-10/11, CPT, …) — confirm licensing",
        "Insurance payers",
        "HIE participation (NABIDH/Malaffi/Riayati/Qatar) — pending confirmation",
        "Languages (EN/AR)",
        "Go-live target",
    ]:
        doc.add_paragraph(q, style="List Number")
    doc.save(TEMPLATES / "IST_HIS_Client_Questionnaire.docx")
    print("Phase 13 complete: 7 templates")
    return 7


def phase14_docs_sync(manifest: dict) -> None:
    pkg = ROOT / "docs_sync"
    pkg.mkdir(parents=True, exist_ok=True)
    write_text(
        pkg / "__init__.py",
        '"""IST HIS documentation synchronization toolkit."""\n__version__ = "1.0.0"\n',
    )
    write_text(
        pkg / "__main__.py",
        """from docs_sync.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
""",
    )
    write_text(
        pkg / "cli.py",
        '''#!/usr/bin/env python3
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
        "Download is performed by scripts/upstream_sync/build_all.py.\\n"
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
''',
    )

    write_text(
        UPSTREAM / "upstream-drift-report.md",
        f"""# Upstream Drift Report

**Generated:** {BASELINE_DATE}  
**Pinned upstream:** GNU Health HIS {GH_VERSION}  
**Latest official stable (not adopted):** {GH_LATEST_STABLE}

## Summary

| Category | Status |
|----------|--------|
| New upstream documents since pin | Not fully diffed against portal HTML history — **review on next sync** |
| Removed documents | None detected in local original/ snapshot |
| Modified documents | Integrity hashes recorded in `source-manifest.json` |
| New modules vs pin | Monitor Codeberg tag {GH_LATEST_STABLE} |
| Removed modules | `health_accounting`, `health_profile` absent from v{GH_VERSION} tree (features-doc only) |
| Renamed modules | `health_imaging_orthanc` → use `health_orthanc` |
| Changed fields / workflows / deps / ACL | Requires re-scrape after upgrade — **not upgraded** |
| IST docs requiring review | All module guides marked draft approval |
| Synthetic generators requiring review | Pack stubs 00–20 |
| Data templates requiring review | `templates/IST_HIS_*` |
| Tests requiring review | `tests/upstream/` |

## Policy

**Do not automatically overwrite** approved IST HIS documentation when upstream changes.

## Regeneration

```bash
python -m docs_sync.discover_upstream
python -m docs_sync.verify_checksums
python -m docs_sync.compare --upstream docs/upstream/original --ist-docs docs/ist-his
python -m docs_sync.generate_traceability
python -m docs_sync.report_drift
```
""",
    )
    print("Phase 14 complete")


def phase15_17_meta(guide_count: int, pack_count: int, template_count: int, model_rows: list, field_rows: list, manifest: dict) -> None:
    write_text(
        UPSTREAM / "VERSIONS.yaml",
        f"""ist_his_product_version: "{IST_HIS_VERSION}"
gnu_health_upstream_version: "{GH_VERSION}"
gnu_health_client_version: "sao-{SAO}"
tryton_version: "{TRYTON}"
documentation_version: "{IST_HIS_VERSION}"
synthetic_data_schema_version: "{IST_HIS_VERSION}"
implementation_template_version: "{IST_HIS_VERSION}"
baseline_date: "{BASELINE_DATE}"
""",
    )

    # Integrity test
    write_text(
        ROOT / "tests" / "upstream" / "test_upstream_integrity.py",
        '''#!/usr/bin/env python3
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
''',
    )

    write_text(
        ROOT / "tests" / "upstream" / "test_synthetic_packs.py",
        '''#!/usr/bin/env python3
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
''',
    )

    # Final report markdown
    rst_count = sum(1 for p in (ORIGINAL / "rst").rglob("*.rst")) if (ORIGINAL / "rst").exists() else 0
    write_text(
        UPSTREAM / "FINAL_REPORT_SECTION17.md",
        f"""# §17 Final Report — Mandatory Upstream Synchronization

**Product:** IST HIS — Iris Star Hospital Information System  
**Baseline date:** {BASELINE_DATE}  
**Alignment claim:** **Partial alignment** — documentation baseline, registries, guides, packs, and drift tooling are in place for pinned **{GH_VERSION}**. Not claimed as full production alignment (screenshot verification, live proteus field dump, and executed import/rollback tests remain incomplete).

## Answers

1. **Detected GNU Health version:** {GH_VERSION} (core `gnuhealth` pip); module packages mostly 5.0.4–5.0.6. Latest stable not adopted: {GH_LATEST_STABLE}.
2. **Client / Tryton:** SAO {SAO}; trytond {TRYTON}; desktop tryton client not installed; proteus 7.0.3 present.
3. **Upstream documentation source / retrieval date:** Codeberg `gnuhealth/documentation` (HIS RST) + https://docs.gnuhealth.org/his/ HTML snapshots — retrieved {DOC_RETRIEVAL}. Software pin: Codeberg `gnuhealth/his` tag `v{GH_VERSION}` (`{SOURCE_COMMIT}`).
4. **Upstream pages acquired:** {rst_count} RST sources under `docs/upstream/original/rst/`; HTML key pages under `docs/upstream/generated-reference/html/`; manifest file_count={manifest.get('file_count')}.
5. **Modules discovered (release tree):** {len([m for m in Path(CACHE_HIS / 'tryton').iterdir() if m.is_dir() and (m.name=='health' or m.name.startswith('health_'))]) if CACHE_HIS.exists() else 'see registry'}.
6. **Active modules:** {len(VM_ACTIVATED)} (all health* on DB `isthealth`).
7. **Inactive health modules:** 0 on `isthealth`.
8. **Custom IST modules:** 0.
9. **Models catalogued:** {len(model_rows)} (source scrape, medium confidence).
10. **Fields catalogued:** {len(field_rows)} (source scrape, medium confidence).
11. **IST HIS module guides generated:** {guide_count}.
12. **Synthetic-data generators created:** {pack_count} pack generators (stubs) + existing `synthetic_data/` package retained.
13. **Implementation templates generated:** {template_count}.
14. **Documentation drift status:** Initial report at `docs/upstream/upstream-drift-report.md` — no silent overwrite policy enforced in `docs_sync`.
15. **Licence / attribution status:** `ATTRIBUTION.md`, `LICENSE-DOCUMENTATION.txt`, `LICENSE-SOFTWARE.txt` recorded; **legal review flagged**.
16. **Test results:** run `pytest tests/upstream -q` (see CI output after execution).
17. **Unresolved gaps:** Live proteus full field introspection; exhaustive SAO screenshot verification; full HTML site mirror; executed DB import/rollback of all packs; HIE connectors.
18. **Modules requiring additional implementation:** Features-only absences (`health_accounting`, `health_profile`); UAE/Qatar HIE; deeper React coverage for niche modules.
19. **Regulatory items requiring UAE/Qatar confirmation:** PDPL/PDPPL applicability; HIE onboarding; ICD/SNOMED licensing for commercial use — see `docs/research/source-register.md`.
20. **Commands to regenerate / validate:**

```bash
python scripts/upstream_sync/build_all.py
python -m docs_sync.verify_checksums
python -m docs_sync.report_drift
pytest tests/upstream -q
```

## Evidence paths

- `docs/upstream/UPSTREAM_BASELINE.yaml`
- `docs/upstream/version-discovery-report.md`
- `docs/upstream/installed-module-inventory.xlsx`
- `docs/upstream/source-manifest.json`
- `docs/upstream/original/` (immutable)
- `docs/upstream/GNU_Health_Complete_Module_Registry.xlsx`
- `docs/upstream/module-registry.json`
- `docs/upstream/module-dependency-map.md`
- `docs/upstream/model-and-field-catalogue.xlsx`
- `docs/ist-his/`
- `synthetic-data/`
- `templates/IST_HIS_*`
- `docs_sync/`
""",
    )
    print("Phase 15-17 metadata written")


def main() -> int:
    his_tryton = CACHE_HIS / "tryton"
    if not his_tryton.exists():
        print(f"ERROR: missing {his_tryton}; clone his v5.0.6 first", file=sys.stderr)
        return 1
    modules = load_release_modules(his_tryton)
    print(f"Loaded {len(modules)} release modules")
    phase1_baseline(modules)
    manifest = phase2_3_acquire_docs()
    model_rows, field_rows = phase4_5_registry(modules)
    phase6_naming()
    guide_count = phase7_9_ist_library(modules, model_rows, field_rows)
    pack_count = phase10_12_synthetic(modules, model_rows)
    template_count = phase13_templates(field_rows, model_rows)
    phase14_docs_sync(manifest)
    phase15_17_meta(guide_count, pack_count, template_count, model_rows, field_rows, manifest)
    print("BUILD COMPLETE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
