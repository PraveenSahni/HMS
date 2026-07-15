# scripts/accounting

On-VM Proteus tools to align IST Health accounting master data on `isthealth`.

| Script | Purpose |
|--------|---------|
| `assess_accounting.py` | Read-only CoA / FY / journal / invoice / safety assessment |
| `upload_ist_health_accounting.py` | Idempotent create: companies AED/QAR, Minimal CoA, FY/periods, journals check, party AR/AP |
| `set_party_accounts_txn.py` | Transaction-API party AR/AP + configuration defaults |
| `verify_accounting_final.py` | Per-company verification JSON |
| `deploy-and-run-accounting.sh` | gcloud scp + dry-run/execute |

Taxes are left unset by default (no invented VAT). See `docs/implementation/ist-health-accounting-upload.md`.
