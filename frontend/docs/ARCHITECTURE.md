# IST Health Frontend — Architecture

## Overview

The IST Health React frontend is a **replacement UI layer** for GNU Health. It does not modify the Tryton/GNU Health backend — all data flows through the existing JSON-RPC API on the GNU Health server at `http://34.18.116.146`.

## Stack

| Layer | Choice |
|-------|--------|
| Framework | React 18 + TypeScript |
| Build | Vite 6 |
| Styling | Tailwind CSS v4 + design tokens from reference HTML |
| Routing | React Router v7 |
| i18n | i18next + react-i18next (EN / AR, RTL) |
| Backend | Tryton JSON-RPC (GNU Health 5 / Tryton 7) |

## Connection Flow

```
┌─────────────────┐     POST /isthealth/      ┌──────────────────────┐
│  React App      │ ─────────────────────────►│  Tryton Server       │
│  TrytonClient   │   JSON-RPC 2.0            │  GNU Health 5        │
└─────────────────┘                           └──────────────────────┘
        │
        │ 1. common.authenticate / common.login
        │ 2. model.{model}.{method} with session or [db, uid, password, ...]
        ▼
   localStorage session (uid, username, database)
```

### RPC URL

```
{base_url}/{database}/
→ http://34.18.116.146/isthealth/
```

### Authentication Methods (tried in order)

1. `common.authenticate` — `[database, login, {password}, language]`
2. `common.login` — `[database, login, password]`
3. `common.db.login` — `[database, login, password]`

### Model Calls

After auth, calls use `model.party.party.search`, `model.party.party.read`, etc.

The client first attempts session-based calls (cookies via `credentials: 'include'`). On failure, it retries with explicit credentials: `[database, uid, password, ...methodArgs]`.

## Dev Proxy (CORS)

Vite proxies `/api/tryton/*` → `{VITE_TRYTON_URL}/{VITE_TRYTON_DATABASE}/*` so the browser sees same-origin requests during development.

## Production Options

1. **Nginx reverse proxy** (recommended) — serve React static files and proxy `/isthealth/` to backend
2. **REST wrapper** (Phase 2) — FastAPI/Node service wrapping JSON-RPC with JWT auth
3. **CORS headers on nginx** — add `Access-Control-Allow-Origin` for the frontend domain

## Module → Model Mapping

| Frontend Route | GNU Health Models | Status |
|----------------|-------------------|--------|
| `/` | aggregate counts across models | **Live** |
| `/patients` | `party.party`, `gnuhealth.patient` | **Live** (+ create) |
| `/appointments` | `gnuhealth.appointment` | **Live** (list/day/create/edit) |
| `/staff` | `gnuhealth.healthprofessional` | **Live** |
| `/laboratory` | `gnuhealth.patient.lab.test` | Empty — `health_lab` not installed |
| `/pharmacy` | `prescription.order`, `product.template`, `medicament` | **Live** |
| `/medications` | `gnuhealth.patient.medication` | **Live** (empty-capable) |
| `/evaluations` | `gnuhealth.patient.evaluation` | **Live** (empty-capable) |
| `/beds` | `gnuhealth.hospital.bed` | **Live** (empty-capable) |
| `/nursing` | — | Module gap notice |
| `/procedures` | — | Module gap notice |
| `/settings` | `gnuhealth.institution` | **Live** |

See [SAO_MIGRATION.md](./SAO_MIGRATION.md) for full SAO menu inventory and parity gaps.

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── auth/          ProtectedRoute
│   │   ├── layout/        AppLayout (toolbar + sidebar)
│   │   └── ui/            Design system components
│   ├── contexts/          AuthContext
│   ├── i18n/              EN + AR translations
│   ├── lib/tryton/        JSON-RPC client + model constants
│   ├── pages/             Route pages
│   └── services/          healthApi (data fetching)
├── docs/
│   ├── ARCHITECTURE.md
│   └── API.md
└── vite.config.ts         Dev proxy config
```

## Institution Context

Configured via environment variables, aligned with `config.yaml`:

- **Company:** IST Technologies LLC
- **Location:** Doha, Qatar
- **Code prefix:** IST (synthetic patient codes: `IST-P-00001`)

## Security Notes

- Do not commit `.env` with production passwords
- Session stores uid + password in localStorage (dev MVP) — Phase 2 should use httpOnly cookies or JWT
- All clinical data stays on GNU Health server; frontend is a thin client

## Next Phases

1. **Phase 2** — Appointments, Staff list/detail, Lab orders, Pharmacy
2. **Phase 3** — EMR forms, billing, inpatient, nursing modules from feature doc
3. **Phase 4** — REST wrapper, role-based access, audit logging
4. **Phase 5** — Offline/PWA, print layouts, Qatar MOH reporting integrations
