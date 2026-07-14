# Full GNU Health HIS documentation acquisition

- **Baseline (software pin):** GNU Health HIS **5.0.6** (not upgraded)
- **Acquisition date:** 2026-07-15

## Sources

| Kind | URL |
|------|-----|
| RST / Sphinx source | https://codeberg.org/gnuhealth/documentation (branch `main`, path `his/source/`) |
| Rendered HTML | https://codeberg.org/gnuhealth/pages (branch `main`, `his/` tree) |
| Published site (reference) | https://docs.gnuhealth.org/his/ |

Documentation repo has no release tags matching HIS 5.0.6; official published tree (`pages` / docs.gnuhealth.org) plus Codeberg `documentation` `main` were used. Existing immutable RST under `original/` was retained where SHA-256 differed from `main` (add-only policy).

## File counts

| Metric | Before | After |
|--------|--------|-------|
| RST under `docs/upstream/original/` | 106 | 106 |
| Images under `docs/upstream/original/` | 119 | 119 |
| HTML under `docs/upstream/generated-reference/html/` | 6 | 107 |
| Total files under `original/` (manifest `file_count`) | 229 | 229 |

RST path coverage vs official `his/source`: **105/105** (plus 1 HIS release-notes `README.rst`). Toctree from `index.rst` fully closed. Zero missing RST paths to add.

## Immutable copy policy

- RST/images from Codeberg documentation `main`: add missing only; **0** files added (tree already complete).
- **107** existing paths skipped because on-disk SHA-256 differed from upstream `main` (immutable store preserved; prior 5.0.6-aligned RST pin kept).
- `release-notes/` from HIS v5.0.6 retained.

## Generated reference

- HTML pages from `gnuhealth/pages`: **107** `.html` files (full toctree including userguide/, techguide/, plugins/, appendix/, plus `_static` / `_images` / `_sources` as published).
- Browse: `docs/upstream/generated-reference/html/index.html`

## Verification

```
python -m docs_sync.verify_checksums
→ OK 229 files

pytest tests/upstream -q
→ 8 passed
```

## Hash conflicts (not overwritten)

Total: **107** — see `docs/upstream/_acq_skip.json` for paths.
