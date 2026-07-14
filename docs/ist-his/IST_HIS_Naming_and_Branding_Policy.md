---
title: IST HIS Naming and Branding Policy
ist_his_version: 1.0.0
upstream_product: GNU Health HIS
upstream_version: 5.0.6
implementation_status: policy
last_verified_against_code: 2026-07-14
licence: CC-BY-SA-4.0
legal_review: REQUIRED
---

# IST HIS Naming and Branding Policy

**Product (customer-facing):** IST HIS — Iris Star Hospital Information System  

**Upstream:** GNU Health HIS 5.0.6 on Tryton 7.0.53

## 6.1 Replace with “IST HIS”

Use IST HIS branding in:

- Product titles, page headers, login screen, navigation headings
- Help-centre headings, user/implementation manuals, training material
- Client-facing screenshots and configurable report headers
- Email/notification templates and architecture diagrams for customers
- Customer-facing file names (e.g. `IST_HIS_*` templates)

## 6.2 Preserve technical names

Do **not** rename without a formal migration design:

- Python package names (`gnuhealth-*`)
- Tryton module names (`health`, `health_lab`, …)
- Model names beginning with `gnuhealth.`
- Database table names, XML IDs, API fields, configuration parameters
- Entry-point commands, module dependencies, `gnuhealth-control` commands
- Existing migration references

### Examples

| Customer-facing name | Technical identifier |
|----------------------|----------------------|
| IST HIS Patient | `gnuhealth.patient` |
| IST HIS Laboratory | module `health_lab` |
| IST HIS Inpatient Management | module `health_inpatient` |

**Do not** perform naive global search-replace of “GNU Health” → “IST HIS” in code or technical docs.

## 6.3 Attribution

IST HIS is a customized healthcare information system developed by
IRIS STAR Technologies and based on GNU Health HIS.

Portions of this documentation are adapted from the GNU Health
Hospital Information System documentation, Copyright GNU Solidario,
and are made available under the Creative Commons
Attribution-ShareAlike 4.0 International licence.

GNU Health software components are licensed under the GNU General
Public License version 3 or later. IST-specific components must carry
the applicable copyright and licence notices.


## 6.4 Legal review flag

**FLAG: LEGAL REVIEW REQUIRED** before commercial release covering trademarks,
CC-BY-SA share-alike for adapted docs, GPL compliance, and non-endorsement wording.
