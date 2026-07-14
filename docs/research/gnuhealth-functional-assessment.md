# GNU Health Functional Assessment — IST Health Context

**Basis:** Official package descriptions ([SRC-GH-01](https://docs.gnuhealth.org/his/features.html)) + local React/model mapping.  
**Constraint:** Capabilities below are those of **upstream GNU Health HIS 5**; IST React coverage may be partial. Do not invent features not documented upstream.

## Core clinical

| Capability | GH package(s) | Upstream support | IST React | Notes |
|------------|---------------|------------------|-----------|-------|
| Demographics / patients | `health` | Full | Live | `gnuhealth.patient` |
| Appointments | `health`, `health_calendar` | Full | Live | Calendar views may need SAO |
| Evaluations / encounters | `health` | Full | Live (subset) | Deep history still SAO |
| Prescriptions | `health` | Full | Live | |
| Medicaments | `health`, `health_who_essential_medicines` | Full | Partial | Catalog via products |
| Lab LIMS | `health_lab` (+ services/crypto) | Full | Live if activated | |
| Imaging | `health_imaging`, Orthanc/worklist | Full | Live if activated | DICOM worklist separate |
| Inpatient / beds | `health_inpatient` | Full | Live | |
| Nursing | `health_nursing` | Full | Live if activated | |
| Surgery | `health_surgery` (+ protocols/stock) | Full | Live if activated | |
| ICU | `health_icu` | Full | Not dedicated UI | Use SAO / ModelBrowser |
| Insurance | `health_insurance` | Full | Not dedicated UI | |
| Stock / pharmacy logistics | `health_stock*` + Tryton stock | Full | List views | |
| Accounting / invoices | `health_accounting` + account_* | Full | Draft stub | |
| Reporting / QR | `health_reporting`, `health_qrcodes` | Full | Not dedicated | |
| Crypto / signatures | `health_crypto*` | Documented | Not in React | Needs plugin testing |
| Federation | `health_federation` | Documented | Not used | |
| ICD catalogs | `health_icd10`, `health_icd11`, … | Catalogs | Not dedicated UI | Licensing confirmation needed |

## Gaps vs UAE/Qatar production expectations

| Expectation | GH native | Gap | Proposed action |
|-------------|-----------|-----|-----------------|
| Emirates ID / Qatar ID validation | Generic party identifiers | No local national-ID validators in GH/React | Custom fields + validation service — **legal rules TBD** |
| NABIDH / Malaffi / Riayati | None | No HIE connectors | Interface layer (HL7/FHIR) — see interoperability assessment |
| Arabic clinical UI | Tryton translations vary | React has EN/AR shells | Expand clinical translation packs |
| Multi-emirate / multi-country tenancy | Tryton multi-company | Not configured for UAE+QA split | Org model in implementation guide |
| Claims / eClaimLink | None native | Major | Partner/claims engine — **needs confirmation** |

## Verification rule

Before claiming a module is “installed and activated,” query `ir.module` on the live DB. Package presence on disk ≠ activated.
