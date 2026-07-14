---
title: Document content parity — IST HIS vs GNU Health HIS
ist_his_version: 1.0.0
upstream_product: GNU Health HIS
upstream_version: 5.0.6
baseline_date: 2026-07-14
licence: CC-BY-SA-4.0
companion_xlsx: docs/ist-his/IST_HIS_Documentation_Traceability.xlsx
---

# Document content parity (substance, not branding)

## Verdict

**Is document context/content exactly the same as GNU Health HIS docs?** **NO.**

IST HIS docs share **topic inventory** with upstream (modules, mapped user-guide IDs) but do **not** carry the same procedural depth, screen walkthroughs, or clinical/ops how-to substance as the upstream RST user/tech guides.

Immutable upstream source of truth remains at `docs/upstream/original/` (and HTML under `docs/upstream/generated-reference/`). That tree **is** GNU Health documentation. The customer-facing `docs/ist-his/` library is a separate, thinner layer.

## Classification (honest)

| Class | Meaning | What we found |
|-------|---------|---------------|
| **Same context** | Substantively equivalent procedures/meaning for that topic | **~0** IST-facing docs. Upstream originals are same as GH; IST library is not a port of that prose. |
| **Adapted context** | Same clinical/ops meaning, rewritten for IST UI/SAO paths + UAE/QA notes | Traceability labels **63/63** rows `Adapted for IST HIS terminology`. In practice this is **topic mapping + scaffolding**, not full adapted how-tos. Help Centre workflows add short IST-route steps (thin adaptation). |
| **Thinner / stub** | Not full upstream depth | **53/53** module guides (~135–175 lines, shared template: activation, models, UAE/QA placeholders). **13** domain overviews (~15–22 lines). Role guides are stubs. **0/53** module READMEs contain procedural phrases like “Click / Open the / To create / Navigate”. |
| **Missing IST coverage** | Upstream topic has no IST equivalent at usable depth | Deep upstream chapters (patient evaluations, book-of-life/core forms, health-center finance/purchase, specialty walkthroughs, techguide install/security/FHIR) are **not** rewritten in IST docs — only stub pointers or Help Centre one-liners. |

## Counts (traceability + spot checks)

From `IST_HIS_Documentation_Traceability.xlsx` (sheet **Traceability**, **63** data rows):

| Metric | Count |
|--------|-------|
| Rows | 63 |
| `adaptation_status` = Adapted for IST HIS terminology | **63** (100%) |
| `adaptation_status` = Same / identical content | **0** |
| `approval_status` = draft | **63** |
| `screenshot_verified` = N | **63** |
| `code_verified` = source-scrape | 53 |
| `code_verified` = partial | 10 |
| `test_scenario_available` = pack-stub / stub | 53 / 10 |

Depth comparison (2026-07-14):

| Corpus | Size |
|--------|------|
| Upstream RST (`docs/upstream/original/rst/`) | **105** files, **~11.8k** lines |
| IST module guides | **53** files, avg **~140** lines (template) |
| IST domain overviews | **13** files, **~15–22** lines each |
| Upstream userguide chapters with Click/Open/To create/Navigate | **23 / 44** |
| IST module READMEs with those phrases | **0 / 53** |

Example: upstream `laboratory.rst` documents lab order request fields, Create Test wizard, analytes, validation/crypto, reports. IST `health_lab/README.md` lists models and activation — **no** equivalent procedure text.

## Practical answer for claims

- Claiming “IST docs teach the same clinical/ops procedures as GNU Health docs” → **false** today.
- Claiming “IST docs cover the same *modules/topics* as the activated HIS set, with IST/UAE–QA framing” → **mostly true** for inventory (53 guides + 63 traceability links), **false** for substance depth.
- For full GNU Health procedure content, use `docs/upstream/original/` (or docs.gnuhealth.org) and apply IST UI/SAO paths separately.

## Related

- Product (not docs) comparison: `GNU_Health_vs_IST_HIS_comparison.md`
- Drift / no silent overwrite: `docs/upstream/upstream-drift-report.md`
