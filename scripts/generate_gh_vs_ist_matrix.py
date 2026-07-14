#!/usr/bin/env python3
"""Generate GNU Health vs IST HIS exhaustive comparison MD + XLSX."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs" / "upstream" / "module-registry.json"
OUT_MD = ROOT / "docs" / "ist-his" / "GNU_Health_vs_IST_HIS_comparison.md"
OUT_XLSX = ROOT / "docs" / "ist-his" / "GNU_Health_vs_IST_HIS_item_matrix.xlsx"

# IST React coverage per activated health* module (SAO_MIGRATION + menuRoutes + App.tsx)
REACT_COVERAGE: dict[str, tuple[str, str]] = {
    # module: (coverage, notes)
    "health": (
        "Partial",
        "Patients/appointments/staff/evaluations/medications/settings live; deep demographics/family/vaccines/photo SAO-only",
    ),
    "health_archives": ("SAO-only", "Paper archive — no dedicated React route"),
    "health_caldav": ("SAO-only", "CalDAV server — not in React"),
    "health_calendar": ("Partial", "/calendar list; create-appointment wizard SAO-only"),
    "health_contact_tracing": ("SAO-only", "No React route"),
    "health_crypto": ("SAO-only", "Crypto signing UX SAO-only"),
    "health_crypto_lab": ("SAO-only", "Lab crypto SAO-only"),
    "health_dentistry": ("SAO-only", "Odontogram wizards SAO-only"),
    "health_disability": ("SAO-only", "ICF assessments SAO-only"),
    "health_ems": ("SAO-only", "Ambulance / support requests SAO-only"),
    "health_federation": ("SAO-only", "Federation config/queue not wired in React"),
    "health_genetics": ("SAO-only", "Genetics risk UI SAO-only"),
    "health_genetics_uniprot": ("SAO-only", "UniProt data pack — SAO/data only"),
    "health_gyneco": ("SAO-only", "OB/GYN forms SAO-only"),
    "health_history": ("SAO-only", "Enhanced history reports SAO-only"),
    "health_icd10": ("None", "Reference data pack; used via pathology lookups"),
    "health_icd10pcs": ("None", "Reference data pack"),
    "health_icd11": ("None", "Reference data pack"),
    "health_icd9procs": ("None", "Reference data pack"),
    "health_icpm": ("None", "Reference data pack"),
    "health_icu": ("SAO-only", "Apache2/Glasgow/ventilation SAO-only"),
    "health_imaging": (
        "Partial",
        "/imaging list/requests; result generation & complex wizards SAO-only",
    ),
    "health_imaging_worklist": ("SAO-only", "Worklist templates SAO-only"),
    "health_inpatient": (
        "Partial",
        "/beds admissions/beds; bed-transfer & inpatient evaluation wizards SAO-only",
    ),
    "health_inpatient_calendar": ("SAO-only", "Inpatient calendar views SAO-only"),
    "health_insurance": (
        "SAO-only",
        "Plans/policies; patient insurance deep forms SAO-only",
    ),
    "health_iss": ("SAO-only", "Injury surveillance SAO-only"),
    "health_lab": (
        "Partial",
        "/laboratory create request; result entry & create-lab-test wizard SAO-only",
    ),
    "health_lifestyle": ("SAO-only", "Lifestyle/CAGE fields on patient — SAO-only"),
    "health_mdg6": ("None", "MDG6 lab/disease pack — data/SAO"),
    "health_ntd": ("None", "NTD metapackage"),
    "health_ntd_chagas": ("SAO-only", "Chagas survey SAO-only"),
    "health_ntd_dengue": ("SAO-only", "Dengue survey SAO-only"),
    "health_nursing": ("Partial", "/nursing ambulatory + rounding list; deep forms SAO"),
    "health_ophthalmology": ("SAO-only", "Ophthalmology evaluations SAO-only"),
    "health_orthanc": ("SAO-only", "Orthanc sync wizards not wired in React"),
    "health_pediatrics": ("SAO-only", "Newborn/PSC SAO-only"),
    "health_pediatrics_growth_charts": ("SAO-only", "Growth chart hooks SAO-only"),
    "health_pediatrics_growth_charts_who": ("SAO-only", "WHO chart wizards/reports SAO-only"),
    "health_qrcodes": ("SAO-only", "QR reports SAO-only"),
    "health_reporting": ("SAO-only", "Epidemics/top-diseases/summary wizards SAO-only"),
    "health_services": (
        "Partial",
        "Backend + invoice link via /financial stub; service invoice wizard SAO-only",
    ),
    "health_services_imaging": ("SAO-only", "Imaging service invoice linkage SAO-only"),
    "health_services_lab": ("SAO-only", "Lab service invoice linkage SAO-only"),
    "health_socioeconomics": ("SAO-only", "SES assessment SAO-only"),
    "health_stock": (
        "Partial",
        "/stock locations/moves list; Rx/vaccination stock-move wizards SAO-only",
    ),
    "health_stock_inpatient": ("SAO-only", "Rounding supply stock SAO-only"),
    "health_stock_nursing": ("SAO-only", "Ambulatory care stock SAO-only"),
    "health_stock_surgery": ("SAO-only", "Surgery stock-move wizard SAO-only"),
    "health_surgery": (
        "Partial",
        "/procedures surgery/operation list; OR schedule & deep surgery UX SAO-only",
    ),
    "health_surgery_protocols": ("None", "Protocol reference data"),
    "health_webdav3_server": ("SAO-only", "WebDAV shares not in React"),
    "health_who_essential_medicines": ("None", "WHO EM data pack"),
}

# Product-layer comparison rows (Same / Partial / Different)
PRODUCT_ROWS: list[tuple[str, str, str, str]] = [
    # area, what_checked, status, evidence
    (
        "Server core (trytond, health packages)",
        "gnuhealth 5.0.6, trytond 7.0.53, SAO 7.0.53, PG 15.18, Python 3.11.2; pin Codeberg v5.0.6",
        "Same",
        "UPSTREAM_BASELINE.yaml; version-discovery-report.md",
    ),
    (
        "Active health modules (53)",
        "DB isthealth: 53 health* activated, 0 inactive vs stock GH 5.0.6 activation set",
        "Same",
        "FINAL_REPORT_SECTION17.md; module-registry.json",
    ),
    (
        "Custom Tryton / IST modules",
        "ir.module ist*/iris*; repo Tryton modules",
        "Same",
        "0 custom IST Tryton modules; no health* fork",
    ),
    (
        "Database models / tables",
        "gnuhealth.* models (~358 catalogued); schema from activated upstream modules",
        "Same",
        "Unmodified upstream model/table names; medium confidence (source scrape)",
    ),
    (
        "Technical identifiers",
        "Package/module/model/table/XML ID names",
        "Same",
        "Remain GNU Health identifiers per naming policy",
    ),
    (
        "Tryton JSON-RPC API surface",
        "common.authenticate + model.* Session API",
        "Same",
        "React and SAO use same transport",
    ),
    (
        "PostgreSQL-backed Tryton schema",
        "No alternate ORM",
        "Same",
        "UPSTREAM_BASELINE.yaml",
    ),
    (
        "Features-doc-only absences",
        "health_accounting / health_profile not in v5.0.6 tree",
        "Same",
        "Same gap as stock pin (upstream-drift-report.md)",
    ),
    (
        "Upstream software licence",
        "GPL-3.0-or-later on HIS components",
        "Same",
        "ATTRIBUTION.md",
    ),
    (
        "SAO client package installed",
        "sao 7.0.53 available at /sao/",
        "Same",
        "Installed; not primary UX",
    ),
    (
        "Desktop / primary UI client",
        "Stock SAO-as-default vs IST React SPA",
        "Different",
        "Primary UX is React at health.irisstar.tech; SAO secondary",
    ),
    (
        "Login / branding / UI chrome",
        "IST HIS / Iris Star branding, navy/gold, EN/AR RTL",
        "Different",
        "Naming policy §6.1; frontend design system",
    ),
    (
        "Help system",
        "React Help Centre /help, /help/admin, EN/AR workflows",
        "Different",
        "IST-only frontend/help-content/",
    ),
    (
        "Docs (IST HIS library)",
        "docs/ist-his/ adapted vs upstream RST/HTML",
        "Different",
        "IST terminology/UI/UAE–QA; CC-BY-SA attribution",
    ),
    (
        "Synthetic data / templates",
        "Deterministic demo packs, IST markers",
        "Different",
        "ISTHIS-DEMO-* / IST-P-*; not stock GH demo",
    ),
    (
        "UAE / Qatar localization overlays",
        "HIE, tenancy, bilingual ops framework",
        "Different",
        "gap-analysis-uae-qatar.md; no production HIE connectors",
    ),
    (
        "Deployment (GCP nginx)",
        "VM gnuhealth-his-01, nginx React+/api+/sao/",
        "Different",
        "IST ops topology; not stock GH appliance layout",
    ),
    (
        "Product versioning",
        "IST HIS 1.0.0 on upstream HIS 5.0.6",
        "Different",
        "UPSTREAM_BASELINE.yaml ist_his_product_version",
    ),
    (
        "Menus / navigation",
        "React MenuTree + menuRoutes vs SAO ir.ui.menu shell",
        "Partial",
        "Menus from Tryton; unmapped/wizards → SAO panel",
    ),
    (
        "Patient / clinical CRUD",
        "Create/edit patients, appointments, evaluations, staff",
        "Partial",
        "Gap 1 closed for core; deep demographics SAO-only",
    ),
    (
        "Lab / pharmacy / inpatient / surgery UI",
        "Lab, Rx, beds, nursing, procedures, imaging routes",
        "Partial",
        "Live React routes; result/admission/shipment wizards SAO-only",
    ),
    (
        "Financial / accounting UX",
        "React /financial vs SAO CoA/FY/journals/taxes/post-pay",
        "Partial",
        "List + draft invoice stub + SAO panel; deep finance SAO-only",
    ),
    (
        "Auth / session client behavior",
        "Tryton Session header; React localStorage",
        "Partial",
        "Same protocol; MVP token storage differs from SAO UX",
    ),
    (
        "APIs / FHIR / HIE",
        "JSON-RPC present; HL7/FHIR HIE absent",
        "Partial",
        "Same transport; no UAE/QA HIE gateway (G-01…G-04)",
    ),
    (
        "Licensing / commercial attribution",
        "GPL software + CC-BY-SA docs + IST notices",
        "Partial",
        "Legal review REQUIRED before commercial claims",
    ),
    (
        "Admin ops (users/groups/modules/sequences)",
        "Gap 4 React admin subset",
        "Partial",
        "List/edit subset; UI config & record-rules editor SAO-only",
    ),
    (
        "Orthanc / WebDAV / federation admin",
        "Modules activated; React wiring",
        "Partial",
        "Backend same; not wired in React (SAO-only admin)",
    ),
]

CAPABILITY_ROWS: list[tuple[str, str, str]] = [
    # capability, status, evidence
    (
        "Parties",
        "Partial",
        "Backend party.party Same; React /parties list live; deep party forms SAO",
    ),
    (
        "Patients",
        "Partial",
        "gnuhealth.patient Same backend; React create/edit core; demographics/insurance/family/vaccines/photo SAO",
    ),
    (
        "Appointments",
        "Partial",
        "/appointments create/edit; specialty/insurance/product linking SAO",
    ),
    (
        "Patient evaluations",
        "Partial",
        "/evaluations live on gnuhealth.patient.evaluation; full SAO form depth not claimed",
    ),
    (
        "Health professionals / staff",
        "Partial",
        "/staff create/edit; specialty O2M / institution unit SAO",
    ),
    (
        "Laboratory",
        "Partial",
        "/laboratory requests; result entry & create-lab-test wizard SAO",
    ),
    (
        "Imaging",
        "Partial",
        "/imaging requests/results list; generate-result & Orthanc wizards SAO",
    ),
    (
        "Pharmacy / prescriptions",
        "Partial",
        "/pharmacy + /medications; stock-move from Rx wizard SAO",
    ),
    (
        "Inpatient / beds / admissions",
        "Partial",
        "/beds; bed-transfer & inpatient evaluation wizards SAO",
    ),
    (
        "ICU",
        "Different",
        "health_icu activated (backend Same); React coverage None/SAO-only",
    ),
    (
        "Surgery",
        "Partial",
        "/procedures list; OR schedule, protocols UX, stock-move wizard SAO",
    ),
    (
        "Nursing",
        "Partial",
        "/nursing ambulatory + rounding; deep nursing forms / stock SAO",
    ),
    (
        "Insurance",
        "Partial",
        "health_insurance activated; plans/patient insurance deep UI SAO-only",
    ),
    (
        "Stock / inventory",
        "Partial",
        "/stock list; health_stock* move wizards SAO",
    ),
    (
        "Accounting / invoicing",
        "Partial",
        "account_* + health_services backend; React stub; CoA/FY/tax/post-pay SAO",
    ),
    (
        "Reporting (clinical/epidemiology)",
        "Different",
        "health_reporting wizards SAO-only; no React report parity",
    ),
    (
        "Federation",
        "Different",
        "health_federation activated; config/queue not in React; not UAE HIE",
    ),
    (
        "Crypto signing",
        "Different",
        "health_crypto(+_lab) activated; signing UX SAO-only",
    ),
    (
        "Genetics",
        "Different",
        "health_genetics(+_uniprot) activated; SAO-only UI",
    ),
    (
        "Pediatrics / growth charts",
        "Different",
        "Modules activated; React None/SAO-only",
    ),
    (
        "Gynecology & obstetrics",
        "Different",
        "health_gyneco activated; SAO-only",
    ),
    (
        "Dentistry",
        "Different",
        "health_dentistry odontogram wizards SAO-only",
    ),
    (
        "Ophthalmology",
        "Different",
        "health_ophthalmology SAO-only",
    ),
    (
        "EMS / ambulance",
        "Different",
        "health_ems SAO-only",
    ),
    (
        "Disability / ICF",
        "Different",
        "health_disability SAO-only",
    ),
    (
        "Contact tracing / NTD / ISS",
        "Different",
        "Activated packs; SAO-only clinical UI",
    ),
    (
        "ICD / coding packs",
        "Same",
        "ICD-10/11/PCS/9procs/ICPM data same as pin; no IST fork",
    ),
    (
        "WHO essential medicines",
        "Same",
        "Data pack activated; same as upstream pin",
    ),
    (
        "Calendar / CalDAV / WebDAV",
        "Partial",
        "Modules activated; /calendar list; CalDAV/WebDAV admin SAO",
    ),
    (
        "Orthanc PACS",
        "Partial",
        "health_orthanc activated; sync wizards SAO; not wired in React",
    ),
    (
        "QR codes",
        "Different",
        "health_qrcodes reports SAO-only",
    ),
    (
        "Help / documentation product",
        "Different",
        "IST Help Centre + docs/ist-his library — not stock GH help",
    ),
    (
        "UAE/QA HIE (NABIDH/Malaffi/Riayati/Qatar)",
        "Different",
        "Neither GH stock nor IST has production HIE connectors",
    ),
    (
        "Multi-entity UAE↔Qatar isolation",
        "Different",
        "Designed in implementation docs; not fully deployed",
    ),
    (
        "Synthetic demo data",
        "Different",
        "IST factories/markers — not stock GH demo content",
    ),
    (
        "Primary product branding",
        "Different",
        "IST HIS / Iris Star vs GNU Health branding",
    ),
]


def load_activated() -> list[dict]:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    mods = [m for m in data["modules"] if m.get("activation_state") == "activated"]
    mods.sort(key=lambda m: m["technical_module_name"])
    assert len(mods) == 53, f"expected 53 activated, got {len(mods)}"
    return mods


def md_escape(s: str) -> str:
    return s.replace("|", "\\|")


def build_markdown(activated: list[dict]) -> str:
    same = [r for r in PRODUCT_ROWS if r[2] == "Same"]
    partial = [r for r in PRODUCT_ROWS if r[2] == "Partial"]
    different = [r for r in PRODUCT_ROWS if r[2] == "Different"]

    cap_same = [r for r in CAPABILITY_ROWS if r[1] == "Same"]
    cap_partial = [r for r in CAPABILITY_ROWS if r[1] == "Partial"]
    cap_diff = [r for r in CAPABILITY_ROWS if r[1] == "Different"]

    lines: list[str] = []
    a = lines.append

    a("---")
    a("title: GNU Health vs IST HIS — Complete Item-by-Item Comparison")
    a("ist_his_version: 1.0.0")
    a("upstream_product: GNU Health HIS")
    a("upstream_version: 5.0.6")
    a("tryton_version: 7.0.53")
    a("baseline_date: 2026-07-14")
    a("production: https://health.irisstar.tech")
    a("licence: CC-BY-SA-4.0")
    a("legal_review: REQUIRED")
    a("companion_xlsx: docs/ist-his/GNU_Health_vs_IST_HIS_item_matrix.xlsx")
    a("---")
    a("")
    a("# GNU Health vs IST HIS — Complete Item-by-Item Comparison")
    a("")
    a("## A. Verdict")
    a("")
    a("**NOT exactly the same** for the product experience.")
    a("")
    a(
        "IST HIS is a **customized / localized presentation and operations layer** on a "
        "**GNU Health HIS 5.0.6** backend (Tryton **7.0.53**). Backend modules, models, and "
        "technical identifiers can be **Same** while the customer-facing product is **not** — "
        "because the primary UI is the IST React SPA (EN/AR), not stock SAO."
    )
    a("")
    a("| Layer | Sameness |")
    a("|-------|----------|")
    a("| Backend HIS packages / 53 activated modules / models | **Same** as pin (0 custom modules) |")
    a("| Product experience (UI, help, docs, branding, deploy) | **Not the same** |")
    a("| Claim “functionally equivalent for X” | Only with an explicit X scope + SAO fallback |")
    a("")
    a(
        f"**Counts in this document:** product-layer rows — Same **{len(same)}**, "
        f"Partial **{len(partial)}**, Different **{len(different)}** "
        f"(total **{len(PRODUCT_ROWS)}**). Capability rows — Same **{len(cap_same)}**, "
        f"Partial **{len(cap_partial)}**, Different **{len(cap_diff)}** "
        f"(total **{len(CAPABILITY_ROWS)}**). Module matrix — **53** activated modules."
    )
    a("")
    a("Evidence baseline: `docs/upstream/UPSTREAM_BASELINE.yaml`, `module-registry.json`, "
      "`FINAL_REPORT_SECTION17.md`, `frontend/docs/SAO_MIGRATION.md`, "
      "`docs/research/gap-analysis-uae-qatar.md`, `IST_HIS_Naming_and_Branding_Policy.md`.")
    a("")
    a("| Status | Meaning |")
    a("|--------|---------|")
    a("| **Same** | Verified equivalent to stock GNU Health 5.0.6 / Tryton 7.0.53 for this area |")
    a("| **Different** | Material IST-specific change, addition, or missing React/product parity |")
    a("| **Partial** | Shared backend / subset parity; presentation or depth differs |")
    a("")
    a("---")
    a("")
    a("## B. Complete SAME items")
    a("")
    a("Everything verified **Same** as stock GNU Health HIS 5.0.6 / Tryton 7.0.53 on the server:")
    a("")
    for i, (area, what, _st, evidence) in enumerate(same, 1):
        a(f"{i}. **{area}** — {what}. Evidence: {evidence}.")
    a("")
    a("### B.1 Activated module names (all 53 — Same backend)")
    a("")
    a("Technical names remain GNU Health identifiers. All are `upstream`, `installed`, `activated`:")
    a("")
    a("| # | Module | Display name | Upstream version |")
    a("|---|--------|--------------|------------------|")
    for i, m in enumerate(activated, 1):
        a(
            f"| {i} | `{m['technical_module_name']}` | {md_escape(m['display_name'])} | "
            f"{m.get('version') or '—'} |"
        )
    a("")
    a("### B.2 Also Same (technical)")
    a("")
    a("- Pin: Codeberg `v5.0.6` commit `f50972fee0d4e001133a09af8d9ea7dbfe67f7a8` "
      "(latest stable **5.0.7 not adopted**).")
    a("- Stack: `gnuhealth` **5.0.6**, trytond **7.0.53**, SAO **7.0.53**, PostgreSQL **15.18**, "
      "Python **3.11.2**, gnuhealth-control **5.0.3**.")
    a("- DB: `isthealth` — 53 `health*` activated, **0** custom `ist*`/`iris*` Tryton modules.")
    a("- Models approach: stock `gnuhealth.*` / Tryton models; no IST schema fork.")
    a("- Features-doc-only absences shared with pin: `health_accounting`, `health_profile` "
      "(and alias `health_imaging_orthanc`) — not IST removals.")
    a("")
    a("---")
    a("")
    a("## C. Complete DIFFERENT / PARTIAL items")
    a("")
    a("### C.1 DIFFERENT (product / ops layer)")
    a("")
    a("| Area | What differs | Evidence |")
    a("|------|--------------|----------|")
    for area, what, _st, evidence in different:
        a(f"| **{md_escape(area)}** | {md_escape(what)} | {md_escape(evidence)} |")
    a("")
    a("### C.2 PARTIAL (shared backend; UI/depth differs)")
    a("")
    a("| Area | What was checked | Evidence |")
    a("|------|------------------|----------|")
    for area, what, _st, evidence in partial:
        a(f"| **{md_escape(area)}** | {md_escape(what)} | {md_escape(evidence)} |")
    a("")
    a("### C.3 Wizard / clinical-area gaps (React vs SAO)")
    a("")
    a("| Clinical / admin area | React today | Still SAO-only |")
    a("|-----------------------|-------------|----------------|")
    a("| Patients | Create/edit core party + patient | Full demographics, insurance, family, diseases, vaccinations, photo |")
    a("| Appointments | Create/edit | Specialty / insurance / consultation product linking |")
    a("| Staff | Create/edit | Main specialty O2M, institution unit |")
    a("| Laboratory | Create lab request | Result entry; create-lab-test wizard |")
    a("| Imaging | List / requests | Generate result; Orthanc sync |")
    a("| Surgery / procedures | List | OR schedule, deep surgery, stock-move wizard |")
    a("| Admissions / inpatient | Beds / registrations list | Bed-transfer, inpatient evaluation wizards |")
    a("| Pharmacy / stock | Rx list; stock locations/moves | Prescription/vaccination/surgery stock-move wizards |")
    a("| Financial | Invoice list + draft stub + SAO panel | CoA template, journals, FY, taxes, post/pay/cancel |")
    a("| Reporting | — | Epidemics, top diseases, summary, evaluations reports |")
    a("| Specialty packs (ICU, dent, gyneco, ophto, EMS, genetics, NTD, …) | — | Full SAO forms/wizards |")
    a("| Federation / WebDAV / Orthanc admin | — | Config + sync wizards |")
    a("| UI config / record rules | — | Menus, views, actions, icons, record-rules editor |")
    a("| Module upgrades | Mark activate when API allows | `trytond-admin` / SAO pending upgrades |")
    a("")
    a("---")
    a("")
    a("## D. Module-by-module matrix (all 53 activated)")
    a("")
    a("Columns: Module | Upstream version | Activated | IST React coverage | Same backend? | Notes")
    a("")
    a("| Module | Upstream version | Activated | IST React coverage | Same backend? | Notes |")
    a("|--------|------------------|-----------|--------------------|---------------|-------|")
    for m in activated:
        name = m["technical_module_name"]
        cov, notes = REACT_COVERAGE.get(name, ("SAO-only", "See SAO_MIGRATION.md"))
        a(
            f"| `{name}` | {m.get('version') or '—'} | Yes | {cov} | Yes | {md_escape(notes)} |"
        )
    a("")
    a("### D.1 Registry entries not in the 53 (features-doc-only / absent)")
    a("")
    a("| Module | State | Notes |")
    a("|--------|-------|-------|")
    a("| `health_accounting` | absent_from_release | Features catalogue only; use Tryton `account_*` + `health_services` |")
    a("| `health_profile` | absent_from_release | Features metapackage; not in HIS 5.0.6 tree |")
    a("| `health_imaging_orthanc` | absent_from_release | Alias; use `health_orthanc` |")
    a("")
    a("React coverage legend: **Full** = React parity for primary workflows; **Partial** = "
      "dedicated React route with CRUD/list but wizards/deep forms SAO; **None** = data pack "
      "only (no UI expected); **SAO-only** = module UI only via SAO / Open-in-SAO.")
    a("")
    a("---")
    a("")
    a("## E. Capability matrix")
    a("")
    a("| Capability | Status | Evidence |")
    a("|------------|--------|----------|")
    for cap, status, evidence in CAPABILITY_ROWS:
        a(f"| **{md_escape(cap)}** | **{status}** | {md_escape(evidence)} |")
    a("")
    a("---")
    a("")
    a('## F. "Getting item-by-item same" — honesty')
    a("")
    a("### What is already item-by-item same")
    a("")
    a("- **Backend:** 0 custom Tryton modules; 53 activated `health*` packages match the "
      "v5.0.6 pin; models/tables/XML IDs are GNU Health.")
    a("- **API:** Same Tryton JSON-RPC Session surface.")
    a("- **Optional stock client:** SAO 7.0.53 is installed — using SAO as the daily client "
      "gives the **same client experience as stock GNU Health** (modulo IST branding on the "
      "React homepage and nginx layout).")
    a("")
    a("### What full product item-by-item sameness would require")
    a("")
    a("Full **product** sameness (customer claim: “exactly the same as GNU Health”) means one of:")
    a("")
    a("1. **Use SAO as primary UI** — product experience ≈ stock GNU Health web client. "
      "Backend already matches. Cost: abandon or demote React as primary; accept SAO UX.")
    a("2. **Implement full React parity** for every SAO form/wizard/report across all 53 "
      "modules (and Tryton account/stock/admin wizards) — a **large multi-sprint program**, "
      "not a docs claim. Today many specialty packs are SAO-only.")
    a("")
    a("Neither path is automatic. Backend sameness ≠ product sameness.")
    a("")
    a('### Credible “functionally equivalent for X” claims')
    a("")
    a("| Claim scope X | Credible today? | Condition |")
    a("|---------------|-----------------|-----------|")
    a("| Backend HIS 5.0.6 modules/models | **Yes** | Cite this matrix + module dump |")
    a("| Ambulatory MVP (patients, appointments, staff, lab request, Rx list) via React | **Partial / Yes with caveats** | Document SAO for deep fields/wizards |")
    a("| Full SAO clinical depth (ICU, surgery wizards, reporting, Orthanc, …) | **Yes via SAO** | Train users on `/sao/`; do not imply React-only |")
    a("| Finance (CoA, FY, post/pay) | **Via SAO only** | React `/financial` is stub |")
    a("| UAE/QA HIE / e-claim | **No** | Neither stock GH nor IST has connectors |")
    a("| “Exactly the same product as GNU Health” | **No** | Branding, React UI, help, docs, deploy differ |")
    a("")
    a("### Work remaining for stronger equivalence claims")
    a("")
    a("- Decide primary UI strategy: **SAO-first** (fastest “same as GH”) vs **React parity program**.")
    a("- If React: prioritize wizard parity per clinical area (lab results, admission, surgery, "
      "finance post/pay, imaging generate-result).")
    a("- Do not claim HIE/e-claim equivalence without new integration work.")
    a("- Legal review before commercial “equivalent to GNU Health” wording.")
    a("")
    a("---")
    a("")
    a("## G. Companion Excel")
    a("")
    a("Filterable workbook: [`GNU_Health_vs_IST_HIS_item_matrix.xlsx`](GNU_Health_vs_IST_HIS_item_matrix.xlsx)")
    a("")
    a("Sheets: `Product_Layer`, `Modules_53`, `Capabilities`, `Summary_Counts`.")
    a("")
    a("---")
    a("")
    a("## Explicit naming statement")
    a("")
    a("| Layer | Name |")
    a("|-------|------|")
    a("| Customer-facing product | **IST HIS** — Iris Star Hospital Information System |")
    a("| Upstream product | **GNU Health HIS** 5.0.6 |")
    a("| Framework | **Tryton** 7.0.53 |")
    a("| Technical modules / models / tables | Remain **GNU Health** names — do not globally rename |")
    a("")
    a("---")
    a("")
    a("## Confidence notes")
    a("")
    a("| Claim | Confidence |")
    a("|-------|------------|")
    a("| Server versions & 53 activated modules | **High** |")
    a("| Zero custom IST Tryton modules | **High** |")
    a("| Models unmodified vs upstream source pin | **Medium–High** |")
    a("| React vs SAO feature matrix | **High** for documented routes; every-wizard exhaustive check **not** claimed |")
    a("| FHIR / HIE | **High** that neither path provides UAE/QA HIE today |")
    a("")
    a("---")
    a("")
    a("## Sources")
    a("")
    a("- `docs/upstream/UPSTREAM_BASELINE.yaml`")
    a("- `docs/upstream/VERSIONS.yaml`")
    a("- `docs/upstream/version-discovery-report.md`")
    a("- `docs/upstream/FINAL_REPORT_SECTION17.md`")
    a("- `docs/upstream/upstream-drift-report.md`")
    a("- `docs/upstream/module-registry.json`")
    a("- `docs/upstream/module-dependency-map.md`")
    a("- `docs/upstream/ATTRIBUTION.md`")
    a("- `docs/ist-his/IST_HIS_Naming_and_Branding_Policy.md`")
    a("- `docs/research/current-system-discovery.md`")
    a("- `docs/research/gap-analysis-uae-qatar.md`")
    a("- `frontend/docs/SAO_MIGRATION.md`")
    a("- `frontend/docs/ARCHITECTURE.md`")
    a("- `frontend/src/lib/tryton/menuRoutes.ts`")
    a("- `frontend/src/App.tsx`")
    a("")
    a("---")
    a("")
    a(
        f"*Comparison compiled 2026-07-14. Product-layer: Same {len(same)} / "
        f"Partial {len(partial)} / Different {len(different)}. "
        f"Capabilities: Same {len(cap_same)} / Partial {len(cap_partial)} / "
        f"Different {len(cap_diff)}. Modules: 53 activated. "
        "Do not claim “exactly the same” without re-verifying against a fresh VM module dump "
        "and UI checklist.*"
    )
    a("")

    return "\n".join(lines)


def build_xlsx(activated: list[dict]) -> None:
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font
        from openpyxl.utils import get_column_letter
    except ImportError:
        # Minimal XLSX via zip/xml without openpyxl
        write_minimal_xlsx(activated)
        return

    wb = Workbook()

    # Summary
    ws0 = wb.active
    ws0.title = "Summary_Counts"
    same_p = sum(1 for r in PRODUCT_ROWS if r[2] == "Same")
    part_p = sum(1 for r in PRODUCT_ROWS if r[2] == "Partial")
    diff_p = sum(1 for r in PRODUCT_ROWS if r[2] == "Different")
    same_c = sum(1 for r in CAPABILITY_ROWS if r[1] == "Same")
    part_c = sum(1 for r in CAPABILITY_ROWS if r[1] == "Partial")
    diff_c = sum(1 for r in CAPABILITY_ROWS if r[1] == "Different")
    cov_counts: dict[str, int] = {}
    for m in activated:
        cov = REACT_COVERAGE.get(m["technical_module_name"], ("SAO-only", ""))[0]
        cov_counts[cov] = cov_counts.get(cov, 0) + 1

    ws0.append(["Metric", "Value"])
    ws0.append(["Verdict", "NOT exactly the same (product experience)"])
    ws0.append(["Upstream", "GNU Health HIS 5.0.6 / Tryton 7.0.53"])
    ws0.append(["IST HIS product", "1.0.0"])
    ws0.append(["Product_Layer Same", same_p])
    ws0.append(["Product_Layer Partial", part_p])
    ws0.append(["Product_Layer Different", diff_p])
    ws0.append(["Product_Layer Total", len(PRODUCT_ROWS)])
    ws0.append(["Capability Same", same_c])
    ws0.append(["Capability Partial", part_c])
    ws0.append(["Capability Different", diff_c])
    ws0.append(["Capability Total", len(CAPABILITY_ROWS)])
    ws0.append(["Modules activated", 53])
    for k, v in sorted(cov_counts.items()):
        ws0.append([f"React coverage {k}", v])
    ws0.append(["Custom IST Tryton modules", 0])
    for cell in ws0[1]:
        cell.font = Font(bold=True)

    # Product layer
    ws1 = wb.create_sheet("Product_Layer")
    ws1.append(["Area", "What_checked", "Status", "Evidence"])
    for row in PRODUCT_ROWS:
        ws1.append(list(row))
    for cell in ws1[1]:
        cell.font = Font(bold=True)

    # Modules
    ws2 = wb.create_sheet("Modules_53")
    ws2.append(
        [
            "Module",
            "Display_name",
            "Upstream_version",
            "Activated",
            "IST_React_coverage",
            "Same_backend",
            "Notes",
        ]
    )
    for m in activated:
        name = m["technical_module_name"]
        cov, notes = REACT_COVERAGE.get(name, ("SAO-only", ""))
        ws2.append(
            [
                name,
                m["display_name"],
                m.get("version") or "",
                "Yes",
                cov,
                "Yes",
                notes,
            ]
        )
    for cell in ws2[1]:
        cell.font = Font(bold=True)

    # Capabilities
    ws3 = wb.create_sheet("Capabilities")
    ws3.append(["Capability", "Status", "Evidence"])
    for row in CAPABILITY_ROWS:
        ws3.append(list(row))
    for cell in ws3[1]:
        cell.font = Font(bold=True)

    for ws in (ws0, ws1, ws2, ws3):
        for col in range(1, ws.max_column + 1):
            ws.column_dimensions[get_column_letter(col)].width = 28

    OUT_XLSX.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUT_XLSX)


def write_minimal_xlsx(activated: list[dict]) -> None:
    """Fallback: write CSV companions if openpyxl missing (should not happen)."""
    import csv

    base = OUT_XLSX.with_suffix("")
    with open(str(base) + "_product.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Area", "What_checked", "Status", "Evidence"])
        w.writerows(PRODUCT_ROWS)
    with open(str(base) + "_modules.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "Module",
                "Display_name",
                "Upstream_version",
                "Activated",
                "IST_React_coverage",
                "Same_backend",
                "Notes",
            ]
        )
        for m in activated:
            name = m["technical_module_name"]
            cov, notes = REACT_COVERAGE.get(name, ("SAO-only", ""))
            w.writerow(
                [name, m["display_name"], m.get("version") or "", "Yes", cov, "Yes", notes]
            )
    raise SystemExit(
        "openpyxl not installed — wrote CSV fallbacks; install openpyxl for xlsx"
    )


def main() -> None:
    activated = load_activated()
    # coverage map must cover all activated
    missing = [m["technical_module_name"] for m in activated if m["technical_module_name"] not in REACT_COVERAGE]
    if missing:
        raise SystemExit(f"REACT_COVERAGE missing modules: {missing}")

    md = build_markdown(activated)
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(md, encoding="utf-8")
    print(f"Wrote {OUT_MD}")

    build_xlsx(activated)
    print(f"Wrote {OUT_XLSX}")

    same_p = sum(1 for r in PRODUCT_ROWS if r[2] == "Same")
    part_p = sum(1 for r in PRODUCT_ROWS if r[2] == "Partial")
    diff_p = sum(1 for r in PRODUCT_ROWS if r[2] == "Different")
    same_c = sum(1 for r in CAPABILITY_ROWS if r[1] == "Same")
    part_c = sum(1 for r in CAPABILITY_ROWS if r[1] == "Partial")
    diff_c = sum(1 for r in CAPABILITY_ROWS if r[1] == "Different")
    print(
        f"COUNTS product Same={same_p} Partial={part_p} Different={diff_p} | "
        f"capability Same={same_c} Partial={part_c} Different={diff_c} | modules=53"
    )


if __name__ == "__main__":
    main()
