# IST Health accounting upload — `isthealth` @ gnuhealth-his-01

**Date:** 2026-07-15  
**Batch:** `ISTHIS-ACCT-20260715`  
**Path:** On-VM Proteus / trytond (same pattern as max-demo)  
**DB:** `isthealth`  
**Safety:** No posted `account.move` rows existed before upload; CoA was created from template (not dropped). Taxes **not** invented.

## 1. Pre-upload assessment

| Item | Before |
|------|--------|
| `company.company` | **0** |
| Currencies AED / QAR | Present (symbols unset) |
| `account.account` (CoA) | **0** |
| Fiscal years / periods | **0** |
| Journals | **6** (Cash, Expense, Revenue, Misc, Stock, Currency Exchange) |
| Invoices / posted moves | **0** / **0** |
| Account template | Minimal Account Chart (`account.account_template_root_en`) |
| Party | `IST-CO` → IST Technologies LLC (+ clinical max-demo parties) |

**Recommendation applied:** create CoA / FY / journals defaults from scratch (safe — no posted moves).

## 2. What was aligned and uploaded

### Companies & branding

| Party code | Name | Currency | Notes |
|------------|------|----------|-------|
| `IST-HC-QA` | IST Healthcare Qatar | **QAR** | Realigned from legacy `IST-CO` / IST Technologies LLC; brands noted: Iris Star / IST Technologies / IST Health |
| `IST-HC-AE` | IST Healthcare UAE | **AED** | New side-by-side legal company |

Admin user assigned to **both** companies (primary Qatar after upload).

### Currencies

| Code | Name | Symbol |
|------|------|--------|
| AED | UAE Dirham | AED |
| QAR | Qatari Rial | QR |

### Chart of Accounts

Per company, from Tryton **Minimal Account Chart** template. Account names suffixed `(IST Health demo)`.

| Company | Accounts |
|---------|---------:|
| IST Healthcare Qatar | **7** |
| IST Healthcare UAE | **7** |
| **Total** | **14** |

Roots / leaves: Minimal Account Chart, Main Receivable, Main Payable, Main Revenue, Main Expense, Main Cash, Main Tax.

### Fiscal year & periods (2026)

| Company | Fiscal year | State | Periods |
|---------|-------------|-------|--------:|
| IST Healthcare Qatar | `2026 - IST Healthcare Qatar (ISTHIS-ACCT-20260715)` (renamed from `2026`) | open | **12** monthly |
| IST Healthcare UAE | `2026 - IST Healthcare UAE (ISTHIS-ACCT-20260715)` | open | **12** monthly |
| **Total** | 2 | | **24** |

Invoice sequences attached via `account_invoice` helper (required for FY save).

### Journals (shared)

Already present — verified, no recreate:

`CASH`, `EXP`, `REV`, `MISC`, `STO`, `EXC`

### Party receivable / payable

| Party | AR | AP |
|-------|----|----|
| IST-HC-QA | Main Receivable (IST Health demo) | Main Payable (IST Health demo) |
| IST-HC-AE | Set on `party.party.account` (company=2, AR/AP ids 12/11) + account.configuration defaults | Same |

### Taxes

**Unset (0 taxes).** No VAT/healthcare rates invented. Optional `--demo-tax-zero` exists on the uploader for a clearly marked synthetic 0% placeholder — **not** used on this load.

### Invoices

Still **0** `account.invoice` rows (pack 18 / draft invoice load remains separate).

## 3. Scripts & packs

| Artefact | Path |
|----------|------|
| Assessor | `scripts/accounting/assess_accounting.py` |
| Uploader (idempotent) | `scripts/accounting/upload_ist_health_accounting.py` |
| Deploy helper | `scripts/accounting/deploy-and-run-accounting.sh` |
| Party AR/AP (Transaction) | `scripts/accounting/set_party_accounts_txn.py` |
| Final verify | `scripts/accounting/verify_accounting_final.py` |
| Pack 17 | `synthetic-data/17_accounting/` (generator + import stub → uploader) |
| Runbook | `docs/implementation/financial-setup.md` (§8 bootstrap) |

### Re-run (idempotent)

```bash
# Laptop
bash scripts/accounting/deploy-and-run-accounting.sh dry-run
bash scripts/accounting/deploy-and-run-accounting.sh execute

# On VM
export GNUHEALTH_TRYTOND_CONF=/opt/gnuhealth/his-50/etc/trytond.conf
cd /opt/gnuhealth/synthetic-data/accounting
/opt/gnuhealth/his-50/venv/bin/python upload_ist_health_accounting.py --execute
/opt/gnuhealth/his-50/venv/bin/python verify_accounting_final.py
```

## 4. Counts after upload

| Model / item | Count |
|--------------|------:|
| `company.company` | **2** |
| `account.account` | **14** |
| `account.fiscalyear` | **2** |
| `account.period` | **24** |
| `account.journal` | **6** |
| `account.tax` | **0** |
| `account.invoice` | **0** |
| Posted moves | **0** |

## 5. Remains SAO-manual

1. **Tax / VAT rates** — needs counsel/finance confirmation (UAE + Qatar healthcare). Do not invent.  
2. **CoA template sign-off** — Minimal chart used for demo; country packs **needs confirmation**.  
3. **Payment terms** and facility invoice sequence policy tweaks.  
4. **Draft → post → pay** sample invoice (React `/financial` stub + SAO post/pay).  
5. **Period close** policy before `wf-close-period` UAT.  
6. **Multi-company ACL** for non-admin finance users (record rules / company membership).  
7. **Product / health service ↔ revenue accounts** for billing lines (pack 18 / SAO).  
8. Optional: richer healthcare CoA (department revenue, insurance clearing) if finance requests.

## 6. How to verify in Workspace (Financial menu)

### React (IST HIS)

1. Sign in → **Companies** `/companies` — expect **IST Healthcare Qatar (QAR)** and **IST Healthcare UAE (AED)**.  
2. **Currencies** `/currency` — AED + QAR present.  
3. **Financial** `/financial` — setup checklist; use **Open in SAO** for CoA / FY / journals.  
4. Help → Finance → **Company financial setup** (`wf-finance-setup`).

### SAO (GNU Health)

1. Open SAO (`/sao/` or trytond UI).  
2. Set user **company** to IST Healthcare Qatar, then UAE.  
3. **Financial → Configuration → Accounts** — 7 demo accounts per company (`(IST Health demo)`).  
4. **Financial → Configuration → Fiscal Years** — 2026 open, 12 periods.  
5. **Financial → Configuration → Journals** — Cash / Revenue / Expense / …  
6. **Party** for `IST-HC-QA` / `IST-HC-AE` — Account Receivable / Payable populated (select matching company context).  
7. Smoke: create draft customer invoice → Post in open period (after payment terms if required).

## 7. Related

- `docs/implementation/financial-setup.md`  
- `docs/implementation/max-demo-synthetic-data.md`  
- `docs/implementation/UAE_Qatar_Implementation_Guide.md` § Phase 5b  
