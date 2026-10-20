# design_01 — Taste analysis, Steps 1–3

**Degraded-data path.** No live page exists: the source is a 12.6 s screen recording of a design presentation (1018×786). The skill's Phase 1 capture (Playwright screenshot plus `extract.js`) could not run. Inputs used instead:

- 14 frames: `../screenshots/f00…f13`.
- Pixel measurements: `pixel_palette_full.json`, `pixel_samples.json`, made with `../../_tools/measure_image.py` on `f04_4.1s.jpg`.

Every size below is in **capture px**: the presentation shrinks each screen into a panel, so true CSS sizes are unknown. `~approx` marks estimates read by eye. "printed" marks values written as text in the reference itself.

### Step 1 Output — Measurements

1. **Color Palette**
   - Printed swatches: `#0C0E1D` (ground), `#616083` (muted violet), `#211F36` (raised surface), `#FF81FF` (pink glow), `#51FAAA` (mint accent).
   - Measured: gutter `#030208`, panel fill `#0A121F`–`#151329`, inner page `#1B1636`, mint button `#53FCAB`, donut pink `#CE73DC` → teal `#51C892`.
   - Area: the ten quantised colours above 6% are all navy or violet between `#02020C` and `#2B2A42`. Mint and pink are each under ~3%.
2. **Font Families** — one rounded-square geometric sans throughout (nav, headlines, labels, figures); closest match Exo 2 (~approx, inferred from letterforms). No serif, no mono.
3. **Font Size Scale (capture px)** — bento pill labels ~16; donut figure "$1.2M" ~19; desktop hero headline ~16 (shrunk page); phone headline ~14; nav ~9; card captions ~7.
4. **Font Weights** — headlines semibold ~600; nav and labels regular ~400; button labels ~600.
5. **Border Radius** — outer bento panels ~18–20; phone frame ~16; inner cards ~10; pills fully rounded; button ~6.
6. **Shadow Types** — no drop shadows seen. Depth comes from 1px light inner borders (~`rgba(255,255,255,0.08)`, ~approx) and diffuse colour glows (pink and mint radial light, 120–200 px blur, ~approx).
7. **Image Aspect Ratios** — device mock-ups only: desktop page ~16:10, phone ~9:19, laptop ~16:10. No photography.
8. **Card Aspect Ratios** — bento panels ~1.3:1 (desktop), ~0.6:1 (phone), ~1.2:1 (donut), ~1.2:1 (swatches), ~7:1 (pill bar).
9. **Spacing Scale** — panel gutter ~10–12; inner panel padding ~20; pill gap ~12.
10. **Layout Grid** — bento of 3 columns at roughly 50% / 24% / 24%, in 2 rows plus one strip; panels share one gutter.
11. **Section Spacing** — one composition, no vertical sections. Separation comes only from the dark gutter.
12. **Component Reuse** — rounded dark panel (×7); pill toggle (×3); mint filled button (×3: phone, desktop nav, laptop nav); 1px-outline secondary button (×2); icon-plus-two-line-caption feature tile (×4).
13. **Text Alignment** — centred hero headlines on desktop and phone; left-aligned nav and dropdown; centred donut figure; swatch labels left and right.
14. **Neutral Color Tinting** — no pure grays. Every neutral leans blue-violet (`#0A121F`, `#1B1636`, `#2B2A42`, `#565871`).
15. **Shadow Construction** — none. Light inner borders plus coloured glows behind panels.
16. **Nested Radius** — outer panel ~20 containing card ~10 containing button ~6: concentric, child smaller than parent.
17. **Typography System** — few sizes; Title Case on every heading ("A Lot Of People Ask Us…"). No visible `ch` measure.
18. **Spacing Method** — `~approx` gap-based bento (uniform gutters); not measurable from video.
19. **Motion Properties** — the recording shows the pill toggle cycling UI/UX → Brand Personality → Illustrations, panel content cross-fading, and the donut ring filling. Durations ~0.4–0.8 s by frame count (~approx).
20. **Interaction Details** — dropdown with a hover row and a mint-tinted active item; active pill gets a mint outline and dark-green fill. Focus styles not observable.

### Step 2 Output — Patterns

### Everything sits in a dark panel
- **Pattern**: Every piece of content lives in one of seven rounded dark panels on a near-black gutter; there is no free-floating content.
- **Evidence**: panels ×7 at radius ~20; gutter `#030208` vs panel `#0A121F`–`#151329`; gutter ~10–12.
- **Design Goal**: Each idea reads as a separate tile the eye can take in one at a time.

### Violet-tinted dark scale
- **Pattern**: All neutrals come from one blue-violet ramp, from `#02020C` to `#2B2A42`.
- **Evidence**: all ten quantised colours above 6% area sit in that ramp; printed `#0C0E1D` and `#211F36`.
- **Design Goal**: The darks feel like one material rather than black plus gray.

### Mint is the only action colour
- **Pattern**: `#51FAAA` marks only actions and the active state: filled buttons, the active pill, the active dropdown item, the "Up 12%" delta.
- **Evidence**: mint under ~3% of area; button `#53FCAB`; active pill fill `#284648` with mint text.
- **Design Goal**: The next thing to click is findable at a glance on a dark field.

### Pink is light, not ink
- **Pattern**: `#FF81FF` appears only as glow and gradient (donut arc, panel underglow), never on text or controls.
- **Evidence**: donut `#CE73DC`; swatch band 3; no pink text in any frame.
- **Design Goal**: Adds warmth and depth without competing with the mint actions.

### Concentric rounding
- **Pattern**: Radii step down by nesting level, from panel ~20 to card ~10 to button ~6, with pills fully round.
- **Evidence**: Step 1 items 5 and 16.
- **Design Goal**: Nested surfaces look built from the same shape.

### One family, Title Case voice
- **Pattern**: One geometric sans carries every role; every heading is Title Case.
- **Evidence**: Step 1 items 2 and 17.
- **Design Goal**: A single consistent voice across marketing and product screens.

### Step 3 Output — Taste Principles (candidates → final 4)

Candidates:
1. Panel-everything — chose a bento of panels over free sections — 7 panels, one gutter.
2. Glow over shadow — chose coloured light over drop shadows — no shadows, pink and mint glows.
3. One action colour — chose mint for actions only over a multi-colour UI — mint <3%.
4. Tinted darks — chose violet-tinted neutrals over pure gray — no pure gray measured.
5. Title Case voice — chose Title Case headings over sentence case — every heading.
6. Concentric radii — chose stepped radii over a single radius — 20/10/6.

Final 4:

### Light Instead of Shadow
- **Trigger**: When the designers needed panels to separate from a near-black ground…
- **Decision**: They chose 1px light inner borders plus coloured glows (pink, mint) over drop shadows.
- **Reason**: On a ground this dark a shadow is invisible; light reads as depth where darkness can't.
- **Evidence**: no drop shadow in 14 frames; gutter `#030208` vs panel `#0A121F`; glows `#CE73DC`, `#51C892`.

### Mint Means "Do This" (restraint)
- **Trigger**: When choosing where the brightest colour goes…
- **Decision**: They kept `#51FAAA` to actions and the current state, under ~3% of the surface, over using it for headings, icons or decoration.
- **Reason**: With one bright colour, the eye goes straight to the action without reading.
- **Evidence**: three mint buttons, active pill, active menu item, delta "Up 12%"; no mint headings.

### One Violet Material
- **Trigger**: When building the dark neutrals…
- **Decision**: They tinted every neutral toward blue-violet (`#0C0E1D` → `#2B2A42`) over neutral grays.
- **Reason**: Tinted darks read as a deliberate night palette; pure grays on black read as unstyled.
- **Evidence**: printed `#0C0E1D` and `#211F36`; all large-area samples carry a blue cast.

### Tiles, Not Sections
- **Trigger**: When presenting many unrelated facts (product, brand, palette, metrics)…
- **Decision**: They chose a bento grid of equal-gutter panels over a long scrolling page of sections.
- **Reason**: Separate tiles let a viewer scan several ideas in one screen, at the cost of each tile being small.
- **Evidence**: 7 panels in 3 uneven columns; gutter ~10–12; no vertical sections.
