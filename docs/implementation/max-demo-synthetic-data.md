# Max Demo Synthetic Data (UAE + Qatar)

Largest **validated** IST HIS demo profile for the IST Healthcare Group org tree.

| Item | Value |
|------|-------|
| Config | `config/synthetic/uae_qatar_max_demo.yaml` |
| Seed | `20260714` |
| Batch ID | `ISTHIS-MAXDEMO-20260714` |
| Ceiling | **4000 patients / 300 staff** |
| Why this ceiling | Matches proven `run_synthetic_data.py` / `config.yaml` scale; CLI `validate` refuses `>5000` in `environment: test`; optional master-brief 50k deferred (sized VM; OOM/timeout risk on laptop) |
| DB import this run | **No** — `server.password: CHANGE_ME`; files + dry-run only |

## Org tree

```
IST Healthcare Group (IST-HC-GRP)
├── IST Healthcare UAE (IST-HC-AE)
│   ├── IST General Hospital Dubai
│   ├── IST Medical Centre Dubai
│   ├── IST Day Surgery Centre Dubai
│   ├── IST General Hospital Abu Dhabi
│   ├── Central Laboratory UAE
│   ├── Central Pharmacy UAE
│   └── Central Store UAE
└── IST Healthcare Qatar (IST-HC-QA)
    ├── IST General Hospital Doha
    ├── IST Medical Centre Doha
    ├── IST Specialist Clinic Doha
    ├── Central Laboratory Qatar
    ├── Central Pharmacy Qatar
    └── Central Store Qatar
```

## Volumes generated (seed 20260714)

Deterministic local connected dataset (`docs/testing/evidence/max-demo-summary.json`).

| Entity | Count | Model (registry) |
|--------|------:|------------------|
| Legal entities | 3 | `company.company` / party |
| Institutions / facilities | 13 | `gnuhealth.institution` |
| Departments | 10 | `gnuhealth.institution.unit` |
| Users | 300 | `res.user` |
| Health professionals | 300 | `gnuhealth.healthprofessional` |
| Patients | 4000 | `gnuhealth.patient` |
| Appointments | 12000 | `gnuhealth.appointment` |
| Evaluations | 2419 | `gnuhealth.patient.evaluation` |
| Lab orders | 1587 | `gnuhealth.patient.lab.test` |
| Lab results | 952 | `gnuhealth.lab` |
| Prescriptions | 2012 | `gnuhealth.prescription.order` |
| Beds | 72 | `gnuhealth.hospital.bed` |
| Admissions | 1065 | `gnuhealth.inpatient.registration` |
| Nursing roundings | 843 | `gnuhealth.patient.rounding` |
| ICU score stubs | 95 | `gnuhealth.icu.glasgow` |
| Imaging requests | 790 | `gnuhealth.imaging.test.request` |
| Surgeries | 205 | `gnuhealth.surgery` |
| Insurance companies | 2 | `party.party` |
| Insurance plans | 2 | `gnuhealth.insurance.plan` |
| Patient insurance | 2784 | `gnuhealth.insurance` |
| Stock locations | 9 | `stock.location` |
| Stock moves | 72 | `stock.move` |
| Health services | 2016 | `gnuhealth.health_service` |
| Draft invoices | 2016 | `account.invoice` |
| Reporting markers | 1 | `gnuhealth.top_diseases` |
| Federation markers | 1 | stub |

All IDs use `IST-P-*` / `IST-ST-*` / `SYN-AE-*` / `SYN-QA-*`. Phones/emails use `synthetic.isthealth.example` / `+971 50 000 ####` / `+974 5000 ####` only.

## Commands

```bash
# Validate
python scripts/synthetic_data/cli.py validate --config config/synthetic/uae_qatar_max_demo.yaml

# Generate connected local JSON (summary + full under evidence/generated/)
python scripts/synthetic_data/cli.py generate_synthetic --config config/synthetic/uae_qatar_max_demo.yaml

# Dry-run master-data / synthetic import plans (no writes)
python scripts/synthetic_data/cli.py import_data --config config/synthetic/uae_qatar_max_demo.yaml --dry-run
python scripts/synthetic_data/cli.py import_synthetic --config config/synthetic/uae_qatar_max_demo.yaml --dry-run

# Live engine import (non-prod / approved demo VM only)
# 1. Copy password into a LOCAL override (config.yaml is gitignored) — never commit secrets
# 2. Merge company/data/server into a runtime yaml, or patch max_demo server.password locally
# 3. Require --allow-production if URL is health.irisstar.tech / 34.18.116.146
python scripts/synthetic_data/cli.py import_synthetic --config config/synthetic/uae_qatar_max_demo.yaml --allow-production

# Equivalent legacy engine (after merging max_demo into a runtime config with real password)
python run_synthetic_data.py --config docs/testing/evidence/_runtime_synthetic_config.yaml --dry-run
python run_synthetic_data.py --config docs/testing/evidence/_runtime_synthetic_config.yaml
```

On the demo VM (historical pattern):

```bash
cd /opt/gnuhealth/synthetic-data
nohup /opt/gnuhealth/his-50/venv/bin/python run_synthetic_data.py \
  --config /path/to/merged_max_demo.yaml > synthetic_max_demo.log 2>&1 &
```

Expect **30–90 minutes** for full 4000-patient engine load.

## Engine vs pack coverage

| Pack | Local generate | Live `run_synthetic_data.py` |
|------|----------------|------------------------------|
| 01 company, 04 HP, 05 patients, 06 appointments, 07 evaluations, 08 inpatient, 11 lab, 13 pharmacy | Yes (connected JSON) | **Yes** (engine steps) |
| 00 foundation, 02 institutions, 03 users, 09 nursing, 10 ICU, 12 imaging, 14 stock, 15 surgery, 16 insurance, 17 accounting, 18 services | Yes (connected JSON) | **Not yet** — local files / future pack importers |
| 19 reporting, 20 federation | Marker stubs only | No |

Pack folders under `synthetic-data/00_*` … `20_*` remain stub modules; orchestration is via the CLI + max-demo config `packs:` map.

## Safety

- `synthetic_data: true` required
- Production hosts listed; live import refused without `--allow-production`
- Prefer dry-run first
- Do **not** upgrade GNU Health as part of this load
- Do not invent fields outside the model registry / existing generators

## Evidence artefacts

| File | Role |
|------|------|
| `docs/testing/evidence/validate-report.json` | Last validate |
| `docs/testing/evidence/max-demo-summary.json` | Counts + samples (commit-friendly) |
| `docs/testing/evidence/generate-max-demo-report.json` | Generate report |
| `docs/testing/evidence/import-*-dry-run.json` | Dry-run plans |
| `docs/testing/evidence/generated/uae_qatar_max_demo_full.json` | Full dataset (**gitignored**, ~14 MB) |
| `synthetic-data/generated/` | Mirror of full/summary (**gitignored**) |

## Next steps for DB load

1. Confirm target is demo/UAT `isthealth` (not production CAB-restricted).  
2. Supply credentials via local gitignored config (never commit).  
3. `import_synthetic --dry-run` then `import_synthetic --allow-production` if host is listed.  
4. Re-run validate counts in Tryton UI / engine summary.  
5. Explicit user approval required before any production load.
