---
title: Synthetic Data Overview
ist_his_version: 1.0.0
upstream_product: GNU Health HIS
upstream_version: 5.0.6
country: [AE, QA]
implementation_status: documented
last_verified_against_code: 2026-07-14
licence: CC-BY-SA-4.0
adaptation_status: Extended with IST-specific functionality
---

# Synthetic Data

Schema registry: `synthetic-data/schema/ist_his_model_registry.json`.  
Markers: `synthetic_data=true`, batch `ISTHIS-DEMO-*` / `ISTHIS-MAXDEMO-*`. Never use real Emirates/Qatar IDs.  
Max demo profile: `config/synthetic/uae_qatar_max_demo.yaml` (seed `20260714`) — guide: `docs/implementation/max-demo-synthetic-data.md`.
