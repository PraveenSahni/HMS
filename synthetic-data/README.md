# IST HIS Synthetic Data Packs

Upstream model alignment: GNU Health **5.0.6**.  
Schema: `schema/ist_his_model_registry.json`.

Existing runtime loaders remain in `synthetic_data/` and `scripts/synthetic_data/` —
these packs extend them with module-ordered stubs. **Prod refuse** and **dry-run**
behaviour in the existing CLI must be preserved.

**Max demo:** `config/synthetic/uae_qatar_max_demo.yaml` +
`python scripts/synthetic_data/cli.py generate_synthetic --config …` builds a
connected local dataset covering packs 00–20 (engine-live steps import via
`run_synthetic_data.py`; other packs are local JSON / markers until importers land).
See `docs/implementation/max-demo-synthetic-data.md`.
