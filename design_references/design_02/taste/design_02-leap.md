# Design Map

Source: `Screenshot 2026-10-14 0914491.jpg`, a cropped hero analysed from pixels. Sizes are in capture px; `~` marks estimates.

## Spacing Scale
- ~10, ~16, ~36, ~38, ~45, ~60 capture px
- Button padding ~10×16; stat gaps ~36; hero to stats ~60

## Font Hierarchy
- Hero: ~58, weight 500–600, extended grotesque, line-height ~1.15
- Figure: ~42, weight 300, monospace
- Body: ~16.5, weight 400, neutral grotesque
- Button: ~15, monospace, uppercase
- Nav: ~14, monospace
- Label: ~9, monospace, with right-aligned index

## Color Palette
- `#1D1D1D` background (75% of area, measured)
- `~#E9F2EE` primary text
- `~#8A8A8A` secondary text
- `#3C3C3C` rules and brackets
- `#00EB9B` accent (measured)

## Image Ratios
- Hero chart graphic ~0.95:1

## Component Tokens
- Radius: 0 everywhere
- Shadows: none
- Frames: L-shaped corner brackets (~8 px arms) plus dotted or hairline rules in `#3C3C3C`
- Grid: hero 2 columns at 50/50; stats 3 equal columns; gutter ~36

---

# Taste DNA

### Corners, Not Cards
- **Trigger**: When the key figures needed grouping.
- **Decision**: L-shaped corner brackets and a hairline baseline over filled or bordered cards.
- **Reason**: Brackets frame a region like a viewfinder; the field stays continuous and figures read as readouts.
- **Evidence**: three bracket-framed stat blocks; the only surface is `#1D1D1D`; no radius, no shadow.

### Monospace Is the Instrument Voice
- **Trigger**: When setting navigation, actions and numbers.
- **Decision**: Monospace for all UI and data strings over one sans for everything.
- **Reason**: Fixed-width digits and labels read as machine output, which is the product's promise.
- **Evidence**: mono nav ~14, button ~15, figures ~42, labels ~9 with 001–003 indices.

### Green Only Where You Can Go
- **Trigger**: When choosing where colour appears.
- **Decision**: Mint `#00EB9B` on three elements over an untinted gray ground, over a branded or tinted palette.
- **Reason**: Against pure gray, green carries one meaning: action or current place.
- **Evidence**: `#1D1D1D` covers 75% of the area; mint only on the active nav item, sign-in and the primary button.

### Square and Flat
- **Trigger**: When styling the primary button and regions.
- **Decision**: Zero radius and no shadow over rounded raised controls.
- **Reason**: Hard edges read as precision; the page reads as a terminal.
- **Evidence**: button radius 0; no rounded element; no shadow.
