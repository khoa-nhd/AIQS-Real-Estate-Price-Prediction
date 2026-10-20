"""design_04 — #REP interface after the "Payal" hero (lit blue panel, translucent tiles, dimmed tail, pills).

Run from the repository root:
    streamlit run ui_variants/design_04/app.py

Design source: design_references/design_04/ (design_spec.md, design_tokens.json).
Only theme, layout and markup live here; behaviour comes from ui_variants/shared.
"""
import sys
from pathlib import Path
from string import Template

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import streamlit as st  # noqa: E402

from shared import content, formatting as fmt, schema, state, widgets as ui  # noqa: E402
from shared.evaluation import load_cross_validation  # noqa: E402

TOKENS = dict(PAGE_A="#112258", PAGE_B="#4468A5", PAGE_C="#81B7F3", PANEL_A="#111D55", PANEL_B="#4C79B7",
              TILE_EDGE="#7281A1", CARD="#18171C", FRAME="#0B0D14", TEXT="#FFFFFF", SECONDARY="#C9D6F2",
              CARD_SECONDARY="#A9AEC0", FIELD_BORDER="#7A8095", CTA_A="#3456C8", CTA_B="#4567DA")

THEME = {
    "theme.base": "dark",
    "theme.primaryColor": TOKENS["CTA_B"],
    "theme.backgroundColor": TOKENS["PAGE_A"],
    "theme.secondaryBackgroundColor": "#101015",
    "theme.textColor": TOKENS["TEXT"],
    "theme.borderColor": TOKENS["FIELD_BORDER"],
    "theme.linkColor": "#C9D6F2",
    "theme.font": "'Manrope':https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600&display=swap",
    "theme.baseFontSize": 16,
    "theme.baseRadius": "0.75rem",
}

CSS = Template((HERE / "styles.css").read_text(encoding="utf-8")).substitute(TOKENS)
LAYOUT = {"location": 2, "size": 3, "structure": 3, "extra": [[1, 1], [1], [1]]}


def tile(label: str, value: str, caption: str = "") -> str:
    return (f'<div class="d4-tile"><p class="d4-k">{ui.e(label)}</p><p class="d4-tile-v">{ui.e(value)}</p>'
            + (f'<p class="d4-c">{ui.e(caption)}</p>' if caption else "") + "</div>")


def tiles(view: state.Page, reference) -> str:
    """Four real facts, after the reference's 2×2 metric tiles."""
    cv = load_cross_validation()
    values = view.outcome.snapshot if view.kind in ("sample", "result") else view.values
    unknown = sum(values.get(s.name) is None for s in schema.FIELDS if not s.required)
    items = [
        tile(content.UNCERTAINTY_LABEL, content.UNCERTAINTY_NONE, "Chưa có khoảng ước lượng được hiệu chỉnh"),
        tile("Mục để «Không rõ»", str(unknown), "Trong các mục không bắt buộc"),
    ]
    if cv.status == "available":
        items.append(tile("MAE kiểm định chéo", f'{ui.cv_best(cv)["mae"]} tỷ', "Ứng viên tốt nhất · chưa phải đánh giá cuối"))
    items.append(tile(content.DATA_FACTS["rows"], fmt.count(reference.n_rows)))
    return '<div class="d4-tiles">' + "".join(items) + "</div>"


def summary_panel(view: state.Page, reference) -> None:
    slots = state.result_slots(view, reference)
    kind = slots["kind"]
    with st.container(key=f"panel_{kind}"):
        left, right = st.columns([7, 5], gap="medium")
        notes = "".join(f'<p class="d4-note">{ui.icon("warning")}{ui.e(t)}</p>'
                        for t in [slots["stale"], slots["simulated"], *slots["warnings"]] if t)
        with left:
            if kind in ("sample", "result"):
                whole, _, tail = slots["price"].partition(",")  # dim the decimals: magnitude first
                st.html(
                    f'<p class="d4-tag">{ui.icon(slots["icon"])}{ui.e(slots["tag"])}</p>{notes}'
                    f'<p class="d4-k">{ui.e(slots["heading"])}</p>'
                    f'<p class="d4-figure">{ui.e(whole)}<span class="dim">,{ui.e(tail)}</span><span class="dim unit">{ui.e(slots["unit"])}</span></p>'
                    f'<p class="d4-words">{ui.e(slots["words"])}</p>'
                    f'<p class="d4-words">{ui.e(slots["statement"])}</p>'
                )
            else:
                st.html(f'{notes}<p class="d4-k">{ui.e(content.RESULT_LABEL)}</p>'
                        f'<p class="d4-state-h">{ui.icon(slots["icon"])}{ui.e(slots["heading"])}</p>'
                        f'<p class="d4-words">{ui.e(slots["body"])}</p>')
                if kind == "error":
                    ui.retry_button()
        with right:
            st.html(tiles(view, reference))


def valuation(view: state.Page, reference) -> None:
    head, desc = st.columns([11, 9], gap="large")
    with head:
        st.html(f'<h1 class="d4-h1">{ui.e(content.TITLE)}</h1>')
    with desc:
        st.html(f'<p class="d4-desc">{ui.e(content.LEAD)}</p>')
    st.html('<div style="height:1.4rem"></div>')
    ui.error_summary(view)
    left, right = st.columns(2, gap="small")
    for column, groups in ((left, ("location", "size")), (right, ("structure", "extra"))):
        with column:
            for group in groups:
                with st.container(key=f"card_{group}"):
                    st.html(f'<p class="d4-h2">{ui.e(schema.GROUPS[group])}</p>')
                    ui.fields(group, view, reference, LAYOUT[group], choices="segmented", gap="small")
    st.html(f'<p class="lab-help" style="color:#FFFFFF">{ui.e(content.REQUIRED_LEGEND)}</p>')
    with st.container(key="actions", horizontal=True, vertical_alignment="center"):
        ui.submit_button(view)
        ui.reset_button()
    ui.blocked_note(view)
    st.html('<div style="height:.6rem"></div>')
    summary_panel(view, reference)
    slots = state.result_slots(view, reference)
    if slots["kind"] in ("sample", "result"):
        with st.container(key="card_recap"):
            st.html(f'<p class="d4-k">{ui.e(slots["recap_label"])}</p><div class="d4-recap">{ui.dl(slots["recap"])}</div>'
                    f'<p class="d4-small">{ui.e(slots["unknown"])}</p>'
                    f'<p class="d4-small"><strong>{ui.e(slots["provenance_label"])}:</strong> {ui.e(slots["provenance"])}</p>')


def evaluation() -> None:
    cv = load_cross_validation()
    copy = ui.eval_copy(cv)
    st.html(f'<h1 class="d4-h1" style="margin-top:1.2rem">{ui.e(content.NAV[1])}</h1><p class="d4-desc" style="margin-top:.8rem">'
            f'{ui.e(content.EVAL_INTRO)}</p><div style="height:1rem"></div>')
    chart, side = st.columns([7, 5], gap="small")
    with side:
        tiles_html = tile(content.EVAL_NO_FINAL_LABEL, content.EVAL_NO_FINAL, content.EVAL_NO_FINAL_TEXT)
        if cv.status == "available":
            best = ui.cv_best(cv)
            tiles_html += "".join(tile(content.METRIC_LABELS[k], best[k], content.BEST_CAPTION.format(model=best["model"]))
                                  for k in ("mae", "rmse", "r2"))
        st.html('<div class="d4-card"><div class="d4-tiles">' + tiles_html + "</div></div>")
    if cv.status != "available":
        with chart:
            st.html(f'<div class="d4-card"><p class="d4-p">{ui.e(cv.problem or content.EVAL_MISSING)}</p></div>')
        return
    with chart:
        with st.container(key="card_cv"):
            st.html(f'<p class="d4-h2">{ui.e(content.EVAL_CV_HEADING)}</p><p class="d4-small">{ui.e(content.EVAL_CV_KIND)} {ui.e(copy["folds"])}</p>')
            st.altair_chart(ui.cv_chart(cv, bar=TOKENS["CTA_B"], text=TOKENS["TEXT"], background="transparent"), width="stretch")
    st.html('<div class="d4-card" style="margin-top:12px">' + ui.table(content.EVAL_COLUMNS, ui.cv_rows(cv))
            + "".join(f'<p class="d4-small"><strong>{ui.e(k)}</strong>: {ui.e(v)}</p>' for k, v in content.METRIC_HELP)
            + f'<p class="d4-small">{ui.e(copy["source"])}</p></div>')


def data(reference) -> None:
    st.html(f'<h1 class="d4-h1" style="margin-top:1.2rem">{ui.e(content.NAV[2])}</h1><p class="d4-desc" style="margin-top:.8rem">'
            f'{ui.e(content.DATA_INTRO)}</p><div style="height:1rem"></div>')
    chart, side = st.columns([7, 5], gap="small")
    with chart:
        with st.container(key="card_hist"):
            st.html(f'<p class="d4-h2">{ui.e(content.DATA_HIST_HEADING)}</p>')
            st.altair_chart(ui.price_hist_chart(reference, bar=TOKENS["CTA_B"], background="transparent", height=280), width="stretch")
    with side:
        st.html('<div class="d4-card"><div class="d4-tiles">' + "".join(tile(k, v) for k, v in ui.data_facts(reference)) + "</div></div>")
    st.html('<div class="d4-card" style="margin-top:12px">' + f'<p class="d4-h2">{ui.e(content.DATA_LIMITS_HEADING)}</p>'
            + ui.bullets(content.DATA_LIMITS) + f'<p class="d4-h2" style="margin-top:1rem">{ui.e(content.DATA_MISSING_HEADING)}</p>'
            + ui.table(content.DATA_MISSING_COLUMNS, ui.missing_rows(reference)) + "</div>")


st.set_page_config(page_title=f"design_04 · Blue — {content.TITLE}", layout="wide")
ui.apply_theme(THEME, CSS)
reference = state.bootstrap()
ui.reference_guard(reference)
view = state.page(reference)

st.html(f'<p class="d4-word">{ui.icon("asterisk")}{ui.e(content.TITLE)}</p>')
ui.banner(view)
tab_valuation, tab_evaluation, tab_data = ui.view_tabs()
with tab_valuation:
    valuation(view, reference)
with tab_evaluation:
    evaluation()
with tab_data:
    data(reference)
ui.lab_panel(view)
