# design_03 — Taste analysis, Steps 1–3

**Degraded-data path.** The source is a 15.5 s screen recording (1018×766) of a website design presentation for "Increase", ending on a showcase caption. There is no URL, so the skill's Playwright capture and `extract.js` could not run. Inputs used instead:

- 16 frames in `../screenshots/`.
- Pixel measurements: `pixel_palette_hero.json`, `pixel_palette_sections.json`, `pixel_samples_hero.json`, `pixel_samples_sections.json`.

Sizes are capture px; the page is shown inside a presentation frame, so CSS sizes are unknown.

### Step 1 Output — Measurements

1. **Color Palette** — page ground `#0E2924` / `#102B26` (measured; ~30% of the hero area); card fill `#12473D` to `#164B40`; code panel `#023030`; headline `#EEFAFA`; body gray-green `~#9DB8B0` (~approx); secondary button `#384647`; action gradient `#4DF4AF` → `#A1FA6A`; presentation frame gradient `#34F3BD` (left) → `#A5FA69` (right).
2. **Font Families** — one squared, rounded techno sans for headlines, nav, buttons and captions (~approx; closest Google match Exo); a monospace for code (~approx).
3. **Font Size Scale (capture px)** — hero ~42, line-height ~1.2; section headline ~34 (Title Case); card title ~15; body ~13; nav ~9; eyebrow label ~9; code ~8.
4. **Font Weights** — headlines ~500; card titles ~500; body ~400; button labels ~500.
5. **Border Radius** — cards ~10; buttons ~8; eyebrow pill ~6 with ~3 bars; code panel ~8; the frame around the dashboard screenshot ~16.
6. **Shadow Types** — no drop shadows; diffuse green radial glows (~200–300 px, ~approx) behind the hero and sections.
7. **Image Aspect Ratios** — product UI fragments only: JSON response card ~1.1:1; transfer card ~2:1; dashboard screenshot ~1.5:1. No photography, people or illustration.
8. **Card Aspect Ratios** — feature cards ~1.6:1 (250×170); list rows ~7:1; tab cards ~5:1.
9. **Spacing Scale** — card gap ~16; card padding ~20; eyebrow to headline ~10; section top ~80–100 (~approx).
10. **Layout Grid** — hero 2 columns (~50/50); feature section 3-column card grid with the headline spanning a column; a 2-column list of action rows; a 6-column feature strip (ACH, Cards, Bank, Wires, Checks, RTP); content width ~840 of 900.
11. **Section Spacing** — sections separated by large dark gaps and a glowing marquee rule ("INCREASE" between nodes), not by background changes.
12. **Component Reuse** — eyebrow pill (lime bar, teal square, label) at every section (×5 seen); dark translucent card with a top-left icon tile (×6+); list row with an icon tile (×8); gradient-filled primary button (×3); dark secondary button.
13. **Text Alignment** — hero left; "Embed Financial Services" section centred; feature sections left; footer left in columns.
14. **Neutral Color Tinting** — every dark is green-tinted: `#0E2924`, `#12473D`, `#384647`. No pure gray seen.
15. **Shadow Construction** — none; glows only.
16. **Nested Radius** — card ~10 containing an icon tile ~6; frame ~16 containing a screenshot ~8.
17. **Typography System** — Title Case headings throughout; about 6 sizes.
18. **Spacing Method** — `~approx` grid with uniform card gaps.
19. **Motion Properties** — scroll-driven; tab-style cards highlight in sequence (active filled with the green gradient); a play button on the dashboard image. Timings not measurable.
20. **Interaction Details** — the active tab card gets a gradient fill; hover states not observable.

### Step 2 Output — Patterns

### Product fragments are the illustration
- **Pattern**: Every image is a piece of real product UI (code response, transfer card, dashboard); there is no art.
- **Evidence**: Step 1 item 7.
- **Design Goal**: Shows a developer what they will actually get.

### One green family
- **Pattern**: Ground, cards, buttons and text all derive from one green-teal hue.
- **Evidence**: `#0E2924`, `#12473D`, `#384647`, `#9DB8B0`, `#4DF4AF`.
- **Design Goal**: Reads as one brand material.

### Saturated colour on the rim and the actions only
- **Pattern**: The lime-cyan gradient appears on the outer frame, primary buttons, eyebrow bars and the active tab, never as a section background.
- **Evidence**: frame `#34F3BD` → `#A5FA69`; button `#4DF4AF` → `#A1FA6A`; sections stay `#0E2924`.
- **Design Goal**: Energy without lowering text contrast.

### Section signage
- **Pattern**: Each section opens with the same eyebrow pill, then a Title Case headline.
- **Evidence**: eyebrow ×5 with identical bars.
- **Design Goal**: Readers always know a new topic has started.

### Card grid as feature catalogue
- **Pattern**: Features are equal cards with an icon tile, title and two-line caption.
- **Evidence**: 3-column grid, ~16 gap, ~10 radius.
- **Design Goal**: Scannable inventory of capabilities.

### Step 3 Output — Taste Principles (candidates → final 4)

Candidates:
1. Show the machine — real UI fragments over illustrations — JSON card, dashboard.
2. One green family — green-tinted darks over neutral grays — `#0E2924`, `#12473D`.
3. Neon on the rim — saturated gradient at edges and actions over saturated sections.
4. Section signage — an identical eyebrow pill per section over plain headings.
5. No photography — product UI over people and stock imagery.
6. Title Case — every heading capitalised.

Final 4:

### Show the Machine
- **Trigger**: When illustrating what a banking API does…
- **Decision**: They used real product fragments (a JSON response, a transfer card, a dashboard) over abstract illustration or stock photography.
- **Reason**: Their reader is a developer; seeing the payload is more persuasive than any metaphor.
- **Evidence**: three UI fragments; zero photographs or illustrations in 16 frames.

### Neon on the Rim (restraint)
- **Trigger**: When placing the brand's saturated lime-cyan…
- **Decision**: They kept it to the outer frame, the primary buttons, the eyebrow bars and the active tab, over using it for section backgrounds.
- **Reason**: The page stays dark enough for long technical text while the brand still glows.
- **Evidence**: frame `#34F3BD` → `#A5FA69`; buttons `#4DF4AF` → `#A1FA6A`; every section background measured `#0E2924`–`#164B40`.

### One Green Material
- **Trigger**: When choosing neutrals for ground, cards and secondary controls…
- **Decision**: They tinted every dark toward green-teal over neutral charcoal.
- **Reason**: Tinted darks keep the brand present even where no accent appears.
- **Evidence**: ground `#0E2924`, card `#12473D`, secondary button `#384647`; no pure gray sampled.

### Signposted Sections
- **Trigger**: When starting each new topic on a long page…
- **Decision**: An identical eyebrow pill (two coloured bars plus a label) before every headline, over plain headings or numbered sections.
- **Reason**: A repeated mark tells a scrolling reader "new topic" before they read a word.
- **Evidence**: eyebrow pill ×5 with the same bars and size; always followed by a Title Case headline.
