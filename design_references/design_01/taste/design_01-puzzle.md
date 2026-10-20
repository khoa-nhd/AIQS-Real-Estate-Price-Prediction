# Design Map

Source: `Screen Recording 2026-10-14 091300.mp4`, a design presentation analysed from frames. Sizes are in capture px; `~` marks estimates.

## Spacing Scale
- ~6, ~10, ~12, ~20 capture px
- Panel gutter ~10–12; inner panel padding ~20

## Font Hierarchy
- Figure: ~19, weight 600 (Exo 2, closest match)
- Panel label: ~16, weight 400
- Headline: ~14–16 on shrunk pages, weight 600, Title Case
- Nav: ~9, weight 400

## Color Palette
- `#0C0E1D` background (printed)
- `#030208` gutter (measured)
- `#211F36` raised surface (printed)
- `#616083` muted text (printed)
- `#51FAAA` action accent (printed; button measured `#53FCAB`)
- `#FF81FF` glow (printed; donut measured `#CE73DC`)

## Image Ratios
- Desktop mock-up ~16:10
- Phone mock-up ~9:19

## Component Tokens
- Radius: button ~6, card ~10, panel ~20, pill fully round
- Shadows: none; 1px light inner border ~`rgba(255,255,255,0.08)` plus colour glows
- Grid: bento of 3 columns at ~50/24/24%, single gutter

---

# Taste DNA

### Light Instead of Shadow
- **Trigger**: When panels needed to separate from a near-black ground.
- **Decision**: 1px light inner borders and coloured glows over drop shadows.
- **Reason**: On a ground this dark a shadow is invisible; light reads as depth where darkness can't.
- **Evidence**: no drop shadow in 14 frames; gutter `#030208` vs panel `#0A121F`; glows `#CE73DC` and `#51C892`.

### Mint Means "Do This"
- **Trigger**: When choosing where the brightest colour goes.
- **Decision**: `#51FAAA` kept to actions and the current state, under ~3% of the surface, over headings or decoration.
- **Reason**: With one bright colour the eye finds the action without reading.
- **Evidence**: three mint buttons, the active pill and the active menu item; no mint headings.

### One Violet Material
- **Trigger**: When building the dark neutrals.
- **Decision**: Every neutral tinted toward blue-violet over neutral grays.
- **Reason**: Tinted darks read as a deliberate night palette; pure grays on black read as unstyled.
- **Evidence**: printed `#0C0E1D` and `#211F36`; no pure gray sampled.

### Tiles, Not Sections
- **Trigger**: When presenting many unrelated facts in one view.
- **Decision**: A bento grid of equal-gutter panels over a scrolling page of sections.
- **Reason**: Tiles let a viewer scan several ideas in one screen, at the cost of each being small.
- **Evidence**: 7 panels in 3 uneven columns; gutter ~10–12; no vertical sections.
