# Implementation Test Report — IST Health UAE/Qatar Framework

**Date:** 2026-07-14  
**Runner:** `python -m pytest tests/implementation -v`  
**Result:** **9 passed, 0 failed**

## Evidence summary

| Test | Result | Evidence |
|------|--------|----------|
| Org hierarchy AE/QA isolation in demo YAML | PASS | `config/synthetic/uae_qatar_demo.yaml` |
| Deterministic synthetic seed (42) | PASS | `docs/testing/evidence/synthetic-demo-dataset.json` |
| Idempotent generate (same counts) | PASS | `generate-synthetic-report.json` |
| Master data Excel validation | PASS | validate_master_data stdout ok |
| Dry-run import_data | PASS | `import-data-dry-run.json` |
| Production import refused | PASS | exit ≠ 0 + REFUSED when `environment: production` |
| Help EN/AR metadata + bodies | PASS | `frontend/help-content/{en,ar}/` |
| Help search / country routing | PASS | uae-hie-readiness AE-only |
| Required docs/xlsx/docx exist | PASS | filesystem checks |

## Synthetic volume (demo evidence run)

| Entity | Count | Notes |
|--------|------:|-------|
| Patients | 50 | Deterministic `IST-P-#####` |
| Staff | 12 | `IST-ST-####` |
| Legal entities | 3 | Group + AE + QA |
| Facilities | 2 | Dubai + Doha |
| Seed | 42 | |

Full-scale profile remains `config.yaml` (4000 patients / 300 staff) for VM loads — not executed in this evidence run (network/credentials).

## Import / rollback

| Action | Result |
|--------|--------|
| `import_data --dry-run` | OK — writes=0 |
| `import_synthetic --dry-run` | OK — no engine write |
| Live GH import | **Not executed** — demo password `CHANGE_ME`; skipped by design |
| Rollback | Documented in `data-import-runbook.md` (DB restore / synthetic prefix delete) — **not exercised on VM** |

## Help features verified

- Index + articles EN/AR with id, title, roles, countries, routes, keywords, version  
- Guided workflows present (`guided: true` + steps)  
- Country filter excludes UAE HIE article for QA  
- React route `/help` + header launcher wired  

## Frontend compile note

Help Centre TypeScript sources added (`HelpCentrePage`, `helpService`, `App` route). Full `npm run build` not required for Python evidence; run locally before deploy.

## Honest gaps in this test cycle

1. No live Tryton import against `34.18.116.146` / `health.irisstar.tech`.  
2. No VM `ir.module` activation dump refreshed in this run.  
3. No browser E2E for Help RTL.  
4. Tenant record-rules not deployed to Tryton — hierarchy tested at config/template level only.
