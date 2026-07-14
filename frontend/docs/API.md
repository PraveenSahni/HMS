# GNU Health / Tryton API Reference (IST Health Frontend)

This document lists the Tryton models and RPC methods used by the IST Health React frontend.

## Endpoint

```
POST http://34.18.116.146/isthealth/
Content-Type: application/json
```

## Authentication

### common.authenticate

```json
{
  "jsonrpc": "2.0",
  "method": "common.authenticate",
  "params": ["gnuhealth", "admin", {"password": "***"}, "en"],
  "id": 1
}
```

**Response:** `[user_id, "admin", "en"]`

## Model Operations

All model calls use the pattern:

```json
{
  "method": "model.{model_name}.{method_name}",
  "params": [/* domain/ids/values */]
}
```

With explicit auth (fallback):

```json
{
  "method": "model.party.party.search",
  "params": ["gnuhealth", 1, "password", [], 0, 50, null, {}]
}
```

---

## Models Used in MVP

### party.party (Patients — base party)

| Method | Params | Purpose |
|--------|--------|---------|
| `search` | `[domain, offset, limit, order, context]` | Find patient IDs |
| `search_count` | `[domain, context]` | Count patients |
| `read` | `[ids, fields]` | Read patient records |

**Fields:** `id`, `name`, `code`, `active`

**Domain examples:**
- All IST patients: `[('code', 'like', 'IST-P-%')]`
- Search: `['|', ('name', 'ilike', '%term%'), ('code', 'ilike', '%term%')]`

### gnuhealth.patient (Patient medical record)

| Method | Params | Purpose |
|--------|--------|---------|
| `search` | `[domain, ...]` | Find by party: `[('name', '=', party_id)]` |
| `read` | `[ids, fields]` | Read medical data |

**Fields:** `id`, `name` (party ref), `puid`, `dob`, `gender`, `active`, `critical_info`

---

## Models Mapped (Phase 2+)

### gnuhealth.appointment

**Fields:** `id`, `name`, `patient`, `healthprof`, `appointment_date`, `state`

### gnuhealth.healthprofessional

**Fields:** `id`, `name` (party), `specialty`, `institution`, `active`

### gnuhealth.institution

**Fields:** `id`, `name`, `code`, `city`, `country`

### gnuhealth.institution.unit

**Fields:** department/unit records linked to institution

### gnuhealth.patient.lab.test

Lab orders linked to patients.

### gnuhealth.lab.test_type

Lab test type catalog.

### gnuhealth.prescription / gnuhealth.prescription.order

Prescription records.

### gnuhealth.medicament

Medication catalog.

### gnuhealth.specialty

Medical specialties for staff.

---

## Dashboard Aggregations

The dashboard calls `search_count` on:

| Model | Metric |
|-------|--------|
| `party.party` | Total patients |
| `gnuhealth.appointment` | Appointments |
| `gnuhealth.healthprofessional` | Staff |
| `gnuhealth.patient.lab.test` | Lab orders |
| `gnuhealth.prescription` | Prescriptions |

Each call is wrapped in `modelExists()` check — models unavailable on a given GNU Health install are skipped gracefully.

---

## Synthetic Data Alignment

The synthetic data engine (`C:\HMS\synthetic_data\`) creates records with prefix `IST`:

- Patients: `IST-P-00001` … on `party.party` + `gnuhealth.patient`
- Appointments: `IST-APT-*` on `gnuhealth.appointment`
- Staff: `IST-STF-*` on `party.party` + `gnuhealth.healthprofessional`

Run seed data:

```bash
python run_synthetic_data.py
```

---

## Error Handling

| HTTP / RPC | Meaning |
|------------|---------|
| 401 | Session expired |
| RPC error | Model/method not found, access denied, validation error |
| CORS block | Browser blocked cross-origin — use dev proxy or nginx |

---

## Future: REST Wrapper (Optional)

A thin FastAPI wrapper could expose:

```
POST /api/v1/auth/login     → common.authenticate
GET  /api/v1/patients       → party.party.search + read
GET  /api/v1/patients/:id   → party.party.read + gnuhealth.patient
GET  /api/v1/dashboard/stats → aggregated search_count calls
```

This would simplify auth (JWT), CORS, and mobile client support.
