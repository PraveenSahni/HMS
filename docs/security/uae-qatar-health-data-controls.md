# UAE / Qatar Health Data Controls

**Date:** 2026-07-14  
**Disclaimer:** Control mapping is engineering guidance. Legal applicability of UAE PDPL and Qatar PDPPL to specific processing activities **requires confirmation** from qualified counsel and competent authorities.

## 1. Data classification

| Class | Examples | Handling |
|-------|----------|----------|
| Synthetic demo | `IST-P-*`, `SYN-AE-*`, `SYN-QA-*` | Allowed in non-prod; mark synthetic |
| Real PHI/PII | Real names, national IDs, phones | Prod only; least privilege; audit |
| Special nature (QA PDPPL) | Health data | Enhanced safeguards — **confirm permits** |
| Sensitive (UAE PDPL) | Health/biometric | **Confirm** lawful basis & exemptions |

## 2. Technical controls (current vs target)

| Control | Current IST | Target |
|---------|-------------|--------|
| TLS | HTTPS via nginx (verify) | TLS1.2+ only; HSTS |
| Auth session | localStorage MVP | httpOnly cookie / JWT gateway |
| RBAC | Tryton groups | Named IST role packs |
| Tenant isolation | Single company demo | Company + institution record rules |
| Encryption at rest | GCP disk default? | Verify CMEK if required |
| Backup | TBD on VM | Documented restore drill |
| Synthetic gate | In progress | Refuse prod import w/o override |
| Logging | nginx + trytond | Central audit for PHI reads |

## 3. Operational controls

1. Non-production databases must contain only synthetic data.  
2. Production access via named accounts; no shared admin passwords in chat.  
3. DPIA before HIE go-live or new secondary use.  
4. Breach response contacts (UAE/QA) — **confirm notification timelines with counsel**.  
5. Vendor (GH/Tryton) upgrades only via CAB.

## 4. Cross-border

UAE ↔ Qatar chart sharing is **not enabled by default**. Any cross-entity access needs legal basis + technical rule.

## 5. Related artefacts

- `security-control-matrix.xlsx`
- `docs/integration/interoperability-assessment.md`
