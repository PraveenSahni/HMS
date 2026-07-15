---
title: Screen-by-Screen Parity Tracker
ist_his_version: 1.0.0
baseline_date: 2026-07-15
status: active
related:
  - docs/ist-his/SAO_EMBED_AND_SCREEN_PARITY.md
  - docs/ist-his/REACT_GAP_REMEDIATION_PLAN.md
  - docs/ist-his/SCREEN_BY_SCREEN_PARITY.xlsx
---

# Screen-by-Screen Parity Tracker

**Strategy:** Embed SAO in `/workspace` now; build React progressively using this tracker.

**Spreadsheet:** [`SCREEN_BY_SCREEN_PARITY.xlsx`](./SCREEN_BY_SCREEN_PARITY.xlsx) (same columns).

**Status:** Missing | Stub | Partial | Parity  
**Priority:** P0 (daily clinical/admin) → P3 (specialty on demand)

**Inventory sources:** `App.tsx` routes · Favorites / Setup Hub · `docs/upstream/module-registry.json` (health*) · core Tryton (party, product, stock, account, …) · ir.ui.menu via sidebar Menus.

---

## P0 batch (seed — honest React status)

| Screen ID | Menu path | SAO | React route | Status | Priority | Compare notes | Build next action | Owner | Updated |
|-----------|-----------|-----|-------------|--------|----------|---------------|-------------------|-------|---------|
| P0-LOGIN | Auth / Login | Y | `/login` | Partial | P0 | IST login works; SAO has own login if session missing in iframe | Share session / SSO note; document dual login | Frontend | 2026-07-15 |
| P0-DASH | Health / Dashboard | Y | `/` | Partial | P0 | React dashboard cards; SAO home richer | Align KPIs with demo script | Frontend | 2026-07-15 |
| P0-CO | Administration / Companies | Y | `/companies` | Partial | P0 | List/create OK; deep CoA link via Workspace | Harden multi-company switch UX | Frontend | 2026-07-15 |
| P0-CUR | Financial / Currency | Y | `/currency` | Partial | P0 | List AED/QAR; rates in SAO | Confirm rates UX if needed | Frontend | 2026-07-15 |
| P0-PARTY | Party / Parties | Y | `/parties` | Partial | P0 | List/basic; deep tabs SAO | Party categories/address depth | Frontend | 2026-07-15 |
| P0-PAT | Health / Patients | Y | `/patients` | Partial | P0 | List + detail; insurance/family SAO | Deep demographics Hybrid | Frontend | 2026-07-15 |
| P0-APT | Health / Appointments | Y | `/appointments` | Partial | P0 | Create/list; specialty links Hybrid | Product/insurance linking | Frontend | 2026-07-15 |
| P0-LAB | Health / Laboratory | Y | `/laboratory` | Stub | P0 | Orders list; create-test/results SAO | Workspace CTA + result view later | Frontend | 2026-07-15 |
| P0-RX | Health / Prescriptions | Y | `/medications`, `/pharmacy` | Stub | P0 | Lists; create/dispense wizards SAO | Rx create + stock-move Hybrid | Frontend | 2026-07-15 |
| P0-EVAL | Health / Evaluations | Y | `/evaluations` | Stub | P0 | List/create thin; full form SAO | Harden consultation form | Frontend | 2026-07-15 |
| P0-BED | Health / Beds / Inpatient | Y | `/beds` | Stub | P0 | Bed board thin; admit/transfer SAO | Admit/discharge basics | Frontend | 2026-07-15 |
| P0-FIN | Financial / Invoices | Y | `/financial` | Stub | P0 | List + draft stub; post/pay SAO | Guided Workspace for CoA/post | Frontend | 2026-07-15 |
| P0-USR | Administration / Users | Y | `/users` | Partial | P0 | CRUD light; ACL depth SAO | Groups permissions summary | Frontend | 2026-07-15 |
| P0-SETUP | IST / Setup Hub | N* | `/setup` | Partial | P0 | IST-only hub; SAO for wizards | Keep; link Workspace | Frontend | 2026-07-15 |
| P0-HELP | IST / Help Centre | N* | `/help` | Partial | P0 | React Help; screenshots backlog | Screenshot pack | Docs | 2026-07-15 |
| P0-WS | IST / Workspace (SAO embed) | Y | `/workspace` | Partial | P0 | Embed live; theming via custom.css | Optional ?path= deep-link | Frontend | 2026-07-15 |
| P0-STAFF | Health / Health Professionals | Y | `/staff` | Partial | P0 | List/detail; specialty O2M SAO | Specialty linking | Frontend | 2026-07-15 |
| P0-IMG | Health / Imaging | Y | `/imaging` | Stub | P0 | List; generate-result/Orthanc SAO | Workspace CTA | Frontend | 2026-07-15 |
| P0-NUR | Health / Nursing | Y | `/nursing` | Stub | P0 | List; rounding/stock SAO | Document Hybrid | Frontend | 2026-07-15 |
| P0-PROC | Health / Procedures | Y | `/procedures` | Stub | P0 | List thin | Workspace for deep form | Frontend | 2026-07-15 |
| P0-PROD | Product / Products | Y | `/products` | Partial | P0 | Catalog list; UoM/accounts SAO | Account categories after CoA | Frontend | 2026-07-15 |
| P0-STK | Stock / Inventory | Y | `/stock` | Partial | P0 | Locations/moves list; wizards SAO | Adjustment wizards Workspace | Frontend | 2026-07-15 |
| P0-CAL | Calendar | Y | `/calendar` | Stub | P0 | Thin; events often SAO | Optional if module empty | Frontend | 2026-07-15 |
| P0-MOD | Administration / Modules | Y | `/modules` | Stub | P0 | Mark-only; apply = SAO/admin | Keep Workspace + trytond-admin | Ops | 2026-07-15 |
| P0-GRP | Administration / Groups | Y | `/groups` | Stub | P0 | List; ACL matrix SAO | Summary view | Frontend | 2026-07-15 |
| P0-SEQ | Administration / Sequences | Y | `/sequences` | Partial | P0 | List/edit light | Confirm numbering per company | Frontend | 2026-07-15 |
| P0-CTR | Administration / Countries | Y | `/countries` | Partial | P0 | Read/list | Rarely change | Frontend | 2026-07-15 |
| P0-LANG | Administration / Languages | Y | `/languages` | Partial | P0 | Read/list | Rarely change | Frontend | 2026-07-15 |
| P0-SET | IST / Settings | N* | `/settings` | Partial | P0 | Client settings + SAO URL | Point to Workspace | Frontend | 2026-07-15 |
| P0-MENU | Menus / Model browser | Y | `/menu/:id` | Partial | P0 | Generic act_window; wizards → Workspace | Extend model coverage | Frontend | 2026-07-15 |

\* IST-only screen (no direct SAO menu equivalent); SAO still used for linked wizards via Workspace.

### P0 summary

| Status | Count (approx) |
|--------|----------------|
| Partial | ~16 |
| Stub | ~12 |
| Parity | 0 |
| Missing | 0 in P0 seed (all have a React entry or Workspace) |

**Next builds (suggested order):** lab create-test/results Hybrid → Rx create → evaluation depth → beds admit/discharge → financial post/pay guided Workspace → patient deep tabs.

---

## Backlog buckets (not fully inventoried here)

| Bucket | Source | Default stance |
|--------|--------|----------------|
| Remaining health* specialty (surgery, ICU, genetics, OB, NTD, …) | module-registry.json | Keep-SAO / Workspace; P2–P3 |
| Core account_* / tax / FY wizards | Tryton account | Workspace; React list only |
| ir.ui.menu leaves without React map | Sidebar Menus | Model browser or Workspace |

Update the **xlsx** when scoring changes; keep this markdown as the human-readable P0 snapshot.
