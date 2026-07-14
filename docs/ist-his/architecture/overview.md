---
title: IST HIS Architecture
ist_his_version: 1.0.0
upstream_product: GNU Health HIS
upstream_version: 5.0.6
country: [AE, QA]
implementation_status: documented
last_verified_against_code: 2026-07-14
licence: CC-BY-SA-4.0
adaptation_status: Adapted for IST HIS user interface
---

# Architecture Overview

IST HIS presents a React SPA over GNU Health HIS / Tryton JSON-RPC.

- Backend: GNU Health 5.0.6, Tryton 7.0.53, PostgreSQL 15.18
- Legacy UI: SAO 7.0.53
- Frontend: `frontend/` (IST branding)
- Technical models remain `gnuhealth.*`

See also `docs/research/current-system-discovery.md`.
