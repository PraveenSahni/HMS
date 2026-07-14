# Finance Employee

**Focus:** Chart of accounts, periods, journals (primarily SAO); invoice list/draft in React

## Access

Assigned via Tryton `res.group`. React currently shows menus based on Tryton menu ACL.

## Typical routes

| Route | Purpose |
|-------|---------|
| `/financial` | Invoice list, draft stub, **Financial setup checklist**, Open in SAO |
| `/companies` | Legal entities (AED / QAR) |
| `/currency` | Confirm AED / QAR present |
| `/help` | Guided workflows (`wf-finance-setup`, `wf-create-invoice`, `wf-close-period`) |

Deep CoA / fiscal year / journals / taxes / post-pay: **Open in SAO** from `/financial`.  
Full runbook: `docs/implementation/financial-setup.md`.

## Guided help

Open Help Centre → role **Finance** → **Workflow: Company financial setup**.

## Notes

- Do not enter real national IDs in training databases.
- Prefer synthetic patients (`IST-P-*`).
- Do not invent VAT/exemption rules; mark tax configuration **needs confirmation**.
