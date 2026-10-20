# design_01 — design specification (Puzzle presentation)

Traceable to: `source.md`, `taste/design_01-puzzle.md`, `taste/analysis_steps.md`, `design_tokens.json`. Values marked "printed" are written in the reference itself; "measured" means sampled from pixels; everything else is estimated.

## 1. What makes it visually distinctive

A night-violet bento board: every piece of content sits in its own rounded dark panel, lit from behind by soft pink and mint glows instead of shadows. One mint colour marks every action. A pink-to-teal gauge is the only large colour shape.

## 2. Core design principles

- **Light instead of shadow:** depth from 1px light borders and colour glows.
- **Mint means "do this":** `#51FAAA` only on actions and the current state.
- **One violet material:** all neutrals tinted blue-violet.
- **Tiles, not sections:** a bento grid with one gutter.

## 3. Tokens

| Token | Value | Basis |
|---|---|---|
| Ground | `#0C0E1D` | printed |
| Gutter | `#030208` | measured |
| Panel | `#0A121F`–`#151329` | measured |
| Raised surface | `#211F36` | printed |
| Muted | `#616083` | printed |
| Action | `#51FAAA` | printed |
| Glow | `#FF81FF` → `#51C892` | printed / measured |
| Family | Exo 2 | inferred |
| Radius | 6 / 10 / 20 / pill | estimated |
| Gutter | ~10–12 capture px | estimated |
| Line height, breakpoints, CSS sizes | unknown | — |

## 4. Recurring components

- Rounded dark panel with a 1px light border.
- Pill toggle group with a mint-outlined active pill.
- Mint filled button with dark label.
- Donut gauge with a gradient arc and a centred figure.
- Banded swatch list: label left, value right, gradient bands.
- Icon over two-line caption feature tile.

## 5. Essential to its identity

The bento of panels on a near-black gutter; violet-tinted darks; mint used only for action and state; glows rather than shadows; one rounded-square sans; concentric radii.

## 6. Adapt rather than copy for #REP

- **Title Case:** Vietnamese headings do not use it. Keep sentence case and carry the voice through weight and the typeface instead.
- **The "$1.2M ↑ 12%" gauge:** a fake growth metric. The ring is kept only for a real quantity: how many required fields are filled.
- **The swatch panel:** becomes a banded summary of the entered property, keeping the label-left / value-right bands.
- **The case-study framing** (devices, laptop mock-up) is dropped. #REP is the product itself.
- **Brand:** no Puzzle name, logo or copy.

## 7. Accessibility and responsive considerations

- **Muted text:** printed `#616083` on `#0C0E1D` measures 3.2:1, below 4.5:1 for body text. Body-size secondary text needs a lighter tint of the same hue; `#616083` stays for borders and decoration.
- **Action button:** dark text on mint passes easily; the active-pill mint outline needs at least 3:1 against the panel.
- **Phone:** the bento collapses to one column; panel order must follow the task (form, action, result).
- **Glows:** decorative only, never carrying information.

## 8. What Streamlit cannot reproduce, and the closest alternative

| Reference element | In Streamlit |
|---|---|
| Free bento with uneven spans | `st.columns` rows with keyed, styled containers |
| Animated pill-driven content change | `st.tabs` styled as the pill bar; no cross-fade |
| Animated donut fill | Static SVG ring, re-rendered when inputs change |
| Glows behind panels | CSS radial gradients on container backgrounds |
| Hover dropdown navigation | Not needed; three tabs |

## 9. #REP interface plan

- **Navigation:** the pill bar holds "Ước tính giá", "Độ chính xác của mô hình" and "Dữ liệu và giới hạn"; the active pill gets the mint outline.
- **Valuation board:** wide form panel on the left (about 50%); a centre column with the result panel and the completeness ring; a right column with the banded property summary and the uncertainty and source tiles.
- **Result:** the labelled sample figure in a panel, the uncertainty tile reading "Chưa có", and the provenance line.
- **Accuracy view:** one panel with the cross-validation table and bar chart from the real file; one panel stating that no final test evaluation exists.
- **Data view:** fact panels, histogram and limits read from the training split.
- **States:** initial, invalid, model unavailable, sample result and simulated error, from the shared state layer.
