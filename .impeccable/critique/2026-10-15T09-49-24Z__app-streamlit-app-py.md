---
target: app (whole Streamlit app)
total_score: 24
max_score: 40
na_heuristics: 
p0_count: 0
p1_count: 4
target_identity: "file:D:\\DangKhoa\\Aiqs\\AIQS-Real-Estate-Price-Prediction\\app\\streamlit_app.py"
target_fingerprint: "sha256:bca22fbf0a34b0483b0639c3f4051e26caf99b44ca46eacd10e94b56e8689077"
target_path: "D:\\DangKhoa\\Aiqs\\AIQS-Real-Estate-Price-Prediction\\app\\streamlit_app.py"
timestamp: 2026-10-15T09-49-24Z
slug: app-streamlit-app-py
closed: true
---
Method: dual-agent (A: design review · B: detector + browser)

## Design Health Score
| # | Heuristic | Score | Key Issue |
|---|---|---|---|
| 1 | Visibility of System Status | 3 | Preview banner, sample tag, stale note, blocked-button reason; a new estimate is not announced to screen readers |
| 2 | Match System / Real World | 3 | Estimate tab speaks listing language; accuracy tab is ML jargon (model ids, RMSE, R², CSV path) |
| 3 | User Control and Freedom | 2 | "Xoá thông tin đã nhập" sits next to the primary button, clears 12 fields, no undo |
| 4 | Consistency and Standards | 2 | Comma decimals in results vs dot decimals in inputs ("54.0"); y-axis "1,800" vs "18.136" elsewhere |
| 5 | Error Prevention | 2 | Comma-decimal entry may be dropped; no min/max on numbers; out-of-range flagged only after submit |
| 6 | Recognition Rather Than Recall | 3 | Recap, units, range hints; judging trust needs three tabs |
| 7 | Flexibility and Efficiency | 2 | Deep links and type-ahead only; no width x length entry, no compare |
| 8 | Aesthetic and Minimalist Design | 2 | Gauge and recap repeat the form; chart and table repeat 8 rows; ambient glows compete with meaning colours |
| 9 | Error Recovery | 3 | Summary with count, per-field errors, coral edge, inputs kept, retry; summary items not linked to fields |
| 10 | Help and Documentation | 2 | Limits only on the Data tab; no help at Mặt tiền / Đường vào or on the 28-province coverage |
| **Total** | | **24/40** | **Acceptable** |

## Design Specificity Verdict
Content and interaction are product-specific (listing vocabulary, price in words, honest "Chưa có", real-data market strip). The visual layer (night-violet bento, mint neon, pink back-light, Exo 2) is category-interchangeable, and ambient pink dilutes pink's "sample" meaning. Detector (rendered-page URL scan, 1-8 warnings per page): dark-glow on selected tab and primary button (styles.css:74, 80-83); ai-color-palette on ring and bands (styles.css:119-130); radial-spotlight-glow on bands; nested-cards on .lab-summary and phone tabs; first-viewport-column-overflow in invalid state. Static scan of app/: 0 (runtime-generated UI). False positives: nested-cards on phone tabs; ring is a data gauge. Overlay injected in a headless tab only; no user-visible overlay.

## Priority Issues
1. [P1] The dataset middle-half range (4,2 – 7,5 tỷ, bold, directly under the price) reads as the estimate's range; "khoảng" used in three senses. Fix: range + source facts directly under the price, strip after; muted note phrased as a comparison without two numbers. Commands: clarify + layout. (Introduced by the overdrive and clarify passes.)
2. [P1] No plain answer to "how far can I trust this?" at the price; recorded CV MAE ~0,986 tỷ sits on a tab written for the team (ids, RMSE/R², CSV path, MAE without unit); preview banner says "số mẫu" on the accuracy tab where numbers are real. Fix: one labelled evidence line in the result facts; accuracy tab leads with it, candidate chart/table in an expander; banner scoped. Commands: clarify + distill.
3. [P1] Screen reader / language: lang="en"; literal "\*" in accessible names of five required fields (core/schema.py:86); no aria-required/invalid/describedby; result has no heading and no live region; English Streamlit control names. Fix: clean labels, h2 + aria-live for the result, summary links to fields, lang="vi". Command: harden.
4. [P1] Decimal comma: inputs show and expect dots ("54.0"); scripted "54,5" was cleared (confirm on a real Vietnamese keyboard); histogram y-axis "1,800". Fix: accept "," and ".", examples "54" / "4,1", thousands-dot labels on every axis. Commands: harden + clarify.
5. [P2] Ambient pink glow behind result text: worst pixel 4,36:1 at 390 px (below AA); real-result panel shares the sample's pink; panels overflow:hidden with ::before at bottom:-45% become programmatically scrollable (~770 px empty glow after scrollIntoView on phone). Fix: neutral violet ambient, teal for real results, less glow under text, overflow:clip. Commands: colorize + harden.

## Persona Red Flags
- Jordan: reads bold 4,2–7,5 as the price range; "Đường vào" width or distance; Mặt tiền = 0 unexplained; "Trong dữ liệu" which data; "Chưa có" without takeaway; accuracy jargon.
- Sam: lang="en"; "\*" read aloud; required state visual only; errors/helpers not associated; result not headed or announced; strip tooltips mouse-only.
- Casey: form ~395-2066 px before the result; reset a thumb away from submit with no undo; comma decimals; panel scroll shift when keyboard opens; gauge + recap add scroll.
- Chị Lan (homeowner checking before a broker): Bình Dương vs Hồ Chí Minh and post-2025 districts; thinks in ngang x dài; hẻm as Đường vào; takes 4,2–7,5 to the broker; "not a transaction price" is muted small text; no next step.

## Minor Observations
- 28 provinces only, reason only on the Data tab; "Quận / Huyện" level abolished 7/2025, no note.
- Rolling counter shows "5,1" mid-roll while words already say 5 tỷ 900 triệu.
- Ring at 0/5 nearly invisible (1,19:1); initial state already reports "7 mục để «Không rõ»".
- Mixed tone-mark styles ("Xoá" vs "Hòa"); «» quotes.
- Histogram x-axis runs to 12,0 though max is 11,5; MAE/RMSE without unit in the best-candidate panel.
- Number inputs have no min/max.
- Masthead + lead take ~40% of the first desktop screen on all tabs.
- Two differently coloured warning triangles stacked in the error state.

## Questions to Consider
- With a typical miss of ~1 tỷ on ~6 tỷ, should the hero be "5,9" at display size, or a coarser "gần 6 tỷ" until a calibrated band exists?
- Should delight on a number taken to a broker be a rolling counter and light swell, or the plainness of a valuation slip?
- Who is the accuracy tab for: the public (one sentence) or course reviewers (move out of main nav)?
- After the 2025 province merger, ask for "địa chỉ theo tin rao (địa giới cũ)" explicitly, or map new wards to old districts first?
