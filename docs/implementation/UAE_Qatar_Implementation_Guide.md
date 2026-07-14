# UAE & Qatar Implementation Guide — IST Health

**Version:** 1.0.0  
**Date:** 2026-07-14  
**Stack:** GNU Health HIS 5 / Tryton 7 + IST React frontend  
**Rule:** Do not upgrade GNU Health/Tryton in this program without CAB.

## 1. Purpose

Deliver a production-quality implementation framework for multi-country (UAE + Qatar) healthcare operations on the existing IST Health platform, with governance, master data, synthetic factories, help, and security artefacts.

## 2. Principles

- Prefer reusable services (integration, identity, audit) over one-off scripts.
- Never use real Emirates ID, Qatar ID, passports, or real phones/emails in non-prod.
- Mark all synthetic rows (`synthetic_data=true` or code prefix markers).
- Do not fabricate regulatory requirements; uncertain items require legal/authority confirmation.
- Do not invent GNU Health capabilities; verify against docs/VM.

## 3. Organization model & tenant isolation

```
IST Health Group
├── Legal Entity — UAE (AED)
│   ├── Hospitals / Clinics / Labs / Pharmacies / Warehouses / Finance
│   └── Emirate attributes (Dubai / Abu Dhabi / Northern)
└── Legal Entity — Qatar (QAR)
    └── Hospitals / Clinics / Labs / Pharmacies / Warehouses / Finance
```

**Isolation approach (proposed):**

| Layer | Mechanism | Status |
|-------|-----------|--------|
| Legal entity | `company.company` per country | To configure |
| Facility | `gnuhealth.institution` (+ units) | Partial (single demo) |
| Data | Tryton record rules by company/institution | To design |
| UI | Country/role context in Help + future filters | Help awareness added |
| DB | Prefer single DB multi-company first; separate DB only if mandated | Confirm with security |

Cross-entity clinical chart sharing must be an explicit clinical/legal decision.

## 4. UAE vs Qatar configuration differences

| Topic | UAE | Qatar |
|-------|-----|-------|
| Currency | AED | QAR |
| HIE | NABIDH / Malaffi / Riayati — **confirm per facility** | MoPH e-health — **confirm** |
| National ID | Emirates ID rules — **confirm**; demos use `SYN-AE-########` | Qatar ID — **confirm**; demos use `SYN-QA-########` |
| Language | EN + AR | EN + AR |
| Privacy law | UAE PDPL — **confirm scope** | PDPPL Law 13/2016 — **confirm** |
| Claims | eClaim/schemes — **confirm** | Local insurance — **confirm** |

## 5. Phases 1–22

### Phase 1
Discovery & baseline (architecture, modules, VM verification).

### Phase 2
Regulatory & privacy kickoff (UAE/QA counsel; classify needs-confirmation items).

### Phase 3
Org model design: Group → UAE/QA legal entities → facilities.

### Phase 4
Environment strategy (dev/test/uat/prod) and synthetic-data gates.

### Phase 5
Tryton company/institution/units configuration (no GH upgrade).

### Phase 5b — Financial setup (per legal company)
CoA from template, fiscal year/periods, journals, party receivable/payable, AED/QAR currency.  
Taxes and healthcare exemptions: **needs confirmation** — do not invent rates.  
Runbook: `docs/implementation/financial-setup.md`. React `/financial` is invoice stub; deep accounting is SAO.  
Help guided workflow: `wf-finance-setup`.

### Phase 6
Master data collection via Excel template + questionnaire.

### Phase 7
Role packs & access matrix (res.group / record rules).

### Phase 8
Clinical catalog: specialties, products, lab types, sequences.

### Phase 9
UAE-specific config (emirate, HIE readiness flags) — pending authority confirmation.

### Phase 10
Qatar-specific config (MoPH facility codes) — pending confirmation.

### Phase 11
Arabic/EN localization & RTL QA.

### Phase 12
Synthetic data load (deterministic, idempotent) in non-prod.

### Phase 13
Integration design (HL7/FHIR adapter) — no production HIE without approval.

### Phase 14
Security controls (TLS, backups, audit, session hardening).

### Phase 15
UAT with role-based scenarios + Help Centre guided workflows.

### Phase 16
Training & user guides sign-off.

### Phase 17
Cutover rehearsal / rollback plan.

### Phase 18
Production import (CAB + --allow-production).

### Phase 19
Hypercare (30 days).

### Phase 20
HIE onboarding (if mandated) with partner.

### Phase 21
Continuous compliance review (PDPL/PDPPL).

### Phase 22
Optimization & reporting handover.


## 6. Governance

### RACI (summary)

| Activity | Sponsor | Compliance | Clinical | Engineering | Ops |
|----------|---------|------------|----------|-------------|-----|
| Regulatory interpretation | A | R | C | I | I |
| Org / tenant model | A | C | C | R | C |
| Master data quality | C | C | A/R | C | I |
| Synthetic loads | I | C | C | R | A |
| HIE go-live | A | R | C | R | C |
| Production import | A | R | C | R | R |

### Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Assuming HIE mandates without confirmation | Legal/ops | Source register + counsel |
| Cross-country data leakage | High | Record rules + company split |
| Real PII in demos | High | Import gates + synthetic markers |
| GH upgrade drift | High | Freeze version; CAB only |
| localStorage session secrets | Medium | Phase-2 auth hardening |

## 7. Master data & questionnaire

- Excel: `templates/Healthcare_Implementation_Master_Data.xlsx` (sheets 6.1–6.10)
- Questionnaire: `templates/Healthcare_Implementation_Questionnaire.docx`
- Validate: `python scripts/implementation/validate_master_data.py …`

## 8. Synthetic data

See `docs/implementation/synthetic-data-guide.md` and `data-import-runbook.md`.  
Demo config: `config/synthetic/uae_qatar_demo.yaml`.

## 9. Help & training

React Help Centre loads Markdown/JSON from `frontend/help-content/{en|ar}/`.  
Role guides: `docs/user-guides/`.  
Finance setup: Help topic `wf-finance-setup` + runbook `docs/implementation/financial-setup.md`.

## 10. Exit criteria (go-live)

- [ ] Legal confirmation logged for open regulatory items or risk acceptance
- [ ] Tenant isolation test passed
- [ ] Synthetic gate blocks prod without override
- [ ] UAT sign-off by role
- [ ] Backup/restore drill evidenced
- [ ] No unapproved GH/Tryton upgrade
- [ ] Financial setup complete per company (CoA, open period, journals) or deferred with risk acceptance; tax rules confirmed or explicitly marked needs confirmation
