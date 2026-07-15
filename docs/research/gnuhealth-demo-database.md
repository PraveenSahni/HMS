# Research: GNU Health Official Demo Database

**Date accessed:** 2026-07-15  
**IST baseline:** GNU Health HIS **5.0.6** / Tryton **7.0.53** / PostgreSQL **15.18** (`docs/upstream/UPSTREAM_BASELINE.yaml`)  
**Scope:** Whether an official demo DB exists, how to obtain it, reuse/modify rights, and fit vs our synthetic max-demo already loaded in `isthealth`.  
**Constraint:** Do **not** upgrade GNU Health. Do **not** load the official demo into production without an explicit risk review (see §7).

---

## 1. Does an official demo DB exist?

**Yes.** GNU Health publishes an official **PostgreSQL demo dump** for the 5.0 series, documents a local installer, ships the same demo in the official VM image, and hosts a public community server that exposes it.

Evidence:

| Channel | What exists | Name / artifact |
|---------|-------------|-----------------|
| Downloadable SQL dump | Series-level demo for 5.0 | `gnuhealth-50-demo.sql.gz` |
| Installer script | Downloads dump + `createdb` + `psql` import | `his-utils/scripts/demodb/install_demo_database.sh` |
| Community server | Shared online demo (resets regularly) | DB `health50` @ `federation.gnuhealth.org:443` |
| Official VM image | Preloaded demo DB | `health50` in `GNUHealth-50-debian12.vdi.gz` |

There is **no** separate patch-specific dump named `5.0.6`; official artifacts are keyed as **`50`** (5.0.x series). Odd minors (e.g. `41`) are unstable/dev dumps.

---

## 2. How is it obtained?

### A. Local dump (recommended for reusable / offline work)

1. Clone/tools: [his-utils](https://codeberg.org/gnuhealth/his-utils)  
2. As the `gnuhealth` OS user (PostgreSQL role able to create DBs):

```bash
his-utils/scripts/demodb/install_demo_database.sh 50
```

3. Script behavior (from upstream source, GPL-3.0-or-later):
   - Downloads `https://www.gnuhealth.org/downloads/postgres_dumps/gnuhealth-50-demo.sql.gz`
   - Creates database **`ghdemo50`**
   - Imports the SQL dump
   - Prints login: `admin` / `gnusolidario`
   - Warns: **check that the GNU Health kernel matches this demo DB**

4. Manual alternative: download the dump from  
   https://www.gnuhealth.org/downloads/postgres_dumps/  
   then `createdb` + `psql` import yourself (same URL pattern).

**Dump metadata (HEAD, 2026-07-15):**

| Field | Value |
|-------|-------|
| URL | https://www.gnuhealth.org/downloads/postgres_dumps/gnuhealth-50-demo.sql.gz |
| HTTP | 200 OK |
| `Last-Modified` | Sun, 03 Aug 2025 17:08:07 GMT |
| `Content-Length` | 36 230 162 bytes (~34.5 MiB gzip) |

**Naming note:** Live docs and community/VM use database name **`health50`**. The installer script creates **`ghdemo50`**. Either name works if you import into that name; client connection must match the DB you created.

Default credentials (docs + script):

- **Username:** `admin`  
- **Password:** `gnusolidario`  
- Also: `admin_es` (Spanish UI) per local-demo docs.

### B. Public community server (try only; not for persistent edits)

- **Server:** `federation.gnuhealth.org:443` (SSL)  
- **Database:** `health50`  
- **User / password:** `admin` / `gnusolidario`  
- Browser hub (alpha): https://federation.gnuhealth.org  

Docs state the community DB **resets regularly** — fine for exploration, **not** for keeping modifications.

### C. Official VirtualBox image

- Image: https://www.gnuhealth.org/downloads/images/GNUHealth-50-debian12.vdi.gz  
- Includes demo DB `health50` (same credentials).  
- Specs in docs: Debian 12, PostgreSQL 15, Python 3.11, Tryton 7.0 — aligned with our stack generation.

### D. Content of the demo (narrative)

Official userguide describes a **fictitious** Zenon–Betz family (Ana Betz, etc.) at GNU Solidario Hospital, Las Palmas, Spain — demographics, clinical history, imaging, labs, genetics, etc. Default empty install has **no** demo data; this pack is for academic/training.

---

## 3. Can it be modified and used for a local/VM deployment?

**Yes, for local/VM training and experimentation — that is the documented purpose.**

| Question | Answer |
|----------|--------|
| Local modifications allowed? | **Yes.** Tech guide: get a local demo “if you want to have demo data but **save your modifications**, access without internet, etc.” First Steps also treats demo DB as disposable/test. |
| Community server for durable changes? | **No** — resets regularly. |
| License (software / tooling) | GNU Health: **GPL v3 or later** (FAQ). Install script SPDX: **GPL-3.0-or-later**. Docs site: CC BY-SA 4.0. |
| Demo dump license | Published as an official project download for demo/training; treat as companion to the free software stack. Characters are fictitious. No separate proprietary EULA found on the dump index. **Not legal advice** — counsel if redistributing commercially. |
| Practical local steps | (1) Keep GH at **5.0.6** / Tryton **7.0.x**. (2) Import into a **new** DB (`ghdemo50` or `health50`), never overwrite `isthealth` without backup/CAB. (3) Point `trytond` / client profile at that DB. (4) Change default passwords before any network exposure. (5) Optionally customize parties/companies after import. |

---

## 4. Compatibility with IST HIS / Tryton 7 / GH 5.0.6

| Factor | Assessment |
|--------|------------|
| Series match | Dump / docs / VM / community are all **5.0 / `50`**. Our pin is **5.0.6** — same **even minor** (stable) series. |
| Patch exactness | Dump is **not** labeled `5.0.6`. File dated **2025-08-03**. Script requires kernel/demo match — expect possible module/schema drift vs a 5.0.6 install with our activated module set. Validate with `trytond` update / module activation after restore. |
| Tryton | Official 5.0 docs/VM: **Tryton 7.0**. IST: **7.0.53** — compatible generation. |
| PostgreSQL | Official VM: **15**. IST baseline: **15.18** — compatible. |
| Client | Docs: use client version matching the server/demo (FAQ). IST uses SAO **7.0.53** + React over JSON-RPC — connect to the demo DB name like any other Tryton DB. |
| Module set | Official demo targets stock GH demo modules/data. IST has **53** activated `health*` modules, **0** custom Tryton modules, DB name **`isthealth`**. Restoring the dump into a **separate** DB is the safe path; merging into `isthealth` is **not** a drop-in. |
| Geography / product | Demo is Spain / GNU Solidario Hospital narrative — **not** UAE/Qatar IST Healthcare Group org tree. |

**Verdict:** Suitable as a **side-by-side** training/reference DB on the same VM or a throwaway VM. **Not** a drop-in replacement for `isthealth` or for UAE/Qatar demos without heavy rework.

---

## 5. Pros/cons vs synthetic max-demo already in `isthealth`

Reference: `docs/implementation/max-demo-synthetic-data.md` — live load **2026-07-14** to `isthealth` (`ISTHIS-MAXDEMO-20260714`, ~4000 patients, UAE+Qatar group).

| | Official GH demo (`health50` / `ghdemo50`) | IST synthetic max-demo (`isthealth`) |
|--|---------------------------------------------|--------------------------------------|
| **Pros** | Canonical GH story (Ana Betz); matches upstream docs/tutorials; small download; community/VM parity; good for learning stock GH UX | UAE+Qatar multi-company; IST markers (`IST-*`/`SYN-*`); scale for demos (4k patients, appointments, labs, Rx, beds); controlled by our generators; aligned with Setup Hub / IST product story |
| **Cons** | Spain-centric; unknown exact patch vs 5.0.6; volume much smaller than max-demo; default public passwords; naming `health50` vs `ghdemo50`; not IST-branded | Not what upstream tutorials assume; engine vs JSON pack gaps for some packs; heavier DB; must keep synthetic-only policy |
| **Best use** | Parallel DB for GH doc walkthroughs / training | Primary IST sales/training demo on our stack |

**Recommendation:** Keep max-demo as the **IST product demo**. Optionally install official dump as **`ghdemo50`** (or `health50`) beside `isthealth` for upstream-doc parity — do **not** replace the synthetic load.

---

## 6. Exact links and access dates

All primary URLs accessed **2026-07-15** unless noted.

| Resource | URL | Accessed |
|----------|-----|----------|
| HIS docs home | https://docs.gnuhealth.org/his/ | 2026-07-15 |
| Using the Demo Database (userguide) | https://docs.gnuhealth.org/his/userguide/demodb.html | 2026-07-15 |
| Local Demo Database (techguide) | https://docs.gnuhealth.org/his/techguide/demodb.html | 2026-07-15 |
| Virtual Machine Image | https://docs.gnuhealth.org/his/techguide/installation/virtualmachine.html | 2026-07-15 |
| FAQ (demo + GPL) | https://docs.gnuhealth.org/his/appendix/faq.html | 2026-07-15 |
| Postgres dumps index | https://www.gnuhealth.org/downloads/postgres_dumps/ | 2026-07-15 |
| 5.0 demo dump | https://www.gnuhealth.org/downloads/postgres_dumps/gnuhealth-50-demo.sql.gz | 2026-07-15 (`Last-Modified`: 2025-08-03) |
| his-utils (installer host) | https://codeberg.org/gnuhealth/his-utils | 2026-07-15 |
| install script (raw) | https://codeberg.org/gnuhealth/his-utils/src/branch/main/scripts/demodb/install_demo_database.sh | 2026-07-15 |
| Community hub | https://federation.gnuhealth.org | 2026-07-15 (docs) |
| Official VM image | https://www.gnuhealth.org/downloads/images/GNUHealth-50-debian12.vdi.gz | 2026-07-15 (docs) |
| Local RST mirrors | `docs/upstream/original/rst/techguide/demodb.rst`, `userguide/demodb.rst`, `techguide/installation/virtualmachine.rst` | 2026-07-15 |
| IST baseline | `docs/upstream/UPSTREAM_BASELINE.yaml` (baseline_date 2026-07-14) | 2026-07-15 |
| IST max-demo | `docs/implementation/max-demo-synthetic-data.md` | 2026-07-15 |

Upstream docs TOC also lists “Using the Demo Database” and “Local Demo Database” under User Guide / Technical Guide (matches local Sphinx HTML under `docs/upstream/generated-reference/`).

---

## 7. Risks — do not load into production casually

**Do not restore `gnuhealth-50-demo.sql.gz` over `isthealth` (or any production DB) without CAB + backups.**

Risks:

1. **Destructive replace** — dump restore wipes/replaces target DB contents (including synthetic max-demo and any real config).  
2. **Credential exposure** — well-known `admin` / `gnusolidario`.  
3. **Schema/module mismatch** — series dump vs exact 5.0.6 + activated modules may fail or leave ir.module inconsistent.  
4. **Wrong narrative for IST demos** — Spain demo vs UAE/Qatar compliance story; synthetic ID policy may be violated if mixed.  
5. **No GH upgrade** — using the demo is not a reason to move past **5.0.6**.

Safe pattern: **new database name** on a non-production instance → validate modules → change passwords → use only for training/reference.

---

## 8. Bottom line

1. **Official demo DB exists** for GH 5.0 (`gnuhealth-50-demo.sql.gz` / `health50` / community / VM).  
2. **Obtain** via dump download, `install_demo_database.sh 50`, community server, or official VM.  
3. **Modify and reuse locally** — explicitly supported; community server is ephemeral; software is GPLv3+.  
4. **Compatible in series** with IST’s Tryton 7 / PG 15 / GH 5.0.6 stack as a **side DB**; not patch-guaranteed and not IST org data.  
5. **Prefer IST max-demo** for product demos; use official demo only as a parallel upstream-training database.
