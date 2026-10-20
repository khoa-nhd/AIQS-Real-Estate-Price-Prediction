# design_03 — design specification (Increase concept)

Traceable to: `source.md`, `taste/design_03-increase.md`, `taste/analysis_steps.md`, `design_tokens.json`.

## 1. What makes it visually distinctive

A deep green-teal page wrapped in a neon lime-to-cyan rim, where the product explains itself: real API payloads and UI fragments stand in for illustration. Every section is signposted by the same small eyebrow pill.

## 2. Core design principles

- **Show the machine:** real interface fragments instead of art.
- **Neon on the rim:** saturated colour only at the frame, actions, eyebrow marks and the active tab.
- **One green material:** all darks tinted green-teal.
- **Signposted sections:** an identical eyebrow pill before each headline.

## 3. Tokens

| Token | Value | Basis |
|---|---|---|
| Ground | `#0E2924` | measured |
| Card | `#12473D` | measured |
| Code surface | `#023030` | measured |
| Primary text | `#EEFAFA` | measured |
| Secondary text | `~#9DB8B0` | estimated |
| Secondary button | `#384647` | measured |
| Action gradient | `#4DF4AF` → `#A1FA6A` | measured |
| Rim gradient | `#34F3BD` → `#A5FA69` | measured |
| Family | Exo, plus a monospace for code | inferred |
| Radius | 6 / 8 / 10 / 16 | estimated |
| Breakpoints, CSS sizes, focus | unknown | — |

## 4. Recurring components

- Eyebrow pill (lime bar, teal square, label).
- Gradient primary button and dark secondary button.
- Feature card with an icon tile.
- Icon list row.
- Tab cards with a gradient-filled active one.
- Code response panel.
- Glowing marquee divider.

## 5. Essential to its identity

The green-tinted dark ground; the lime-cyan gradient confined to the rim and actions; eyebrow pills; real product fragments; Exo-like squared letterforms; dark cards with icon tiles.

## 6. Adapt rather than copy for #REP

- **The JSON response panel** becomes a real fragment of #REP: the exact feature payload the model receives (the 12 dataset fields and values). This applies "show the machine" with true content.
- **The transfer card** ("$100.00 · Submitted") becomes the estimate card: the labelled sample figure with its status.
- **Partner logos and the marquee wordmark** are dropped: #REP has no partners to show, and the wordmark would be brand decoration.
- **The six-icon feature strip** becomes the field-group summary (Vị trí, Kích thước, Kết cấu, Thông tin thêm) with a completion state for each, a real quantity.
- **Title Case** is not used in Vietnamese; sentence case.
- **Brand:** no Increase name or logo.

## 7. Accessibility and responsive considerations

- **Secondary text:** `~#9DB8B0` on `#0E2924` is 7.3:1, so it passes.
- **The action gradient** carries a dark label, which passes; white text on the lime end would fail.
- **The rim gradient** is decorative; it must not reduce the content area on a phone, so it thins to a few pixels below 640px.
- **Code text** is set at 14px or more in #REP, not the reference's tiny size.
- **Phone:** the two hero columns stack.

## 8. What Streamlit cannot reproduce, and the closest alternative

| Reference element | In Streamlit |
|---|---|
| Gradient presentation rim | CSS gradient border on the app container |
| Syntax-highlighted JSON panel | `st.html` `<pre>` with spans (no live highlighting library) |
| Tab cards with a sliding highlight | `st.tabs` styled as cards; no animation |
| Starfield and glows | CSS radial gradients (static) |

## 9. #REP interface plan

- **Header:** wordmark, nav tabs, primary action.
- **Hero:** eyebrow "Ước tính giá", headline, lead.
- **Workbench:** form in dark cards on the left (one card per group, with icon tiles); on the right, the estimate card (sample figure plus status) stacked over the payload panel (the real JSON of current inputs).
- **Group strip:** four field groups with a done or missing state.
- **Accuracy section:** eyebrow pill, a cross-validation card grid (real values), and a final-evaluation card reading "Chưa có".
- **Data section:** eyebrow pill, histogram card and limits list rows.
