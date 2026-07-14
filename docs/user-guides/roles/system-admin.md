# System Administrator

**Focus:** Users, groups, modules, sequences, companies, settings, **full module setup order**

## Access

Assigned via Tryton `res.group`. React currently shows menus based on Tryton menu ACL.

## Typical routes

See main Role_Based_User_Guide.md route table; prioritize screens listed in focus.

**Start here for new deployments:**

1. **Setup Hub** — `/setup` (Favorites → Setup)  
2. Help guided workflow — `/help?topic=wf-system-setup`  
3. Master doc — `docs/implementation/module-setup-dependencies.md`  
4. Financial deep runbook — `docs/implementation/financial-setup.md` (`/financial`)

Order: Companies → Currency → Administration → Party → Product → Stock → Calendar → Financial → Health.

## Guided help

Open Help Centre → `wf-system-setup` and per-area `setup-*` topics (EN/AR).

## Notes

- Do not enter real national IDs in training databases.
- Prefer synthetic patients (`IST-P-*`).
- CoA, fiscal years, journals, taxes, module apply: **SAO**. Do not invent tax rates.
