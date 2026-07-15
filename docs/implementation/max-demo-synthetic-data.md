# Max Demo Synthetic Data (UAE + Qatar)

Largest **validated** IST HIS demo profile for the IST Healthcare Group org tree.

| Item | Value |
|------|-------|
| Config | `config/synthetic/uae_qatar_max_demo.yaml` |
| Seed | `20260714` |
| Batch ID | `ISTHIS-MAXDEMO-20260714` |
| Ceiling | **4000 patients / 300 staff** |
| Why this ceiling | Matches proven `run_synthetic_data.py` / `config.yaml` scale; CLI `validate` refuses `>5000` in `environment: test`; optional master-brief 50k deferred (sized VM; OOM/timeout risk on laptop) |
| DB import this run | **Yes** — live load to `isthealth` on `gnuhealth-his-01` via Proteus/trytond (2026-07-14T19:27:36Z → 19:32:28Z UTC, **4.8 min**) |

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

## Live DB import result (`isthealth` @ gnuhealth-his-01)

| Field | Value |
|-------|-------|
| Timestamp (UTC) | **2026-07-14T19:27:36Z → 19:32:28Z** (COMPLETE) |
| Duration | **4.8 minutes** |
| Path | On-VM Proteus/`trytond` (`GNUHEALTH_TRYTOND_CONF=/opt/gnuhealth/his-50/etc/trytond.conf`) |
| Config used | Merged max-demo runtime (`max_demo_runtime.yaml` on VM; password from local gitignored `config.yaml`) |
| Laptop HTTP import | Failed first: JSON-RPC login HTTP 500 (`'str' object has no attribute 'copy'`) — used VM socket path instead |
| SQL verify | Matched engine summary below |

### Engine-live counts in DB (actual)

| Entity | Loaded |
|--------|-------:|
| Patients (`gnuhealth.patient`) | **4000** |
| Health professionals | **299** (target 300; idempotent reuse) |
| Appointments | **12000** |
| Lab orders | **2184** |
| Lab results | **873** |
| Prescriptions | **1820** |
| Evaluations | **2184** |
| Beds | **72** |
| Admissions | **216** |

Note: engine ratios vs local JSON generators differ slightly (e.g. admissions/evaluations), so live counts are not identical to the connected-JSON table above.

### Still local-JSON / stub only (not written by engine)

| Pack | Status |
|------|--------|
| 00 foundation, 02 multi-facility institutions, 03 users/access | Local connected JSON only |
| 09 nursing, 10 ICU, 12 imaging, 14 stock, 15 surgery | Local connected JSON only |
| 16 insurance, 18 services/billing | Local connected JSON only |
| **17 accounting** | **Master data uploaded 2026-07-15** via `scripts/accounting/upload_ist_health_accounting.py` — see `docs/implementation/ist-health-accounting-upload.md` (CoA/FY/journals/companies; invoices still 0) |
| 19 reporting, 20 federation | Marker stubs only |
| `gnuhealth.institution.unit` departments | Skipped on this VM (`Model … not available`) |

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

On the demo VM (successful path for this load):

```bash
cd /opt/gnuhealth/synthetic-data
export GNUHEALTH_TRYTOND_CONF=/opt/gnuhealth/his-50/etc/trytond.conf
nohup /opt/gnuhealth/his-50/venv/bin/python run_synthetic_data.py \
  --config max_demo_runtime.yaml > synthetic_max_demo.log 2>&1 &
```

Expect **5–90 minutes** depending on whether parties already exist (this run: **4.8 min** after prior party seed).

## Engine vs pack coverage

| Pack | Local generate | Live `run_synthetic_data.py` |
|------|----------------|------------------------------|
| 01 company, 04 HP, 05 patients, 06 appointments, 07 evaluations, 08 inpatient, 11 lab, 13 pharmacy | Yes (connected JSON) | **Yes** (engine steps) — loaded 2026-07-14 |
| 00 foundation, 02 institutions, 03 users, 09 nursing, 10 ICU, 12 imaging, 14 stock, 15 surgery, 16 insurance, 17 accounting, 18 services | Yes (connected JSON) | **Not yet** — local files / future pack importers |
| 19 reporting, 20 federation | Marker stubs only | No |

Pack folders under `synthetic-data/00_*` … `20_*` remain stub modules; orchestration is via the CLI + max-demo config `packs:` map.

## Safety

- `synthetic_data: true` required
- Production hosts listed; live import refused without `--allow-production`
- Prefer dry-run first
- Do **not** upgrade GNU Health as part of this load
- Do not invent fields outside the model registry / existing generators
- Prefer on-VM Proteus when laptop JSON-RPC auth fails against nginx

## Evidence artefacts

| File | Role |
|------|------|
| `docs/testing/evidence/validate-report.json` | Last validate |
| `docs/testing/evidence/max-demo-summary.json` | Counts + samples (commit-friendly) |
| `docs/testing/evidence/generate-max-demo-report.json` | Generate report |
| `docs/testing/evidence/import-*-dry-run.json` | Dry-run plans |
| `docs/testing/evidence/max-demo-import-report.json` | Import status (updated after live load) |
| `docs/testing/evidence/generated/uae_qatar_max_demo_full.json` | Full dataset (**gitignored**, ~14 MB) |
| `synthetic-data/generated/` | Mirror of full/summary (**gitignored**) |
| VM `/opt/gnuhealth/synthetic-data/synthetic_max_demo.log` | Live engine log for this load |

## Next steps

1. Optional: pack importers for nursing / ICU / imaging / surgery / insurance / services.  
2. Optional: wire multi-facility institution tree + departments when `gnuhealth.institution.unit` is available.  
3. Keep passwords in gitignored local config only.  
4. Explicit user approval required before any further production load.
