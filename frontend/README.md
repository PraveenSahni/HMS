# IST Health — React Frontend

Modern React dashboard for **IST Technologies LLC** GNU Health / Tryton 7 backend, styled with the IST Health design system (Swiss clarity + IST navy & gold).

## Quick Start

```bash
cd frontend
cp .env.example .env
# Edit .env — set VITE_TRYTON_PASSWORD for convenience (optional)
npm install
npm run dev
```

Open **http://localhost:5173** — login with GNU Health credentials (default: `admin` / see `config.yaml`).

## Environment

| Variable | Default | Description |
|----------|---------|-------------|
| `VITE_TRYTON_URL` | `https://health.irisstar.tech` | GNU Health server base URL (relative `/api/tryton/` in prod) |
| `VITE_TRYTON_DATABASE` | `isthealth` | Tryton database name |
| `VITE_TRYTON_USERNAME` | `admin` | Pre-filled login username |
| `VITE_TRYTON_PASSWORD` | _(empty)_ | Pre-filled login password (dev only) |
| `VITE_USE_PROXY` | `true` | Use Vite dev proxy (avoids CORS) |
| `VITE_COMPANY_NAME` | `IST Technologies LLC` | Institution display name |
| `VITE_COMPANY_CITY` | `Doha` | City |
| `VITE_COMPANY_COUNTRY` | `Qatar` | Country |

## Architecture

```
Browser (React 19 + Vite + TypeScript)
    │
    ├─ Dev:  /api/tryton/*  →  Vite proxy  →  GNU Health Tryton JSON-RPC
    └─ Prod: nginx reverse proxy (same path) or direct with CORS headers
              │
              ▼
        Tryton JSON-RPC (GNU Health 5)
```

See [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) and [docs/API.md](./docs/API.md).

## Design System

CSS lives in `src/styles/` (copied from `design/styles/`):

- **Master import:** `src/styles/ist-health.css`
- **App overrides:** `src/index.css` (login footer, contact block)
- **Logos:** `public/assets/logo-full.svg`, `logo-symbol.svg`
- **Legal:** `public/legal/privacy.html`, `terms.html`

Theme is persisted in `localStorage` key `ist-health-theme` (`data-theme` on `<html>`). Language uses i18next + `ist-health-lang`; Arabic applies `dir="rtl"` and `rtl.css`.

Reference preview: `design/preview.html`

## MVP Status

| Module | Status |
|--------|--------|
| Login | ✅ Live — Tryton JSON-RPC auth, split inspire + form layout |
| Dashboard | ✅ Live — counts + recent appointments, schedule rows |
| Patients (list + detail) | ✅ Live — `party.party` + `gnuhealth.patient` |
| Appointments | 🔲 Stub — nav only |
| Staff | 🔲 Stub |
| Laboratory | ✅ Live (orders / results / types) |
| Pharmacy | 🔲 Stub |
| Settings | 🔲 Stub — institution info from env |

Stub pages show heading + “coming soon” notice; New Patient / Book Appointment buttons are disabled placeholders.

## Bilingual (EN / AR)

- i18next with English and Arabic locales (`src/i18n/locales/`)
- Header language pill toggle (EN / AR)
- RTL layout via `dir="rtl"` and `rtl.css` when Arabic is selected

## Production Build

```bash
npm run sync-design   # optional — refresh CSS/logos from design/
npm run build
npm run preview       # http://localhost:3000 with Tryton proxy
```

For production, configure nginx to proxy `/api/tryton/` to the Tryton backend and serve the React static files. See `deploy/nginx-ist-health.conf` and `deploy/deploy-vm.sh`.

**VM deploy (summary):**

```bash
cd frontend
npm run sync-design
npm ci && npm run build
sudo rsync -av dist/ /var/www/ist-health/frontend/dist/
sudo cp deploy/nginx-ist-health.conf /etc/nginx/sites-available/ist-health
sudo ln -sf /etc/nginx/sites-available/ist-health /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

Set `VITE_USE_PROXY=true` (default) so the built app calls `/api/tryton/` on the same origin. Set `VITE_USE_PROXY=false` only if the backend exposes CORS headers for your frontend origin.

## Known Blockers

1. **CORS** — Browsers block direct cross-origin JSON-RPC. Dev proxy handles this; production needs nginx CORS headers or same-origin proxy.
2. **Session cookies** — Tryton session cookies may not persist cross-origin; client falls back to credential-in-params RPC.
3. **HTTPS** — Gap 3 closed with self-signed TLS on `:443` (IP-only). Browsers warn until a domain + Let’s Encrypt cert exists. See `docs/HTTPS.md`. Same-origin `/api/tryton/` avoids mixed content.

## Scripts

- `npm run dev` — development server with HMR
- `npm run build` — production bundle
- `npm run preview` — preview production build
