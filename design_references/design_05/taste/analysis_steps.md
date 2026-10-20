# design_05 — Taste analysis, Steps 1–3

**Degraded-data path.** The source is a 44.1 s screen recording (880×668) scrolling a full landing page for "Finotive" (footer "© 2026 Oripic"). There is no URL, so the skill's Playwright capture and `extract.js` could not run. Inputs used instead:

- 26 frames in `../screenshots/`.
- Pixel measurements: `pixel_palette_hero.json`, `pixel_palette_features.json`, `pixel_samples_*.json`.

Sizes are capture px; the recording is downscaled, so CSS sizes are unknown.

### Step 1 Output — Measurements

1. **Color Palette** — hero ground `#17161C` / `#16151B` (violet-tinted charcoal); lower sections pure black `#000000` (33% of the features frame); cards `#1D1C24` to `#221E2F`; nav pill border `#38373C`; violet action `#5C408D` → `#6D4AA8` (hero CTA) and `#6F47C2` (pricing CTA); check dots `#815CCE`; highlighted chart bar `#5B39AA`; spotlight `#FEFCFD`; headline white `#FDFDFF`; body gray `~#9E9AA6` (~approx).
2. **Font Families** — one tight neo-grotesque with negative tracking for every role (~approx; Inter Display / Satoshi-like).
3. **Font Size Scale (capture px)** — hero ~40 (two lines, line-height ~1.05); closing headline ~48; section headings ~30; price "$13.99" ~28; card titles ~16; body ~11–12; nav ~10.
4. **Font Weights** — hero ~600; section and closing headings ~400 (lighter than the hero); card titles ~400; body ~400.
5. **Border Radius** — CTAs and toggles fully rounded; nav group pill; cards ~14; FAQ rows ~10; dashboard frame ~16; pricing card ~14.
6. **Shadow Types** — no conventional drop shadows; a white spotlight beam from the CTA onto the dashboard; violet radial glows inside cards and behind the closing panel.
7. **Image Aspect Ratios** — dashboard mock-up ~1.7:1 (hero); feature cards contain product UI fragments; card-fan illustration in pricing. No photography except testimonial avatars (1:1).
8. **Card Aspect Ratios** — feature cards ~1.8:1 (wide) and ~1.4:1; testimonial cards ~0.9:1; FAQ rows ~11:1.
9. **Spacing Scale** — card gap ~10; card padding ~16; section gap ~100–140 (~approx, long black stretches between sections).
10. **Layout Grid** — centred single column for headings; a feature bento of 2 + 2 cards with uneven widths (~60/40, ~40/60); testimonials 3 columns; FAQ ~620 wide centred; content width ~730 of 880.
11. **Section Spacing** — very large black gaps; sections are separated by emptiness, not rules.
12. **Component Reuse** — violet pill CTA with ↗ (×4); dark card with a violet corner glow (×8+); pill toggle (Monthly / Yearly); FAQ accordion row (×4); check-dot list row (×7).
13. **Text Alignment** — centred hero, section titles, pricing and closing panel; left-aligned inside cards and FAQ rows.
14. **Neutral Color Tinting** — hero neutrals tinted violet (`#17161C`, `#1D1C24`); lower sections pure black.
15. **Shadow Construction** — light beam plus glows; not shadows.
16. **Nested Radius** — dashboard frame ~16 containing tiles ~10 containing buttons ~6.
17. **Typography System** — tight tracking on headings (~-0.03 to -0.04 em, ~approx); a heavy hero, then lighter section headings.
18. **Spacing Method** — `~approx` gap-based grids.
19. **Motion Properties** — headings reveal word by word from blur ("See what…" caught mid-blur in f11–f13); the spotlight pulses; scroll-linked reveals. Timings not measurable.
20. **Interaction Details** — FAQ rows expand (the first open, with a chevron); the pricing toggle has an active violet pill. Focus not observable.

### Step 2 Output — Patterns

### Centre line
- **Pattern**: Every section headline, the CTA, the pricing card and the closing panel sit on one centred axis; only card interiors are left-aligned.
- **Evidence**: Step 1 item 13.
- **Design Goal**: Steady, single-path scrolling.

### Violet only for "act" and "selected"
- **Pattern**: Violet fills CTAs, the active toggle, check dots and the highlighted chart bar; everything else is charcoal or black.
- **Evidence**: `#5C408D`–`#6F47C2` on 4 CTAs; `#815CCE` dots; neutrals `#000000`–`#221E2F`.
- **Design Goal**: Actions are unmissable on a dark page.

### Emptiness as the separator
- **Pattern**: Sections are divided by 100+ px of pure black, with no rules or alternating bands.
- **Evidence**: Step 1 items 9 and 11.
- **Design Goal**: Each section is read on its own.

### Product as illustration
- **Pattern**: Cards show UI fragments (balances, activity, cards) instead of icons or photos.
- **Evidence**: hero dashboard; feature cards; a card fan.
- **Design Goal**: Shows what the product looks like.

### Heavy entry, light continuation
- **Pattern**: The hero is weight ~600; all later headings are ~400.
- **Evidence**: Step 1 item 4.
- **Design Goal**: One loud moment, then a calmer reading voice.

### Step 3 Output — Taste Principles (candidates → final 4)

Candidates:
1. Light falls on the product — a spotlight beam from the CTA onto the dashboard over a static hero image.
2. Violet means act — violet restricted to actions and the selected state over violet surfaces.
3. One centre line — every section centred over alternating left/right layouts.
4. Black floor, lifted cards — pure black sections with slightly lifted tinted cards over coloured section bands.
5. Heavy entry, light continuation — weight 600 hero, 400 elsewhere.
6. Blur-reveal headings — motion on type over static headings.

Final 4:

### Light Falls on the Product
- **Trigger**: When connecting the hero's call to action with the product shot below it…
- **Decision**: They drew a white spotlight beam from the "Get Started" button down onto the dashboard over placing a static screenshot under the hero.
- **Reason**: The beam links "click here" to "this is what you get" in one gesture and pulls the eye down the page.
- **Evidence**: spotlight `#FEFCFD` directly under the CTA; dashboard frame lit at its top edge in f00–f02.

### Violet Means Act (restraint)
- **Trigger**: When choosing where the brand violet appears…
- **Decision**: They kept violet to CTAs, the active toggle, check dots and one highlighted chart bar, over violet section backgrounds or tinted headings.
- **Reason**: On an almost colourless page the violet button is the only thing that asks to be pressed.
- **Evidence**: CTAs `#5C408D`–`#6F47C2`; dots `#815CCE`; all section grounds `#000000` / `#17161C`; headings white.

### One Centre Line
- **Trigger**: When laying out a long single-product page…
- **Decision**: Every section headline, CTA, pricing card and FAQ on one centred axis, over alternating left/right feature rows.
- **Reason**: A single axis makes the page read as one continuous argument; the eye never has to look for where the next section starts.
- **Evidence**: hero, "Simplify the way you see your money", pricing, FAQ (~620 wide) and closing panel all centred.

### Black Floor, Lifted Cards
- **Trigger**: When separating sections and grouping content…
- **Decision**: Pure black ground with long empty gaps, and content in slightly lifted violet-tinted cards, over alternating section bands or divider rules.
- **Reason**: Empty black lets each section breathe; lifted cards show where to read without adding lines.
- **Evidence**: `#000000` covers 33% of the features frame; cards `#1D1C24`–`#221E2F`; no rules; gaps ~100–140.
