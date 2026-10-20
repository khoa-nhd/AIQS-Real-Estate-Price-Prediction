# design_05 — design specification (Finotive page)

Traceable to: `source.md`, `taste/design_05-finotive.md`, `taste/analysis_steps.md`, `design_tokens.json`.

## 1. What makes it visually distinctive

A centred, near-colourless dark page where one violet pill CTA casts a spotlight onto the product beneath it. Content lives in slightly lifted, violet-glowing cards on a black floor, with long empty gaps between sections. Headings are tight-tracked: one heavy hero, then lighter section headings.

## 2. Core design principles

- **Light falls on the product.**
- **Violet means act.**
- **One centre line.**
- **Black floor, lifted cards.**

## 3. Tokens

| Token | Value | Basis |
|---|---|---|
| Hero ground | `#17161C` | measured |
| Section ground | `#000000` | measured |
| Card / raised card | `#1D1C24` / `#221E2F` | measured |
| Border | `#38373C` | measured |
| Primary text | `#FDFDFF` | measured |
| Secondary text | `~#9E9AA6` | estimated |
| Accent | `#6F47C2` (dark `#5C408D`, light `#815CCE`) | measured |
| Spotlight | `#FEFCFD` | measured |
| Family | tight neo-grotesque | inferred |
| Radius | 6 / 10 / 14 / 16 / pill | estimated |
| Breakpoints, focus, CSS sizes | unknown | — |

## 4. Recurring components

- Violet pill CTA with ↗.
- Outlined pill nav group.
- Dark card with a violet corner glow.
- Pill toggle.
- FAQ accordion row.
- Check-dot list.
- Dashboard frame lit from above.

## 5. Essential to its identity

The centred axis; the black and violet-charcoal grounds; violet only on actions and the selected state; the spotlight-to-product link; lifted glowing cards; tight-tracked headings; FAQ accordions.

## 6. Adapt rather than copy for #REP

- **The spotlight** links the "Ước tính giá" action to the result card below it, keeping the gesture of action lighting up the outcome.
- **Testimonials, review badges and social icons** are invented proof and are dropped; #REP has none.
- **Pricing card and virtual-card renders** are dropped (#REP has no pricing). The check-dot list is reused for the data limits ("Giới hạn cần biết").
- **The FAQ accordion** becomes real questions about the estimate (asking vs transaction price, uncertainty, data coverage), answered only with facts from the repository.
- **The blur word-reveal** is not reproduced. It is motion for persuasion, and Streamlit reruns would replay it on every input.
- **Title Case hero** becomes sentence case in Vietnamese.
- **Brand:** no Finotive name or logo.

## 7. Accessibility and responsive considerations

- **Secondary text:** `~#9E9AA6` on `#000000` is 7.6:1, so it passes.
- **CTA:** white on `#6F47C2` is 6.3:1, so it passes. White on `#815CCE` is 4.8:1, which passes for normal text with little margin.
- **Centred layout:** long centred paragraphs are hard to read, so body text stays left-aligned inside cards with a max width.
- **Phone:** centred headings stay centred; cards become one column.
- **Accordion:** `st.expander` gives keyboard support.

## 8. What Streamlit cannot reproduce, and the closest alternative

| Reference element | In Streamlit |
|---|---|
| Animated spotlight beam | Static CSS radial or linear gradient beam |
| Blur-in word reveal | Omitted |
| FAQ accordion | `st.expander` styled as rounded rows |
| Bento with uneven widths | `st.columns` with weighted widths |

## 9. #REP interface plan

- **Header:** wordmark left, outlined pill nav group centre (as tabs), primary pill right.
- **Hero:** centred tight headline, two-line description and violet pill action, with the spotlight beam falling on the valuation "dashboard" card.
- **Dashboard card:** the form on the left; the result tiles on the right (sample figure, uncertainty, provenance).
- **Accuracy view:** centred heading, a 2+2 card bento holding the cross-validation chart, table, final-evaluation status and metric help.
- **Data view:** centred heading, histogram card, check-dot limits list, and an FAQ accordion about data limits.
