---
title: Workspace Vision QA (IST SAO chrome)
date: 2026-07-15
status: complete
sources:
  - user_screenshot: assets image-e329b1c2 (Workspace SAO header + Party)
  - live_capture: docs/ist-his/vision-qa/live-*.png (Playwright; MCP browser tabs unavailable)
blocker_notes:
  - cursor-ide-browser MCP: tabs created then immediately unavailable (`Browser view not found` / empty tab list); could not use `browser_take_screenshot`.
  - Live `/workspace` after login landed on React dashboard (not SAO embed crop); live `/sao/` captured login chrome (navy/gold). Primary SAO-in-Workspace judgments use the user screenshot.
---

# Workspace Vision QA — IST brand / icons / spacing

## Evidence

| Source | What it shows |
|--------|----------------|
| **User screenshot** | IST Workspace shell title + navy SAO bar (`IST` gold + gold hamburger + Action search) + Party row with multi-color icon |
| **live-workspace.png** | React home after login (IST navy/gold shell) — confirms shell palette; not the SAO embed crop |
| **live-sao.png / live-sao-navbar.png** | Public `/sao/` login: navy bar, gold accents, “Login **IST HIS**” — no green/teal |

## Checks (Pass / Fail)

| # | Check | Verdict | Pixel / visual judgment |
|---|--------|---------|-------------------------|
| 1 | **IST brand vs Action search gap** | **Fail** (then fixed) | User crop: gold `IST` + hamburger sit flush left; Action search sits clearly to the right with a **~40–60px+** empty run (stacked CSS margins previously ~16+8+12px on top of Bootstrap). Reads **uneven** vs the **~8–10px** left gutter (cramped). Target: **~12–16px** brand cluster → search; **~14px** bar left padding. |
| 2 | **Menu icon colors (no green/teal)** | **Pass** | Hamburger is **gold** (`#c9a66b` family) on navy. No residual GH teal `#267f82` / green in the header icons on the user crop or live SAO login bar. |
| 3 | **Party icon colors (navy-only)** | **Fail** (then fixed) | Party figures: **navy torsos** + **beige/peach heads**. Navy/beige is **not** acceptable for IST monochrome menu icons — heads must be **navy-only**. |
| 4 | **Header alignment / gold IST wordmark** | **Pass** (wordmark) / **Fail** (left pad) | Gold `IST` wordmark present and legible; vertically centered with Action. **Fail:** wordmark **too close to left edge** (~8–10px), slightly clipped feel vs Workspace title above. |
| 5 | **Overall IST look-and-feel** | **Pass** | Navy `#0a1f44` bar + gold accents + white Action field = IST shell. Live login modal uses navy header + gold top rule + gold “IST HIS”. |
| 6 | **Visual bugs (overlap / clipping / cramped)** | **Fail** (minor) | No overlap. **Cramped** left brand; Party multi-color is the main inconsistency. Live unauthenticated navbar crop also showed truncated brand text (`I…`) — expected pre-login / non-embedded title sizing, not Workspace embed. |

## Recommended CSS / JS tweaks (applied in repo)

### CSS (`frontend/deploy/sao-custom.css`)

```css
/* Left pad ~14px; tighten brand→Action to ~8+4px (was 16+8+12) */
.navbar.navbar-inverse { padding-inline-start: 14px !important; }
.navbar-header { margin-inline-end: 8px !important; padding-inline-end: 0 !important; }
#global-search { margin-inline-start: 4px !important; }
html.ist-embedded .navbar-brand { margin-inline-end: 8px !important; }
```

### JS (`frontend/deploy/sao-custom.js`)

- Extend recolor to **beige/flesh** hexes (explicit list + HSL warm tan/peach).
- Do **not** preserve `#f0e6d4` / gold-muted on the **navy** path (that blocked Party heads).
- MutationObserver walk: recolor when `svgNeedsIstRecolor` (teal **or** beige), not only when teal is present.

## Deploy

**Done 2026-07-15:** copied to VM SAO root `/opt/gnuhealth/his-50/sao/custom.css` + `custom.js` (via `/tmp` + `sudo cp`). Hard-refresh `/workspace` (and `/sao/`). No trytond restart required.

## Retest after deploy

1. Open `/workspace` logged in → SAO bar: measure brand→Action ≈ **12–16px**, left pad ≈ **14px**.
2. Confirm hamburger remains **gold**, no teal.
3. Party (and similar GH people icons): **all-navy** silhouettes, no beige heads.
4. Favorites stars still **gold**.
