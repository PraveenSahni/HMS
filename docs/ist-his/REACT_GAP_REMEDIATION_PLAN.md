---
title: React Gap Remediation Plan — IST HIS
ist_his_version: 1.0.0
upstream_product: GNU Health HIS
upstream_version: 5.0.6
tryton_version: 7.0.53
baseline_date: 2026-07-15
status: draft
licence: CC-BY-SA-4.0
related:
  - docs/ist-his/GNU_Health_vs_IST_HIS_comparison.md
  - docs/ist-his/UPSTREAM_IMAGE_SYNC_REVIEW.md
  - docs/ist-his/DOCUMENT_CONTENT_PARITY.md
  - docs/ist-his/SAO_EMBED_AND_SCREEN_PARITY.md
  - docs/ist-his/SCREEN_BY_SCREEN_PARITY.md
  - frontend/docs/SAO_MIGRATION.md
  - docs/research/gap-analysis-uae-qatar.md
  - docs/implementation/financial-setup.md
---

# React Gap Remediation Plan

## 1. Executive summary

IST HIS is a **thin React client** on an unmodified **GNU Health HIS 5.0.6** / **Tryton 7.0.53** backend (53 activated `health*` modules, **0** custom Tryton modules). Backend and JSON-RPC are stock; the **product experience is not**.

| Fact | Evidence |
|------|----------|
| **0 Full React module coverage** | Comparison matrix: no module rated **Full**; Partial ≈ 12 clinical/ops areas; rest **SAO-only** / data packs |
| React routes exist for daily ops | `App.tsx`: patients, appointments, lab, Rx, evaluations, beds, nursing, procedures, imaging, parties, stock, financial stub, admin, Setup Hub, **Workspace**, menu browser |
| Depth gaps are wizards & specialty forms | Lab create-test/results, admit/transfer, invoice post/pay, Orthanc, ICU, genetics, OB, NTD, reporting — **SAO via Workspace** |
| Docs/screenshots are not React-synced | Upstream images: ~15% aligned (feature), ~52% partial, ~33% gap/N/A; **0** IST docs match screenshot how-to fidelity |
| UAE/QA product gaps are orthogonal | No HIE/e-claim connectors; multi-entity isolation designed, not fully deployed |

### Locked product strategy (2026-07-15)

1. **Embed SAO now** inside the IST shell at **`/workspace`** (same-origin iframe → `/sao/`, IST navy/gold `custom.css`).
2. **Screen-by-screen React build** using [`SCREEN_BY_SCREEN_PARITY.md`](./SCREEN_BY_SCREEN_PARITY.md) / `.xlsx` — progressive parity, not big-bang rewrite.
3. Details: [`SAO_EMBED_AND_SCREEN_PARITY.md`](./SAO_EMBED_AND_SCREEN_PARITY.md).

**Honest scope for this plan:** Close the highest-value **ambulatory + inpatient + finance path** gaps in React; keep SAO (via Workspace) as the deep client for wizards and specialties; run a **parallel Help/screenshot** track so operators are never shown unlabeled GNU Solidario chrome as “the IST app.” Do **not** upgrade GNU Health unless separately approved.

**Credible product claim today:** “Ambulatory MVP via React, with Workspace (embedded SAO) for deep fields/wizards.” Not: “Full React parity with GNU Health SAO.”

---

## 2. Gap inventory (prioritized)

Legend — **Effort:** S ≤ 3d · M 1–2 w · L 3–6 w · XL multi-sprint · **Rec:** React | Keep-SAO | Hybrid (React shell + SAO deep-link).

### A. UX / branding & Help screenshots

| Gap | Impact | GH dependency | Effort | Rec |
|-----|--------|---------------|--------|-----|
| Upstream SAO/GTK images in Help as if they were React | High — trust/branding break; violates naming policy | None (docs) | M | Hybrid: capture React shots for core; label SAO secondary |
| Help workflows thin vs upstream RST walkthroughs | High — operators cannot finish lab/invoice/admit without tribal knowledge | Activated modules already present | L | Docs track; React only where UI exists |
| ghcontrol / Evolution / branding art treated as IST UX | Medium — wrong install story vs Setup Hub | N/A | S | Keep-SAO / N/A; ops appendix only |
| Version-drift screenshots (GH 4.x / Tryton 6) | Low–Med — misleading for 5.0.6/7.0.53 | Pin already fixed | S | Docs: mark illustrative |

### B. Core ambulatory MVP parity

| Gap | Impact | GH modules | Effort | Rec |
|-----|--------|------------|--------|-----|
| Patient deep demographics / insurance / family / vaccines / photo | High for registration completeness | `health`, `health_insurance` | L | Hybrid: harden React core; SAO for deep tabs |
| Appointment specialty / insurance / product linking | High for scheduling fidelity | `health`, `health_calendar` | M | React for create/edit; SAO for advanced links until done |
| Evaluation form depth (chief complaint → discharge) | High for consultation demo | `health` | M | React harden create-edit; SAO for rare tabs |
| Lab request OK; **create-test wizard + result entry** SAO-only | Critical for lab ops demo | `health_lab`, `health_crypto_lab` | L | Hybrid: React order/list; SAO wizard until Phase 1–2 |
| Prescription create/edit + stock-move from Rx | High for pharmacy demo | `health`, `health_stock` | L | Hybrid |
| Staff specialty O2M / institution unit | Medium | `health` | M | Hybrid |

### C. Inpatient / nursing / beds

| Gap | Impact | GH modules | Effort | Rec |
|-----|--------|------------|--------|-----|
| Beds list vs hospitalization form / bed-assign wizard | High for admit demo | `health_inpatient` | M–L | React admit/discharge basics; Keep-SAO transfer wizard short-term |
| Inpatient evaluation wizards | Medium | `health_inpatient` | M | Keep-SAO → React later |
| Nursing ambulatory + rounding deep forms / stock | Medium | `health_nursing`, `health_stock_nursing` | L | Hybrid: list React; deep SAO |
| Inpatient calendar views | Low–Med | `health_inpatient_calendar` | M | Keep-SAO |

### D. Finance / services / invoicing (beyond stub)

| Gap | Impact | GH modules | Effort | Rec |
|-----|--------|------------|--------|-----|
| `/financial` = list + draft stub; CoA/FY/journals/taxes SAO-only | Critical for billing UAT | `account_*`, `health_services` | XL full React; M guided Hybrid | **Hybrid** — Setup Hub + SAO wizards; React post path optional Phase 2 |
| Health service → invoice → pay wizards | Critical demo path | `health_services`, `health_services_lab`, `health_services_imaging` | L | Keep-SAO guided from React |
| Per-entity AED/QAR GL (G-16) | Required for UAE↔QA legal entities | Tryton company + account | M (config) | Tryton/config + SAO; not a React rewrite |
| Period close / cancel | Medium | `account_*` | S–M | Keep-SAO |

### E. Specialty modules (surgery, imaging, ICU, genetics, OB, Orthanc, NTD…)

| Gap | Impact | GH modules | Effort | Rec |
|-----|--------|------------|--------|-----|
| Surgery deep form / ICD-10-PCS / RCRI / OR schedule | Demo-dependent | `health_surgery`, coding packs | XL | Keep-SAO; React list OK |
| Imaging list OK; generate-result + Orthanc sync (11 upstream images) | Demo-dependent | `health_imaging`, `health_orthanc` | XL | Keep-SAO; optional Orthanc runbook |
| ICU APACHE / ECG / GCS | Niche | `health_icu` | XL | Keep-SAO |
| Genetics / OB-GYN / pediatrics / lifestyle / socioeconomics / NTD / dentistry / ophthalmology / EMS / disability | Niche | respective packs | XL each | Keep-SAO on demand |
| Reporting epidemics / top diseases | Medium for epidemiology demos | `health_reporting` | L | Keep-SAO |
| Federation queue ≠ UAE HIE | High confusion risk | `health_federation` | — | Docs only; do not imply HIE |

### F. Admin / config wizards still SAO-only

| Gap | Impact | Dependency | Effort | Rec |
|-----|--------|------------|--------|-----|
| Perform Pending module upgrade | High for ops safety | `ir.module` / trytond-admin | S (docs) | Keep-SAO; React mark-only |
| UI config (menus/views/actions/icons), record rules | Medium | Tryton admin | XL | Keep-SAO |
| WebDAV / CalDAV admin / Evolution client | Low for end users | `health_webdav3_server`, `health_caldav` | — | Keep-SAO / N/A |
| Scheduler / cron forms | Low–Med ops | Tryton | S | Keep-SAO |
| Groups access permissions depth | Medium | `res.group` | M | Hybrid (React summary OK) |

### G. Documentation depth (IST guides vs upstream procedures)

| Gap | Impact | Dependency | Effort | Rec |
|-----|--------|------------|--------|-----|
| 53 module READMEs = template stubs; **0** procedural Click/Open language | High for training | Upstream RST exists | L–XL | Docs workstream; adapt don’t clone branding |
| 63/63 traceability `screenshot_verified = N` | High for Help credibility | React UI capture | M | Parallel screenshot track |
| Missing IST how-tos: ICU, genetics, OB, Orthanc, NTD, surgery depth, lab create-test | High for specialty support | SAO + upstream RST | L | Stub + “Open in SAO” + labeled upstream |

### H. Multi-facility / tenant isolation / UAE–QA

| Gap | Impact | Dependency | Effort | Rec |
|-----|--------|------------|--------|-----|
| Multi-entity UAE↔QA isolation (G-12) | Critical governance | Tryton company + record rules | L | Tryton/config first; React company switch later |
| HIE NABIDH/Malaffi/Riayati/Qatar (G-01…G-04) | Regulatory | Integration layer **outside** GH | XL | Non-goal for React parity; separate program |
| e-claim (G-14) | Revenue cycle | Partner + `health_insurance` | XL | Non-goal for this plan |
| Bilingual clinical docs completeness (G-11) | Medium | i18n | M | Frontend |
| National ID validation UX (G-10) | Medium | Legal confirm | M | Hybrid; synthetic-only in demos |
| Privacy audit UI (G-13) | Medium | Tryton history | L | Later |

---

## 3. Strategy principles

1. **Embed SAO in IST Workspace first** (`/workspace`) so operators stay in IST chrome for wizards; then **build React screen-by-screen** per the parity tracker (P0 → P3). Do not rebuild all of SAO in one go.
2. **Prefer React for daily high-volume workflows** (register patient, book appointment, consult evaluation, lab order, Rx list, bed board, nursing list). **Workspace (embedded SAO)** for wizards until parity is funded.
3. **Model-driven generic forms where possible** — extend `ModelBrowserPage` / `menu/:menuId` for unmapped `act_window` before hand-building specialty pages.
4. **Screenshot/doc track runs in parallel to code** — never paste unlabeled GNU Health SAO/GTK shots into IST Help as the primary UI.
5. **No GNU Health / Tryton upgrade** unless separately CAB-approved. Close gaps with UI, config, Help, and Workspace bridging on the current pin (5.0.6 / 7.0.53).
6. **Hybrid is success.** A React page with a clear **Open in Workspace** for the next wizard step is shippable; a half-built React wizard that cannot post is not.
7. **UAE/QA demos** use Setup Hub order 1–9, synthetic data markers (`IST-*` / `SYN-*`), and separate legal companies (AED / QAR) — not federation-as-HIE.
8. **Track every screen** in `SCREEN_BY_SCREEN_PARITY.xlsx` / `.md` before claiming Parity.

---

## 4. Phased roadmap

### Phase 0 — Triage & bridge (1–2 weeks)

**Goals**

- Inventory every React stub/list page; ensure **Open in Workspace** (or Help deep-link) for the next operator action.
- Ship `/workspace` embed + SAO `custom.css` IST theme (done when this strategy is active).
- Help Centre: “Using Workspace” + callouts on thin workflows.
- Capture **React** screenshots for core flows (patient, appointment, lab order, Setup Hub 1–9).
- Label any reused upstream images as **SAO (secondary client / Workspace)**.

**Exit criteria**

- [x] Workspace route embeds same-origin `/sao/` under AppLayout.
- [ ] SaoPanel (or equivalent) present on financial, lab, imaging, procedures, beds, modules, Setup Hub.
- [ ] Help articles for P1 flows reference React routes first; `using-workspace` published.
- [ ] Screenshot pack started: ≥ 8 React frames checked into Help/docs with IST branding.
- [ ] Gap register (this doc §2) + screen tracker P0 accepted by product owner.

**Demo milestone (UAE/QA):** Operator walks Setup Hub → companies/currency → registers synthetic patient in React → books appointment → opens **Workspace** only when prompted.

---

### Phase 1 — MVP parity (ambulatory + inpatient basics)

**Goals**

- Harden React create/edit: patients, appointments, evaluations, lab requests, prescriptions.
- Inpatient: admit + discharge basics on `/beds` (or guided hospitalization create); bed board usable for demo.
- Lab: document create-test + results as SAO steps from React; optionally thin result view if API-safe.
- Expand Help `wf-register-patient`, `wf-consultation`, `wf-lab-order`, admit/transfer.

**Exit criteria**

- [ ] Happy-path ambulatory demo **without** SAO for: party/patient create, appointment, evaluation create, lab request create, Rx create/list.
- [ ] Admit → assign bed → discharge (or documented Hybrid with one SAO wizard max).
- [ ] Playwright smoke covering those React paths.
- [ ] UAE + Qatar synthetic companies present; no real national IDs in demo data.

**Demo milestone:** Full ambulatory day + simple inpatient stay for IST demo hospital (UAE entity); repeat company switch narrative for Qatar entity (same React, different company).

---

### Phase 2 — Health services + invoice path + pharmacy stock

**Goals**

- Health services → invoice → pay: **guided SAO** from React `/financial` + Help, *or* minimal React post/pay if models allow safely.
- Complete CoA/FY/journals per legal entity per `docs/implementation/financial-setup.md` (config work).
- Stock/pharmacy: Rx dispense / stock-move — Hybrid with clear SAO wizard until React move create exists.
- Lab/imaging service invoice linkage documented (`health_services_lab` / `_imaging`).

**Exit criteria**

- [ ] Finance can post and pay at least one customer invoice from a health service (UAE AED and Qatar QAR paths documented).
- [ ] React financial page shows invoice state + SAO instructions that match runbook.
- [ ] Pharmacy dispense demo path recorded (React + SAO steps).
- [ ] Help `wf-finance-setup`, `wf-create-invoice`, `wf-receive-payment` screenshot-verified.

**Demo milestone:** Billable ambulatory visit (lab line → service → invoice → pay) for UAE company; mirror checklist for Qatar.

---

### Phase 3 — Surgery / imaging / ICU as needed by demo

**Goals**

- Only build React depth for specialties **required by a named demo script**.
- Default: React list + SAO deep form + IST Help stub pointing to labeled upstream RST/images.
- Orthanc: ops runbook if imaging demo requires PACS; do not wire sync into React unless demo-critical.

**Exit criteria**

- [ ] Demo script list frozen (which of surgery / imaging / ICU).
- [ ] Each selected specialty has: React entry point *or* menu browser path + Open in SAO + Help article.
- [ ] No claim of React Full coverage for unselected specialties.

**Demo milestone:** Optional OR or imaging vignette for UAE facility tour — SAO-backed, React shell.

---

### Phase 4 — Specialty modules on demand

**Goals**

- Genetics, OB/GYN, pediatrics, NTD, dentistry, ophthalmology, EMS, disability, lifestyle, socioeconomics, reporting, federation admin — **priority pull**, not push.
- Prefer ModelBrowser + SAO; invest in handcrafted React only with a funded clinical owner.

**Exit criteria**

- [ ] Demand backlog with owner + demo date per specialty.
- [ ] Module README upgraded from stub to Hybrid procedure (React/SAO) when pulled.
- [ ] Federation docs explicitly **not** UAE HIE.

**Demo milestone:** As requested by country program or specialty lead.

---

## 5. Workstreams & ownership

| Workstream | Owns | Primary artifacts |
|------------|------|-------------------|
| **Frontend** | React SPA routes, forms, SaoPanel coverage, ModelBrowser, i18n EN/AR | `frontend/src/`, `SAO_MIGRATION.md` |
| **Tryton / config** | Companies, currencies, CoA/FY/journals, record rules, module mark/activate, no silent upgrades | SAO + `docs/implementation/*`, Setup Hub |
| **Docs / Help** | Help Centre workflows, IST guides depth, screenshot policy, upstream labeling | `frontend/help-content/`, `docs/ist-his/` |
| **Synthetic data** | Deterministic demo packs, IST markers, multi-company seeds | factories / seed scripts |
| **QA / Playwright** | Smoke + critical path E2E; SAO handoff checks as manual or semi-auto | `frontend` e2e suite |

RACI note: Product owner prioritizes Phase 3/4 demos; Frontend + Docs pair on every Phase 0–2 exit criterion; Tryton/config is gate for Phase 2 billing.

---

## 6. Risks & non-goals

### Risks

| Risk | Mitigation |
|------|------------|
| Stakeholders assume React Full = GH SAO | Use this plan + comparison matrix in every demo brief |
| Unlabeled upstream screenshots ship in Help | Branding policy + image sync review; React-first captures |
| Finance blocked on missing CoA | Phase 0–2 config checklist; SAO-first accounting |
| Scope creep into all 53 modules | Phase 4 on-demand only |
| HIE/e-claim confusion with federation module | Explicit docs; G-01…G-04 out of React parity scope |
| Accidental GH upgrade | CAB gate; pin 5.0.6 |

### Non-goals (this program)

- Rebuilding **all** SAO forms/wizards/reports in React.
- Cloning **ghcontrol** TUI or Evolution CalDAV into IST.
- Presenting GNU Solidario / GNU Health chrome as IST branding.
- Production UAE/QA **HIE or e-claim** connectors (separate integration program).
- Claiming “exactly the same product as GNU Health.”
- Upgrading to HIS 5.0.7+ or Tryton beyond pin without approval.
- Full rewrite of 53 module READMEs to upstream RST depth in one sprint (incremental with phases).

### Legal / branding on screenshots

- Upstream images remain **CC-BY-SA** / GNU Health attribution where reused; follow `IST_HIS_Naming_and_Branding_Policy.md` and `docs/upstream/ATTRIBUTION.md`.
- Customer-facing Help must use **IST HIS** naming; SAO shots labeled secondary.
- Legal review **REQUIRED** before commercial “equivalent to GNU Health” wording (`GNU_Health_vs_IST_HIS_comparison.md`).

---

## 7. Immediate next 10 concrete tasks (this sprint)

1. **Audit SaoPanel coverage** on `/financial`, `/laboratory`, `/imaging`, `/procedures`, `/beds`, `/nursing`, `/pharmacy`, `/modules`, `/setup` — add missing Open-in-SAO blocks with model/menu hints.
2. **Help P1 pass:** Update `wf-register-patient`, appointment booking, `wf-lab-order` (include SAO create-test + results steps), `wf-consultation` — React routes first.
3. **Capture React screenshots** (patient list/detail, appointment form, lab order, Setup Hub, users/groups) into Help; mark `screenshot_verified` where applicable.
4. **Financial Hybrid checklist:** Verify UAE AED + Qatar QAR companies; ensure `/financial` checklist matches `docs/implementation/financial-setup.md`; CoA via SAO if missing.
5. **Patient/appointment harden:** Confirm create-edit happy path; list fields still SAO-only in UI copy (insurance, specialty linking).
6. **Lab handoff UX:** From React lab request row/detail, deep-link or instruction to SAO “Lab: Create test” + result entry (per upstream image cluster).
7. **Beds admit path:** Document or implement minimal hospitalization create; Playwright or manual script for admit → bed → discharge Hybrid.
8. **Menu browser QA:** Spot-check unmapped Health menu leaves → `/menu/:menuId` vs wizard → SaoPanel; fix broken mappings in `menuRoutes.ts`.
9. **Synthetic data:** Ensure demo pack covers patients, appointments, ≥1 lab request, ≥1 Rx, beds occupancy for both demo companies.
10. **Playwright smoke:** Login → patients create → appointment → lab request → open financial page (assert SAO panel visible); fail CI if Open-in-SAO missing on stub pages.

---

## Appendix A — React routes vs SAO-only (snapshot)

From `frontend/src/App.tsx` + `frontend/docs/SAO_MIGRATION.md` (2026-07-14/15):

| React route | Typical depth | Still SAO-only |
|-------------|---------------|----------------|
| `/patients`, `/patients/:id` | Create/edit core | Deep demographics, insurance, family, vaccines, photo |
| `/appointments` | Create/edit | Specialty / insurance / product linking |
| `/staff`, `/staff/:id` | Create/edit | Specialty O2M, institution unit |
| `/laboratory` | Create request | Create-test wizard, result entry |
| `/pharmacy`, `/medications` | List / Rx | Stock-move wizards |
| `/evaluations` | Thin create/list | Full evaluation form depth |
| `/beds` | Beds / registrations | Bed-transfer, inpatient evaluation wizards |
| `/nursing` | Ambulatory + rounding list | Deep nursing / stock |
| `/procedures` | Surgery/operation list | OR schedule, RCRI, deep surgery, stock-move |
| `/imaging` | Requests/results list | Generate result, Orthanc sync |
| `/financial` | Invoice list + draft stub | CoA, FY, journals, taxes, post/pay/cancel |
| `/stock`, `/products`, `/parties`, `/calendar` | Lists | Deep wizards |
| `/companies`, `/setup` | Lite + Hub order 1–9 | CoA template, tax confirmation |
| `/users`, `/groups`, `/modules`, … | Gap 4 subset | Record rules, UI config, Perform Pending |
| `/menu/:menuId` | Generic model browser | Wizards/reports → SaoPanel |
| — | — | ICU, genetics, OB, NTD, dentistry, ophthalmology, EMS, reporting, federation admin |

**Full React module coverage count: 0 / 53.**

---

## Appendix B — Source inputs

- `docs/ist-his/UPSTREAM_IMAGE_SYNC_REVIEW.md`
- `docs/ist-his/GNU_Health_vs_IST_HIS_comparison.md` (+ item matrix xlsx)
- `docs/ist-his/DOCUMENT_CONTENT_PARITY.md`
- `frontend/docs/SAO_MIGRATION.md`
- `docs/research/gap-analysis-uae-qatar.md`
- `docs/implementation/financial-setup.md`
- `frontend/src/App.tsx`
- `frontend/src/pages/SetupHubPage.tsx`

---

*Plan drafted 2026-07-15. Re-verify against a fresh VM module dump and UI checklist before changing phase exit criteria.*
