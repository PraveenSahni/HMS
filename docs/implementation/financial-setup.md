# Financial Setup Runbook — IST Health (UAE / Qatar)

**Version:** 1.0.0  
**Date:** 2026-07-14  
**Stack:** GNU Health HIS 5 / Tryton 7 + IST React frontend  
**Rule:** Do not upgrade GNU Health/Tryton without CAB. Do not invent tax or exemption rules.

## 1. What “Financial Setup” means here

In this system, **Financial Setup** is the one-time (per legal company) accounting configuration that must exist before invoices can post:

| Area | React UI | SAO / Tryton |
|------|----------|--------------|
| Legal company + party | `/companies` (list + setup wizard) | Full company options |
| Currencies (AED / QAR) | `/currency` (list) | Create/edit currency if missing |
| Chart of Accounts (CoA) | — | **SAO-only** (create from template) |
| Fiscal year & periods | — | **SAO-only** |
| Journals | — | **SAO-only** |
| Taxes / payment terms | — | **SAO-only** (rates **needs confirmation**) |
| Draft customer/supplier invoice | `/financial` stub | Post / pay / cancel |
| Period close | Help workflow → SAO | Period close wizard |

React **Financial** (`/financial`) is an **invoice list + draft stub**, not a full GL UI. Deep accounting stays in GNU Health SAO (`account_*` / `health_accounting`).

## 2. Where to click (operators)

1. Sign in to IST React.  
2. **Companies** → `/companies` — ensure UAE and/or Qatar legal entity exists with correct currency.  
3. **Currencies** → `/currency` — verify AED and/or QAR are present.  
4. **Financial** → `/financial` — use the **Financial setup checklist** and **Open in SAO** panel.  
5. **Help Centre** → `/help` — filter role **Finance**, open guided workflow **Company financial setup** (`wf-finance-setup`).  
6. Related later flows: Creating an invoice (`wf-create-invoice`), Receiving payment (`wf-receive-payment`), Closing period (`wf-close-period`).

SAO entry points (from React SaoPanel or browser):

- Proxied: `/sao/` on the same host  
- Direct fallback: trytond `:8000` (see `frontend/docs/SAO_MIGRATION.md`)

## 3. Prerequisites

- [ ] `company.company` created per country legal entity (UAE AED, Qatar QAR) — see `UAE_Qatar_Implementation_Guide.md` §3–4.  
- [ ] Accounting / invoice modules installed and active (typically `account`, `account_invoice`, `health_accounting` — **verify on VM**; do not upgrade packages).  
- [ ] Users in Finance / SystemAdmin groups have Tryton ACL for account menus.  
- [ ] Non-prod: synthetic parties only (`IST-*` / `SYN-*`); no real Emirates ID / Qatar ID.

## 4. Ordered setup (SAO-first)

Perform **once per company**. Do not share one CoA across UAE and Qatar entities without an explicit legal/accounting decision.

### 4.1 Company & currency

1. React `/companies` or SAO **Company** — create/select legal entity.  
2. Set **currency** to **AED** (UAE) or **QAR** (Qatar).  
3. React `/currency` — confirm codes exist; add in SAO if missing.

### 4.2 Chart of Accounts

1. In SAO, open accounting → **Create Chart of Accounts from template** (Tryton wizard; exact menu label may vary by locale).  
2. Select the **company** and an appropriate template for that country/currency.  
3. Confirm receivable, payable, revenue, and expense root accounts exist.

> **Needs confirmation:** Which CoA template (country pack) finance signs off for UAE vs Qatar.

### 4.3 Fiscal year & periods

1. Create **fiscal year** for the company (calendar year is common; confirm with finance).  
2. Create **periods** (usually monthly).  
3. Open the current period before posting invoices.

### 4.4 Journals

Create at least:

| Journal (typical) | Use |
|-------------------|-----|
| Sales / Revenue | Customer invoices |
| Purchase | Supplier invoices |
| Cash / Bank | Receipts and payments |

Exact names follow the CoA template — do not rename blindly after postings exist.

### 4.5 Taxes (configurable — no invented rules)

- Configure tax codes in SAO only after **counsel / finance** confirms:
  - Whether VAT (or other) applies to the facility’s services  
  - Rates, inclusive vs exclusive pricing  
  - Any healthcare **exemptions / zero-rating**  
- Until confirmed, leave tax configuration blank or draft-only and mark the item **needs confirmation**.  
- **Do not** assume UAE or Qatar healthcare is tax-exempt in the system.

### 4.6 Payment terms & sequences

- Payment terms: SAO (net days, etc.) — facility policy.  
- Invoice sequences: React `/sequences` or SAO — separate sequences per company if required.

### 4.7 Party accounting

For patients, insurers, and suppliers (party):

- Set **account receivable** / **account payable** on the party (or defaults from CoA).  
- Insurance payers: receivable on the insurer party; patient co-pay as configured by billing — **claims e-submission is a separate gap** (see gap analysis G-14).

### 4.8 Insurance receivable (operational)

1. Ensure insurer parties exist (synthetic in non-prod).  
2. Link patient insurance plans in clinical/billing flows (deep fields may be SAO).  
3. Invoice payer = patient or insurer per case.  
4. Post and reconcile in SAO; write-offs follow finance policy (**needs confirmation**).

## 5. Smoke test

1. React `/financial` → **Create draft invoice** for a synthetic party (customer out).  
2. If stub fails: CoA / defaults missing → return to §4 and SAO.  
3. In SAO: add lines if needed → **Post** → **Pay** (or partial pay).  
4. Confirm open period accepts the move.  
5. Help → run `wf-close-period` only after UAT sign-off of close policy.

## 6. UAE vs Qatar checklist

| Item | UAE | Qatar | Notes |
|------|-----|-------|-------|
| Company currency | AED | QAR | Required |
| CoA template | Confirm | Confirm | Needs confirmation |
| Fiscal calendar | Confirm | Confirm | Often Jan–Dec |
| Tax / VAT on clinical services | **Needs confirmation** | **Needs confirmation** | Do not invent |
| Insurance / eClaim | **Needs confirmation** (G-14) | Local schemes — confirm | Out of GL core |
| Multi-company isolation | Record rules TBD | Same | See org model |

## 7. React vs SAO ownership

| Task | Owner |
|------|--------|
| Invoice list, draft stub | React `/financial` |
| Company list/create stub | React `/companies` |
| Currency list | React `/currency` |
| CoA, FY, journals, taxes, post/pay, period close | **SAO** |
| Guided setup narrative | Help `wf-finance-setup` |

Extending React with full CoA wizards is **out of scope** unless product prioritizes Gap 4+ accounting parity.

## 8. Related artefacts

- Help: `wf-finance-setup`, `wf-create-invoice`, `wf-receive-payment`, `wf-close-period`  
- Full module order: `docs/implementation/module-setup-dependencies.md` · Setup Hub `/setup` · `wf-system-setup`  
- Guide: `docs/implementation/UAE_Qatar_Implementation_Guide.md`  
- Role: `docs/user-guides/roles/finance.md`  
- SAO map: `frontend/docs/SAO_MIGRATION.md`  
- Gaps: `docs/research/gap-analysis-uae-qatar.md` (claims G-14; finance config G-16; setup order G-17)

## 9. Exit criteria

- [ ] AED and/or QAR companies have CoA + open fiscal period + journals  
- [ ] Draft invoice creates from React; post/pay works in SAO  
- [ ] Tax configuration either confirmed by counsel or explicitly deferred with risk acceptance  
- [ ] Finance role can find Help workflow and SAO panel without training guesswork  
