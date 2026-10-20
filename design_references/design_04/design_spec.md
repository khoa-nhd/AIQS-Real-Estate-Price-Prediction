# design_04 — design specification (Payal hero)

Traceable to: `source.md`, `taste/design_04-payal.md`, `taste/analysis_steps.md`, `design_tokens.json`.

## 1. What makes it visually distinctive

A lit blue gradient world: the product's summary panel glows with a 3D glass render behind translucent figure tiles. The one big balance figure dims its decimals. Every control is a pill or a circle, and the headline stays quiet so the panel can lead.

## 2. Core design principles

- **Dim the decimals.**
- **Glass over light:** translucent tiles on a lit gradient.
- **Round controls, stepped containers.**
- **Quiet headline.**

## 3. Tokens

| Token | Value | Basis |
|---|---|---|
| Page gradient | `#112258` → `#4468A5` → `#81B7F3` | measured |
| Panel gradient | `#111D55` → `#4C79B7` | measured |
| Tile | `#283961`, edge `#7281A1` | measured |
| Dark card | `#18171C` | measured |
| Secondary text | `~#B9CED1` | estimated |
| CTA gradient | `#5379E4` → `#719DDC` | measured |
| Field | `#EAEAEA` | measured |
| Family | geometric grotesque (Manrope-like) | inferred |
| Radius | 10 / 18 / 20 / 22 / pill | estimated |
| Breakpoints, focus, CSS sizes | unknown | — |

## 4. Recurring components

- Translucent metric tile (label above, figure below).
- Round icon button (the active one white).
- Pill CTA with a blue gradient.
- White pill input with an inline round submit button.
- Pill badge with avatars.
- Near-black rounded content card.

## 5. Essential to its identity

The blue gradient field with a lit panel; translucent tiles with light edges; the dimmed-decimal hero figure; pill and circle controls; one calm geometric sans; blue summary above black detail.

## 6. Adapt rather than copy for #REP

- **The balance figure** becomes the estimate figure in tỷ đồng. The dimming idea maps to "5" in full and ",9 tỷ đồng" dimmed, keeping magnitude first.
- **The fake metrics** (revenue growth, chargeback rate) are dropped. The 2×2 tiles hold real facts: uncertainty status, number of unknown inputs, best cross-validated MAE (labelled as such), and training rows.
- **The 3D glass render** is decoration with no purpose in #REP and no asset available. A CSS radial light on the panel replaces it.
- **The email capture** becomes the primary action area. The pill input style carries over to the form fields.
- **The avatar trust badge** is invented proof and is dropped (no testimonials exist).
- **Brand:** no Payal name or logo.

## 7. Accessibility and responsive considerations

- **Text over the gradient:** white on the light end (`#81B7F3`) is 2.1:1 and fails. Text must sit on the darker part, or on tiles darkened enough.
- **Dimmed decimals** at 40% opacity fail as text. In #REP the dim part is not information-bearing alone: the full value is repeated in words.
- **Pill inputs** need visible boundaries of at least 3:1.
- **Phone:** the 2×2 tiles stay 2×2 at 390px only if each tile is wide enough; otherwise they go to 1 column.

## 8. What Streamlit cannot reproduce, and the closest alternative

| Reference element | In Streamlit |
|---|---|
| 3D glass render | CSS radial gradients |
| True backdrop-blur glass | Semi-transparent fills (blur optional, adds cost) |
| Pill email input with an inline button | Styled `st.number_input` / `st.selectbox` in pill shape; a separate pill button |
| Round icon nav | `st.tabs` styled as round-ended segments |

## 9. #REP interface plan

- **Header:** wordmark left, pill nav centre, pill primary action right.
- **Hero:** quiet headline left, description right.
- **Summary panel (blue, lit):** estimate figure with dimmed tail on the left; 2×2 translucent tiles of real facts on the right.
- **Form:** near-black cards below, in pill-shaped fields, grouped by Vị trí, Kích thước, Kết cấu, Thông tin thêm.
- **Accuracy and data views:** near-black cards with a real table and chart, and a pill segment switch.
