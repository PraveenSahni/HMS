#!/usr/bin/env python3
"""Generate Phase 2 research Markdown deliverables for UAE/Qatar IST Health framework."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs" / "research"
OUT.mkdir(parents=True, exist_ok=True)


def write(name: str, body: str) -> Path:
    path = OUT / name
    path.write_text(body.strip() + "\n", encoding="utf-8")
    print(f"Wrote {path}")
    return path


def source_register() -> None:
    write(
        "source-register.md",
        """
# Source Register — UAE / Qatar / GNU Health / Interoperability

**Compiled:** 2026-07-14  
**Purpose:** Traceable official and primary references for implementation research.  
**Disclaimer:** Citations support planning only. Binding obligations require confirmation from counsel and the competent authority.

| ID | Topic | Authority / Publisher | Title / Description | URL | Retrieved | Notes |
|----|-------|----------------------|---------------------|-----|-----------|-------|
| SRC-GH-01 | GNU Health modules | GNU Solidario | HIS Features — package catalog | https://docs.gnuhealth.org/his/features.html | 2026-07-14 | Official module descriptions |
| SRC-GH-02 | GNU Health version | GNU Solidario | HIS Changelog — 5.0 / Tryton 7.0 | https://docs.gnuhealth.org/his/changelog.html | 2026-07-14 | Confirms Tryton 7.0 LTS |
| SRC-GH-03 | Imaging package | PyPI / GNU Health | gnuhealth-imaging | https://pypi.org/project/gnuhealth-imaging/ | 2026-07-14 | Package metadata |
| SRC-GH-04 | Lab userguide | GNU Solidario | Laboratory module guide | https://docs.gnuhealth.org/his/userguide/modules/laboratory.html | 2026-07-14 | LIMS workflows |
| SRC-GH-05 | Dev migration | Codeberg | HIS developer corner (5.0 modules) | https://codeberg.org/gnuhealth/his/wiki/GNU-Health-HIS-developer%27s-corner | 2026-07-14 | Module migration list |
| SRC-UAE-01 | National HIE | MOHAP | Riayati / Malaffi / Nabidh integration announcement | https://mohap.gov.ae/en/w/uae-health-authorities-announce-successful-integration-between-riayati-malaffi-and-nabidh- | 2026-07-14 | Policy context |
| SRC-UAE-02 | Riayati standards | MOHAP | Riayati Integration Terminology and Coding Standards v2.1 | https://mohap.gov.ae/documents/20117/674129/Riayati_Integration_Terminology_and_Coding_Standards_v2.1.pdf/14228d81-1e58-8ffc-91d1-a675bf240e6f | 2026-07-14 | HL7v2 / FHIR / IHE — confirm currency with MOHAP |
| SRC-UAE-03 | Nabidh standards | DHA | Standards for Interoperability and Data Exchange | https://dha.gov.ae/uploads/102022/NABIDH%20Policies%20&%20Standards%20-%20Interoperability%20and%20Data%20Exchange%20Standards2022100429.pdf | 2026-07-14 | Oct 2022 PDF |
| SRC-UAE-04 | Nabidh IG | DHA | NABIDH integration implementation guidelines | https://nabidh.dha.gov.ae/cms/uploads/2e7d1d314895443b98019bd4c6e0acfc.pdf | 2026-07-14 | HL7 v2.5 / C-CDA |
| SRC-UAE-05 | Malaffi | DoH Abu Dhabi | Malaffi / Riayati integration news | https://www.malaffi.ae/dohs-malaffi-and-mohap-announce-the-completion-of-the-latest-phase-of-riayati-integration/ | 2026-07-14 | HIE program context |
| SRC-UAE-06 | UAE PDPL | UAE Federal | Federal Decree-Law No. 45 of 2021 (PDPL) | Official gazette / UAEPASS counsel copy | — | **Needs legal confirmation** of applicability to health providers & exemptions |
| SRC-QA-01 | Qatar PDPPL | State of Qatar | Law No. 13 of 2016 — Personal Data Privacy Protection | Official gazette; secondary summaries exist | — | Health = special nature data; **needs counsel** |
| SRC-QA-02 | Qatar MoPH | MoPH | Ministry of Public Health — facility licensing / e-health strategy | https://www.moph.gov.qa/ | 2026-07-14 | Confirm specific HIS mandates with MoPH |
| SRC-INT-01 | HL7 | HL7 International | HL7 Version 2 / FHIR licensing & trademarks | https://www.hl7.org/ | 2026-07-14 | Trademark/use policies apply |
| SRC-INT-02 | FHIR | HL7 | FHIR specification | https://hl7.org/fhir/ | 2026-07-14 | Open specification; implementation guides may have terms |
| SRC-INT-03 | DICOM | NEMA | DICOM Standard | https://www.dicomstandard.org/ | 2026-07-14 | Free standard; implementer obligations apply |
| SRC-INT-04 | ICD | WHO | ICD-10 / ICD-11 licensing | https://www.who.int/standards/classifications/classification-of-diseases | 2026-07-14 | National licensing may apply for commercial use — **confirm** |
| SRC-INT-05 | SNOMED CT | SNOMED International | Affiliate / national member licensing | https://www.snomed.org/ | 2026-07-14 | UAE/Qatar membership status — **confirm** |
| SRC-INT-06 | LOINC | Regenstrief | LOINC license | https://loinc.org/license/ | 2026-07-14 | Free with attribution conditions |
| SRC-LOCAL-01 | IST discovery | IST | current-system-discovery.md | docs/research/current-system-discovery.md | 2026-07-14 | Local architecture evidence |

## Licensing notes (non-exhaustive)

| Standard | Typical commercial HIS note | Action |
|----------|----------------------------|--------|
| HL7 / FHIR | Specs generally free to implement; logos/trademarks restricted | Follow HL7 IP policy |
| DICOM | Standard freely available | Follow NEMA terms |
| ICD-10/11 | WHO; countries often regulate commercial redistribution | Confirm with WHO national focal point |
| SNOMED CT | Requires affiliate license via national release center | Confirm UAE & Qatar membership |
| LOINC | Free with license conditions | Retain attribution |

Items marked **confirm** must not be treated as final compliance advice.
""",
    )


def functional_assessment() -> None:
    write(
        "gnuhealth-functional-assessment.md",
        """
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
""",
    )


def dependency_map() -> None:
    write(
        "gnuhealth-module-dependency-map.md",
        """
# GNU Health Module Dependency Map (Planning)

**Source:** Official features list + IST `activate_modules.sh` batching.  
**Note:** Exact Tryton `depends` graphs should be verified from installed `tryton.cfg` on the VM. This map is a **planning** view, not a dump of `ir.module.dependency`.

```mermaid
flowchart TB
  subgraph core [Core]
    health[health]
  end
  subgraph clinical [Clinical extensions]
    lab[health_lab]
    img[health_imaging]
    inp[health_inpatient]
    nurs[health_nursing]
    surg[health_surgery]
    icu[health_icu]
    ped[health_pediatrics]
    gyn[health_gyneco]
  end
  subgraph services [Services and stock]
    svc[health_services]
    svclab[health_services_lab]
    svcimg[health_services_imaging]
    stock[health_stock]
    stocki[health_stock_inpatient]
    stocks[health_stock_surgery]
  end
  subgraph tryton [Tryton enterprise]
    account[account / invoice]
    tstock[stock / stock_lot]
  end
  subgraph coding [Coding]
    icd10[health_icd10]
    icd11[health_icd11]
  end
  health --> lab
  health --> img
  health --> inp
  health --> nurs
  health --> surg
  health --> icu
  health --> ped
  health --> gyn
  health --> svc
  health --> stock
  health --> icd10
  health --> icd11
  lab --> svclab
  img --> svcimg
  svc --> svclab
  svc --> svcimg
  inp --> stocki
  surg --> stocks
  stock --> tstock
  svc --> account
```

## Activation order (IST script)

1. Tryton: `account`, `account_product`, `account_invoice`, `stock`, `stock_lot`  
2. Clinical core batch (see discovery doc)  
3. Remaining `health_*` not yet activated  

## Custom modules

None in `C:\\HMS`. Future UAE/QA connectors should be **separate** Tryton modules or an external integration service — do not fork core `health` without a governance decision.
""",
    )


def gap_analysis() -> None:
    write(
        "gap-analysis-uae-qatar.md",
        """
# Gap Analysis — UAE & Qatar vs IST Health / GNU Health

**Date:** 2026-07-14  
**Method:** Map regulatory/program expectations (official sources where cited) to current IST stack. Uncertain legal items marked **needs legal confirmation**.

## Target architecture (proposed)

```mermaid
flowchart LR
  subgraph group [IST Health Group]
    HQ[Group governance]
  end
  subgraph uae [UAE Entity]
    DXB[Dubai facilities]
    AUH[Abu Dhabi facilities]
    NE[Northern Emirates facilities]
  end
  subgraph qa [Qatar Entity]
    DOH[Doha clinics / hospitals]
  end
  subgraph platforms [Platforms]
    GH[GNU Health Tryton 7]
    UI[IST React UI]
    INT[Integration layer TBD]
  end
  subgraph hie [External HIE / claims]
    NAB[NABIDH DHA]
    MAL[Malaffi DoH]
    RIY[Riayati MOHAP]
    QHIE[Qatar MoPH / national e-health TBD]
  end
  HQ --> uae
  HQ --> qa
  uae --> GH
  qa --> GH
  UI --> GH
  GH --> INT
  INT --> NAB
  INT --> MAL
  INT --> RIY
  INT --> QHIE
```

## Gap register (summary)

| ID | Requirement | Country | Authority | Mandatory? | GH support | Gap | Action |
|----|-------------|---------|-----------|------------|------------|-----|--------|
| G-01 | Connect to Dubai HIE (NABIDH) if licensed in Dubai | UAE-DXB | DHA | **Needs confirmation** per facility license | None | No HL7/FHIR gateway | Design interface; engage DHA onboarding |
| G-02 | Abu Dhabi HIE (Malaffi) | UAE-AUH | DoH | **Needs confirmation** | None | Same | Engage Malaffi / DoH |
| G-03 | Federal HIE (Riayati) / NUMR | UAE | MOHAP | **Needs confirmation** | None | Same | Align coding standards doc v2.1 |
| G-04 | HL7 v2 and/or FHIR for HIE | UAE | DHA/MOHAP docs | Recommended in published standards | None native as HIE client | Build/buy interface engine | Prefer reusable integration service |
| G-05 | C-CDA clinical documents | UAE-DXB | DHA NABIDH IG | Per IG — confirm | None | Document generation | Map evaluations/labs → C-CDA |
| G-06 | Terminology (ICD, LOINC, SNOMED…) | UAE | Riayati coding standards | Per program | ICD modules available; SNOMED/LOINC not verified | Licensing + maps | Confirm licenses; map catalogs |
| G-07 | Qatar facility licensing / MoPH e-health | QA | MoPH | **Needs confirmation** | Partial HIS | Unknown mandate set | Formal MoPH inquiry |
| G-08 | Qatar PDPPL special-nature health data | QA | NDPO / NCSA | Likely applicable — **confirm** | Technical controls partial | DPIA, permits, retention | Security controls doc + counsel |
| G-09 | UAE PDPL sensitive personal data | UAE | Federal PDPL | **Needs confirmation** of scope/exemptions | Partial | Same | Counsel + DPIA |
| G-10 | National ID capture rules | UAE/QA | Multiple | **Needs confirmation** | Generic IDs only | Validation & consent UX | Synthetic formats only in demos |
| G-11 | Bilingual clinical documentation | Both | Practice / regulator TBD | Recommended | Partial | Translation completeness | Expand i18n |
| G-12 | Multi-entity tenant isolation | Both | Governance | Recommended | Tryton company/rules unused | Cross-entity leakage risk | Org model + record rules |
| G-13 | Audit logging for clinical access | Both | Privacy laws | Likely expected — **confirm** | Tryton history partial | No dedicated privacy audit UI | Enhance logging |
| G-14 | Claims / insurance e-submission | UAE | eClaim / DHA schemes | **Needs confirmation** | `health_insurance` local only | No e-claim connector | Partner integration |
| G-15 | DICOM / PACS | Both | Clinical ops | Optional unless imaging | Orthanc package exists | Not wired in IST React | Optional Orthanc deploy |

## Priority remediation

1. **Governance:** Legal confirmation of G-01…G-09, G-14.  
2. **Tenancy:** Implement group → UAE/QA → facility model (implementation guide).  
3. **Integration service:** External HL7/FHIR adapter (do not upgrade GH core).  
4. **Data controls:** Enforce synthetic-only demos; production import gates.  
5. **Evidence:** VM module activation report.

## What is already strong

- Modern React UI with EN/AR RTL.  
- Core ambulatory workflows mapped to GH models.  
- Synthetic data engine with deterministic seed.  
- Ops/admin parity for users/groups/modules listing.
""",
    )


def main() -> None:
    source_register()
    functional_assessment()
    dependency_map()
    gap_analysis()
    print("Research markdown complete.")


if __name__ == "__main__":
    main()
