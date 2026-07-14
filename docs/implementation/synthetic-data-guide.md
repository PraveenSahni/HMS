# Synthetic Data Guide

## Goals

Deterministic, idempotent, bilingual-capable demo data for UAE + Qatar **without real PII**.

## Markers

| Mechanism | Example |
|-----------|---------|
| Code prefix | `IST-P-00001`, `IST-ST-DOC-0001` |
| Comment/text | `IST synthetic: …` |
| Config flag | `synthetic_data: true` |
| National ID (fake) | `SYN-QA-00000001`, `SYN-AE-00000001` |

## Determinism

`seed: 42` (or config value) seeds Python `random` and Faker.

## Scale

| Profile | Patients | Staff | Use |
|---------|----------|-------|-----|
| Demo (`uae_qatar_demo.yaml`) | 50 | 12 | CI / evidence |
| **Max demo** (`uae_qatar_max_demo.yaml`) | **4000** | **300** | Full UAE+Qatar org + connected packs (see `max-demo-synthetic-data.md`) |
| Default `config.yaml` | 4000 | 300 | VM load test (engine-only steps) |
| Full brief optional | 50000 | — | Only on sized VM; document runtime |

Max demo guide: [`docs/implementation/max-demo-synthetic-data.md`](max-demo-synthetic-data.md).

## Safety

- Default idempotent top-up  
- `--dry-run` validates connectivity / plan  
- Production refused without override
