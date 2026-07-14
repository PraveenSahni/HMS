# Version Discovery Report — IST HIS Upstream Baseline

**Baseline date:** 2026-07-14  
**Product:** IST HIS — Iris Star Hospital Information System  
**VM:** `gnuhealth-his-01` (project `isthealth`, zone `me-central1-a`)  
**Status:** Live VM evidence captured via `gcloud compute ssh`

## Detected versions

| Component | Version | Source |
|-----------|---------|--------|
| GNU Health HIS (core `gnuhealth`) | **5.0.6** | `pip show` on VM |
| Latest official stable (not adopted) | 5.0.7 | Codeberg tag `5.0.7` |
| Tryton server (`trytond`) | **7.0.53** | `pip show` |
| Tryton web client (SAO) | **7.0.53** | `/opt/gnuhealth/his-50/sao/package.json` |
| Desktop Tryton client | Not installed | `pip show tryton` empty |
| GNU Health Control | 5.0.3 | `pip show gnuhealth-control` |
| PostgreSQL | 15.18 | `psql --version` |
| Python | 3.11.2 | VM venv |
| Source pin | tag `v5.0.6` commit `f50972fee0d4e001133a09af8d9ea7dbfe67f7a8` | Codeberg |

## Upgrade policy

**No automatic upgrade.** Installed series is 5.0.x with core package 5.0.6.
Latest patchset 5.0.7 exists upstream; adoption requires a separate change window.

## Modules

| Metric | Count |
|--------|------:|
| Health modules in release source tree | 53 |
| Activated (`ir.module`, DB `isthealth`) | 53 |
| Inactive health modules on VM | 0 |
| Custom IST modules (`ist*` / `iris*`) | 0 |

All 53 discovered `health*` / `health` modules are **activated** on `isthealth`.

## Database schema version

Tryton module states are authoritative for schema. Exact `ir.configuration` / DB revision
string was not separately exported; schema corresponds to activated modules at baseline.

## Confidence

| Item | Confidence |
|------|------------|
| Server / Tryton / SAO / PG / Python | **High** (live VM) |
| Module activation list | **High** (live `ir.module`) |
| Per-module field catalogue | **Medium** (scraped from tag `v5.0.6` source; not live proteus introspection) |
| Documentation RST portal | **Medium** (Codeberg `documentation` main branch at retrieval; may lag/lead patchset) |

## Commands used

```bash
gcloud compute ssh gnuhealth-his-01 --project=isthealth --zone=me-central1-a --command='...'
# pip show / pip list | grep gnuhealth
# psql -d isthealth -c "SELECT name, state FROM ir_module WHERE name LIKE 'health%' OR name='health'"
```
