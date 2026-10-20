# design_02 — design specification (leap hero)

Traceable to: `source.md`, `taste/design_02-leap.md`, `taste/analysis_steps.md`, `design_tokens.json`. Only the first screen exists as evidence; everything below the fold is unknown and is designed here by extension, not copied.

## 1. What makes it visually distinctive

A trading-terminal hero on flat untinted charcoal. Monospace sets every piece of UI and every number; a wide grotesque sets one big claim. Regions are marked by corner brackets instead of boxes, and one mint green means "go".

## 2. Core design principles

- **Corners, not cards:** bracket marks and hairlines instead of containers.
- **Monospace is the instrument voice.**
- **Green only where you can go.**
- **Square and flat:** no radius, no shadow.

## 3. Tokens

| Token | Value | Basis |
|---|---|---|
| Ground | `#1D1D1D` | measured (75% of area) |
| Primary text | `~#E9F2EE` | estimated |
| Secondary text | `~#8A8A8A` | estimated |
| Rule and bracket | `#3C3C3C` | measured |
| Accent | `#00EB9B` | measured |
| Display / body / mono | wide grotesque / Inter-like / Plex Mono-like | inferred |
| Radius | 0 | observed |
| Shadow | none | observed |
| Sizes | 58 / 42 / 16.5 / 15 / 14 / 9 capture px | estimated |

## 4. Recurring components

- Mono nav item; the active one in mint.
- Mono uppercase link or button with ↗.
- Flat square mint button with a dark mono label.
- Corner-bracket frame with a hairline baseline.
- Stat block: big mono figure, small mono label, right-aligned index (001).
- Dotted vertical grid with diamond markers (chart idiom).

## 5. Essential to its identity

Flat `#1D1D1D` with no surfaces; mono for UI and data; one mint accent; corner brackets; zero radius; one large wide-grotesque headline per screen.

## 6. Adapt rather than copy for #REP

- **Marketing stats** ("$100B+") become real facts from the repository: training rows, the training price range, and the best cross-validated MAE, each labelled with its source.
- **The decorative chart** becomes a real chart in the same idiom: the training-split price distribution drawn as dotted columns with diamond markers.
- **Form fields:** the reference shows none. They are styled in the reference's language: mono labels, square inputs, a hairline underline and bracketed groups.
- **↗ arrows** stay only on the primary action; there are no external links.
- **Brand:** no leap logo or name.

## 7. Accessibility and responsive considerations

- **Secondary text:** `#8A8A8A` on `#1D1D1D` is 4.9:1, which passes for body text with little margin; dimmer grays must not be used for running text.
- **Labels:** the reference's ~9 capture px labels are too small; #REP sets labels at 14px or more.
- **Uppercase Vietnamese in mono** is legible, but only short labels are set this way.
- **Phone:** the two hero columns stack, and the three stat blocks become one column.
- **Focus:** a mint outline on the dark ground.

## 8. What Streamlit cannot reproduce, and the closest alternative

| Reference element | In Streamlit |
|---|---|
| Diamond-marker chart with gradient whiskers | Altair layered chart (rule marks plus diamond point marks) |
| Corner brackets | CSS pseudo-elements on keyed containers |
| Dotted rules | CSS dotted borders |
| Wide grotesque | Mona Sans at an expanded width (Vietnamese-capable stand-in) |
| Mono | IBM Plex Mono (Vietnamese-capable) |

## 9. #REP interface plan

- **Header:** wordmark, mono view switcher (current view in mint), then a dotted rule with brackets.
- **Hero row:** a wide-grotesque headline "Ước tính giá nhà" with a two-tone lead (white statement, gray caveat).
- **Terminal row:** form on the left (mono labels, square inputs, bracketed groups, flat mint "ƯỚC TÍNH GIÁ ↗" button); result readout on the right (big mono figure, label, sample tag, uncertainty, provenance).
- **Facts row:** three bracket-framed stat blocks with indices 001–003, all real.
- **Accuracy view:** mono table and a dotted bar chart of cross-validated MAE.
- **Data view:** the diamond-marker price distribution, plus limits.
