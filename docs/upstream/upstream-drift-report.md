# Upstream Drift Report

**Generated:** 2026-07-14  
**Pinned upstream:** GNU Health HIS 5.0.6  
**Latest official stable (not adopted):** 5.0.7

## Summary

| Category | Status |
|----------|--------|
| New upstream documents since pin | Not fully diffed against portal HTML history — **review on next sync** |
| Removed documents | None detected in local original/ snapshot |
| Modified documents | Integrity hashes recorded in `source-manifest.json` |
| New modules vs pin | Monitor Codeberg tag 5.0.7 |
| Removed modules | `health_accounting`, `health_profile` absent from v5.0.6 tree (features-doc only) |
| Renamed modules | `health_imaging_orthanc` → use `health_orthanc` |
| Changed fields / workflows / deps / ACL | Requires re-scrape after upgrade — **not upgraded** |
| IST docs requiring review | All module guides marked draft approval |
| Synthetic generators requiring review | Pack stubs 00–20 |
| Data templates requiring review | `templates/IST_HIS_*` |
| Tests requiring review | `tests/upstream/` |

## Policy

**Do not automatically overwrite** approved IST HIS documentation when upstream changes.

## Regeneration

```bash
python -m docs_sync.discover_upstream
python -m docs_sync.verify_checksums
python -m docs_sync.compare --upstream docs/upstream/original --ist-docs docs/ist-his
python -m docs_sync.generate_traceability
python -m docs_sync.report_drift
```
