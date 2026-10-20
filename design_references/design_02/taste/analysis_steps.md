# design_02 — Taste analysis, Steps 1–3

**Degraded-data path.** The source is one cropped screenshot (1014×759) of a landing-page hero, with no URL. The skill's Playwright capture and `extract.js` could not run. Inputs used instead:

- `../screenshots/source_screenshot.jpg`.
- Pixel measurements: `pixel_palette_full.json`, `pixel_samples.json`.

Sizes are capture px; the original was probably wider (likely about 1440 CSS px, so about 0.70× scale), but this is unconfirmed. Only the first screen is visible: no lower sections, footer, forms or states.

### Step 1 Output — Measurements

1. **Color Palette** — ground `#1D1D1D` (75.1% of area; 89% with near-identical `#1B1B1B` and `#1F1F1F`); headline near-white with a faint green cast `~#E9F2EE` (quantised `#CAEFE2`); accent mint `#00EB9B` (button fill, measured), also on the active nav item and "SIGN IN"; body text white, second sentence gray `~#8A8A8A` (~approx); rules and brackets `#3C3C3C`.
2. **Font Families** — three roles:
   - display: an extended grotesque for the headline (~approx; close to a wide-cut neo-grotesk);
   - body: a neutral grotesque (~approx, Inter-like);
   - mono: nav, button label, stat figures and stat labels (~approx, IBM Plex Mono-like).
3. **Font Size Scale (capture px)** — headline ~58, line-height ~1.15; stat figures ~42 mono light; body ~16.5; nav ~14 mono; button label ~15 mono uppercase; stat labels ~9 mono.
4. **Font Weights** — headline ~500–600; body ~400; mono nav ~400; stat figures ~300.
5. **Border Radius** — 0 on the button and everything else. No rounded elements.
6. **Shadow Types** — none.
7. **Image Aspect Ratios** — one abstract chart graphic, ~0.95:1, right half of the hero. No photographs.
8. **Card Aspect Ratios** — no cards. Stat blocks are bracket-framed regions ~3.2:1 (282×88).
9. **Spacing Scale** — button padding ~10×16; hero text block to button ~38; stat blocks 3 across with ~36 gaps; nav to rule ~45.
10. **Layout Grid** — hero 2 columns, ~50/50 (text left, chart right); stats 3 equal columns; content width ~910 of 1014 (~56 side margins).
11. **Section Spacing** — hero to stats ~60. Separated by bracket marks and a thin underline, not by fills.
12. **Component Reuse** — corner-bracket frame (header rule, 3 stat blocks); mono label + right-aligned index "001 / 002 / 003" (×3); mono link with ↗ arrow (Docs, SIGN IN, TRADE NOW).
13. **Text Alignment** — headline, body and button left-aligned; stat figures centred in their blocks; stat labels left with index right.
14. **Neutral Color Tinting** — pure gray: `#1D1D1D`, `#3C3C3C`, `#8A8A8A`. Only the headline white carries a faint green tint.
15. **Shadow Construction** — none.
16. **Nested Radius** — not applicable (0 everywhere).
17. **Typography System** — about 6 sizes; large jumps (58 → 42 → 16.5). Mono for every data or UI string, sans for prose, display for one headline. Uppercase only on button and sign-in.
18. **Spacing Method** — `~approx` grid-based; not measurable.
19. **Motion Properties** — not observable in a still.
20. **Interaction Details** — the active nav item is shown in mint; external links carry ↗. Focus not observable.

### Step 2 Output — Patterns

### Frame marks replace containers
- **Pattern**: Regions are defined by L-shaped corner brackets and dotted or hairline rules, never by filled boxes or borders.
- **Evidence**: brackets at the header rule and three stat blocks; rule `#3C3C3C`; no surface other than `#1D1D1D`.
- **Design Goal**: Groups content while keeping one continuous dark field.

### Monospace for anything that is data or UI
- **Pattern**: Every nav item, button, figure, label and index is mono; only the headline and prose are not.
- **Evidence**: Step 1 items 2, 3 and 12.
- **Design Goal**: Signals "instrument" and aligns digits.

### One hue on pure gray
- **Pattern**: The only saturated colour is mint `#00EB9B`; all neutrals are untinted gray.
- **Evidence**: `#1D1D1D` 75%; mint on the button, active nav and sign-in only.
- **Design Goal**: Every green item reads as "go" or "here".

### Square, flat, borderless
- **Pattern**: Zero radius, zero shadow, the button a flat fill.
- **Evidence**: Step 1 items 5 and 6.
- **Design Goal**: Reads as a tool rather than a consumer app.

### Big contrast between headline and labels
- **Pattern**: The headline is about 6× the stat labels; figures sit between them.
- **Evidence**: 58 / 42 / 16.5 / 9.
- **Design Goal**: Three clear reading levels: claim, numbers, captions.

### Step 3 Output — Taste Principles (candidates → final 4)

Candidates:
1. Frame marks — corner brackets over boxed cards — 4 bracket frames, no surfaces.
2. Mono voice — mono for UI and data over one sans — nav, button, figures, labels.
3. One hue on pure gray — untinted gray ground over brand-tinted dark — `#1D1D1D`.
4. Square and flat — 0 radius, no shadow over rounded cards — whole screen.
5. Indexed facts — "001/002/003" numbering over unlabelled stats.
6. Two-tone lead — the second sentence in gray over a single-colour paragraph.

Final 4:

### Corners, Not Cards (restraint)
- **Trigger**: When the three key figures needed grouping…
- **Decision**: They marked each block with four L-shaped corner brackets and a hairline baseline over enclosing it in a filled or bordered card.
- **Reason**: Brackets frame a region the way a viewfinder does; the field stays one continuous surface and the figures read as readouts, not as tiles.
- **Evidence**: 3 stat blocks and the header rule use brackets; the only surface is `#1D1D1D`; no radius, no shadow.

### Monospace Is the Instrument Voice
- **Trigger**: When setting navigation, actions and numbers…
- **Decision**: A monospace face for all UI and data strings, keeping a grotesque only for the headline and prose, over one sans for everything.
- **Reason**: Fixed-width digits and labels read as machine output; for a trading terminal that is the promise.
- **Evidence**: mono nav 14, button 15, figures 42, labels 9 with indices; headline in a wide grotesque.

### Green Only Where You Can Go
- **Trigger**: When choosing where colour appears…
- **Decision**: Mint `#00EB9B` on the current nav item, sign-in and the primary action only, on an untinted gray ground, over a branded or tinted palette.
- **Reason**: With pure gray around it, green carries one meaning: available action or current place.
- **Evidence**: ground `#1D1D1D` (75%); mint on 3 elements; neutrals have no tint.

### Square and Flat
- **Trigger**: When styling the primary button and every region…
- **Decision**: Zero corner radius and no shadow over the rounded, raised controls of consumer fintech.
- **Reason**: Hard edges read as precision; the page looks like a terminal rather than an app store.
- **Evidence**: button radius 0; no rounded element; no shadow anywhere in the capture.
