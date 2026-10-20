"""design_02 — #REP interface after the "leap" hero (flat charcoal, monospace, corner brackets, one green).

Run from the repository root:
    streamlit run ui_variants/design_02/app.py

Design source: design_references/design_02/ (design_spec.md, design_tokens.json).
Only theme, layout and markup live here; behaviour comes from ui_variants/shared.
"""
import sys
from pathlib import Path
from string import Template

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import streamlit as st  # noqa: E402

from components import diamond_distribution  # noqa: E402
from shared import content, formatting as fmt, schema, state, widgets as ui  # noqa: E402
from shared.evaluation import load_cross_validation  # noqa: E402

TOKENS = dict(GROUND="#1D1D1D", TEXT="#E9F2EE", SECONDARY="#9A9A9A", RULE="#3C3C3C", BRACKET="#5A5A5A",
              FIELD_BORDER="#6B6B6B", MINT="#00EB9B")

THEME = {
    "theme.base": "dark",
    "theme.primaryColor": TOKENS["MINT"],
    "theme.backgroundColor": TOKENS["GROUND"],
    "theme.secondaryBackgroundColor": TOKENS["GROUND"],
    "theme.textColor": TOKENS["TEXT"],
    "theme.borderColor": TOKENS["FIELD_BORDER"],
    "theme.linkColor": TOKENS["MINT"],
    "theme.font": "'IBM Plex Mono':https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500&display=swap",
    "theme.headingFont": "'Mona Sans':https://fonts.googleapis.com/css2?family=Mona+Sans:wdth,wght@75..125,400..700&display=swap",
    "theme.baseFontSize": 16,
    "theme.baseRadius": "0rem",
    "theme.buttonRadius": "0rem",
}
EXTRA_FONTS = ("https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap",)

CSS = Template((HERE / "styles.css").read_text(encoding="utf-8")).substitute(TOKENS)
LAYOUT = {"location": 2, "size": 3, "structure": 3, "extra": [[1, 1], [1], [1]]}


def row(label: str, value: str) -> str:
    return f'<div class="d2-row"><span>{ui.e(label)}</span><span>{ui.e(value)}</span></div>'


def readout(view: state.Page, reference) -> None:
    slots = state.result_slots(view, reference)
    kind = slots["kind"]
    with st.container(key=f"frame_result_{kind}"):
        notes = "".join(f'<p class="d2-note">{ui.icon("warning")}{ui.e(t)}</p>'
                        for t in [slots["stale"], slots["simulated"], *slots["warnings"]] if t)
        if kind not in ("sample", "result"):
            st.html(f'<p class="d2-label">{ui.e(content.RESULT_LABEL)}</p>{notes}'
                    f'<p class="d2-state-h">{ui.icon(slots["icon"])}{ui.e(slots["heading"])}</p>'
                    f'<p class="d2-p">{ui.e(slots["body"])}</p>')
            if kind == "error":
                ui.retry_button()
            return
        st.html(
            f'<p class="d2-tag">{ui.icon(slots["icon"])}{ui.e(slots["tag"])}</p>{notes}'
            f'<p class="d2-label" style="margin-top:1.1rem">{ui.e(slots["heading"])}</p>'
            f'<p class="d2-figure">{ui.e(slots["price"])}</p><p class="d2-unit">{ui.e(slots["unit"])} · {ui.e(slots["words"])}</p>'
            f'<p class="d2-small">{ui.e(slots["statement"])}</p><div style="height:.8rem"></div>'
            + row(slots["uncertainty_label"], slots["uncertainty"])
            + f'<p class="d2-small">{ui.e(slots["uncertainty_text"])}</p>'
            + row(slots["provenance_label"], "")
            + f'<p class="d2-small">{ui.e(slots["provenance"])}</p>'
            + f'<p class="d2-small">{ui.e(slots["unknown"])}</p>'
        )


def stats(reference) -> None:
    """Three bracket-framed facts, all read from repository files."""
    cv = load_cross_validation()
    p = reference.price
    items = [
        (fmt.count(reference.n_rows), "Căn trong tập huấn luyện"),
        (f'{fmt.number(p["min"])} – {fmt.number(p["max"])}', "Khoảng giá trong dữ liệu, tỷ đồng"),
    ]
    if cv.status == "available":
        items.append((ui.cv_best(cv)["mae"], "MAE kiểm định chéo tốt nhất, chưa phải đánh giá cuối"))
    for i, (cell, (value, label)) in enumerate(zip(st.columns(len(items), gap="large"), items), start=1):
        with cell:
            with st.container(key=f"frame_stat_{i}"):
                st.html(f'<div class="d2-stat"><p class="d2-stat-v">{ui.e(value)}</p>'
                        f'<div class="d2-stat-l"><span>{ui.e(label)}</span><span>{i:03d}</span></div></div>')


def valuation(view: state.Page, reference) -> None:
    claim, _, caveat = content.LEAD.partition(". ")  # the reference's two-tone lead: claim, then a gray caveat
    st.html(f'<h1 class="d2-h1">{ui.e(content.TITLE)}</h1>'
            f'<p class="d2-lead">{ui.e(claim)}. <span>{ui.e(caveat)}</span></p><div style="height:1.6rem"></div>')
    form, out = st.columns([7, 5], gap="large")
    with form:
        ui.error_summary(view)
        with st.container(key="frame_form"):  # one bracket frame; dotted rules divide the groups, as in the reference hero
            for i, (group, label) in enumerate(schema.GROUPS.items()):
                st.html(f'<p class="d2-h2{" d2-h2--rule" if i else ""}">{ui.e(label)}</p>')
                ui.fields(group, view, reference, LAYOUT[group], gap="small")
        st.html(f'<p class="lab-help">{ui.e(content.REQUIRED_LEGEND)}</p>')
        with st.container(key="actions", horizontal=True, vertical_alignment="center"):
            ui.submit_button(view)
            ui.reset_button()
        ui.blocked_note(view)
    with out:
        with st.container(key="sticky_readout"):
            readout(view, reference)
    st.html('<div style="height:2.4rem"></div>')
    stats(reference)


def evaluation() -> None:
    cv = load_cross_validation()
    copy = ui.eval_copy(cv)
    st.html(f'<h1 class="d2-h1" style="font-size:clamp(2rem,3.6vw,3rem)">{ui.e(content.NAV[1])}</h1>'
            f'<p class="d2-lead">{ui.e(content.EVAL_INTRO)}</p>')
    left, right = st.columns([7, 5], gap="large")
    with right:
        with st.container(key="frame_final"):
            st.html(f'<p class="d2-label">{ui.e(content.EVAL_NO_FINAL_LABEL)}</p>'
                    f'<p class="d2-figure" style="font-size:2.6rem">{ui.e(content.EVAL_NO_FINAL)}</p>'
                    f'<p class="d2-small">{ui.e(content.EVAL_NO_FINAL_TEXT)}</p>')
    if cv.status != "available":
        with left:
            st.html(f'<p class="d2-p">{ui.e(cv.problem or content.EVAL_MISSING)}</p>')
        return
    with left:
        st.html(f'<p class="d2-h2">{ui.e(content.EVAL_CV_HEADING)}</p><p class="d2-small">{ui.e(content.EVAL_CV_KIND)} {ui.e(copy["folds"])}</p>')
        st.altair_chart(ui.cv_chart(cv, bar=TOKENS["TEXT"], text=TOKENS["TEXT"], background="transparent"), width="stretch")
        st.html(ui.table(content.EVAL_COLUMNS, ui.cv_rows(cv)))
    with right:
        st.html("".join(row(k, v) + "" for k, v in [(content.METRIC_LABELS[m], ui.cv_best(cv)[m]) for m in ("mae", "rmse", "r2")])
                + f'<p class="d2-small">{ui.e(content.BEST_CAPTION.format(model=ui.cv_best(cv)["model"]))}</p>'
                + "".join(f'<p class="d2-small"><strong>{ui.e(k)}</strong>: {ui.e(v)}</p>' for k, v in content.METRIC_HELP)
                + f'<p class="d2-small">{ui.e(copy["source"])}</p>')


def data(reference) -> None:
    st.html(f'<h1 class="d2-h1" style="font-size:clamp(2rem,3.6vw,3rem)">{ui.e(content.NAV[2])}</h1>'
            f'<p class="d2-lead">{ui.e(content.DATA_INTRO)}</p>')
    left, right = st.columns([7, 5], gap="large")
    with left:
        st.html(f'<p class="d2-h2">{ui.e(content.DATA_HIST_HEADING)}</p>')
        st.altair_chart(diamond_distribution(reference, text=TOKENS["TEXT"], grid=TOKENS["BRACKET"]), width="stretch")
    with right:
        st.html("".join(row(k, v) for k, v in ui.data_facts(reference))
                + f'<p class="d2-h2">{ui.e(content.DATA_LIMITS_HEADING)}</p>' + ui.bullets(content.DATA_LIMITS)
                + f'<p class="d2-h2">{ui.e(content.DATA_MISSING_HEADING)}</p>'
                + ui.table(content.DATA_MISSING_COLUMNS, ui.missing_rows(reference)))


st.set_page_config(page_title=f"design_02 · Terminal — {content.TITLE}", layout="wide")
ui.apply_theme(THEME, CSS)
ui.load_fonts(*EXTRA_FONTS)
reference = state.bootstrap()
ui.reference_guard(reference)
view = state.page(reference)

st.html(f'<p class="d2-word">{ui.e(content.TITLE)}</p>')
ui.banner(view)
tab_valuation, tab_evaluation, tab_data = ui.view_tabs()
with tab_valuation:
    valuation(view, reference)
with tab_evaluation:
    evaluation()
with tab_data:
    data(reference)
ui.lab_panel(view)
