"""Canonical GNU Health HIS module catalogue helpers for IST HIS upstream sync."""

from __future__ import annotations

import configparser
import re
from pathlib import Path
from typing import Any

# Features-page modules that may be absent / renamed in a given release
FEATURES_EXTRA = {
    "health_accounting": {
        "display_name": "Health Accounting",
        "description": "Financial accounting / billing (features catalogue). May map to Tryton account_* + health_services.",
        "status_note": "Listed in docs features; not a separate tryton package in HIS 5.0.6 source tree.",
    },
    "health_profile": {
        "display_name": "Health Profile",
        "description": "Metapackage bundling common clinical modules.",
        "status_note": "Listed in docs features; not present as tryton package in HIS 5.0.6 source tree.",
    },
    "health_imaging_orthanc": {
        "display_name": "Imaging Orthanc (alias)",
        "description": "Features alias for Orthanc imaging integration.",
        "status_note": "Use health_orthanc in HIS 5.0.6.",
    },
}

BRIEF_SECTION5 = [
    "health",
    "health_accounting",
    "health_archives",
    "health_caldav",
    "health_calendar",
    "health_contact_tracing",
    "health_crypto",
    "health_crypto_lab",
    "health_dentistry",
    "health_disability",
    "health_ems",
    "health_federation",
    "health_genetics",
    "health_genetics_uniprot",
    "health_gyneco",
    "health_history",
    "health_icd9procs",
    "health_icd10",
    "health_icd11",
    "health_icd10pcs",
    "health_icpm",
    "health_icu",
    "health_imaging",
    "health_imaging_worklist",
    "health_imaging_orthanc",
    "health_inpatient",
    "health_inpatient_calendar",
    "health_insurance",
    "health_iss",
    "health_lab",
    "health_lifestyle",
    "health_mdg6",
    "health_ntd",
    "health_ntd_chagas",
    "health_ntd_dengue",
    "health_nursing",
    "health_ophthalmology",
    "health_orthanc",
    "health_pediatrics",
    "health_pediatrics_growth_charts",
    "health_pediatrics_growth_charts_who",
    "health_qrcodes",
    "health_reporting",
    "health_services",
    "health_services_imaging",
    "health_services_lab",
    "health_stock",
    "health_stock_surgery",
    "health_surgery",
    "health_surgery_protocols",
    "health_webdav3_server",
    "health_who_essential_medicines",
]

# Live ir.module state from VM gnuhealth-his-01 / isthealth (2026-07-14)
VM_ACTIVATED = [
    "health",
    "health_archives",
    "health_caldav",
    "health_calendar",
    "health_contact_tracing",
    "health_crypto",
    "health_crypto_lab",
    "health_dentistry",
    "health_disability",
    "health_ems",
    "health_federation",
    "health_genetics",
    "health_genetics_uniprot",
    "health_gyneco",
    "health_history",
    "health_icd10",
    "health_icd10pcs",
    "health_icd11",
    "health_icd9procs",
    "health_icpm",
    "health_icu",
    "health_imaging",
    "health_imaging_worklist",
    "health_inpatient",
    "health_inpatient_calendar",
    "health_insurance",
    "health_iss",
    "health_lab",
    "health_lifestyle",
    "health_mdg6",
    "health_ntd",
    "health_ntd_chagas",
    "health_ntd_dengue",
    "health_nursing",
    "health_ophthalmology",
    "health_orthanc",
    "health_pediatrics",
    "health_pediatrics_growth_charts",
    "health_pediatrics_growth_charts_who",
    "health_qrcodes",
    "health_reporting",
    "health_services",
    "health_services_imaging",
    "health_services_lab",
    "health_socioeconomics",
    "health_stock",
    "health_stock_inpatient",
    "health_stock_nursing",
    "health_stock_surgery",
    "health_surgery",
    "health_surgery_protocols",
    "health_webdav3_server",
    "health_who_essential_medicines",
]

PIP_VERSIONS = {
    "health": "5.0.6",
    "health_archives": "5.0.4",
    "health_caldav": "5.0.4",
    "health_calendar": "5.0.5",
    "health_contact_tracing": "5.0.4",
    "health_crypto": "5.0.4",
    "health_crypto_lab": "5.0.4",
    "health_dentistry": "5.0.6",
    "health_disability": "5.0.4",
    "health_ems": "5.0.4",
    "health_federation": "5.0.4",
    "health_genetics": "5.0.4",
    "health_genetics_uniprot": "5.0.4",
    "health_gyneco": "5.0.4",
    "health_history": "5.0.4",
    "health_icd10": "5.0.4",
    "health_icd10pcs": "5.0.3",
    "health_icd11": "5.0.4",
    "health_icd9procs": "5.0.4",
    "health_icpm": "5.0.4",
    "health_icu": "5.0.4",
    "health_imaging": "5.0.4",
    "health_imaging_worklist": "5.0.4",
    "health_inpatient": "5.0.4",
    "health_inpatient_calendar": "5.0.4",
    "health_insurance": "5.0.4",
    "health_iss": "5.0.4",
    "health_lab": "5.0.4",
    "health_lifestyle": "5.0.4",
    "health_mdg6": "5.0.4",
    "health_ntd": "5.0.3",
    "health_ntd_chagas": "5.0.4",
    "health_ntd_dengue": "5.0.4",
    "health_nursing": "5.0.4",
    "health_ophthalmology": "5.0.4",
    "health_orthanc": "5.0.4",
    "health_pediatrics": "5.0.4",
    "health_pediatrics_growth_charts": "5.0.4",
    "health_pediatrics_growth_charts_who": "5.0.4",
    "health_qrcodes": "5.0.4",
    "health_reporting": "5.0.4",
    "health_services": "5.0.4",
    "health_services_imaging": "5.0.4",
    "health_services_lab": "5.0.4",
    "health_socioeconomics": "5.0.4",
    "health_stock": "5.0.4",
    "health_stock_inpatient": "5.0.4",
    "health_stock_nursing": "5.0.4",
    "health_stock_surgery": "5.0.4",
    "health_surgery": "5.0.4",
    "health_surgery_protocols": "5.0.4",
    "health_webdav3_server": "5.0.4",
    "health_who_essential_medicines": "5.0.4",
}

DISPLAY_NAMES = {
    "health": "Core HIS",
    "health_accounting": "Health Accounting",
    "health_archives": "Archives",
    "health_caldav": "CalDAV",
    "health_calendar": "Calendar",
    "health_contact_tracing": "Contact Tracing",
    "health_crypto": "Crypto",
    "health_crypto_lab": "Crypto Laboratory",
    "health_dentistry": "Dentistry",
    "health_disability": "Disability / ICF",
    "health_ems": "EMS / Ambulance",
    "health_federation": "Federation",
    "health_genetics": "Genetics",
    "health_genetics_uniprot": "Genetics UniProt",
    "health_gyneco": "Gynecology & Obstetrics",
    "health_history": "Enhanced History",
    "health_icd9procs": "ICD-9 Procedures",
    "health_icd10": "ICD-10",
    "health_icd11": "ICD-11",
    "health_icd10pcs": "ICD-10-PCS",
    "health_icpm": "ICPM",
    "health_icu": "ICU",
    "health_imaging": "Medical Imaging",
    "health_imaging_worklist": "Imaging Worklist",
    "health_imaging_orthanc": "Imaging Orthanc (alias)",
    "health_inpatient": "Inpatient",
    "health_inpatient_calendar": "Inpatient Calendar",
    "health_insurance": "Insurance",
    "health_iss": "Injury Surveillance",
    "health_lab": "Laboratory",
    "health_lifestyle": "Lifestyle",
    "health_mdg6": "MDG6",
    "health_ntd": "NTD Metapackage",
    "health_ntd_chagas": "NTD Chagas",
    "health_ntd_dengue": "NTD Dengue",
    "health_nursing": "Nursing",
    "health_ophthalmology": "Ophthalmology",
    "health_orthanc": "Orthanc PACS",
    "health_pediatrics": "Pediatrics",
    "health_pediatrics_growth_charts": "Growth Charts",
    "health_pediatrics_growth_charts_who": "WHO Growth Charts",
    "health_profile": "Health Profile",
    "health_qrcodes": "QR Codes",
    "health_reporting": "Reporting",
    "health_services": "Services & Billing",
    "health_services_imaging": "Imaging Services",
    "health_services_lab": "Lab Services",
    "health_socioeconomics": "Socioeconomics",
    "health_stock": "Health Stock",
    "health_stock_inpatient": "Stock Inpatient",
    "health_stock_nursing": "Stock Nursing",
    "health_stock_surgery": "Stock Surgery",
    "health_surgery": "Surgery",
    "health_surgery_protocols": "Surgery Protocols",
    "health_webdav3_server": "WebDAV3 Server",
    "health_who_essential_medicines": "WHO Essential Medicines",
}


def parse_tryton_cfg(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    # tryton.cfg is INI-like but may have list values without =
    cp = configparser.ConfigParser(allow_no_value=True)
    cp.read_string(text)
    version = cp.get("tryton", "version", fallback="")
    depends_raw = ""
    if cp.has_option("tryton", "depends"):
        depends_raw = cp.get("tryton", "depends")
    # Multi-line depends are often listed as keys under [tryton] after depends:
    depends: list[str] = []
    in_depends = False
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("depends:"):
            in_depends = True
            rest = s[len("depends:") :].strip()
            if rest:
                depends.append(rest)
            continue
        if in_depends:
            if not s or s.endswith(":") or s.startswith("["):
                in_depends = False
            elif s and not s.startswith("#"):
                depends.append(s.rstrip(","))
            else:
                in_depends = False
    xml_files: list[str] = []
    in_xml = False
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("xml:"):
            in_xml = True
            continue
        if in_xml:
            if not s or s.endswith(":") or s.startswith("["):
                in_xml = False
            elif s and not s.startswith("#"):
                xml_files.append(s)
    return {"version": version, "depends": depends, "xml": xml_files}


def scrape_models(module_dir: Path) -> list[str]:
    models: set[str] = set()
    pattern = re.compile(r"""__name__\s*=\s*['\"]([^'\"]+)['\"]""")
    for py in module_dir.rglob("*.py"):
        try:
            text = py.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for m in pattern.findall(text):
            if "." in m:
                models.add(m)
    return sorted(models)


def scrape_fields(module_dir: Path) -> list[dict[str, str]]:
    """Best-effort field catalogue from Python Model definitions."""
    fields: list[dict[str, str]] = []
    model_re = re.compile(r"""__name__\s*=\s*['\"]([^'\"]+)['\"]""")
    field_re = re.compile(
        r"""(\w+)\s*=\s*fields\.(\w+)\s*\(\s*['\"]([^'\"]*)['\"]""",
        re.MULTILINE,
    )
    for py in module_dir.rglob("*.py"):
        try:
            text = py.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        current_model = ""
        for line in text.splitlines():
            mm = model_re.search(line)
            if mm:
                current_model = mm.group(1)
            for fm in field_re.finditer(line):
                if not current_model:
                    continue
                fields.append(
                    {
                        "model": current_model,
                        "field": fm.group(1),
                        "type": fm.group(2),
                        "string": fm.group(3),
                        "source_file": str(py.name),
                    }
                )
    return fields


def load_release_modules(his_tryton_root: Path) -> dict[str, dict[str, Any]]:
    modules: dict[str, dict[str, Any]] = {}
    for d in sorted(his_tryton_root.iterdir()):
        if not d.is_dir():
            continue
        name = d.name
        if name != "health" and not name.startswith("health_"):
            continue
        cfg = d / "tryton.cfg"
        meta = parse_tryton_cfg(cfg) if cfg.exists() else {}
        models = scrape_models(d)
        field_rows = scrape_fields(d)
        modules[name] = {
            "technical_name": name,
            "display_name": DISPLAY_NAMES.get(name, name),
            "version": PIP_VERSIONS.get(name) or meta.get("version") or "",
            "tryton_cfg_version": meta.get("version") or "",
            "depends": meta.get("depends") or [],
            "xml_files": meta.get("xml") or [],
            "models": models,
            "fields": field_rows,
            "in_release_source": True,
            "activation_state": "activated" if name in VM_ACTIVATED else "not activated",
            "upstream_or_ist": "upstream",
            "path": str(d),
        }
    return modules
