# SAO → React Migration Map (IST Health)

Inventory date: 2026-07-14 (Gap 4 admin parity closed)  
Source: Tryton DB `gnuhealth` on `gnuhealth-his-01` via JSON-RPC  
SAO: `https://health.irisstar.tech/sao/` (nginx; `:8000` closed publicly)  
React: `https://health.irisstar.tech/` after DNS + LE — until then `http://34.18.116.146/` (see `docs/HTTPS.md`)

## Gaps 1–4 summary

| Gap | Scope | Status |
|-----|--------|--------|
| **1** | Create/edit clinical forms (patients, appointments, staff, lab) | **CLOSED** |
| **2** | Seed clinical data | **CLOSED** |
| **3** | HTTPS (self-signed on `:443`) | **CLOSED** |
| **4** | Deep SAO admin wizards / advanced admin parity (practical subset) | **CLOSED** |

## API / session status

Tryton 7 Session auth works:

`Authorization: Session base64(username:uid:sessionToken)`

Proxy: nginx `/api/tryton/` → `http://127.0.0.1:8000/` (path includes DB, e.g. `/api/tryton/isthealth/`)  
SAO proxy: nginx `/sao/` → `http://127.0.0.1:8000/` (same-origin; `:8000` kept as fallback)

Verified live counts (example): parties ≈ 4301, patients ≈ 50, appointments ≥ 1, health professionals ≈ 299.

## Top-level SAO menus (active)

| SAO menu | React coverage |
|----------|----------------|
| Party | `/parties` **Live** |
| Product | `/products` **Live** |
| Financial | `/financial` (list + draft invoice stub + SAO panel) **Live** |
| Currency | `/currency` **Live** |
| Inventory & Stock | `/stock` **Live** |
| Calendar | `/calendar` **Live** (may be empty) |
| Companies | `/companies` **Live** (+ setup wizard when empty) |
| Health | Clinical routes below **Live** |
| Administration | `/users`, `/groups`, `/modules`, `/sequences`, `/countries`, `/languages` **Live** |

## Health → React

| SAO Health menu | Model(s) | React route | Status |
|-----------------|----------|-------------|--------|
| Patients | `gnuhealth.patient`, `party.party` | `/patients` | **Live** |
| Appointments | `gnuhealth.appointment` | `/appointments` | **Live** |
| Health Professionals | `gnuhealth.healthprofessional` | `/staff` | **Live** |
| Prescriptions | `gnuhealth.prescription.order` | `/pharmacy` | **Live** |
| Institutions | `gnuhealth.institution` | `/settings` | **Live** |
| Patient medications | `gnuhealth.patient.medication` | `/medications` | **Live** |
| Patient evaluations | `gnuhealth.patient.evaluation` | `/evaluations` | **Live** |
| Hospital beds / admissions | bed + inpatient | `/beds` | **Live** |
| Nursing | ambulatory + rounding | `/nursing` | **Live** |
| Procedures / surgery | procedure / surgery | `/procedures` | **Live** |
| Laboratory | lab models | `/laboratory` | **Live** |
| Imaging | imaging models | `/imaging` | **Live** |

## Operations / Admin → React (Gap 4)

| Area | Models | Route | Capability |
|------|--------|-------|------------|
| Parties | `party.party` | `/parties` | List |
| Products | `product.template`, `product.product` | `/products` | List |
| Stock | `stock.location`, `stock.move` | `/stock` | List |
| Financial | `account.invoice` | `/financial` | List + draft stub + SAO panel |
| Currency | `currency.currency` | `/currency` | List |
| Calendar | `calendar.calendar`, `calendar.event` | `/calendar` | List |
| Companies | `company.company` + party | `/companies` | List + setup wizard lite |
| Users | `res.user` | `/users` | List / create / edit / groups / password reset |
| Groups | `res.group`, `ir.model.access` | `/groups` | List + users + access summary (RO) |
| Modules | `ir.module` | `/modules` | List + mark activate/upgrade + server instructions |
| Sequences | `ir.sequence` | `/sequences` | List + edit next/prefix/suffix |
| Countries | `country.country` | `/countries` | List + search |
| Languages | `ir.lang` | `/languages` | List |

## Still SAO-only (wizards / deep UI)

React Gap 1 (2026-07-14) closed create/edit for:

| Module | React capability | Still SAO-only |
|--------|------------------|----------------|
| Patients | Create + edit (party + core patient fields) | Full demographics, insurance, family, diseases, vaccinations, photo |
| Appointments | Create + edit | Specialty / insurance / consultation product linking |
| Staff | Create + edit | Main specialty O2M, institution unit |
| Laboratory | Create lab request when model allows | Lab result entry; installs requiring SAO wizard |

Also still SAO-only after Gap 4:

- Chart of accounts from template, journals, fiscal years, tax configuration
- Invoice post / pay / cancel workflows (draft stub only in React)
- Imaging / surgery / admissions / shipment wizards
- UI config (menus, views, actions, icons), record rules editor
- WebDAV shares, Orthanc, federation, specialty packs
- Applying module upgrades (`trytond-admin` / SAO pending upgrades) — React can only *mark* when API allows

Use SAO at `http://34.18.116.146/sao/` or `http://34.18.116.146:8000/` for those. Wizard menu leaves open an **Open in SAO** panel.

## Sidebar: Tryton-like menu tree

1. After login, `MenuTree` calls `ir.ui.menu.search_read` …
2. Mapped models → dedicated React routes via `menuRoutes.ts`
3. Unmapped act_window → `/menu/:menuId`
4. Wizards / reports → **Open in SAO** panel (`SaoPanel` + `/sao/`)

## Gap 4 nginx note (optional hardening)

- `/sao/` proxy is configured so SAO can be reached without exposing `:8000` long-term.
- Binding trytond to `127.0.0.1` and closing GCP firewall `allow-gnuhealth-8000` is recommended **after** verifying `/sao/` works; not applied automatically in this gap to avoid breaking SAO access mid-cutover.

## How to verify

1. Open `http://34.18.116.146/` (or https) — sign in (`admin` / `IstHealth@2026!Admin`).
2. Dashboard shows patient / appointment / staff counts.
3. `/users` — create/edit user; optional password reset.
4. `/groups` — open a group for users + model access summary.
5. `/modules` — list states; try mark activate (then follow server instructions).
6. `/sequences` — edit next number / prefix if writable.
7. `/languages`, `/countries` — lists load.
8. `/companies` — if empty, setup wizard creates IST Technologies LLC + party.
9. `/financial` — list + draft stub (may fail without CoA — use SAO panel).
10. Wizard menu leaf → Open in SAO panel links to `/sao/`.
