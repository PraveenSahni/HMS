---
title: GNU Health vs IST HIS — Item-by-Item Comparison
ist_his_version: 1.0.0
upstream_product: GNU Health HIS
upstream_version: 5.0.6
tryton_version: 7.0.53
baseline_date: 2026-07-14
production: https://health.irisstar.tech
licence: CC-BY-SA-4.0
legal_review: REQUIRED
---

# GNU Health vs IST HIS — Item-by-Item Comparison

## One-line verdict

**NOT exactly the same.**

## Executive summary

**IST HIS** (Iris Star Hospital Information System) is a **customized / localized presentation and operations layer** on a **GNU Health HIS 5.0.6** backend (Tryton **7.0.53**). The server-side health packages, activated modules, and `gnuhealth.*` models match the pinned upstream stock; the customer-facing product differs in React UI, branding, Help Centre, documentation library, synthetic data, UAE/Qatar implementation framework, and GCP/nginx deployment.

**Naming (explicit):** Technical module names, Python packages, models, tables, and XML IDs remain **GNU Health** identifiers. The customer product name is **IST HIS**.

Evidence baseline: `docs/upstream/UPSTREAM_BASELINE.yaml`, `docs/upstream/version-discovery-report.md`, `docs/upstream/FINAL_REPORT_SECTION17.md`, `docs/upstream/module-registry.json`, `docs/research/current-system-discovery.md`, `docs/research/gap-analysis-uae-qatar.md`, `frontend/docs/SAO_MIGRATION.md`, `docs/ist-his/IST_HIS_Naming_and_Branding_Policy.md`.

Legend for status column:

| Status | Meaning |
|--------|---------|
| **Same** | Verified equivalent to stock GNU Health 5.0.6 / Tryton 7.0.53 for this area |
| **Different** | Material IST-specific change or addition |
| **Partial** | Shared backend / subset parity; presentation or depth differs |
| **Unknown** | Insufficient live evidence in baseline docs |

---

## Full item-by-item table

| Area | What was checked | Status | Evidence / notes |
|------|------------------|--------|------------------|
| **Server core** (trytond, health packages) | VM `gnuhealth-his-01`: `gnuhealth` **5.0.6**, trytond **7.0.53**, SAO **7.0.53**, PG **15.18**, Python **3.11.2**; pin Codeberg `v5.0.6` (`f50972fee0d4e001133a09af8d9ea7dbfe67f7a8`); latest stable **5.0.7 not adopted** | **Same** | `UPSTREAM_BASELINE.yaml`, `version-discovery-report.md` — stock GH HIS server stack at pin |
| **Active health modules (53)** | Inventory vs stock GH 5.0.6; DB `isthealth`: 53 `health*` activated, 0 inactive | **Same** | `FINAL_REPORT_SECTION17.md`, `version-discovery-report.md`, `module-registry.json` — matches release tree activation set |
| **Custom Tryton / IST modules** | `ir.module` for `ist*` / `iris*`; repo Tryton modules | **Same** (none) | Baseline: **0** custom IST Tryton modules; no fork of `health*` packages detected |
| **Database models / tables** | `gnuhealth.*` models (~358 catalogued from source scrape); schema from activated upstream modules | **Same** | Unmodified upstream model names/tables; field catalogue medium confidence (source scrape, not full live proteus dump) |
| **Desktop / SAO client** | Stock SAO 7.0.53 vs IST React SPA as primary UI | **Different** | SAO still served at `/sao/`; production UX is React at `https://health.irisstar.tech/` — not stock SAO-only product |
| **Login / branding / UI** | IST HIS / Iris Star branding, design system, EN/AR RTL | **Different** | Naming policy §6.1; `frontend/` IST navy/gold; login/product titles are IST, not “GNU Health” |
| **Menus / navigation** | React tree (`MenuTree` + `menuRoutes`) vs SAO `ir.ui.menu` | **Partial** | Menus sourced from Tryton; mapped routes + Setup Hub + Help; unmapped/wizards → SAO panel — not 1:1 SAO chrome |
| **Patient / clinical workflows** | Create/edit patients, appointments, evaluations, staff | **Partial** | Core CRUD live in React (Gap 1 closed); full demographics, insurance, family, diseases, vaccinations, photo remain SAO-only |
| **Lab, pharmacy, inpatient, surgery** | Lab, Rx, beds/admissions, nursing, procedures/imaging routes | **Partial** | Live React routes on upstream models; lab result entry, imaging/surgery/admission/shipment wizards still SAO-only |
| **Financial / accounting** | React `/financial` vs SAO CoA / FY / journals / taxes / post-pay | **Partial** | Backend `account_*` (+ optional `health_accounting` features-doc gap); React = list + draft invoice stub + SAO panel; deep finance SAO-only |
| **Help system** | React Help Centre `/help`, `/help/admin`, EN/AR workflows | **Different** | IST-only operational layer (`frontend/help-content/`); not stock GNU Health help UX |
| **Docs (IST HIS library)** | `docs/ist-his/` adapted library vs upstream RST/HTML | **Different** | Adapted for IST terminology/UI/UAE–QA; CC-BY-SA attribution; upstream originals kept under `docs/upstream/original/` |
| **Synthetic data / templates** | Deterministic demo packs, IST markers, implementation templates | **Different** | IST-only (`synthetic_data/`, `synthetic-data/`, IST markers `ISTHIS-DEMO-*` / `IST-P-*`); not stock GH demo content |
| **UAE / Qatar localization** | Multi-country framework, HIE, tenancy, bilingual ops | **Different** | IST implementation/gap docs and Help country awareness; **no** production HIE connectors; tenant isolation designed, not fully deployed |
| **APIs / FHIR** | Tryton JSON-RPC usage; HL7/FHIR HIE | **Partial** | **Same** transport: Tryton JSON-RPC Session API. **Different / gap:** no IST FHIR/HL7 HIE gateway; Orthanc/Federation modules exist upstream but not wired as UAE/QA HIE |
| **Auth / session** | `common.authenticate` + Session header | **Partial** | Same Tryton auth protocol; IST React stores session in `localStorage` (MVP security debt) — presentation/ops differ from stock SAO |
| **Deployment (GCP nginx)** | VM `gnuhealth-his-01`, project `isthealth`, zone `me-central1-a`; nginx `/` React, `/api/tryton/`, `/sao/` | **Different** | IST ops topology (GCP + nginx reverse proxy + React static); not a generic stock GH appliance layout |
| **Licensing attribution** | GPL software + CC-BY-SA adapted docs + IST notices | **Partial** | Upstream GPL-3.0-or-later preserved; IST product naming + ATTRIBUTION.md; **legal review required** before commercial claims |

---

## Things that ARE the same (upstream on the server)

1. **GNU Health HIS core package 5.0.6** and **Tryton 7.0.53** server stack (pinned; 5.0.7 not adopted).
2. **SAO client package 7.0.53** installed alongside (legacy UI path).
3. **53 activated `health*` modules** on DB `isthealth`, matching the v5.0.6 release activation inventory (0 custom IST Tryton modules).
4. **Technical identifiers:** `gnuhealth-*` PyPI packages, Tryton module names (`health`, `health_lab`, …), models (`gnuhealth.patient`, …), DB tables, XML IDs.
5. **Clinical / ops data model** — patients, appointments, lab, prescriptions, inpatient, surgery, imaging, stock, insurance, ICD packs, etc. — from upstream modules (not an IST schema fork).
6. **Tryton JSON-RPC API surface** used by the React client (authenticate + `model.*` methods).
7. **PostgreSQL-backed Tryton schema** driven by activated upstream modules (no alternate ORM).
8. **Features-doc-only absences** shared with pin: `health_accounting` / `health_profile` not in v5.0.6 tree (drift report) — same gap as stock pin, not an IST removal of installed code.
9. **Licence of upstream software components:** GPL-3.0-or-later (GNU Solidario / contributors).
10. **No claimed endorsement** rewrite of the HIS engine — product policy preserves GNU Health as upstream product name for technical layers.

Representative activated module set (technical names remain GNU Health):  
`health`, `health_lab`, `health_nursing`, `health_inpatient`, `health_surgery`, `health_imaging`, `health_icu`, `health_pharmacy`-related Rx via prescription models, ICD/genetics/NTD/pediatrics/stock/services packs, `health_orthanc`, `health_federation`, `health_webdav3_server`, `health_who_essential_medicines`, and the rest of the 53-module baseline inventory — see `docs/upstream/module-registry.json` and `installed-module-inventory.xlsx`.

---

## Things that DIFFER (IST presentation / ops layer)

1. **Customer product name and branding:** IST HIS / Iris Star — not “GNU Health” on login, headers, Help, manuals.
2. **Primary UI:** custom **React** SPA (EN/AR RTL) instead of SAO-as-default desktop/web client experience.
3. **Navigation chrome:** React sidebar, Setup Hub (`/setup`), route mapping, “Open in SAO” for wizards — not stock SAO menu shell alone.
4. **Workflow depth in UI:** many deep wizards (CoA, tax, post/pay invoice, lab results, surgery/admission shipments, Orthanc/federation config) remain **SAO-only** while React covers ambulatory MVP + admin subset.
5. **Financial UX:** React `/financial` stub vs full SAO accounting configuration.
6. **Help Centre:** IST guided workflows, feedback, onboarding, publish flag — IST-only content under `frontend/help-content/`.
7. **Documentation library:** `docs/ist-his/` adapted (terminology, UI, UAE/Qatar) with attribution; not a verbatim docs.gnuhealth.org portal.
8. **Synthetic data & demo markers:** IST factories, seeds, and ID prefixes for demos — IST-only.
9. **UAE/Qatar implementation framework:** gap register, multi-entity design, HIE pending — IST program layer; stock GH has no NABIDH/Malaffi/Riayati/Qatar HIE client in this deployment.
10. **Deployment:** GCP VM `gnuhealth-his-01`, nginx fronting React + API + SAO, production hostname `health.irisstar.tech`.
11. **Auth client behavior:** Session token handling in React `localStorage` (MVP) vs stock SAO session UX.
12. **Product versioning:** IST HIS product **1.0.0** / docs **1.0.0** layered on upstream HIS **5.0.6**.

---

## Parity gaps (do not treat as “same product”)

| Gap | Upstream capability | IST React today |
|-----|---------------------|-----------------|
| Deep patient demographics / insurance / family / vaccines | SAO forms | Partial / SAO |
| Lab result entry & complex lab wizards | SAO | Partial / SAO |
| Surgery / admission / shipment wizards | SAO | Partial / SAO |
| Chart of accounts, journals, FY, taxes, invoice post/pay | SAO + account modules | Stub + SAO |
| Orthanc / WebDAV / federation admin | Modules present | Not wired in React |
| UAE/QA HIE (FHIR/HL7) | Not native HIE client | Not built |
| Multi-entity UAE↔Qatar record-rule isolation | Tryton companies/rules | Designed, not fully deployed |
| Live proteus full field dump / exhaustive SAO screenshots | N/A | Marked incomplete in §17 |

---

## Explicit naming statement

| Layer | Name |
|-------|------|
| Customer-facing product | **IST HIS** — Iris Star Hospital Information System |
| Upstream product | **GNU Health HIS** 5.0.6 |
| Framework | **Tryton** 7.0.53 |
| Technical modules / models / tables | Remain **GNU Health** names (`health_*`, `gnuhealth.*`) — do not globally rename |

Per `IST_HIS_Naming_and_Branding_Policy.md`: replace branding in UI/docs; **preserve** technical names without a formal migration design.

---

## Confidence notes

| Claim | Confidence |
|-------|------------|
| Server versions & 53 activated modules | **High** (live VM evidence in version-discovery / baseline) |
| Zero custom IST Tryton modules | **High** (`ir.module` baseline) |
| Models unmodified vs upstream source pin | **Medium–High** (source scrape + no custom modules; full live field dump incomplete) |
| React vs SAO feature matrix | **High** for documented routes (`SAO_MIGRATION.md`); exhaustive every-wizard check **not** claimed |
| FHIR / HIE | **High** that neither production path provides UAE/QA HIE connectors today |

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
- `frontend/docs/API.md`

---

*Comparison compiled 2026-07-14. Do not claim “exactly the same” without re-verifying this table against a fresh VM module dump and UI checklist.*
