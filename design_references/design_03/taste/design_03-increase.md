# Design Map

Source: `Screen Recording 2026-10-14 091701.mp4`, a website design presentation analysed from frames. Sizes are in capture px; `~` marks estimates.

## Spacing Scale
- ~10, ~16, ~20, ~80 capture px
- Card gap ~16; card padding ~20; section top ~80–100

## Font Hierarchy
- Hero: ~42, weight 500 (Exo, closest match), Title Case
- Section: ~34, weight 500
- Card title: ~15, weight 500
- Body: ~13, weight 400
- Eyebrow: ~9
- Code: ~8, monospace

## Color Palette
- `#0E2924` background
- `#12473D` card
- `#023030` code surface
- `#EEFAFA` primary text
- `~#9DB8B0` secondary text
- `#384647` secondary button
- `#4DF4AF` → `#A1FA6A` action gradient
- `#34F3BD` → `#A5FA69` presentation frame

## Image Ratios
- Code response card ~1.1:1
- Dashboard screenshot ~1.5:1

## Component Tokens
- Radius: icon tile and eyebrow ~6; button and code panel ~8; card ~10; screenshot frame ~16
- Shadows: none; green radial glows
- Grid: hero 2 columns; cards 3 columns; feature strip 6 columns; gutter ~16

---

# Taste DNA

### Show the Machine
- **Trigger**: When illustrating what a banking API does.
- **Decision**: Real product fragments (JSON response, transfer card, dashboard) over abstract illustration or photography.
- **Reason**: The reader is a developer; seeing the payload persuades more than a metaphor.
- **Evidence**: three UI fragments; no photographs or illustrations in 16 frames.

### Neon on the Rim
- **Trigger**: When placing the saturated lime-cyan.
- **Decision**: Kept to the outer frame, primary buttons, eyebrow bars and the active tab, over section backgrounds.
- **Reason**: The page stays dark enough for long technical text while the brand still glows.
- **Evidence**: frame `#34F3BD` → `#A5FA69`; buttons `#4DF4AF` → `#A1FA6A`; sections `#0E2924`–`#164B40`.

### One Green Material
- **Trigger**: When choosing neutrals for ground, cards and secondary controls.
- **Decision**: Every dark tinted toward green-teal over neutral charcoal.
- **Reason**: Tinted darks keep the brand present where no accent appears.
- **Evidence**: ground `#0E2924`, card `#12473D`, secondary button `#384647`.

### Signposted Sections
- **Trigger**: When starting each topic on a long page.
- **Decision**: An identical eyebrow pill before every headline over plain or numbered headings.
- **Reason**: A repeated mark signals a new topic before a word is read.
- **Evidence**: the eyebrow pill appears five times, identical, each followed by a Title Case headline.
