# §17 Final Report — Mandatory Upstream Synchronization

**Product:** IST HIS — Iris Star Hospital Information System  
**Baseline date:** 2026-07-14  
**Alignment claim:** **Partial alignment** — documentation baseline, registries, guides, packs, and drift tooling are in place for pinned **5.0.6**. Not claimed as full production alignment (screenshot verification, live proteus field dump, and executed import/rollback tests remain incomplete).

## Answers

1. **Detected GNU Health version:** 5.0.6 (core `gnuhealth` pip); module packages mostly 5.0.4–5.0.6. Latest stable not adopted: 5.0.7.
2. **Client / Tryton:** SAO 7.0.53; trytond 7.0.53; desktop tryton client not installed; proteus 7.0.3 present.
3. **Upstream documentation source / retrieval date:** Codeberg `gnuhealth/documentation` (HIS RST) + https://docs.gnuhealth.org/his/ HTML snapshots — retrieved 2026-07-14. Software pin: Codeberg `gnuhealth/his` tag `v5.0.6` (`f50972fee0d4e001133a09af8d9ea7dbfe67f7a8`).
4. **Upstream pages acquired:** 106 RST sources under `docs/upstream/original/rst/`; HTML key pages under `docs/upstream/generated-reference/html/`; manifest file_count=229.
5. **Modules discovered (release tree):** 53.
6. **Active modules:** 53 (all health* on DB `isthealth`).
7. **Inactive health modules:** 0 on `isthealth`.
8. **Custom IST modules:** 0.
9. **Models catalogued:** 358 (source scrape, medium confidence).
10. **Fields catalogued:** 919 (source scrape, medium confidence).
11. **IST HIS module guides generated:** 53.
12. **Synthetic-data generators created:** 21 pack generators (stubs) + existing `synthetic_data/` package retained.
13. **Implementation templates generated:** 7.
14. **Documentation drift status:** Initial report at `docs/upstream/upstream-drift-report.md` — no silent overwrite policy enforced in `docs_sync`.
15. **Licence / attribution status:** `ATTRIBUTION.md`, `LICENSE-DOCUMENTATION.txt`, `LICENSE-SOFTWARE.txt` recorded; **legal review flagged**.
16. **Test results:** **8 passed** (`pytest tests/upstream -q`, 2026-07-14); `python -m docs_sync.verify_checksums` → OK 229 files.
17. **Unresolved gaps:** Live proteus full field introspection; exhaustive SAO screenshot verification; full HTML site mirror; executed DB import/rollback of all packs; HIE connectors.
18. **Modules requiring additional implementation:** Features-only absences (`health_accounting`, `health_profile`); UAE/Qatar HIE; deeper React coverage for niche modules.
19. **Regulatory items requiring UAE/Qatar confirmation:** PDPL/PDPPL applicability; HIE onboarding; ICD/SNOMED licensing for commercial use — see `docs/research/source-register.md`.
20. **Commands to regenerate / validate:**

```bash
python scripts/upstream_sync/build_all.py
python -m docs_sync.verify_checksums
python -m docs_sync.report_drift
pytest tests/upstream -q
```

## Evidence paths

- `docs/upstream/UPSTREAM_BASELINE.yaml`
- `docs/upstream/version-discovery-report.md`
- `docs/upstream/installed-module-inventory.xlsx`
- `docs/upstream/source-manifest.json`
- `docs/upstream/original/` (immutable)
- `docs/upstream/GNU_Health_Complete_Module_Registry.xlsx`
- `docs/upstream/module-registry.json`
- `docs/upstream/module-dependency-map.md`
- `docs/upstream/model-and-field-catalogue.xlsx`
- `docs/ist-his/`
- `synthetic-data/`
- `templates/IST_HIS_*`
- `docs_sync/`
