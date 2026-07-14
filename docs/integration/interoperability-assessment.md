# Interoperability Assessment — IST Health

**Date:** 2026-07-14

## Current state

| Interface | Status |
|-----------|--------|
| React ↔ Tryton JSON-RPC | Live |
| SAO ↔ Tryton | Live |
| HL7 v2 | Not implemented |
| FHIR | Not implemented |
| C-CDA | Not implemented |
| DICOM / Orthanc | Package may exist; not wired in React |
| NABIDH / Malaffi / Riayati | Not implemented |
| Qatar national HIE | Mandate/spec **unconfirmed** |

## Standards notes (licensing)

| Standard | Note |
|----------|------|
| HL7 / FHIR | Implement freely per HL7 policies; respect trademarks |
| DICOM | Free standard; follow NEMA terms |
| ICD | Confirm national/commercial licensing |
| SNOMED CT | Confirm affiliate license for UAE & Qatar |
| LOINC | Free with license attribution |

## Recommended design (reusable service)

```
HIS (Tryton) → Outbox / events → Integration Service → HL7/FHIR adapters → HIE endpoints
```

Do **not** embed HIE credentials in the React app. Prefer a server-side integration service with audit, retries, and payload minimization.

## Next actions

1. Confirm which facilities are legally required to connect to which HIE.  
2. Obtain current interface specs from DHA/DoH/MOHAP/MoPH.  
3. Prototype ADT^A01 + ORU^R01 against a vendor test harness (non-prod).  
4. Update `interface-register.xlsx` statuses.
