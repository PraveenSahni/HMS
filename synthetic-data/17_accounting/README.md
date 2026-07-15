# Synthetic pack `17_accounting`

Modules: `account`, `account_invoice`, `health_services`

Models: `company.company`, `currency.currency`, `account.account`,
`account.fiscalyear`, `account.period`, `account.journal`, `account.invoice`

## Live upload (preferred)

Accounting master data for IST Health is applied on the HIS VM via Proteus:

```bash
# From laptop
bash scripts/accounting/deploy-and-run-accounting.sh dry-run
bash scripts/accounting/deploy-and-run-accounting.sh execute
```

On VM:

```bash
export GNUHEALTH_TRYTOND_CONF=/opt/gnuhealth/his-50/etc/trytond.conf
cd /opt/gnuhealth/synthetic-data/accounting
/opt/gnuhealth/his-50/venv/bin/python upload_ist_health_accounting.py --dry-run
/opt/gnuhealth/his-50/venv/bin/python upload_ist_health_accounting.py --execute
```

Docs: `docs/implementation/ist-health-accounting-upload.md`,
`docs/implementation/financial-setup.md`.

## Local generator

```bash
python synthetic-data/17_accounting/generator.py
```

Taxes: **not invented** — left unset unless `--demo-tax-zero` (synthetic 0%, marked DEMO).
