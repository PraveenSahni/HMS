---
title: IST HIS Module Guide — Health Stock
ist_his_version: 1.0.0
upstream_product: GNU Health HIS
upstream_version: 5.0.6
upstream_document: features / module source tryton.cfg
upstream_modules:
  - health_stock
country:
  - AE
  - QA
roles:
  - system-admin
  - facility-admin
implementation_status: activated
last_verified_against_code: 2026-07-14
licence: CC-BY-SA-4.0
adaptation_status: Adapted for IST HIS terminology
---

# IST HIS — Health Stock

> IST HIS is a customized healthcare information system developed by

## Module purpose

Customer-facing capability area for **Health Stock**, implemented by upstream
GNU Health module `health_stock` (package version 5.0.4).

## Technical module name

`health_stock`

## Dependencies

health, stock_lot

## Activation procedure

On the HIS server (do **not** run casually in production):

```bash
# Prefer gnuhealth-control / trytond-admin against the configured database
trytond-admin -c /opt/gnuhealth/his-50/etc/trytond.conf -d isthealth -u health_stock --activate-dependencies
```

Baseline DB `isthealth` already has this module **activated** (2026-07-14).

## Configuration prerequisites

- Company / institution master data (`company.company`, `gnuhealth.institution`)
- Users and access groups in Tryton
- Any coding catalogues required by depends (e.g. ICD modules)

## Master-data requirements

Populate reference data required by the module before synthetic clinical loads.
See `templates/IST_HIS_Implementation_Master_Data.xlsx`.

## Roles and permissions

Managed via Tryton `res.group` / `ir.model.access`. IST HIS React UI respects session roles;
do not invent permissions beyond upstream access XML without an IST custom module.

## Menu paths

Upstream SAO menus remain under GNU Health menu XML. IST React routes map selected models
(see `frontend/src/lib/tryton/models.ts`). Unmapped menus open SAO fallback.

## Screen descriptions

Prefer IST HIS React screens where implemented; otherwise SAO at `:8000` / `/sao/`.
Screen inventory is **best-effort** — verify against live menus after deploy.

## Field definitions

See `docs/upstream/model-and-field-catalogue.xlsx` filtered by module `health_stock`.
Confidence: medium (source scrape of tag `v5.0.6`).

## Models

- `gnuhealth.prescription.order`
- `gnuhealth.prescription.stock.move.create`
- `gnuhealth.prescription.stock.move.init`
- `gnuhealth.vaccination`
- `gnuhealth.vaccination.stock.move.create`
- `gnuhealth.vaccination.stock.move.init`
- `party.party`
- `stock.lot`
- `stock.move`

## Workflow states

Follow upstream model state fields (e.g. draft/confirmed/done) — do not invent states.
Mark **unverified** until confirmed in UI or proteus.

## Approval rules

Upstream wizard/button rules apply unless an IST customization is documented.

## Reports

Upstream ODT/PDF reports remain technically `gnuhealth.*` report actions; customer-facing
titles may show IST HIS where configurable.

## Integrations

Module-specific integrations (Orthanc, federation, CalDAV, etc.) only where the module
provides them. UAE/Qatar HIE connectors are **not** provided by upstream — pending IST work.

## Synthetic-data scenarios

See `synthetic-data/` packs that list `health_stock` under applicable modules.

## UAE-specific considerations

- Use synthetic Emirates ID format `SYN-AE-*` only.
- National HIE (NABIDH / Malaffi / Riayati) — **pending regulatory confirmation**; not in upstream module.

## Qatar-specific considerations

- Use synthetic Qatar ID format `SYN-QA-*` only.
- MoPH / national e-health mandates — **pending regulatory confirmation**.

## Known gaps

- Live menu/field verification against SAO screens not exhaustively screenshot-tested in this baseline.
- No IST custom Tryton module for synthetic markers; markers live in external registry.

## Troubleshooting

1. Confirm module state: `SELECT name, state FROM ir_module WHERE name='health_stock';`
2. Check trytond logs under `/opt/gnuhealth/his-50/log`
3. Do not upgrade modules as part of troubleshooting without change control

## Source traceability

| Item | Reference |
|------|-----------|
| Upstream features | https://docs.gnuhealth.org/his/features.html |
| Source | `docs/upstream/_cache/his-5.0.6/tryton/health_stock` (local cache) / Codeberg tag v5.0.6 |
| Immutable docs | `docs/upstream/original/` |
| IST policy | `docs/ist-his/IST_HIS_Naming_and_Branding_Policy.md` |
