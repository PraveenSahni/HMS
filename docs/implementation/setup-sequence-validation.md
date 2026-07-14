# Setup sequence validation — IST Health vs GNU Health HIS

**Date accessed (official docs):** 2026-07-14  
**Validator:** Cross-check of IST onboarding checklist / Setup Hub order against [docs.gnuhealth.org/his](https://docs.gnuhealth.org/his/)  
**IST artefacts:** `docs/implementation/module-setup-dependencies.md`, Help `onboarding-checklist` / `wf-system-setup`, `SetupHubPage`  
**Discovery context:** `docs/research/current-system-discovery.md`

---

## Verdict

**MOSTLY CORRECT** for GNU Health HIS / Tryton dependency practice.

The numbered order **Companies → Currency → Administration → Party → Product → Inventory & Stock → Calendar → Financial → Health** matches official post-install and module dependency guidance. No reorder of steps 1–9 is required. Soft clarifications (institution timing, currency install-at-DB, Calendar optional) are documented below; checklist content already covers them adequately.

---

## Official doc findings

Primary sources (paraphrased; accessed 2026-07-14):

### Post-install configuration order

From [Vanilla Installation — Creating a Company](https://docs.gnuhealth.org/his/techguide/installation/vanilla.html):

1. After DB create and login, **create the initial company** (wizard); that company “will be your health center.”
2. On the company party, set the **institution** attribute; link to the main health institution later.
3. Optionally create **new instance users** (can skip initially).
4. Activate extra packages via **Administration → Modules**.

DB instance creation already **installs currencies and countries** with the core health package.

### Health institution

From [Health Institutions](https://docs.gnuhealth.org/his/userguide/basics/coremodule/healthinstitutions.html):

> The Health Institution plays a central role in GNU Health. As a matter of fact, [it] is the first thing you will have to create in the installation. The very first health institution that you create is special because it is also your company.

Institution facilities (buildings, wards, beds, ORs, units) are configured under Health → Configuration → Institutions. **Beds** require Product (+ variant) records before bed records ([same page](https://docs.gnuhealth.org/his/userguide/basics/coremodule/healthinstitutions.html)).

### Party → Patient

From [First Steps](https://docs.gnuhealth.org/his/userguide/basics/firststeps.html) and [Patient Management](https://docs.gnuhealth.org/his/userguide/patientmanagement/patientmanagement.html):

- A **party** is the legal/entity unit (patients, companies, health professionals, health centers).
- Patients are parties with Person + Patient properties; the patient record **requires** a linked party with the patient attribute.

### Product → Stock / Medicaments / Invoicing

From [Products and Services Management](https://docs.gnuhealth.org/his/userguide/healthcenter/products.html):

- Products are basic Tryton master data; needed for invoices and medicaments.
- Medicament products must be created in Product **before** Health → Configuration → Medicaments.
- Invoicing via Health Services needs product **Account Revenue / Expense** and party **Customer Payment Term** (implies CoA / financial config before successful invoice post).

### Stock

From [Stock Management](https://docs.gnuhealth.org/his/userguide/modules/stockmanagement.html):

- Stock tracks products **within a company**; locations under Inventory & Stock → Locations.
- Especially useful for pharmacy medicaments → company + products first.

### Administration (users / groups)

From [Access Management](https://docs.gnuhealth.org/his/userguide/healthcenter/accessmanagement.html):

- Groups and users under Administration → Users; assign groups so users can work.
- Users are login accounts; link to a Person (party) via Internal User when needed.

### Calendar

From [Calendar and WebDAV](https://docs.gnuhealth.org/his/techguide/administration/calendarwebdav.html):

- Optional packages (`health_calendar`, CalDAV/WebDAV). Create calendars under Calendar → Calendars and assign to users.
- Appointments exist in Health without requiring calendar master records ([Appointments](https://docs.gnuhealth.org/his/userguide/patientmanagement/patientappointment.html)).

### Financial

[Financial Accounting](https://docs.gnuhealth.org/his/userguide/healthcenter/financialaccounting.html) is largely a **TODO** stub in official HIS docs. Dependency evidence comes from Products invoicing (accounts on products, payment terms on parties) and Tryton `account` / `company` model practice: **company + currency before CoA/FY/journals**.

### Features / packages

From [Features](https://docs.gnuhealth.org/his/features.html): `health_accounting`, `health_services`, `health_stock`, etc. extend billing and stock; core `health` covers demographics, patients, appointments, institutions, medicaments, HPs.

---

## Step-by-step validation table

| # | IST checklist step | Rating | Reason from GH docs |
|---|-------------------|--------|---------------------|
| 1 | Companies — UAE AED / Qatar QAR | **OK** | Vanilla: create company first after login; institution attribute on company party. Multi-entity = separate `company.company` records (Tryton/IST practice). |
| 2 | Currency — confirm AED / QAR | **OK** | Currencies installed at DB create; company assigns currency. Confirm/create-if-missing is correct (not a invent-from-scratch-first step). |
| 3 | Administration — users, groups, sequences | **OK** | Vanilla: users after company; Modules activation under Administration. Access Management: groups then users. Sequences are Tryton `ir.sequence` for numbering (standard ops). |
| 4 | Party — master parties | **OK** | Party is foundational; patients/HPs/insurers/suppliers are parties. Company already created a party; further masters follow. |
| 5 | Product — catalogs | **OK** | Products required before medicaments import, bed variants, stock moves, invoice lines. |
| 6 | Inventory & Stock — locations under company | **OK** | Stock is company-scoped; needs products. Pharmacy use case documented. |
| 7 | Calendar — if module used | **OK (optional)** | Calendar/WebDAV is optional; appointments work via Health appointments. Correctly late / optional in order. |
| 8 | Financial — CoA/FY in SAO; draft invoice smoke | **OK** | Company+currency first; product/party accounting fields needed before successful Health Services invoicing. Official CoA chapter incomplete — SAO for deep setup matches Tryton reality. |
| 9 | Health — institution, patients, appointments (+ lab/Rx/beds) | **OK** | Patients after party; beds after product+institution; lab/Rx after products (+ stock for dispense). Institution *record* is tightly coupled with company (step 1) — IST already notes institution early in `module-setup-dependencies.md` §3.9 / mermaid. |

**Preamble / post (Help):** Sign in, Help filters, Setup Hub; find synthetic patient, appointments, `wf-system-setup`, synthetic policy — **OK** (IST operational layer; not contradicted by GH).

---

## Recommended corrected sequence

**No change to the numbered 1–9 order.** Soft operator notes only (already reflected in IST deps doc):

1. Companies *(create company party with institution attribute; link `gnuhealth.institution`)*  
2. Currency *(confirm AED/QAR)*  
3. Administration  
4. Party  
5. Product  
6. Inventory & Stock  
7. Calendar *(skip if unused)*  
8. Financial  
9. Health *(patients, appointments, lab/Rx/beds; complete institution facilities)*

---

## Gaps vs official HIS (checklist omissions)

GH docs describe configuration items IST onboarding does not list as separate numbered steps (acceptable if covered inside Health/Admin/SAO):

| Gap | Official source | IST handling |
|-----|-----------------|--------------|
| Explicit **Health Professionals** (party + HP record, specialty, institution) | [Configuration — Health Professionals](https://docs.gnuhealth.org/his/userguide/basics/configuration.html) | Implied via staff / appointments; not a numbered checklist step |
| **Medicaments** import after Product | [Products](https://docs.gnuhealth.org/his/userguide/healthcenter/products.html), Configuration → Medicaments | Under Product / Pharmacy scope |
| **Lab Test Types / units** | Configuration → Laboratory | Under Health → laboratory |
| **Insurance companies / plans** | Configuration → Misc → Insurances | Not in 1–9; claims gap elsewhere |
| **Party payment terms** / product revenue-expense accounts before invoice | Products invoicing section | Financial + Party/Product SAO |
| **Module package selection** (minimal packages) | Vanilla — Choosing additional packages | Administration → modules |
| **Federation / Thalamus / PMI** | First Steps ecosystem | Out of scope for HIS sidebar onboarding |
| **Countries / languages** | Installed with instance; Admin menus | Admin routes exist; not numbered |

None of these require reordering Companies→…→Health.

---

## Cross-check: claimed IST order vs discovery

| Source | Order |
|--------|--------|
| `module-setup-dependencies.md` §2 | 1–9 identical |
| Setup Hub `MODULES` | 1–9 identical |
| Help `onboarding-checklist` / `wf-system-setup` / `setup-order` | Same narrative |
| `current-system-discovery.md` | Routes/models align; no alternate order |

Typical Tryton pattern (company → accounting → party → product → stock → domain modules) is satisfied: Financial is before Health billing, after master data; CoA can still be completed in SAO as soon as company+currency exist (operators may run CoA earlier without breaking the checklist).

---

## Action taken

- Sequence **not** rewritten in Help / Setup Hub / `module-setup-dependencies.md` (already aligned).
- This evidence file created: `docs/implementation/setup-sequence-validation.md`.

---

## References (URLs)

- https://docs.gnuhealth.org/his/
- https://docs.gnuhealth.org/his/techguide/installation/vanilla.html
- https://docs.gnuhealth.org/his/userguide/basics/coremodule/healthinstitutions.html
- https://docs.gnuhealth.org/his/userguide/basics/firststeps.html
- https://docs.gnuhealth.org/his/userguide/basics/configuration.html
- https://docs.gnuhealth.org/his/userguide/patientmanagement/patientmanagement.html
- https://docs.gnuhealth.org/his/userguide/patientmanagement/patientappointment.html
- https://docs.gnuhealth.org/his/userguide/healthcenter/products.html
- https://docs.gnuhealth.org/his/userguide/healthcenter/accessmanagement.html
- https://docs.gnuhealth.org/his/userguide/modules/stockmanagement.html
- https://docs.gnuhealth.org/his/techguide/administration/calendarwebdav.html
- https://docs.gnuhealth.org/his/userguide/healthcenter/financialaccounting.html
- https://docs.gnuhealth.org/his/features.html
