# Design Map

Source: `Screen Recording 2026-10-14 092120.mp4`, a full landing page analysed from frames. Sizes are in capture px; `~` marks estimates.

## Spacing Scale
- ~10, ~16, ~100, ~140 capture px
- Card gap ~10; card padding ~16; section gaps ~100–140

## Font Hierarchy
- Closing headline: ~48, weight 400
- Hero: ~40, weight 600, line-height ~1.05, tight tracking
- Section: ~30, weight 400
- Price: ~28
- Card title: ~16
- Body: ~11–12
- One tight neo-grotesque (Inter Display / Satoshi-like)

## Color Palette
- `#17161C` hero ground
- `#000000` section ground
- `#1D1C24` card, `#221E2F` raised card
- `#38373C` border
- `#FDFDFF` primary text, `~#9E9AA6` secondary text
- `#6F47C2` accent, `#5C408D` accent dark, `#815CCE` accent light
- `#FEFCFD` spotlight

## Image Ratios
- Hero dashboard mock-up ~1.7:1
- Testimonial avatar 1:1

## Component Tokens
- Radius: small button ~6, FAQ row ~10, card ~14, frame ~16; CTA, toggle and nav group fully round
- Shadows: none conventional; spotlight beam and violet radial glows
- Grid: centred column; feature bento 2+2; testimonials 3 columns; gutter ~10

---

# Taste DNA

### Light Falls on the Product
- **Trigger**: When connecting the hero call to action with the product shot.
- **Decision**: A white spotlight beam from the CTA onto the dashboard over a static screenshot.
- **Reason**: The beam links "click here" to "what you get" in one gesture and pulls the eye down.
- **Evidence**: spotlight `#FEFCFD` under the CTA; dashboard lit at its top edge in f00–f02.

### Violet Means Act
- **Trigger**: When choosing where the brand violet appears.
- **Decision**: Violet only on CTAs, the active toggle, check dots and one chart bar, over violet backgrounds or tinted headings.
- **Reason**: On an almost colourless page the violet button is the only thing that asks to be pressed.
- **Evidence**: CTAs `#5C408D`–`#6F47C2`; dots `#815CCE`; grounds `#000000` and `#17161C`.

### One Centre Line
- **Trigger**: When laying out a long single-product page.
- **Decision**: Every headline, CTA, pricing card and FAQ on one centred axis, over alternating left/right rows.
- **Reason**: A single axis makes the page read as one argument; the eye never searches for the next start.
- **Evidence**: hero, section titles, pricing, FAQ (~620 wide) and the closing panel are all centred.

### Black Floor, Lifted Cards
- **Trigger**: When separating sections and grouping content.
- **Decision**: Pure black ground with long gaps and lifted tinted cards, over section bands or divider rules.
- **Reason**: Empty black lets each section breathe; lifted cards show where to read without lines.
- **Evidence**: `#000000` covers 33% of the features frame; cards `#1D1C24`–`#221E2F`; no rules; gaps ~100–140.
