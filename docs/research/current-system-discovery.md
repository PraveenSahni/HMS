# IST Health — Current System Discovery

**Discovery date:** 2026-07-14  
**Workspace:** `C:\HMS`  
**Status:** Local evidence complete; live VM module-state verification recommended where marked.

---

## 1. Executive summary

IST Health is a **React replacement UI** over **GNU Health HIS 5 / Tryton 7** hosted on a GCP VM. The frontend does not embed clinical logic; it calls Tryton JSON-RPC. Synthetic data, design tokens, and legal pages already exist under `C:\HMS`. There is **no** top-level `docs/` tree prior to this framework (frontend docs live under `frontend/docs/`). Git status of the workspace is not required for this framework delivery.

---

## 2. Architecture (discovered)

```
┌──────────────────────────────┐     HTTPS / nginx      ┌─────────────────────────────────────┐
│  React SPA (Vite)            │ ─────────────────────► │  GCP VM gnuhealth-his-01            │
│  C:\HMS\frontend             │   /api/tryton/{db}/    │  External IP: 34.18.116.146         │
│  EN/AR + RTL                 │   JSON-RPC 2.0         │  Zone: me-central1-a (Doha)         │
│  Session in localStorage     │                        │  Project: isthealth                 │
└──────────────────────────────┘                        │  ┌─────────────┐  ┌──────────────┐ │
                                                        │  │ nginx       │  │ trytond       │ │
                                                        │  │ :80/:443    │─►│ 127.0.0.1:8000│ │
                                                        │  │ /sao/       │  │ GNU Health 5  │ │
                                                        │  └─────────────┘  └──────┬───────┘ │
                                                        │                          │         │
                                                        │                   PostgreSQL       │
                                                        │                   DB: isthealth    │
                                                        │                   (also gnuhealth) │
                                                        └─────────────────────────────────────┘
```

| Layer | Evidence |
|-------|----------|
| Frontend | React 19 + TypeScript, Vite 8, React Router 7, i18next EN/AR, Tailwind v4 — `frontend/package.json`, `frontend/docs/ARCHITECTURE.md` |
| Design | `design/` tokens synced into `frontend/src/styles/` |
| Backend | Tryton 7 / GNU Health 5 — path `/opt/gnuhealth/his-50/` on VM (scripts, README) |
| DB | PostgreSQL; databases referenced: `isthealth` (primary for React), `gnuhealth` (legacy/install) |
| Auth | `common.authenticate` / Session header; `AuthContext` stores uid+session in localStorage |
| Roles | Tryton `res.user` / `res.group` / `ir.model.access` — React admin pages list/edit; **no custom RBAC layer in React yet** |
| Arabic RTL | `frontend/src/i18n/`, `rtl.css`, `LangSwitch` |
| Legal | `legal/PRIVACY_POLICY.md`, `TERMS_OF_SERVICE.md`, mirrored in `frontend/public/legal/` |

**How the app relates to GNU Health:** thin client. Models are mapped in `frontend/src/lib/tryton/models.ts`. Unmapped SAO menus open `/menu/:menuId` or an “Open in SAO” panel.

---

## 3. Frontend routes (actual)

| Route | Page | GH models (primary) |
|-------|------|---------------------|
| `/login` | LoginPage | auth |
| `/` | DashboardPage | aggregate counts |
| `/patients`, `/patients/:id` | Patients / detail | `party.party`, `gnuhealth.patient` |
| `/appointments` | AppointmentsPage | `gnuhealth.appointment` |
| `/staff`, `/staff/:id` | Staff | `gnuhealth.healthprofessional` |
| `/laboratory` | LaboratoryPage | lab models |
| `/pharmacy` | PharmacyPage | `gnuhealth.prescription.order` |
| `/medications` | MedicationsPage | `gnuhealth.patient.medication` |
| `/evaluations` | EvaluationsPage | `gnuhealth.patient.evaluation` |
| `/beds` | BedsPage | bed + inpatient |
| `/nursing` | NursingPage | rounding / ambulatory |
| `/procedures` | ProceduresPage | surgery / operation |
| `/imaging` | ImagingPage | imaging models |
| `/parties`, `/products`, `/stock`, `/financial`, `/currency`, `/calendar`, `/companies` | OpsPages | party/product/stock/account/… |
| `/users`, `/groups`, `/modules`, `/sequences`, `/countries`, `/languages` | Admin | res.*, ir.* |
| `/settings` | SettingsPage | `gnuhealth.institution` |
| `/menu/:menuId` | ModelBrowserPage | dynamic act_window |

---

## 4. GNU Health version and modules

### 4.1 Version (local evidence)

| Item | Value | Confidence |
|------|-------|------------|
| HIS major | **GNU Health 5.0** (`his-50` path) | High (scripts/docs) |
| Framework | **Tryton 7.0 LTS** | High (ARCHITECTURE, SAO_MIGRATION, official docs) |
| Exact patch (e.g. 5.0.x) | **Needs VM verification** (`pip show` / `trytond --version`) | Low |

Official source: [GNU Health HIS Features](https://docs.gnuhealth.org/his/features.html), [Changelog](https://docs.gnuhealth.org/his/changelog.html) — GH 5.0 uses Tryton 7.0.

### 4.2 Modules referenced for activation (repo scripts)

From `frontend/scripts/activate_modules.sh` (intended activation set — **not a live DB dump**):

**Tryton deps:** `account`, `account_product`, `account_invoice`, `stock`, `stock_lot`

**Core clinical batch:**  
`health_lab`, `health_nursing`, `health_inpatient`, `health_surgery`, `health_imaging`, `health_icu`, `health_gyneco`, `health_pediatrics`, `health_lifestyle`, `health_socioeconomics`, `health_history`, `health_disability`, `health_ophthalmology`, `health_dentistry`, `health_ems`, `health_genetics`, `health_qrcodes`, `health_reporting`, `health_calendar`, `health_crypto`, `health_services`, `health_services_lab`, `health_services_imaging`, `health_stock`, `health_stock_inpatient`, `health_stock_nursing`, `health_stock_surgery`, `health_surgery_protocols`, `health_imaging_worklist`, `health_inpatient_calendar`, `health_insurance`, `health_crypto_lab`

**Also historically planned (install notes):** `health`, `health_calendar`, `health_services`, `health_accounting`, `health_stock`, plus package `all` for training/POC (50+ packages on disk).

**Additional packages present in official GH 5 catalog (may be installed on VM even if not in activate script):**  
`health_archives`, `health_caldav`, `health_contact_tracing`, `health_federation`, `health_genetics_uniprot`, `health_icd9procs`, `health_icd10`, `health_icd11`, `health_icpm`, `health_icd10pcs`, `health_iss`, `health_mdg6`, `health_ntd*`, `health_orthanc`, `health_pediatrics_growth_charts*`, `health_profile`, `health_webdav3_server`, `health_who_essential_medicines`, `health_imaging_orthanc` (naming per PyPI/docs).

### 4.3 Module → React status (local docs; ARCHITECTURE vs SAO_MIGRATION)

| Area | Local note |
|------|------------|
| Patients / appointments / staff / pharmacy / evaluations / beds | Live in React |
| Laboratory / nursing / procedures / imaging | Live routes; graceful “module missing” if models absent |
| Financial deep wizards | Draft stub + SAO panel |
| Custom Tryton modules in repo | **None** found under `C:\HMS` |

**VM verification required:**

```bash
gcloud compute ssh gnuhealth-his-01 --project=isthealth --zone=me-central1-a \
  --command "sudo -u postgres psql -d isthealth -c \"SELECT name, state FROM ir_module WHERE name LIKE 'health%' ORDER BY state, name;\""
```

---

## 5. Synthetic data (existing)

| Item | Location |
|------|----------|
| Entry | `run_synthetic_data.py` |
| Package | `synthetic_data/` |
| Config | `config.yaml` (patients: 4000, staff: 300, seed: 42) |
| Markers | Code prefixes `IST-P-*`, comments `IST synthetic: …` |
| Idempotent | Yes (default) |
| Dry-run | `--dry-run` (connection validate only) |

Company: **IST Technologies LLC** (Doha primary; UAE Dubai office in config). Synthetic IDs only — no real Emirates/Qatar national IDs.

---

## 6. Auth, tenancy, isolation

| Topic | Current state |
|-------|---------------|
| Multi-company | Tryton `company.company` supported; React `/companies` wizard lite |
| Tenant isolation UAE vs QA | **Not implemented** as separate DBs/companies in frontend — single demo company Qatar-centric |
| Record rules | Managed in Tryton; React does not configure them |
| Session secrets | Password may be held in localStorage (MVP) — flagged as Phase-2 security debt |

---

## 7. Gaps relevant to UAE/Qatar framework

1. No HIE connectors (NABIDH / Malaffi / Riayati / Qatar HIE).  
2. No FHIR/HL7 interface layer in repo.  
3. No formal org hierarchy (group → country entity → facility) beyond single institution.  
4. Help Centre delivered (`/help`, `/help/admin`) with EN/AR content, 26 guided workflows, feedback, onboarding, publish flag — redeploy frontend to refresh production static assets when content changes.  
5. Live activated-module inventory still needs VM query (section 4.3) — local evidence lists intended activation set + official catalog extras, not a live `ir.module` dump.  
6. Regulatory obligations need legal confirmation (see research matrix).  
7. Tenant record rules for UAE↔Qatar isolation are designed in config/docs but **not deployed** to Tryton.

---

## 8. Assumptions

- Production DB name for the React app is **`isthealth`** (`config.yaml`, nginx docs).  
- GNU Health will **not** be upgraded as part of this work.  
- Partner review HTML/DOC exist for feature discussion; they are marketing/review aids, not source of truth for installed modules.

---

## 9. Next actions (ops)

1. Run VM module state query (section 4.3).  
2. Confirm exact GH patch version.  
3. Confirm which DB (`isthealth` vs `gnuhealth`) is the production instance.  
4. Engage compliance for UAE PDPL / Qatar PDPPL health-data permits before any real patient data.
