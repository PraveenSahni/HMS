---
title: SAO Tab Toolbar & Action Menu — IST Health Theming
ist_his_version: 1.0.0
upstream_product: GNU Health HIS / Tryton SAO
sao_version: 7.0.53
baseline_date: 2026-07-15
status: active
vm_evidence: gnuhealth-his-01:/opt/gnuhealth/his-50/sao/src/tab.js
related:
  - docs/ist-his/SAO_EMBED_AND_SCREEN_PARITY.md
  - docs/ist-his/WORKSPACE_VISION_QA.md
  - frontend/deploy/sao-custom.css
  - frontend/deploy/sao-custom.js
---

# SAO Tab Toolbar & Action Menu — IST Health Theming

Research + implementation notes for aligning the SAO **horizontal tab toolbar**, **vertical action dropdown** (Switch → Close Tab), and **tab strip headers** with IST Health (navy / gold / Inter).

## 1. How SAO builds the chrome (source of truth)

Inspected on VM `gnuhealth-his-01`:

| Path | Role |
|------|------|
| `/opt/gnuhealth/his-50/sao/src/tab.js` | `Sao.Tab.menu_def`, `set_menu`, `create_toolbar`, `Sao.Tab.add` |
| `/opt/gnuhealth/his-50/sao/src/sao-variables.less` | `@brand-primary: #267f82` (compiled teal) |
| `/opt/gnuhealth/his-50/sao/src/theme.less` | `.dropdown-menu` shadow; `.nav-tabs` brand underline |
| `/opt/gnuhealth/his-50/sao/src/sao.less` | `nav.toolbar` sticky; `#tablist` flex strip |
| `/opt/gnuhealth/his-50/sao/src/common.js` | `ICONFACTORY._convert` → `Sao.config.icon_colors[0]` |

SAO is **jQuery + Bootstrap 3** (dropdowns via `data-toggle="dropdown"`, tabs via `data-toggle="tab"`). No separate React toolbar.

### `menu_def()` — shared action list

Both the **vertical dropdown** and the **horizontal icon buttons** are driven by the same `menu_def()` array in `Sao.Tab`:

`Switch` → `Previous` → `Next` → `Search` → *(divider)* → `New` → `Save` → `Reload/Undo` → `Duplicate` → `Delete` → … → `Close Tab`.

- Items with a `tooltip` also get a horizontal toolbar button.
- Items with `dropdown: true` (e.g. Attachment) wrap in a Bootstrap `.btn-group.dropdown`.
- `null` entries become `.divider` separators in the vertical menu.

### DOM structure

```
#tablist
  li#nav-tab-N[role=presentation]
    a[role=tab][data-toggle=tab]
      button.close  (×)
      span          ← tab.name_el (“Heal…”, truncated model name)

#tabcontent
  .tab-pane#tab-N
    .panel.panel-default.tab-form   (or .tab-board)
      nav.toolbar.panel-heading[role=toolbar]
        .container-fluid.navbar-inverse
          .dropdown.navbar-header.navbar-left
            a.navbar-brand.dropdown-toggle[data-toggle=dropdown]
              span.title            ← same short name as tab
              span.caret
            ul.dropdown-menu[role=menu]   ← VERTICAL ACTION MENU
              li[role=presentation]
                a[role=menuitem]#switch_ … #close
                  img.icon (blob SVG) + label text
              li.divider
              …
          .btn-toolbar.navbar-right[role=toolbar]   ← HORIZONTAL ICONS
            .btn-group
              button.btn.btn-default.navbar-btn#previous …
                img.icon (blob SVG)
```

Key hooks:

| UI piece | Selectors |
|----------|-----------|
| Sticky toolbar bar | `nav.toolbar.panel-heading`, `.tab-form nav.toolbar`, `.tab-board nav.toolbar` |
| Inner dark strip | `.toolbar .navbar-inverse`, `.toolbar .container-fluid.navbar-inverse` |
| Title / caret | `.toolbar .navbar-brand`, `.toolbar span.title`, `.toolbar .caret` |
| Vertical menu panel | `.toolbar .dropdown-menu`, `.toolbar .navbar-header .dropdown-menu` |
| Menu rows | `.toolbar .dropdown-menu > li > a`, `.divider` |
| Horizontal icons | `.toolbar .btn-toolbar .btn`, `.toolbar .btn.navbar-btn` |
| Tab headers | `#tablist > li > a`, `#tablist > li.active > a`, `#tablist .close` |
| Icons | `img.icon` (blob:/data: SVG from `ICONFACTORY.get_icon_img`) |

## 2. IST tokens (match login / Workspace)

From `frontend/src/styles/variables.css` + `base.css` (login uses the same stack):

| Token | Value |
|-------|--------|
| Navy | `#0a1f44` / dark `#071428` / light `#1a3056` |
| Gold | `#c9a66b` / muted `#f0e6d4` |
| Font (EN) | `"Inter", "Segoe UI", -apple-system, BlinkMacSystemFont, sans-serif` |
| Font (AR) | `"Noto Sans Arabic", …` |
| Google Fonts | Inter 400–900 + Noto Sans Arabic (same `@import` as React) |

SAO mirrors these as `--ist-*` in `frontend/deploy/sao-custom.css`.

## 3. Options (ranked) — recommend non-fork

| Rank | Approach | Pros | Cons | Verdict |
|------|----------|------|------|---------|
| **1** | **`custom.css` + `custom.js` only** (SAO auto-load) | Survives SAO upgrades; no fork; already deployed | Cannot change markup/order; blob SVG fills need JS | **Recommended** |
| **2** | Patch `sao-variables.less` + rebuild SAO | Native `@brand-primary` | Rebuild on every upstream bump; diverges from package | Avoid unless CSS specificity fails |
| **3** | Fork / edit `src/tab.js` | Full control of menu structure | Permanent merge tax; breaks “do not upgrade / do not fork SAO” strategy | **Not recommended** |

IST strategy (see `SAO_EMBED_AND_SCREEN_PARITY.md`): keep GNU Health / Tryton pinned; theme via deploy mirrors only.

## 4. What we theme (implemented)

Repo mirrors → VM:

| Repo | VM |
|------|-----|
| `frontend/deploy/sao-custom.css` | `/opt/gnuhealth/his-50/sao/custom.css` |
| `frontend/deploy/sao-custom.js` | `/opt/gnuhealth/his-50/sao/custom.js` |

### CSS (`sao-custom.css`)

- **Toolbar bar:** navy background, gold top accent, Inter, no Bootstrap green panel fill.
- **Title (“Heal…”):** white → gold on hover/open; Inter 600.
- **Horizontal buttons:** transparent on navy; gold label/icon color; navy-light hover.
- **Vertical dropdown:** white panel, gold top border, IST shadow, navy text, gold-muted hover — **no `#267f82` active**.
- **Global dropdown kill:** `.dropdown-menu > .active > a` forced to gold-muted / navy (overrides compiled Bootstrap teal).
- **`#tablist`:** muted navy inactive; active gold underline; Inter.

### JS (`sao-custom.js`)

- `Sao.config.icon_colors = [navy, muted, gold]` (Tryton monochrome root fill).
- Blob SVG rewrite (teal + beige → target color) via patched `_convert` + MutationObserver.
- **Toolbar chrome icons** (`.toolbar .btn-toolbar img`, not inside `.dropdown-menu`) → **gold**.
- Dropdown / menu-tree icons → **navy**.
- Favorites → **gold**.

## 5. Limitations

1. **Blob SVG fills** — Multi-color GH icons bake hexes into paths; CSS `color` / `fill` on `<img>` cannot recolor them. JS rewrite is required; race conditions possible on very late inserts (mitigated by observer + short sweeps).
2. **Bootstrap / compiled teal** — `dist/tryton-sao.css` hardcodes `#267f82` in many rules. Overrides need `!important` and broad selectors; a future SAO rebuild that changes class names may need selector updates.
3. **`panel-heading` shared class** — Toolbar uses `panel-heading`; global panel-header rules also apply. Toolbar-specific rules must stay more specific (`.tab-form nav.toolbar.panel-heading`).
4. **No markup changes** — Cannot rename labels, reorder actions, or replace Bootstrap dropdown with a custom React menu without forking `tab.js`.
5. **Embedded mode** — `html.ist-embedded` hides the **top** SAO navbar only; the **per-tab** `nav.toolbar` remains visible inside the Workspace iframe (by design).
6. **currentColor icons** — Only help when SVG is inline or uses `currentColor`. Toolbar actions are almost always blob `<img class="icon">`.

## 6. Deploy / verify

```bash
# From workstation (example)
gcloud compute scp frontend/deploy/sao-custom.css \
  gnuhealth-his-01:/tmp/sao-custom.css \
  --project=isthealth --zone=me-central1-a
gcloud compute scp frontend/deploy/sao-custom.js \
  gnuhealth-his-01:/tmp/sao-custom.js \
  --project=isthealth --zone=me-central1-a
gcloud compute ssh gnuhealth-his-01 --project=isthealth --zone=me-central1-a \
  --command='sudo cp /tmp/sao-custom.css /opt/gnuhealth/his-50/sao/custom.css && sudo cp /tmp/sao-custom.js /opt/gnuhealth/his-50/sao/custom.js'
```

Hard-refresh `/workspace` or `/sao/` (no trytond restart).

Checklist:

1. Open a form tab → toolbar is IST navy with gold top edge.
2. Title dropdown: Inter, navy labels, gold-muted hover, gold top border, no teal.
3. Horizontal icons: gold on navy (visible), hover navy-light.
4. Tab strip: active tab gold underline; Inter labels.
5. Left menu icons remain navy; favorites gold.
