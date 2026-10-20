# #REP UI variants — one per reference design

Five independent Streamlit front ends, one for each reference in `design_references/`.

**design_01 was chosen as the app's design and moved to `app/`** (`app/streamlit_app.py`, `app/styles.css`, with the shared logic copied to `app/core/`). Work on the interface continues there. The other four stay here for reference.

**Status: work in progress.** The session hit its usage limit before verification was finished. What is done and what is left is listed below.

## Variants

| Variant | Reference | Direction | Entry point |
|---|---|---|---|
| design_01 | Puzzle presentation (video) | Night-violet bento, glows instead of shadows, mint only for actions | moved to `app/streamlit_app.py` |
| design_02 | leap hero (screenshot) | Flat charcoal, monospace, corner brackets, square edges, one mint | `ui_variants/design_02/app.py` |
| design_03 | Increase concept (video) | Green-teal material, neon rim, bar-and-square status markers, real input payload as JSON | `ui_variants/design_03/app.py` |
| design_04 | Payal hero (screenshot) | Lit blue gradient, translucent tiles, dimmed decimals, pill controls | `ui_variants/design_04/app.py` |
| design_05 | Finotive page (video) | Centred axis, black floor, violet only for action, spotlight onto the result | `ui_variants/design_05/app.py` |

Each variant's design spec and tokens are in `design_references/design_0X/`.

## Run (PowerShell, from the repository root)

```powershell
design_lab\.venv\Scripts\python.exe -m streamlit run ui_variants\design_02\app.py --server.port 8702
```

Use `design_03` … `design_05` and ports 8703 … 8705 for the others. Streamlit 1.65.0 is in `design_lab\.venv`; with your own environment, `streamlit run ui_variants\design_02\app.py` works too. The chosen design runs with `streamlit run app/streamlit_app.py`.

## How it is built

- **`shared/`** holds the design-neutral logic: schema, copy, validation, `model_interface.py` (the only model seam), session state and widgets. It is copied from `design_lab/lab`, so either folder can be deleted on its own.
- **Each `design_0X/`** holds only `app.py`, `styles.css` and, for 02 and 03, `components.py`. Deleting one variant folder does not affect the others. `design_01/` now holds only its screenshots and a note about the move.
- **No model exists in the repository**, so no variant shows a real prediction. The price is a labelled sample ("Dữ liệu mẫu"): the training-split median, not a prediction. The uncertainty interval always reads "Chưa có". The accuracy figures come from the real cross-validation file.

## Verification so far

| Check | 01 | 02 | 03 | 04 | 05 |
|---|---|---|---|---|---|
| Compiles | ✓ | ✓ | ✓ | ✓ | ✓ |
| Renders at 1440×900 with no exception, console error or overflow; fonts load | ✓ | ✓ | ✓ | ✓ | ✓ |
| Playwright: empty submit blocked (5 errors), typed area 0 rejected, valid submit gives labelled sample | ✓ | ✓ | not run | not run | not run |
| Screenshots saved in `design_0X/screenshots/` | ✓ | ✓ | none | none | none |
| Last round of CSS fixes visually re-checked | ✓ | ✓ | ✓ | ✓ | ✓ |
| Polish pass: full-page desktop and 390 px phone render, no exception, console error or horizontal overflow | ✓ | ✓ | ✓ | ✓ | ✓ |

Saved screenshots:

- **All five:** `polish_sample_desktop_full.png` (1440 px wide, full page) and `polish_sample_phone_390.png` (390 px, full page), taken after the polish pass with a headless-Chrome tool that enlarges the viewport to the page height.
- **01 and 02 only:** `01_initial_1440x900.png` and `03_result_1440x900.png` from the Playwright runs, plus `02_invalid_full.png` for 01. These predate the polish pass. Playwright's full-page capture shows only the viewport, because Streamlit scrolls an inner container.

## Polish pass

Fixes made after review. Each variant keeps its reference's look; nothing about the model, the data or the copy's claims changed.

**All variants** (in `shared/widgets.py`):

- Number fields show − / + only for whole-number counts. Area, frontage and road width are typed, so their steppers are hidden.
- The clear button (×) on fields and dropdowns appears on hover or focus. On touch screens it stays visible.
- On phones the tabs stay on one swipeable row instead of stacking. Streamlit's misplaced scroll arrow is hidden there.
- Range hints such as "Mô hình đã học: 4 – 595 m²" no longer break inside the range.
- Text selection, the caret and scrollbars use each variant's palette.
- The result column follows the form while it scrolls, in 01, 02 and 03. On phones it returns to normal flow.

**Per variant:**

- **design_01:** The completeness ring rendered as nothing, because Streamlit strips inline SVG. It is now a CSS ring. The price unit sits beside the figure.
- **design_02:**
  - One corner-bracket frame around the whole form, with dotted rules between groups, replaces four separate frames.
  - The sample readout's dashed outline sits on the frame itself.
  - The three stat rules line up.
  - The "↗" text character is replaced with a drawn arrow.
- **design_03:**
  - Removed the kicker labels above the headings.
  - Removed the strip of four group cards that repeated the form below it.
  - Each group card's header now shows its real status (complete, missing fields, or fields left «Không rõ»), using the reference's bar-and-square marker.
  - The JSON panel scrolls sideways instead of breaking lines.
- **design_04:**
  - Fixed the selected choice in Pháp lý / Nội thất, whose label was invisible. All choices are now separate round pills, and the selected one is white.
  - Tighter phone header and a lighter sample border.
- **design_05:**
  - The light now fans out from the button and lands as a bright line on the result panel's top edge.
  - Price sits on the left; the uncertainty interval and data source are stacked to its right; the recap runs full width in three columns.
  - The "↗" text character is replaced with a drawn arrow.

## Left to do

1. Run the Playwright sequence on design_03, 04 and 05 and save their screenshots. Clear input focus before using "Điền căn nhà mẫu"; otherwise a focused number field keeps its typed value.
2. Save model-unavailable and simulated-error screenshots for each variant in its `screenshots/` folder, and adapt `design_lab/check_prototypes.py` into a headless check for `ui_variants`. The polish pass rendered several of these states with no errors, but did not save them in the repository.
3. Write the comparison table: faithfulness, hierarchy, readability, suitability, completeness, open issues.
4. Delete the `.playwright-mcp/` folder that Playwright created in the repository root.
