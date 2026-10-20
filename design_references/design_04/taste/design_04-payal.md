# Design Map

Source: `Screenshot 2026-10-14 091959.jpg`, a hero with a dashboard mock-up analysed from pixels. Sizes are in capture px; `~` marks estimates.

## Spacing Scale
- ~8, ~10, ~18, ~30, ~70 capture px
- Tile gap ~8; tile padding ~10; panel padding ~18

## Font Hierarchy
- Hero figure: ~42, weight 300, decimals dimmed
- Headline: ~30, weight 400–500, sentence case
- Tile figure: ~19, weight 400
- Card title: ~14
- Nav: ~11
- Label: ~8
- One geometric grotesque (Manrope / General Sans-like)

## Color Palette
- `#112258` → `#4468A5` → `#81B7F3` page gradient
- `#111D55` → `#4C79B7` panel gradient
- `#283961` translucent tile, `#7281A1` tile edge
- `#18171C` dark card
- `#FFFFFF` primary text, `~#B9CED1` secondary text
- `#5379E4` → `#719DDC` call-to-action gradient
- `#EAEAEA` input field

## Image Ratios
- 3D render behind the panel (~2.6:1 panel)
- Avatars 1:1

## Component Tokens
- Radius: tile ~10, panel ~18, card ~20, frame ~22; controls are pills or circles
- Shadows: none; translucency and 1px light edges
- Grid: hero 2 columns; tiles 2×2; cards 3 columns; tile gap ~8

---

# Taste DNA

### Dim the Decimals
- **Trigger**: When showing a large monetary figure.
- **Decision**: Integer part in full white, decimals at ~40% opacity, over uniform weight and colour.
- **Reason**: People read money's size from its leading digits; dimming the tail keeps precision without competing.
- **Evidence**: "$375,928" white plus ".00" dimmed; ~42 capture px at weight 300.

### Glass Over Light
- **Trigger**: When giving metric tiles depth on a coloured panel.
- **Decision**: Translucent tiles with a lighter 1px edge over a lit gradient, over opaque shadowed cards.
- **Reason**: Translucency keeps the panel's light visible through the data, so figures feel part of one surface.
- **Evidence**: tile `#283961`, edge `#7281A1`; panel `#111D55` → `#4C79B7`; no drop shadow.

### Round Controls, Stepped Containers
- **Trigger**: When shaping controls and containers.
- **Decision**: Pills and circles for controls, with radii stepping ~22 → ~18 → ~10, over square or single-radius UI.
- **Reason**: Round controls read as touchable and friendly, which a payments product needs to feel safe.
- **Evidence**: CTA, email field, badge and icon buttons are fully round; frame ~22, panel ~18, tile ~10.

### Quiet Headline
- **Trigger**: When writing the hero headline.
- **Decision**: Sentence case at regular weight in plain white, with no bold or gradient text, over a heavy display headline.
- **Reason**: The dashboard below is the spectacle; a calm headline lets it carry the first screen.
- **Evidence**: headline ~30 capture px at weight 400–500; no bold anywhere; the balance figure (~42) is larger than the headline.
