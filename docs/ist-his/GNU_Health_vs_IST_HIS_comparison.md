---
title: GNU Health vs IST HIS — Complete Item-by-Item Comparison
ist_his_version: 1.0.0
upstream_product: GNU Health HIS
upstream_version: 5.0.6
tryton_version: 7.0.53
baseline_date: 2026-07-14
production: https://health.irisstar.tech
licence: CC-BY-SA-4.0
legal_review: REQUIRED
companion_xlsx: docs/ist-his/GNU_Health_vs_IST_HIS_item_matrix.xlsx
---

# GNU Health vs IST HIS — Complete Item-by-Item Comparison

## A. Verdict

**NOT exactly the same** for the product experience.

IST HIS is a **customized / localized presentation and operations layer** on a **GNU Health HIS 5.0.6** backend (Tryton **7.0.53**). Backend modules, models, and technical identifiers can be **Same** while the customer-facing product is **not** — because the primary UI is the IST React SPA (EN/AR), not stock SAO.

| Layer | Sameness |
|-------|----------|
| Backend HIS packages / 53 activated modules / models | **Same** as pin (0 custom modules) |
| Product experience (UI, help, docs, branding, deploy) | **Not the same** |
| Claim “functionally equivalent for X” | Only with an explicit X scope + SAO fallback |

**Counts in this document:** product-layer rows — Same **10**, Partial **9**, Different **8** (total **27**). Capability rows — Same **2**, Partial **16**, Different **18** (total **36**). Module matrix — **53** activated modules.

Evidence baseline: `docs/upstream/UPSTREAM_BASELINE.yaml`, `module-registry.json`, `FINAL_REPORT_SECTION17.md`, `frontend/docs/SAO_MIGRATION.md`, `docs/research/gap-analysis-uae-qatar.md`, `IST_HIS_Naming_and_Branding_Policy.md`.

| Status | Meaning |
|--------|---------|
| **Same** | Verified equivalent to stock GNU Health 5.0.6 / Tryton 7.0.53 for this area |
| **Different** | Material IST-specific change, addition, or missing React/product parity |
| **Partial** | Shared backend / subset parity; presentation or depth differs |

---

## B. Complete SAME items

Everything verified **Same** as stock GNU Health HIS 5.0.6 / Tryton 7.0.53 on the server:

1. **Server core (trytond, health packages)** — gnuhealth 5.0.6, trytond 7.0.53, SAO 7.0.53, PG 15.18, Python 3.11.2; pin Codeberg v5.0.6. Evidence: UPSTREAM_BASELINE.yaml; version-discovery-report.md.
2. **Active health modules (53)** — DB isthealth: 53 health* activated, 0 inactive vs stock GH 5.0.6 activation set. Evidence: FINAL_REPORT_SECTION17.md; module-registry.json.
3. **Custom Tryton / IST modules** — ir.module ist*/iris*; repo Tryton modules. Evidence: 0 custom IST Tryton modules; no health* fork.
4. **Database models / tables** — gnuhealth.* models (~358 catalogued); schema from activated upstream modules. Evidence: Unmodified upstream model/table names; medium confidence (source scrape).
5. **Technical identifiers** — Package/module/model/table/XML ID names. Evidence: Remain GNU Health identifiers per naming policy.
6. **Tryton JSON-RPC API surface** — common.authenticate + model.* Session API. Evidence: React and SAO use same transport.
7. **PostgreSQL-backed Tryton schema** — No alternate ORM. Evidence: UPSTREAM_BASELINE.yaml.
8. **Features-doc-only absences** — health_accounting / health_profile not in v5.0.6 tree. Evidence: Same gap as stock pin (upstream-drift-report.md).
9. **Upstream software licence** — GPL-3.0-or-later on HIS components. Evidence: ATTRIBUTION.md.
10. **SAO client package installed** — sao 7.0.53 available at /sao/. Evidence: Installed; not primary UX.

### B.1 Activated module names (all 53 — Same backend)

Technical names remain GNU Health identifiers. All are `upstream`, `installed`, `activated`:

| # | Module | Display name | Upstream version |
|---|--------|--------------|------------------|
| 1 | `health` | Core HIS | 5.0.6 |
| 2 | `health_archives` | Archives | 5.0.4 |
| 3 | `health_caldav` | CalDAV | 5.0.4 |
| 4 | `health_calendar` | Calendar | 5.0.5 |
| 5 | `health_contact_tracing` | Contact Tracing | 5.0.4 |
| 6 | `health_crypto` | Crypto | 5.0.4 |
| 7 | `health_crypto_lab` | Crypto Laboratory | 5.0.4 |
| 8 | `health_dentistry` | Dentistry | 5.0.6 |
| 9 | `health_disability` | Disability / ICF | 5.0.4 |
| 10 | `health_ems` | EMS / Ambulance | 5.0.4 |
| 11 | `health_federation` | Federation | 5.0.4 |
| 12 | `health_genetics` | Genetics | 5.0.4 |
| 13 | `health_genetics_uniprot` | Genetics UniProt | 5.0.4 |
| 14 | `health_gyneco` | Gynecology & Obstetrics | 5.0.4 |
| 15 | `health_history` | Enhanced History | 5.0.4 |
| 16 | `health_icd10` | ICD-10 | 5.0.4 |
| 17 | `health_icd10pcs` | ICD-10-PCS | 5.0.3 |
| 18 | `health_icd11` | ICD-11 | 5.0.4 |
| 19 | `health_icd9procs` | ICD-9 Procedures | 5.0.4 |
| 20 | `health_icpm` | ICPM | 5.0.4 |
| 21 | `health_icu` | ICU | 5.0.4 |
| 22 | `health_imaging` | Medical Imaging | 5.0.4 |
| 23 | `health_imaging_worklist` | Imaging Worklist | 5.0.4 |
| 24 | `health_inpatient` | Inpatient | 5.0.4 |
| 25 | `health_inpatient_calendar` | Inpatient Calendar | 5.0.4 |
| 26 | `health_insurance` | Insurance | 5.0.4 |
| 27 | `health_iss` | Injury Surveillance | 5.0.4 |
| 28 | `health_lab` | Laboratory | 5.0.4 |
| 29 | `health_lifestyle` | Lifestyle | 5.0.4 |
| 30 | `health_mdg6` | MDG6 | 5.0.4 |
| 31 | `health_ntd` | NTD Metapackage | 5.0.3 |
| 32 | `health_ntd_chagas` | NTD Chagas | 5.0.4 |
| 33 | `health_ntd_dengue` | NTD Dengue | 5.0.4 |
| 34 | `health_nursing` | Nursing | 5.0.4 |
| 35 | `health_ophthalmology` | Ophthalmology | 5.0.4 |
| 36 | `health_orthanc` | Orthanc PACS | 5.0.4 |
| 37 | `health_pediatrics` | Pediatrics | 5.0.4 |
| 38 | `health_pediatrics_growth_charts` | Growth Charts | 5.0.4 |
| 39 | `health_pediatrics_growth_charts_who` | WHO Growth Charts | 5.0.4 |
| 40 | `health_qrcodes` | QR Codes | 5.0.4 |
| 41 | `health_reporting` | Reporting | 5.0.4 |
| 42 | `health_services` | Services & Billing | 5.0.4 |
| 43 | `health_services_imaging` | Imaging Services | 5.0.4 |
| 44 | `health_services_lab` | Lab Services | 5.0.4 |
| 45 | `health_socioeconomics` | Socioeconomics | 5.0.4 |
| 46 | `health_stock` | Health Stock | 5.0.4 |
| 47 | `health_stock_inpatient` | Stock Inpatient | 5.0.4 |
| 48 | `health_stock_nursing` | Stock Nursing | 5.0.4 |
| 49 | `health_stock_surgery` | Stock Surgery | 5.0.4 |
| 50 | `health_surgery` | Surgery | 5.0.4 |
| 51 | `health_surgery_protocols` | Surgery Protocols | 5.0.4 |
| 52 | `health_webdav3_server` | WebDAV3 Server | 5.0.4 |
| 53 | `health_who_essential_medicines` | WHO Essential Medicines | 5.0.4 |

### B.2 Also Same (technical)

- Pin: Codeberg `v5.0.6` commit `f50972fee0d4e001133a09af8d9ea7dbfe67f7a8` (latest stable **5.0.7 not adopted**).
- Stack: `gnuhealth` **5.0.6**, trytond **7.0.53**, SAO **7.0.53**, PostgreSQL **15.18**, Python **3.11.2**, gnuhealth-control **5.0.3**.
- DB: `isthealth` — 53 `health*` activated, **0** custom `ist*`/`iris*` Tryton modules.
- Models approach: stock `gnuhealth.*` / Tryton models; no IST schema fork.
- Features-doc-only absences shared with pin: `health_accounting`, `health_profile` (and alias `health_imaging_orthanc`) — not IST removals.

---

## C. Complete DIFFERENT / PARTIAL items

### C.1 DIFFERENT (product / ops layer)

| Area | What differs | Evidence |
|------|--------------|----------|
| **Desktop / primary UI client** | Stock SAO-as-default vs IST React SPA | Primary UX is React at health.irisstar.tech; SAO secondary |
| **Login / branding / UI chrome** | IST HIS / Iris Star branding, navy/gold, EN/AR RTL | Naming policy §6.1; frontend design system |
| **Help system** | React Help Centre /help, /help/admin, EN/AR workflows | IST-only frontend/help-content/ |
| **Docs (IST HIS library)** | docs/ist-his/ adapted vs upstream RST/HTML | IST terminology/UI/UAE–QA; CC-BY-SA attribution |
| **Synthetic data / templates** | Deterministic demo packs, IST markers | ISTHIS-DEMO-* / IST-P-*; not stock GH demo |
| **UAE / Qatar localization overlays** | HIE, tenancy, bilingual ops framework | gap-analysis-uae-qatar.md; no production HIE connectors |
| **Deployment (GCP nginx)** | VM gnuhealth-his-01, nginx React+/api+/sao/ | IST ops topology; not stock GH appliance layout |
| **Product versioning** | IST HIS 1.0.0 on upstream HIS 5.0.6 | UPSTREAM_BASELINE.yaml ist_his_product_version |

### C.2 PARTIAL (shared backend; UI/depth differs)

| Area | What was checked | Evidence |
|------|------------------|----------|
| **Menus / navigation** | React MenuTree + menuRoutes vs SAO ir.ui.menu shell | Menus from Tryton; unmapped/wizards → SAO panel |
| **Patient / clinical CRUD** | Create/edit patients, appointments, evaluations, staff | Gap 1 closed for core; deep demographics SAO-only |
| **Lab / pharmacy / inpatient / surgery UI** | Lab, Rx, beds, nursing, procedures, imaging routes | Live React routes; result/admission/shipment wizards SAO-only |
| **Financial / accounting UX** | React /financial vs SAO CoA/FY/journals/taxes/post-pay | List + draft invoice stub + SAO panel; deep finance SAO-only |
| **Auth / session client behavior** | Tryton Session header; React localStorage | Same protocol; MVP token storage differs from SAO UX |
| **APIs / FHIR / HIE** | JSON-RPC present; HL7/FHIR HIE absent | Same transport; no UAE/QA HIE gateway (G-01…G-04) |
| **Licensing / commercial attribution** | GPL software + CC-BY-SA docs + IST notices | Legal review REQUIRED before commercial claims |
| **Admin ops (users/groups/modules/sequences)** | Gap 4 React admin subset | List/edit subset; UI config & record-rules editor SAO-only |
| **Orthanc / WebDAV / federation admin** | Modules activated; React wiring | Backend same; not wired in React (SAO-only admin) |

### C.3 Wizard / clinical-area gaps (React vs SAO)

| Clinical / admin area | React today | Still SAO-only |
|-----------------------|-------------|----------------|
| Patients | Create/edit core party + patient | Full demographics, insurance, family, diseases, vaccinations, photo |
| Appointments | Create/edit | Specialty / insurance / consultation product linking |
| Staff | Create/edit | Main specialty O2M, institution unit |
| Laboratory | Create lab request | Result entry; create-lab-test wizard |
| Imaging | List / requests | Generate result; Orthanc sync |
| Surgery / procedures | List | OR schedule, deep surgery, stock-move wizard |
| Admissions / inpatient | Beds / registrations list | Bed-transfer, inpatient evaluation wizards |
| Pharmacy / stock | Rx list; stock locations/moves | Prescription/vaccination/surgery stock-move wizards |
| Financial | Invoice list + draft stub + SAO panel | CoA template, journals, FY, taxes, post/pay/cancel |
| Reporting | — | Epidemics, top diseases, summary, evaluations reports |
| Specialty packs (ICU, dent, gyneco, ophto, EMS, genetics, NTD, …) | — | Full SAO forms/wizards |
| Federation / WebDAV / Orthanc admin | — | Config + sync wizards |
| UI config / record rules | — | Menus, views, actions, icons, record-rules editor |
| Module upgrades | Mark activate when API allows | `trytond-admin` / SAO pending upgrades |

---

## D. Module-by-module matrix (all 53 activated)

Columns: Module | Upstream version | Activated | IST React coverage | Same backend? | Notes

| Module | Upstream version | Activated | IST React coverage | Same backend? | Notes |
|--------|------------------|-----------|--------------------|---------------|-------|
| `health` | 5.0.6 | Yes | Partial | Yes | Patients/appointments/staff/evaluations/medications/settings live; deep demographics/family/vaccines/photo SAO-only |
| `health_archives` | 5.0.4 | Yes | SAO-only | Yes | Paper archive — no dedicated React route |
| `health_caldav` | 5.0.4 | Yes | SAO-only | Yes | CalDAV server — not in React |
| `health_calendar` | 5.0.5 | Yes | Partial | Yes | /calendar list; create-appointment wizard SAO-only |
| `health_contact_tracing` | 5.0.4 | Yes | SAO-only | Yes | No React route |
| `health_crypto` | 5.0.4 | Yes | SAO-only | Yes | Crypto signing UX SAO-only |
| `health_crypto_lab` | 5.0.4 | Yes | SAO-only | Yes | Lab crypto SAO-only |
| `health_dentistry` | 5.0.6 | Yes | SAO-only | Yes | Odontogram wizards SAO-only |
| `health_disability` | 5.0.4 | Yes | SAO-only | Yes | ICF assessments SAO-only |
| `health_ems` | 5.0.4 | Yes | SAO-only | Yes | Ambulance / support requests SAO-only |
| `health_federation` | 5.0.4 | Yes | SAO-only | Yes | Federation config/queue not wired in React |
| `health_genetics` | 5.0.4 | Yes | SAO-only | Yes | Genetics risk UI SAO-only |
| `health_genetics_uniprot` | 5.0.4 | Yes | SAO-only | Yes | UniProt data pack — SAO/data only |
| `health_gyneco` | 5.0.4 | Yes | SAO-only | Yes | OB/GYN forms SAO-only |
| `health_history` | 5.0.4 | Yes | SAO-only | Yes | Enhanced history reports SAO-only |
| `health_icd10` | 5.0.4 | Yes | None | Yes | Reference data pack; used via pathology lookups |
| `health_icd10pcs` | 5.0.3 | Yes | None | Yes | Reference data pack |
| `health_icd11` | 5.0.4 | Yes | None | Yes | Reference data pack |
| `health_icd9procs` | 5.0.4 | Yes | None | Yes | Reference data pack |
| `health_icpm` | 5.0.4 | Yes | None | Yes | Reference data pack |
| `health_icu` | 5.0.4 | Yes | SAO-only | Yes | Apache2/Glasgow/ventilation SAO-only |
| `health_imaging` | 5.0.4 | Yes | Partial | Yes | /imaging list/requests; result generation & complex wizards SAO-only |
| `health_imaging_worklist` | 5.0.4 | Yes | SAO-only | Yes | Worklist templates SAO-only |
| `health_inpatient` | 5.0.4 | Yes | Partial | Yes | /beds admissions/beds; bed-transfer & inpatient evaluation wizards SAO-only |
| `health_inpatient_calendar` | 5.0.4 | Yes | SAO-only | Yes | Inpatient calendar views SAO-only |
| `health_insurance` | 5.0.4 | Yes | SAO-only | Yes | Plans/policies; patient insurance deep forms SAO-only |
| `health_iss` | 5.0.4 | Yes | SAO-only | Yes | Injury surveillance SAO-only |
| `health_lab` | 5.0.4 | Yes | Partial | Yes | /laboratory create request; result entry & create-lab-test wizard SAO-only |
| `health_lifestyle` | 5.0.4 | Yes | SAO-only | Yes | Lifestyle/CAGE fields on patient — SAO-only |
| `health_mdg6` | 5.0.4 | Yes | None | Yes | MDG6 lab/disease pack — data/SAO |
| `health_ntd` | 5.0.3 | Yes | None | Yes | NTD metapackage |
| `health_ntd_chagas` | 5.0.4 | Yes | SAO-only | Yes | Chagas survey SAO-only |
| `health_ntd_dengue` | 5.0.4 | Yes | SAO-only | Yes | Dengue survey SAO-only |
| `health_nursing` | 5.0.4 | Yes | Partial | Yes | /nursing ambulatory + rounding list; deep forms SAO |
| `health_ophthalmology` | 5.0.4 | Yes | SAO-only | Yes | Ophthalmology evaluations SAO-only |
| `health_orthanc` | 5.0.4 | Yes | SAO-only | Yes | Orthanc sync wizards not wired in React |
| `health_pediatrics` | 5.0.4 | Yes | SAO-only | Yes | Newborn/PSC SAO-only |
| `health_pediatrics_growth_charts` | 5.0.4 | Yes | SAO-only | Yes | Growth chart hooks SAO-only |
| `health_pediatrics_growth_charts_who` | 5.0.4 | Yes | SAO-only | Yes | WHO chart wizards/reports SAO-only |
| `health_qrcodes` | 5.0.4 | Yes | SAO-only | Yes | QR reports SAO-only |
| `health_reporting` | 5.0.4 | Yes | SAO-only | Yes | Epidemics/top-diseases/summary wizards SAO-only |
| `health_services` | 5.0.4 | Yes | Partial | Yes | Backend + invoice link via /financial stub; service invoice wizard SAO-only |
| `health_services_imaging` | 5.0.4 | Yes | SAO-only | Yes | Imaging service invoice linkage SAO-only |
| `health_services_lab` | 5.0.4 | Yes | SAO-only | Yes | Lab service invoice linkage SAO-only |
| `health_socioeconomics` | 5.0.4 | Yes | SAO-only | Yes | SES assessment SAO-only |
| `health_stock` | 5.0.4 | Yes | Partial | Yes | /stock locations/moves list; Rx/vaccination stock-move wizards SAO-only |
| `health_stock_inpatient` | 5.0.4 | Yes | SAO-only | Yes | Rounding supply stock SAO-only |
| `health_stock_nursing` | 5.0.4 | Yes | SAO-only | Yes | Ambulatory care stock SAO-only |
| `health_stock_surgery` | 5.0.4 | Yes | SAO-only | Yes | Surgery stock-move wizard SAO-only |
| `health_surgery` | 5.0.4 | Yes | Partial | Yes | /procedures surgery/operation list; OR schedule & deep surgery UX SAO-only |
| `health_surgery_protocols` | 5.0.4 | Yes | None | Yes | Protocol reference data |
| `health_webdav3_server` | 5.0.4 | Yes | SAO-only | Yes | WebDAV shares not in React |
| `health_who_essential_medicines` | 5.0.4 | Yes | None | Yes | WHO EM data pack |

### D.1 Registry entries not in the 53 (features-doc-only / absent)

| Module | State | Notes |
|--------|-------|-------|
| `health_accounting` | absent_from_release | Features catalogue only; use Tryton `account_*` + `health_services` |
| `health_profile` | absent_from_release | Features metapackage; not in HIS 5.0.6 tree |
| `health_imaging_orthanc` | absent_from_release | Alias; use `health_orthanc` |

React coverage legend: **Full** = React parity for primary workflows; **Partial** = dedicated React route with CRUD/list but wizards/deep forms SAO; **None** = data pack only (no UI expected); **SAO-only** = module UI only via SAO / Open-in-SAO.

---

## E. Capability matrix

| Capability | Status | Evidence |
|------------|--------|----------|
| **Parties** | **Partial** | Backend party.party Same; React /parties list live; deep party forms SAO |
| **Patients** | **Partial** | gnuhealth.patient Same backend; React create/edit core; demographics/insurance/family/vaccines/photo SAO |
| **Appointments** | **Partial** | /appointments create/edit; specialty/insurance/product linking SAO |
| **Patient evaluations** | **Partial** | /evaluations live on gnuhealth.patient.evaluation; full SAO form depth not claimed |
| **Health professionals / staff** | **Partial** | /staff create/edit; specialty O2M / institution unit SAO |
| **Laboratory** | **Partial** | /laboratory requests; result entry & create-lab-test wizard SAO |
| **Imaging** | **Partial** | /imaging requests/results list; generate-result & Orthanc wizards SAO |
| **Pharmacy / prescriptions** | **Partial** | /pharmacy + /medications; stock-move from Rx wizard SAO |
| **Inpatient / beds / admissions** | **Partial** | /beds; bed-transfer & inpatient evaluation wizards SAO |
| **ICU** | **Different** | health_icu activated (backend Same); React coverage None/SAO-only |
| **Surgery** | **Partial** | /procedures list; OR schedule, protocols UX, stock-move wizard SAO |
| **Nursing** | **Partial** | /nursing ambulatory + rounding; deep nursing forms / stock SAO |
| **Insurance** | **Partial** | health_insurance activated; plans/patient insurance deep UI SAO-only |
| **Stock / inventory** | **Partial** | /stock list; health_stock* move wizards SAO |
| **Accounting / invoicing** | **Partial** | account_* + health_services backend; React stub; CoA/FY/tax/post-pay SAO |
| **Reporting (clinical/epidemiology)** | **Different** | health_reporting wizards SAO-only; no React report parity |
| **Federation** | **Different** | health_federation activated; config/queue not in React; not UAE HIE |
| **Crypto signing** | **Different** | health_crypto(+_lab) activated; signing UX SAO-only |
| **Genetics** | **Different** | health_genetics(+_uniprot) activated; SAO-only UI |
| **Pediatrics / growth charts** | **Different** | Modules activated; React None/SAO-only |
| **Gynecology & obstetrics** | **Different** | health_gyneco activated; SAO-only |
| **Dentistry** | **Different** | health_dentistry odontogram wizards SAO-only |
| **Ophthalmology** | **Different** | health_ophthalmology SAO-only |
| **EMS / ambulance** | **Different** | health_ems SAO-only |
| **Disability / ICF** | **Different** | health_disability SAO-only |
| **Contact tracing / NTD / ISS** | **Different** | Activated packs; SAO-only clinical UI |
| **ICD / coding packs** | **Same** | ICD-10/11/PCS/9procs/ICPM data same as pin; no IST fork |
| **WHO essential medicines** | **Same** | Data pack activated; same as upstream pin |
| **Calendar / CalDAV / WebDAV** | **Partial** | Modules activated; /calendar list; CalDAV/WebDAV admin SAO |
| **Orthanc PACS** | **Partial** | health_orthanc activated; sync wizards SAO; not wired in React |
| **QR codes** | **Different** | health_qrcodes reports SAO-only |
| **Help / documentation product** | **Different** | IST Help Centre + docs/ist-his library — not stock GH help |
| **UAE/QA HIE (NABIDH/Malaffi/Riayati/Qatar)** | **Different** | Neither GH stock nor IST has production HIE connectors |
| **Multi-entity UAE↔Qatar isolation** | **Different** | Designed in implementation docs; not fully deployed |
| **Synthetic demo data** | **Different** | IST factories/markers — not stock GH demo content |
| **Primary product branding** | **Different** | IST HIS / Iris Star vs GNU Health branding |

---

## F. "Getting item-by-item same" — honesty

### What is already item-by-item same

- **Backend:** 0 custom Tryton modules; 53 activated `health*` packages match the v5.0.6 pin; models/tables/XML IDs are GNU Health.
- **API:** Same Tryton JSON-RPC Session surface.
- **Optional stock client:** SAO 7.0.53 is installed — using SAO as the daily client gives the **same client experience as stock GNU Health** (modulo IST branding on the React homepage and nginx layout).

### What full product item-by-item sameness would require

Full **product** sameness (customer claim: “exactly the same as GNU Health”) means one of:

1. **Use SAO as primary UI** — product experience ≈ stock GNU Health web client. Backend already matches. Cost: abandon or demote React as primary; accept SAO UX.
2. **Implement full React parity** for every SAO form/wizard/report across all 53 modules (and Tryton account/stock/admin wizards) — a **large multi-sprint program**, not a docs claim. Today many specialty packs are SAO-only.

Neither path is automatic. Backend sameness ≠ product sameness.

### Credible “functionally equivalent for X” claims

| Claim scope X | Credible today? | Condition |
|---------------|-----------------|-----------|
| Backend HIS 5.0.6 modules/models | **Yes** | Cite this matrix + module dump |
| Ambulatory MVP (patients, appointments, staff, lab request, Rx list) via React | **Partial / Yes with caveats** | Document SAO for deep fields/wizards |
| Full SAO clinical depth (ICU, surgery wizards, reporting, Orthanc, …) | **Yes via SAO** | Train users on `/sao/`; do not imply React-only |
| Finance (CoA, FY, post/pay) | **Via SAO only** | React `/financial` is stub |
| UAE/QA HIE / e-claim | **No** | Neither stock GH nor IST has connectors |
| “Exactly the same product as GNU Health” | **No** | Branding, React UI, help, docs, deploy differ |

### Work remaining for stronger equivalence claims

- Decide primary UI strategy: **SAO-first** (fastest “same as GH”) vs **React parity program**.
- If React: prioritize wizard parity per clinical area (lab results, admission, surgery, finance post/pay, imaging generate-result).
- Do not claim HIE/e-claim equivalence without new integration work.
- Legal review before commercial “equivalent to GNU Health” wording.

---

## G. Companion Excel

Filterable workbook: [`GNU_Health_vs_IST_HIS_item_matrix.xlsx`](GNU_Health_vs_IST_HIS_item_matrix.xlsx)

Sheets: `Product_Layer`, `Modules_53`, `Capabilities`, `Summary_Counts`.

---

## Explicit naming statement

| Layer | Name |
|-------|------|
| Customer-facing product | **IST HIS** — Iris Star Hospital Information System |
| Upstream product | **GNU Health HIS** 5.0.6 |
| Framework | **Tryton** 7.0.53 |
| Technical modules / models / tables | Remain **GNU Health** names — do not globally rename |

---

## Confidence notes

| Claim | Confidence |
|-------|------------|
| Server versions & 53 activated modules | **High** |
| Zero custom IST Tryton modules | **High** |
| Models unmodified vs upstream source pin | **Medium–High** |
| React vs SAO feature matrix | **High** for documented routes; every-wizard exhaustive check **not** claimed |
| FHIR / HIE | **High** that neither path provides UAE/QA HIE today |

---

## Sources

- `docs/upstream/UPSTREAM_BASELINE.yaml`
- `docs/upstream/VERSIONS.yaml`
- `docs/upstream/version-discovery-report.md`
- `docs/upstream/FINAL_REPORT_SECTION17.md`
- `docs/upstream/upstream-drift-report.md`
- `docs/upstream/module-registry.json`
- `docs/upstream/module-dependency-map.md`
- `docs/upstream/ATTRIBUTION.md`
- `docs/ist-his/IST_HIS_Naming_and_Branding_Policy.md`
- `docs/research/current-system-discovery.md`
- `docs/research/gap-analysis-uae-qatar.md`
- `frontend/docs/SAO_MIGRATION.md`
- `frontend/docs/ARCHITECTURE.md`
- `frontend/src/lib/tryton/menuRoutes.ts`
- `frontend/src/App.tsx`

---

## H. Document content parity (substance, not names)

**Exactly the same docs content/context as GNU Health?** **NO.**

IST `docs/ist-his/` maps the same module/topics (traceability: **63** rows, all marked Adapted, none Same) but module guides and overviews are **stubs** vs upstream RST how-tos. Full substance lives in `docs/upstream/original/`. Detail: [`DOCUMENT_CONTENT_PARITY.md`](DOCUMENT_CONTENT_PARITY.md).

---

*Comparison compiled 2026-07-14. Product-layer: Same 10 / Partial 9 / Different 8. Capabilities: Same 2 / Partial 16 / Different 18. Modules: 53 activated. Do not claim “exactly the same” without re-verifying against a fresh VM module dump and UI checklist.*
