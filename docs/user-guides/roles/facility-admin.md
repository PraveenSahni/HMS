# Facility Administrator

**Focus:** Institution settings, departments, local users, facility-scoped setup after legal company exists

## Access

Assigned via Tryton `res.group`. React currently shows menus based on Tryton menu ACL.

## Typical routes

See main Role_Based_User_Guide.md route table; prioritize screens listed in focus.

**Setup orientation:**

1. Confirm country company exists (Country/System admin) — then use **Setup Hub** `/setup`  
2. Help — `/help?topic=wf-system-setup` and `setup-health`  
3. Dependencies — `docs/implementation/module-setup-dependencies.md`  
4. Institution — `/settings`; clinical smoke via `/patients`, `/appointments`

Facility admins typically own institution/units and local users after Companies + Administration foundation.

## Guided help

Open Help Centre → workflows for this role (EN/AR); system setup overview `wf-system-setup`.

## Notes

- Do not enter real national IDs in training databases.
- Prefer synthetic patients (`IST-P-*`).
- Do not share stock or CoA across UAE/Qatar entities without legal approval.
