---
title: SAO Embed and Screen-by-Screen Parity
ist_his_version: 1.0.0
upstream_product: GNU Health HIS
upstream_version: 5.0.6
tryton_version: 7.0.53
baseline_date: 2026-07-15
status: active
licence: CC-BY-SA-4.0
related:
  - docs/ist-his/REACT_GAP_REMEDIATION_PLAN.md
  - docs/ist-his/SCREEN_BY_SCREEN_PARITY.md
  - frontend/docs/SAO_MIGRATION.md
---

# SAO Embed and Screen-by-Screen Parity

## Strategy (locked)

1. **Embed SAO now** inside the IST React shell (`/workspace`) with IST header + sidebar and IST navy/gold theming on SAO.
2. **Build React screen-by-screen** using the parity tracker — progressive parity, not a big-bang rewrite.
3. **Do not upgrade** GNU Health / Tryton. Keep nginx split: SPA **GET /** vs trytond **POST /** (JSON-RPC).
4. Iframe is **same-origin only** (`/sao/` via nginx). Never point the Workspace iframe at a third-party host.

## Workspace URL

| Environment | URL |
|-------------|-----|
| Production | https://health.irisstar.tech/workspace |
| SAO (direct / new tab) | https://health.irisstar.tech/sao/ |

Favorites → **Workspace**. Setup Hub / Financial / Companies / Model browser SaoPanel CTAs → **Open in Workspace** → `/workspace` (optional secondary “Open SAO in new tab”).

## How embedding works

```
AppLayout (IST header + sidebar)
  └── /workspace → WorkspacePage
        └── iframe src = same-origin /sao/  (saoUrl())
```

- Route: `frontend/src/pages/WorkspacePage.tsx` registered in `App.tsx` under `AppLayout`.
- `?path=` is reserved for future deep-links; currently loads SAO root.
- Footer hidden on Workspace so the iframe can use full remaining height.
- SaoPanel primary button is a React Router `Link` to `/workspace`.

## How theming works

Tryton SAO auto-loads `custom.css` and `custom.js` from the **SAO web root** (trytond `[web] root`).

| Repo mirror | Deploy target (VM) |
|-------------|-------------------|
| `frontend/deploy/sao-custom.css` | `<SAO_ROOT>/custom.css` (e.g. `/opt/gnuhealth/his-50/sao/custom.css`) |
| `frontend/deploy/sao-custom.js` | `<SAO_ROOT>/custom.js` |

Theme: IST navy `#0a1f44`, gold `#c9a66b` on navbar, primary buttons, tabs, and selection highlights. Safe reductions only — do not strip functional chrome.

After copying CSS/JS, hard-refresh `/sao/` (or Workspace). No trytond restart required for static CSS.

## Screen-by-screen framework

| Artifact | Path |
|----------|------|
| Markdown tracker | `docs/ist-his/SCREEN_BY_SCREEN_PARITY.md` |
| Spreadsheet | `docs/ist-his/SCREEN_BY_SCREEN_PARITY.xlsx` |
| Gap plan | `docs/ist-his/REACT_GAP_REMEDIATION_PLAN.md` (strategy = embed + progressive React) |

Status values: **Missing** | **Stub** | **Partial** | **Parity**. Priority: **P0–P3**.

Workflow per screen: compare SAO vs React → update tracker → implement React or leave Hybrid (Workspace) → re-score.

## Nginx / routing rules (do not break)

- React SPA: `GET /` (and client routes) → static `dist/`.
- trytond JSON-RPC: `POST /` (and `/api/tryton/`) → `127.0.0.1:8000`.
- SAO assets: `/sao/` → trytond web root.
- Workspace iframe must use `/sao/` on the same host as the SPA.

## Help

Topic **`using-workspace`**: Help Centre → using Workspace (SAO inside IST).

## Deploy checklist

1. `cd frontend && npm ci && npm run build`
2. Rsync `dist/` → `/var/www/ist-health/frontend/dist/`
3. Copy `frontend/deploy/sao-custom.css` → SAO root `custom.css`
4. Copy `frontend/deploy/sao-custom.js` → SAO root `custom.js`
5. Verify: https://health.irisstar.tech/workspace loads SAO inside IST chrome; POST / still JSON-RPC.
