# design_04 — Taste analysis, Steps 1–3

**Degraded-data path.** The source is one screenshot (910×562) of a landing-page hero with a dashboard mock-up for "Payal". There is no URL, so the skill's Playwright capture and `extract.js` could not run. Inputs used instead:

- `../screenshots/source_screenshot.jpg`.
- Pixel measurements: `pixel_palette_full.json`, `pixel_samples.json`.

Sizes are capture px. Only the first screen and the top of the dashboard are visible.

### Step 1 Output — Measurements

1. **Color Palette**
   - Page gradient: deep navy `#112258` / `#182D64` at top-left → `#4468A5` → light blue `#81B7F3` at bottom-right (measured).
   - Dashboard panel: blue gradient `#111D55` → `#4C79B7`.
   - Metric tiles: translucent `#283961` with lighter edge `#7281A1`.
   - Lower cards: near-black `#18171C` (72% of their region).
   - Text: white; secondary `~#B9CED1`.
   - CTA gradient `#5379E4` → `#719DDC`; email field `#EAEAEA`.
2. **Font Families** — one geometric grotesque for everything: headline, nav, figures, labels (~approx; Manrope / General Sans-like). No mono, no serif.
3. **Font Size Scale (capture px)** — big balance ~42 light; headline ~30; tile figures ~19; card titles ~14; nav ~11; tile labels ~8.
4. **Font Weights** — headline ~400–500; balance ~300; tile figures ~400; nav ~400. No bold seen.
5. **Border Radius** — CTA, email field, badge and icon buttons fully rounded (pill or circle); metric tiles ~10; dashboard panel ~18; outer dashboard frame ~22; lower cards ~20.
6. **Shadow Types** — no drop shadows. Depth from translucency, lighter tile edges and a glossy 3D ring render behind the tiles.
7. **Image Aspect Ratios** — 3D render as panel background (~2.6:1 panel); avatar circles ~1:1.
8. **Card Aspect Ratios** — metric tiles ~1.9:1 (100×52); lower cards ~1.4:1.
9. **Spacing Scale** — tile gap ~8; tile padding ~10; panel padding ~18; header-to-hero ~70.
10. **Layout Grid** — hero 2 columns (headline left ~55%, text and email right ~35%); dashboard panel full width; tiles in a 2×2 grid at right; lower cards in 3 columns.
11. **Section Spacing** — hero to dashboard ~30; the dashboard overlaps the page gradient as a framed object.
12. **Component Reuse** — translucent metric tile (×4); round icon button (×6, active one white); pill controls (CTA, email, badge).
13. **Text Alignment** — all left-aligned, including figures inside tiles.
14. **Neutral Color Tinting** — darks tinted blue (`#112258`, `#283961`); the lower cards `#18171C` are slightly violet-black.
15. **Shadow Construction** — none.
16. **Nested Radius** — frame ~22 > panel ~18 > tile ~10 > icon button circle: concentric.
17. **Typography System** — few sizes; the balance figure dims its decimals ("375,928" white, ".00" at ~40% opacity).
18. **Spacing Method** — `~approx` gap-based tile grid.
19. **Motion Properties** — not observable.
20. **Interaction Details** — the active icon button is filled white; the email field has an inline round submit button. Focus not observable.

### Step 2 Output — Patterns

### Translucent tiles over a lit gradient
- **Pattern**: Data sits in semi-transparent tiles on a blue gradient lit by a 3D render.
- **Evidence**: tile `#283961` with lighter edge `#7281A1`; panel `#111D55` → `#4C79B7`.
- **Design Goal**: Data looks like a layer floating above the product's surface.

### Integer first, decimals dimmed
- **Pattern**: Large figures dim the fractional part.
- **Evidence**: "$375,928" white plus ".00" at ~40%.
- **Design Goal**: Reads the magnitude at a glance while keeping precision available.

### Everything round
- **Pattern**: Controls are pills or circles; containers step down concentrically.
- **Evidence**: Step 1 items 5 and 16.
- **Design Goal**: A soft, approachable tone for a finance product.

### Blue, then black
- **Pattern**: The hero and the summary panel are blue; working cards below are near-black.
- **Evidence**: blue `#112258`–`#81B7F3` vs cards `#18171C`.
- **Design Goal**: Separates the headline view from operational detail.

### One light-to-regular voice
- **Pattern**: One family, no bold, large figures in light weight.
- **Evidence**: Step 1 items 2 to 4.
- **Design Goal**: Calm reading of large numbers.

### Step 3 Output — Taste Principles (candidates → final 4)

Candidates:
1. Dim the decimals — fractional digits at ~40% over full-strength figures.
2. Glass over light — translucent tiles over a lit gradient over solid cards with shadows.
3. Pill geometry — pills and circles for every control over rectangular buttons.
4. Quiet headline — sentence case, regular weight, no gradient text over a bold display headline.
5. Blue, then black — blue summary vs black detail cards.

Final 4:

### Dim the Decimals
- **Trigger**: When showing a large monetary figure…
- **Decision**: They printed the integer part in full white and the decimals at ~40% opacity, over one uniform weight and colour.
- **Reason**: People read the size of money from its leading digits; dimming the tail keeps precision without competing.
- **Evidence**: "$375,928" white plus ".00" dimmed; ~42 capture px, light weight.

### Glass Over Light
- **Trigger**: When giving metric tiles depth on a coloured panel…
- **Decision**: Translucent tiles with a lighter 1px edge over a gradient lit by a 3D render, over opaque cards with drop shadows.
- **Reason**: Translucency keeps the panel's light visible through the data, so the figures feel part of one surface.
- **Evidence**: tile `#283961` / edge `#7281A1`; panel `#111D55` → `#4C79B7`; no drop shadow.

### Round Controls, Stepped Containers
- **Trigger**: When shaping controls and containers…
- **Decision**: Pills and circles for every control, with container radii stepping down (~22 → ~18 → ~10), over square or single-radius UI.
- **Reason**: Round controls read as touchable and friendly, which a payments product needs to feel safe.
- **Evidence**: CTA, email field, badge and icon buttons fully round; frame ~22, panel ~18, tile ~10.

### Quiet Headline (restraint)
- **Trigger**: When writing the hero headline…
- **Decision**: Sentence case at regular weight in plain white, with no bold, gradient text or eyebrow label (only a small trust badge), over a heavy display headline.
- **Reason**: The dashboard below is the spectacle; a calm headline lets it carry the first screen.
- **Evidence**: headline ~30 capture px at weight ~400–500; no bold anywhere; the balance figure (~42) is larger than the headline.
