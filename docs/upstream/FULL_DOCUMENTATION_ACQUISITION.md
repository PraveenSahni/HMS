# Full GNU Health HIS documentation acquisition

- **Baseline (software pin):** GNU Health HIS **5.0.6** (not upgraded)
- **Acquisition date:** 2026-07-15

## Sources

| Kind | URL |
|------|-----|
| RST / Sphinx source | https://codeberg.org/gnuhealth/documentation (branch main, path his/source/) |
| Rendered HTML | https://codeberg.org/gnuhealth/pages (branch main, his/ tree) |
| Published site (reference) | https://docs.gnuhealth.org/his/ |

## File counts

| Metric | Before | After |
|--------|--------|-------|
| RST under docs/upstream/original/ | 106 | 106 |
| Images under docs/upstream/original/ | 119 | 119 |
| HTML under docs/upstream/generated-reference/html/ | 6 | 107 |
| Total files under original/ (manifest ile_count) | 229 | 229 |

## Immutable copy policy

- RST/images from Codeberg documentation **main**: add missing only; **0** files added.
- **107** existing paths skipped because on-disk SHA-256 differed from upstream main (immutable store preserved; matches prior 5.0.6-aligned RST pin).
- 
elease-notes/ from HIS v5.0.6 retained.

## Generated reference

- HTML pages copied from gnuhealth/pages: **107** .html files (includes _static, _images as published).
- Optional _sources mirror under generated-reference/_sources/: **8** .txt files present.

## Verification

`
OK 229 files
`

`
........                                                                 [100%]
8 passed in 2.30s
C:\Users\PraveenSAHNI\AppData\Local\Programs\Python\Python312\Lib\site-packages\pytest_asyncio\plugin.py:208: PytestDeprecationWarning: The configuration option "asyncio_default_fixture_loop_scope" is unset.
The event loop scope for asynchronous fixtures will default to the fixture caching scope. Future versions of pytest-asyncio will default the loop scope for asynchronous fixtures to function scope. Set the default fixture loop scope explicitly in order to avoid unexpected behavior in the future. Valid fixture loop scopes are: "function", "class", "module", "package", "session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET))
`

## Hash conflicts (not overwritten)

Total: **107** — see docs/upstream/_acq_skip.json for paths.
