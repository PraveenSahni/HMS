# GNU Health Synthetic Data Engine

Config-driven synthetic data generator for **GNU Health 5 / Tryton 7**.  
Edit **`config.yaml`** to change the company name, location, data volumes, and server — then run one command.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Edit config.yaml (change company name, counts, etc.)

# 3. Test connection
python run_synthetic_data.py --dry-run

# 4. Generate data
python run_synthetic_data.py
```

## Change Company Name

Open `config.yaml` and edit:

```yaml
company:
  name: "Your Company Name LLC"    # ← change this
  name_ar: "اسم الشركة"             # Arabic display name
  code: "YCN"                      # Short code for record IDs
  city: "Doha"
  country: "Qatar"
```

Then run:

```bash
python run_synthetic_data.py
```

The script is **idempotent** — re-running skips records that already exist (matched by code prefix). Use `--force` to disable this.

## Default Configuration (IST Technologies LLC)

| Setting | Value |
|---------|-------|
| Company | IST Technologies LLC |
| Location | Doha, Qatar |
| Facility | Multi-specialty Clinic |
| Patients | 4,000 |
| Staff | 300 (doctors, nurses, admin, reception, lab, pharmacy) |
| Appointments | 6 months history |
| Modules | Outpatient, Laboratory, Pharmacy |
| Languages | English + Arabic names |

## Command Options

```bash
python run_synthetic_data.py                     # Full run from config.yaml
python run_synthetic_data.py --config my.yaml    # Custom config file
python run_synthetic_data.py --dry-run           # Test connection only
python run_synthetic_data.py --force             # Allow duplicates
python run_synthetic_data.py --only company,patients   # Run specific steps
python run_synthetic_data.py -v                  # Verbose logging
```

### Steps (in order)

1. `company` — Institution, departments, specialties
2. `staff` — Health professionals (300)
3. `patients` — Patient demographics (4,000)
4. `appointments` — Outpatient appointments (6 months; idempotent **top-up**)
5. `laboratory` — Lab orders (`gnuhealth.patient.lab.test`) + results (`gnuhealth.lab`)
6. `pharmacy` — Medications and prescriptions (`gnuhealth.prescription.order`)
7. `inpatient` — Building, ward, beds, admissions
8. `evaluations` — Patient evaluations

### Re-seed clinical data only (Gap 2)

When patients/staff already exist and lists are empty for Lab / Appointments / Beds:

```bash
cd /opt/gnuhealth/synthetic-data
/opt/gnuhealth/his-50/venv/bin/python run_synthetic_data.py \
  --only appointments,laboratory,pharmacy,inpatient,evaluations
```

Idempotent mode **tops up** to configured targets (it no longer skips appointments after finding a single existing row). Use `--force` only if you intentionally want duplicates.

## File Structure

```
C:\HMS\
├── config.yaml                 # ← EDIT THIS (only file users need to change)
├── run_synthetic_data.py       # Main entry point
├── requirements.txt
├── deploy-and-run.sh           # Deploy to GCP VM
├── README_SYNTHETIC_DATA.md
└── synthetic_data/
    ├── client.py               # Tryton JSON-RPC / Proteus client
    ├── generators.py           # Faker + Qatar/Arabic names
    ├── company.py              # Institution setup
    ├── staff.py                # Health professionals
    ├── patients.py             # Patient records
    ├── appointments.py         # Outpatient appointments
    ├── laboratory.py           # Lab orders & results
    ├── pharmacy.py             # Medications & prescriptions
    ├── inpatient.py            # Beds & admissions
    └── evaluations.py          # Patient evaluations
```

## Server Connection

Configured in `config.yaml`:

```yaml
server:
  url: "http://34.18.116.146"
  database: "isthealth"
  username: "admin"
  password: "IstHealth@2026!Admin"
```

Uses Tryton **JSON-RPC** at `{url}/{database}/` (session auth).

## Deploy to GCP VM

From Cloud Shell or local machine with gcloud:

```bash
chmod +x deploy-and-run.sh
./deploy-and-run.sh
```

Or manually on VM:

```bash
gcloud compute ssh gnuhealth-his-01 --project=isthealth --zone=me-central1-a
cd /opt/gnuhealth/synthetic-data
/opt/gnuhealth/his-50/venv/bin/pip install -r requirements.txt
/opt/gnuhealth/his-50/venv/bin/python run_synthetic_data.py --dry-run
/opt/gnuhealth/his-50/venv/bin/python run_synthetic_data.py
```

For 4,000 patients, run in background:

```bash
nohup /opt/gnuhealth/his-50/venv/bin/python run_synthetic_data.py > synthetic_run.log 2>&1 &
tail -f synthetic_run.log
```

## Record ID Convention

All synthetic records use the company `code` prefix from config:

| Type | Example Code |
|------|-------------|
| Patient | `IST-P-00001` |
| Staff | `IST-ST-DOC-0001` |
| Appointment | comments `IST synthetic: IST-APT-*` |
| Lab order | comment `IST synthetic: IST-LABORD-*` |
| Lab result | results text `IST synthetic: IST-LABRES-*` |
| Prescription | notes `IST synthetic: IST-RX-*` |
| Evaluation | chief_complaint `IST synthetic: …` |
| Admission | info `IST synthetic: IST-ADM-*` |
| Medication | `IST-MED-0001` |

## Testing with Smaller Dataset

For a quick test, temporarily change `config.yaml`:

```yaml
data:
  patients: 50
  staff: 20
  appointment_months: 1
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Connection failed | Verify GNU Health is running at the URL; check credentials |
| Model not found | Module may not be installed — generator skips gracefully |
| Slow for 4000 patients | Normal — expect 30–90 min; use `nohup` on VM |
| Duplicates on re-run | Default is idempotent; don't use `--force` unless intended |

## Requirements

- Python 3.10+
- Network access to GNU Health server
- Packages: `faker`, `pyyaml`, `requests`
