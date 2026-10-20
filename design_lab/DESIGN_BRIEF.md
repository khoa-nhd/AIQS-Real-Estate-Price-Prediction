# Design Brief — Ứng dụng ước tính giá nhà

Status: design brief only. Nothing here is implemented, and no application code exists in the repository yet.

Sources of truth: [`PRODUCT.md`](../PRODUCT.md) for product facts, `data/_v1.csv` for input ranges, `experiments/` and `notebooks/` for model evidence. Where this brief and `PRODUCT.md` disagree, `PRODUCT.md` wins.

Conventions used below:

- `‹…›` marks a value that must come from a real artifact at run time. No number in this brief is a model output.
- **OD-n** marks an open decision the team must make. They are listed in section 8.
- Vietnamese strings are proposed interface copy. English is used for everything else.

---

## 0. What the product is

A Vietnamese Streamlit application where a person enters the details of a house and receives an estimated total price, in tỷ đồng, from the team's trained model.

Facts that constrain the design:

- There is no saved model, no final test evaluation and no calibrated interval today. Every state that depends on them must be designed to be absent.
- The model's 12 inputs are fixed by the dataset (section 4, FR-02). The interface adds none and hides none.
- The cleaned data only contains prices from 1.0 to 11.5 tỷ đồng.
- The team has not verified whether dataset prices are asking prices or transaction prices.

---

## 1. Target-user assumptions

Confirmed in `PRODUCT.md`: the audience is the general public in Vietnam, with no narrower segment chosen. Everything below is an assumption made for design purposes. None has been tested with users.

| # | Assumption | Design consequence |
|---|---|---|
| A1 | The person is checking one specific house: one they want to buy, sell or compare. | One form, one result. No accounts, history or batch upload. |
| A2 | They do not know every detail. House and balcony direction are missing in 70% and 83% of dataset rows. | Unknown is a first-class answer for optional fields, not an error (depends on OD-2). |
| A3 | They think about price in "tỷ" and "triệu", not in decimals of a billion. | Show the figure and also spell it out in tỷ and triệu. |
| A4 | They have no machine learning background. | No jargon on the valuation page. MAE, R² and cross-validation live only on the evaluation page, each with a plain explanation. |
| A5 | They may read a single number as an appraisal. | The estimate is always labelled as an estimate, at body size, next to the number. |
| A6 | Many will use a phone. Unverified. | The page must work as a single column. Nothing may depend on hover. |
| A7 | Ages and eyesight vary widely. | 16px minimum body text, contrast of at least 4.5:1, no meaning carried by colour alone. |
| A8 | Some arrive sceptical of an online price tool. | Show where the number comes from: model version, data version, known limits. Never show a figure the model did not produce. |

---

## 2. Information architecture and user journey

### 2.1 Pages

Three pages, in this order. Navigation labels are sentence case and always visible.

| Page | Nav label | Purpose | Shown when |
|---|---|---|---|
| Valuation | Ước tính giá | Enter details, get an estimate. Default page. | Always |
| Model evaluation | Độ chính xác của mô hình | Show real evaluation results and explain them. | Always in the menu. Content depends on which artifacts exist (section 5.2). |
| Data and limits | Dữ liệu và giới hạn | Where the data comes from, what it covers, what the estimate is not. | Always |

A navigation item is never hidden because its content is unavailable. The page explains what is missing instead.

### 2.2 Journey

| Step | What the person does | What the interface does |
|---|---|---|
| Arrive | Opens the app. | States in one sentence what the tool does and that the result is an estimate. Shows the empty result panel so the outcome is visible before any input. |
| Enter | Chooses location, then fills size, structure and optional details. | Labels carry units. Helper text gives the range the model has seen. Optional fields offer "Không rõ". |
| Validate | Presses "Ước tính giá". | Checks required fields and value rules. Blocks only on real errors, and warns without blocking on values outside the training range. |
| Predict | Waits. | Shows a progress indicator on the action. Calls the real model, or shows the model-unavailable state. |
| Understand | Reads the result. | Shows the price, its unit, the estimate label, the uncertainty section (real interval or an explicit "not available"), and provenance. |
| Explore | Optionally opens the evaluation or data page. | Shows only results that exist as files, each labelled with what kind of evaluation it is. |
| Adjust | Changes a field and runs again. | Keeps all previous input. Marks the old result as out of date until the new one arrives. |

### 2.3 Field grouping

Groups are named by content, not numbered.

| Group | Fields (dataset name → label) |
|---|---|
| Vị trí | `City` → Tỉnh / Thành phố · `District` → Quận / Huyện |
| Kích thước | `Area` → Diện tích · `Frontage` → Mặt tiền · `Access Road` → Đường vào |
| Kết cấu | `Floors` → Số tầng · `Bedrooms` → Số phòng ngủ · `Bathrooms` → Số phòng tắm |
| Thông tin thêm | `House direction` → Hướng nhà · `Balcony direction` → Hướng ban công · `Legal status` → Pháp lý · `Furniture state` → Nội thất |

"Thông tin thêm" stays expanded by default. Collapsing it would hide four model inputs.

---

## 3. Wireframe — valuation page

### 3.1 Desktop (wide viewport)

Two columns in roughly a 7 : 5 ratio. The form is on the left and the result panel on the right, so the result sits beside the form instead of below it.

```
┌──────────────────────────────────────────────────────────────────────────┐
│ ‹Tên sản phẩm›      Ước tính giá · Độ chính xác của mô hình · Dữ liệu…   │
├──────────────────────────────────────────────────────────────────────────┤
│ [ System banner — only when the model is unavailable or in preview ]     │
│                                                                          │
│ Ước tính giá nhà                                              (h1)       │
│ Nhập thông tin căn nhà để nhận mức giá ước tính từ mô hình.              │
│ Đây là con số tham khảo, không phải kết quả thẩm định.                   │
│                                                                          │
│ ┌─ FORM ───────────────────────────────┐  ┌─ RESULT PANEL ─────────────┐ │
│ │ [ Error summary — only after a      ]│  │ Giá ước tính               │ │
│ │ [ failed submit                     ]│  │                            │ │
│ │                                      │  │ ‹X,X› tỷ đồng   (largest)  │ │
│ │ Vị trí                               │  │ khoảng ‹X› tỷ ‹YYY› triệu  │ │
│ │ Tỉnh / Thành phố *   Quận / Huyện *  │  │                            │ │
│ │ [ select        ▾ ]  [ select    ▾ ] │  │ Estimate statement (body)  │ │
│ │                                      │  │                            │ │
│ │ Kích thước                           │  │ Khoảng dao động            │ │
│ │ Diện tích (m²) *  Mặt tiền (m)  Đường│  │ ‹interval› or "chưa có"    │ │
│ │ [      ]          [      ]      [   ]│  │                            │ │
│ │ helper text under each field         │  │ Dựa trên thông tin bạn nhập│ │
│ │                                      │  │ ‹recap of inputs›          │ │
│ │ Kết cấu                              │  │                            │ │
│ │ Số tầng   Số phòng ngủ  Số phòng tắm │  │ Nguồn kết quả              │ │
│ │ [    ]    [    ]        [    ]       │  │ ‹model · data · date›      │ │
│ │                                      │  │                            │ │
│ │ Thông tin thêm (không bắt buộc)      │  │ Link → Độ chính xác của    │ │
│ │ Hướng nhà        Hướng ban công      │  │ mô hình                    │ │
│ │ [ select    ▾ ]  [ select    ▾ ]     │  └────────────────────────────┘ │
│ │ Pháp lý          Nội thất            │                                 │
│ │ ( ) ( ) ( )      ( ) ( ) ( )         │                                 │
│ │                                      │                                 │
│ │ [ Ước tính giá ]   Nhập lại          │                                 │
│ └──────────────────────────────────────┘                                 │
│                                                                          │
│ Footer: data source line · link to Dữ liệu và giới hạn                   │
└──────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Phone (narrow viewport)

One column in this order: banner, title and lead, form (all groups, each field full width), action, result panel, footer. The result panel lands directly under the action button, so pressing the button and seeing the result need no navigation.

### 3.3 Element notes

| Element | Content and behaviour |
|---|---|
| Lead sentence | States what the tool does and that the result is an estimate, before any input. |
| Location group | District options depend on the chosen city. See the Streamlit constraint in section 6.6. |
| Numeric fields | Label with unit, helper text with the range seen in training data, error text directly under the field. |
| Optional selects | First option is "Không rõ". It is a real choice, not a placeholder. |
| Two-value fields | Pháp lý and Nội thất show both values plus "Không rõ" as visible choices, not a dropdown. |
| Primary action | "Ước tính giá". The only filled button on the page. |
| Secondary action | "Nhập lại" as a text-weight button, visually subordinate. |
| Result panel | Always present. Its content is one of the states in section 5.1. |
| Estimate statement | Body size, same panel as the number, never collapsed or placed in a tooltip. |
| Provenance | Model name and version, training data version, date. Read from model metadata, never typed into the interface. |

### 3.4 Proposed display labels for dataset values

The value sent to the model stays exactly as it appears in the training data. Only the label shown is translated. These translations need team confirmation (OD-8).

| Field | Dataset value | Proposed label |
|---|---|---|
| Pháp lý | `Have certificate` | Đã có sổ (giấy chứng nhận) |
| Pháp lý | `Sale contract` | Hợp đồng mua bán |
| Nội thất | `Full` | Đầy đủ |
| Nội thất | `Basic` | Cơ bản |
| Hướng nhà, Hướng ban công | 8 values, already Vietnamese | Shown as stored, for example "Đông - Nam" |

---

## 4. Shared functional requirements

Every prototype built in `design_lab/` must satisfy the same list, so prototypes differ in design and not in behaviour.

**Input**

- **FR-01** The interface is in Vietnamese: labels, helper text, messages, navigation and results.
- **FR-02** The form collects exactly the 12 model features: Area, Frontage, Access Road, Floors, Bedrooms, Bathrooms, House direction, Balcony direction, Legal status, Furniture state, City, District. No field is added or removed.
- **FR-03** Every field has a visible label. Fields measured in a unit show that unit in the label (units pending OD-1).
- **FR-04** Required fields are marked. Which fields are required follows the model's input contract (OD-2), not a design preference.
- **FR-05** City and District options come from the categories the model was trained on, after the pipeline's own normalisation. The raw CSV contains dirty variants such as `Hà Nội.` and must not be the source.
- **FR-06** District options are limited to districts that occur with the chosen city in the training data.
- **FR-07** Optional categorical fields offer "Không rõ", sent to the model as a missing value, only if the final pipeline accepts missing values (OD-2).
- **FR-08** Input is kept after every outcome: failed validation, model unavailable, inference error and success.

**Validation**

- **FR-09** Blocking errors: a required field is empty, a number is not positive, a count is not a whole number.
- **FR-10** Non-blocking warnings: a value lies outside the range seen in training data. The estimate still runs and the warning is repeated in the result.
- **FR-11** Training ranges and category lists are read from an artifact shipped with the model, not hard-coded in the interface.
- **FR-12** After a failed submit, an error summary appears above the form and each invalid field shows its own message directly below it. Messages state the cause and the fix.

**Prediction**

- **FR-13** A price is shown only when the loaded model returned it for the current input.
- **FR-14** If the model cannot be loaded, the interface says so and shows no price.
- **FR-15** While the model is running, the action shows progress and cannot be triggered a second time.
- **FR-16** If inference fails, the interface says so in plain language, keeps the input and offers a retry. No stack trace is shown to the public.
- **FR-17** When an input changes after a result is shown, the old result is marked as out of date or removed.

**Result**

- **FR-18** The price is shown in tỷ đồng using Vietnamese number formatting (decimal comma), and spelled out in tỷ and triệu.
- **FR-19** Precision does not exceed what the model supports. Proposed: one decimal place of a tỷ, subject to OD-5.
- **FR-20** The statement that the figure is a model estimate, not an appraisal or a transaction price, sits next to the figure at body size.
- **FR-21** An uncertainty interval is shown only when a calibrated interval artifact exists. Otherwise the uncertainty section says it is not available. No interval is derived from MAE or any other summary metric.
- **FR-22** The result shows which inputs it was based on and how many were left as "Không rõ".
- **FR-23** The result shows provenance from model metadata. If metadata is missing, the interface says the version is unknown.

**Evaluation and data pages**

- **FR-24** Metrics are read from files in the repository at run time. Nothing is typed into the page.
- **FR-25** Each result is labelled with its kind: cross-validation on training data, validation, or final test. Cross-validation results are labelled as used for model selection and not as final accuracy.
- **FR-26** If no final test evaluation exists, the page says so. This is the situation today.
- **FR-27** The data page states the dataset, its size, the price range covered, and that prices have not been verified as asking or transaction prices.

**Demo and preview**

- **FR-28** A preview mode exists only for design review. It is off by default, is enabled only by an explicit developer setting and must not be enabled in a public deployment.
- **FR-29** In preview mode a persistent banner states that the figures are samples. The result panel carries a visible "Dữ liệu mẫu" label and a distinct treatment that does not rely on colour alone.
- **FR-30** Sample figures in preview mode do not change with the input, so they cannot be read as predictions.

**Quality**

- **FR-31** Text contrast is at least 4.5:1, and control boundaries and focus indicators at least 3:1.
- **FR-32** Every action is reachable by keyboard with a visible focus indicator.
- **FR-33** The layout works from 375px wide without horizontal scrolling.
- **FR-34** The stack stays Python and Streamlit. Styling uses Streamlit's theme configuration first. Custom CSS is a last resort and must not replace native widgets.

---

## 5. UI states

### 5.1 Valuation page

| State | Trigger | Result panel shows | Must not show |
|---|---|---|---|
| **Initial** | First load, model loaded, nothing submitted. | Heading "Chưa có kết quả". Text: "Điền thông tin căn nhà rồi chọn «Ước tính giá»." | Any number, sample figure or placeholder digits. |
| **Invalid input** | Submit with blocking errors. | Unchanged from before the submit. If an earlier result exists, it is marked out of date. | A new price. |
| **Model unavailable** | Model file missing or failed to load. | Heading "Mô hình chưa sẵn sàng". Text: "Hiện chưa thể ước tính giá vì mô hình chưa được tải lên hệ thống. Thông tin bạn nhập vẫn được giữ nguyên." | Any price, sample or fallback estimate. |
| **Running** | Valid submit, model working. | Progress indicator with "Đang ước tính…". | The previous price presented as current. |
| **Successful prediction** | Model returned a value. | Price, spelled-out amount, estimate statement, uncertainty section, input recap, provenance. | Accuracy claims not backed by a file. |
| **Inference error** | Model raised an error or timed out. | Heading "Không ước tính được". Text: "Đã xảy ra lỗi khi mô hình xử lý thông tin. Thông tin bạn nhập vẫn được giữ nguyên. Hãy thử lại." Action "Thử lại". | A stack trace, or a stale price presented as current. |
| **Uncertainty unavailable** | Success, but no calibrated interval artifact. | Inside the result: "Khoảng dao động: chưa có." Text: "Mô hình chưa có khoảng ước lượng được hiệu chỉnh nên ứng dụng không hiển thị khoảng giá." | A ± figure, a range, or a bar implying a range. |
| **Uncertainty available** | Success with a calibrated interval artifact. | "Khoảng ước lượng ‹mức phủ›%: ‹thấp› – ‹cao› tỷ đồng", with one sentence on what the coverage means. | A coverage level not taken from the calibration artifact. |
| **Out-of-range warning** | Success with one or more inputs outside the training range. | The normal result plus a warning naming each field: "‹Tên mục› nằm ngoài khoảng dữ liệu mô hình đã học (‹min›–‹max›). Kết quả có thể kém tin cậy." | — |
| **Preview** | Developer preview setting on. | Sample layout with the "Dữ liệu mẫu" label and dashed boundary. | Anything that could pass as a real result. |

Supporting details:

- **Model unavailable** also shows a system banner above the title. The primary action is disabled and the reason is written beside it, so the button is never silently inert.
- **Invalid input** shows the summary "Chưa thể ước tính. Vui lòng kiểm tra ‹n› mục sau:" followed by one line per field. Field messages are specific, for example "Nhập diện tích lớn hơn 0." and "Chọn tỉnh / thành phố."
- **Preview** banner text: "Chế độ xem trước giao diện — các con số là dữ liệu mẫu, không phải kết quả dự đoán."
- Every state pairs its colour with an icon and a text heading.

### 5.2 Evaluation page

| State | Trigger | Shows |
|---|---|---|
| No artifacts | No evaluation files found. | "Chưa có kết quả đánh giá." and what will appear here later. |
| Selection results only | Cross-validation files exist, no final test file. Today's situation. | The cross-validation table, labelled "Kết quả kiểm định chéo trên tập huấn luyện, dùng để chọn mô hình — chưa phải đánh giá cuối cùng." Plus a notice that final test results do not exist yet. |
| Final evaluation available | A final test evaluation file exists. | Final test metrics first, with plain explanations. Selection results below as supporting detail. |
| Artifact unreadable | A file exists but cannot be parsed. | An error naming the file, and no partial numbers. |

---

## 6. Design system recommendation

### 6.1 Direction

Calm, plain and exact: a public utility, not a property showroom. The page should look like something a person can check, with the price as the one loud element and everything that qualifies it readable beside it.

Style basis: **Minimalism & Swiss Style** from the UI UX Pro Max style data (clean, functional, high contrast, grid-based, single accent, no shadows or gradients). Section 7 explains why its companion recommendation, Glassmorphism, is rejected.

Rules that follow:

- No gradients, no blur or glass, no shadows on elements at rest.
- No emoji as icons. One icon family only.
- No decorative imagery and no stock property photos. The interface has none of its own to show.
- No small uppercase letter-spaced labels. Labels are sentence case at a readable size.
- No more than two typefaces.

### 6.2 Typography

| Role | Family | Why |
|---|---|---|
| Headings and the price figure | Lexend | Designed for readability; covers the Vietnamese subset. |
| Body, labels, helper text | Source Sans 3 | Covers the Vietnamese subset; Source Sans is Streamlit's default family, so body text needs no extra font. |

This is the "Corporate Trust" pairing from the UI UX Pro Max typography data. Vietnamese subset support for both families was checked in the skill's Google Fonts data. Fallback if a custom heading font cannot be loaded: Source Sans 3 for everything, with weight carrying the hierarchy (OD-6).

| Token | Size | Weight | Line height | Use |
|---|---|---|---|---|
| `price` | 44px desktop, 36px phone | 600 | 1.2 | The estimated price only |
| `h1` | 28px | 600 | 1.3 | Page title |
| `h2` | 20px | 600 | 1.35 | Group and panel headings |
| `lead` | 18px | 400 | 1.55 | Lead sentence, spelled-out price |
| `body` | 16px | 400 | 1.55 | Text, statements, messages |
| `label` | 16px | 500 | 1.4 | Field labels |
| `helper` | 14px | 400 | 1.5 | Helper and provenance text; never below 14px |

Rules:

- Vietnamese stacks diacritics above capitals (Ễ, Ộ). Heading line height stays at 1.3 or more, and headings are not set in all capitals.
- Prices and table figures use tabular figures so digits align.
- Line length stays between 60 and 75 characters on desktop.
- Emphasis comes from weight and size, not from colour.

### 6.3 Colour

Base palette: the Real Estate/Property entry in the UI UX Pro Max colour data ("Trust teal + professional blue"), with one token replaced and state colours added. Contrast ratios were calculated for this brief.

| Token | Hex | Use | Contrast |
|---|---|---|---|
| `background` | `#F0FDFA` | Page | — |
| `surface` | `#FFFFFF` | Panels, input fills | — |
| `text` | `#134E4A` | Headings and body | 9.09 on background, 9.48 on surface |
| `text-muted` | `#475569` | Helper and provenance text | 7.27 on background, 7.58 on surface |
| `primary` | `#0F766E` | Primary button, focus ring, links | 5.25 on background, 5.47 on surface |
| `on-primary` | `#FFFFFF` | Text on the primary button | 5.47 |
| `border` | `#5F8A84` | Input and panel boundaries | 3.69 on background, 3.85 on surface |
| `accent` | `#0369A1` | Informational notices, second chart series | 5.93 on surface |

State colours, each always paired with an icon and a text heading:

| State | Text | Background | Contrast |
|---|---|---|---|
| Error | `#B91C1C` | `#FEF2F2` | 5.91 |
| Warning, out of date, preview | `#92400E` | `#FEF3C7` | 6.37 |
| Information, not available | `#075985` | `#E0F2FE` | 6.59 |
| Confirmed real result | `#166534` | `#DCFCE7` | 6.49 |

Rules:

- The skill's border colour `#99F6E4` is replaced because it measures 1.26:1 on white. Input boundaries need 3:1.
- Teal is the only brand colour. Blue appears only in informational notices and charts.
- The result panel uses no success-green fill. A price is not good news or bad news. Green is reserved for the small "real model result" provenance mark.
- Light theme only for the first version. A dark theme is a separate design task and must be contrast-checked on its own.

### 6.4 Spacing and layout

- Spacing scale on a 4px base: 4, 8, 12, 16, 24, 32, 48.
- Label to field: 4. Field to helper or error text: 4. Between fields: 16. Between groups: 32. Between page sections: 48.
- Corner radius: 6px on inputs and buttons, 8px on panels. No pill shapes.
- Desktop: two columns, about 7 : 5, with a 32 gap. Phone: one column with 16 side padding.
- Inputs and buttons are at least 44px tall.
- Surfaces are separated by the step from `background` to `surface` plus the `border` line. No shadows.

### 6.5 Hierarchy

1. The price is the single largest element on the page. Nothing else uses the `price` size.
2. The estimate statement and the uncertainty section sit at body size in the same panel. Qualifications are never fine print.
3. One primary action per page. Everything else is a secondary or text-weight control.
4. System banners sit above the title because they change what the whole page means.
5. Provenance is the quietest text in the panel, but is always present.

### 6.6 Components, mapped to Streamlit

| Component | Streamlit basis | Notes |
|---|---|---|
| Navigation | Multipage navigation | Three items, current page marked. |
| System banner | Warning or info alert | Model unavailable and preview only. |
| Field group | Sub-heading plus columns | Columns collapse to one on narrow screens. |
| Numeric field | `number_input` with help text | Empty by default, not pre-filled with a typical value. |
| Select field | `selectbox` | City and District; searchable. |
| Choice field | Radio or segmented control | Two values plus "Không rõ". |
| Field error | Text directly below the widget | Specific message with an icon. |
| Error summary | Error alert at the top of the form | One line per invalid field. |
| Primary action | Primary button | "Ước tính giá". |
| Result panel | Bordered container | Holds every state from section 5.1. |
| Price figure | Custom text at `price` size | Not `st.metric`: no delta arrow, since there is nothing to compare against. |
| Uncertainty block | Text block in the result panel | Interval or the "chưa có" statement. |
| Provenance line | Caption text | From model metadata. |
| Metrics table | `dataframe` or table | Each column explained in plain Vietnamese. |
| Model comparison chart | Horizontal bar chart with direct value labels | Always paired with the table. |
| Icons | Streamlit's Material Symbols | One family, same weight throughout. |

Streamlit constraints the prototypes must respect. Streamlit is not installed on this machine, so its version is unknown (OD-7) and each point needs checking at implementation:

- **Dependent selects.** Widgets inside `st.form` do not rerun the script until submit, so District cannot react to City inside a form. The location selects sit outside the batched form, or the page uses a plain button instead of a form.
- **Focus.** Streamlit does not let the app move keyboard focus to the error summary. The summary's position above the form does that job instead.
- **Field-level semantics.** Error text cannot be programmatically attached to its input. It must sit immediately below the field and name the field.
- **Number format.** Numeric inputs may display a decimal point rather than the Vietnamese decimal comma. Helper text should show an example in the format the input accepts.
- **Theme options.** Border colour, corner radius, custom fonts and top navigation depend on the Streamlit version. The fallback is the default theme with only primary, background and text colours set.
- **Scrolling.** The app cannot scroll to the result after submit. The two-column desktop layout and the stacked phone order are chosen so the result is adjacent to the action in both.

### 6.7 Motion

- Progress on the primary action while the model runs.
- No entrance animations, no count-up on the price, no decorative motion.
- Anything that moves respects the reduced-motion setting.

### 6.8 Charts on the evaluation page

- Model comparison: horizontal bars sorted by value, one metric per chart, values labelled directly.
- The metric's unit is in the axis title, for example "MAE (tỷ đồng)".
- Every chart has the same data as a table next to it.
- No radar charts, pie charts or dual axes.

---

## 7. How the installed skills were used

**UI UX Pro Max.** Followed its workflow: a `--design-system` query, then focused domain searches for colour, typography, Google Fonts, style, form validation and charts. Its contract says to verify each result against the product and platform before using it.

| Result | Decision | Reason |
|---|---|---|
| Colour palette for Real Estate/Property | Adopted, one token replaced | Verified category match. Border colour failed the 3:1 boundary check. |
| "Corporate Trust" pairing, Lexend + Source Sans 3 | Adopted | Both cover Vietnamese; Source Sans is Streamlit's default family. |
| Minimalism & Swiss Style | Adopted as the style basis | Fits a form-and-result tool; low accessibility risk in the skill's data. |
| Error summary, inline error and form label guidance | Adopted in FR-12 and section 5 | Applied within Streamlit's limits, noted in section 6.6. |
| Glassmorphism | Rejected | Conditional accessibility risk, and blur panels are not a Streamlit capability. |
| Hero-Centric landing pattern | Rejected | A marketing page pattern; this is a task page. |
| Cinzel + Josefin Sans | Rejected | Cinzel has no Vietnamese subset in the skill's own font data. |
| Anti-patterns "poor photos, no virtual tours" | Not applicable | They describe a listings site. |
| Radar chart for model comparison | Rejected | The same result advises bars when values need precise comparison. |
| Stack guidance | None available | The skill has no Streamlit stack. |

The design system was not persisted with `--persist`. This brief is the only file written.

**Taste (`design-taste-frontend`).** Its own description excludes this work: "Not for dashboards or app screens". Its procedure deals art directions, hero compositions and imagery for landing pages, so that procedure was not run. Its house-style rules that carry over to a tool screen are applied in section 6.1: no gradients, no glass, no shadows at rest, no emoji, no tiny uppercase labels, at most two typefaces. The skill itself exempts real form fields and tables from its "no thin rules" rule. If a public landing page is ever built for this product, that is the place to run the skill in full.

**Impeccable.** Not invoked for this brief. Its `PRODUCT.md` is the source of product facts here.

---

## 8. Open decisions

| ID | Decision | Owner | Blocks |
|---|---|---|---|
| OD-1 | Units for Area, Frontage and Access Road. Not documented in the repository; m² and m are assumed in the wireframe labels. | Data | FR-03, all field labels |
| OD-2 | The model's input contract: which fields are required, and whether missing values are accepted. Includes what happens when Frontage or Access Road is blank. | Model | FR-04, FR-07, "Không rõ" |
| OD-3 | Which model ships, and the metadata saved with it (name, version, data version, date, training ranges, category lists). | Model | FR-05, FR-11, FR-23 |
| OD-4 | Whether a calibrated interval will be produced from the calibration split. | Model | FR-21, uncertainty states |
| OD-5 | Display precision for the price. | Model and design | FR-19 |
| OD-6 | Whether a custom heading font is loaded, and whether it is self-hosted. | App | Section 6.2 |
| OD-7 | The Streamlit version the app targets. | App | Section 6.6 |
| OD-8 | Vietnamese labels for Legal status and Furniture state values. | Team | Section 3.4 |
| OD-9 | Product name shown in the navigation. | Team | Wireframe header |
