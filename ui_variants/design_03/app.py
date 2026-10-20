"""design_03 — #REP interface after the "Increase" concept (green material, neon rim, payload panel).

Run from the repository root:
    streamlit run ui_variants/design_03/app.py

Design source: design_references/design_03/ (design_spec.md, design_tokens.json).
Only theme, layout and markup live here; behaviour comes from ui_variants/shared.
"""
import sys
from pathlib import Path
from string import Template

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import streamlit as st  # noqa: E402

from components import GROUP_ICONS, group_status, payload  # noqa: E402
from shared import content, schema, state, widgets as ui  # noqa: E402
from shared.evaluation import load_cross_validation  # noqa: E402

TOKENS = dict(RIM_A="#34F3BD", RIM_B="#A5FA69", GROUND="#0E2924", CARD="#12473D", CODE="#023030", TEXT="#EEFAFA",
              SECONDARY="#9DB8B0", SEC_BTN="#384647", ACC_A="#4DF4AF", ACC_B="#A1FA6A", FIELD_BORDER="#6FA898",
              LIGHT_CARD="#E8F1EE", LIGHT_TEXT="#0E2924", LIGHT_MUTED="#4A6B63")

THEME = {
    "theme.base": "dark",
    "theme.primaryColor": TOKENS["ACC_A"],
    "theme.backgroundColor": TOKENS["GROUND"],
    "theme.secondaryBackgroundColor": TOKENS["GROUND"],
    "theme.textColor": TOKENS["TEXT"],
    "theme.borderColor": TOKENS["FIELD_BORDER"],
    "theme.linkColor": TOKENS["ACC_A"],
    "theme.font": "'Exo':https://fonts.googleapis.com/css2?family=Exo:wght@400;500;600;700&display=swap",
    "theme.codeFont": "'JetBrains Mono':https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap",
    "theme.baseFontSize": 16,
    "theme.baseRadius": "0.5rem",
}

CSS = Template((HERE / "styles.css").read_text(encoding="utf-8")).substitute(TOKENS)
LAYOUT = {"location": 2, "size": 3, "structure": 3, "extra": [[1, 1], [1], [1]]}


def status(group: str, values: dict) -> str:
    """The group's real state, signposted with the reference's bar-and-square marker."""
    text, ok = group_status(group, values)
    return (f'<span class="d3-status {"d3-ok" if ok else "d3-miss"}"><span class="d3-bar"></span>'
            f'<span class="d3-sq"></span>{ui.e(text)}</span>')


def estimate(view: state.Page, reference) -> None:
    slots = state.result_slots(view, reference)
    kind = slots["kind"]
    with st.container(key=f"estimate_{kind}"):
        notes = "".join(f'<p class="d3-note">{ui.icon("warning")}{ui.e(t)}</p>'
                        for t in [slots["stale"], slots["simulated"], *slots["warnings"]] if t)
        if kind not in ("sample", "result"):
            st.html(f'{notes}<p class="d3-k">{ui.e(content.RESULT_LABEL)}</p>'
                    f'<p class="d3-state-h">{ui.icon(slots["icon"])}{ui.e(slots["heading"])}</p>'
                    f'<p class="d3-small">{ui.e(slots["body"])}</p>')
            if kind == "error":
                ui.retry_button()
            return
        st.html(
            f'<div style="display:flex;justify-content:space-between;gap:1rem;align-items:center">'
            f'<p class="d3-k">{ui.icon("home")}{ui.e(slots["heading"])}</p>'
            f'<p class="d3-chip">{ui.icon(slots["icon"])}{ui.e(slots["tag"])}</p></div>{notes}'
            f'<p class="d3-price">{ui.e(slots["price"])}<span>{ui.e(slots["unit"])}</span></p>'
            f'<p class="d3-small">{ui.e(slots["words"])}</p><div class="d3-track"></div>'
            f'<p class="d3-small">{ui.e(slots["statement"])}</p>'
            f'<p class="d3-small"><strong>{ui.e(slots["uncertainty_label"])}: {ui.e(slots["uncertainty"])}.</strong> '
            f'{ui.e(slots["uncertainty_text"])}</p>'
            f'<p class="d3-small">{ui.e(slots["provenance"])}</p>'
        )


def valuation(view: state.Page, reference) -> None:
    st.html(f'<h1 class="d3-h1">{ui.e(content.TITLE)}</h1><p class="d3-lead">{ui.e(content.LEAD)}</p>'
            '<div style="height:1rem"></div>')
    form, side = st.columns([6, 5], gap="large")
    with form:
        ui.error_summary(view)
        for group, label in schema.GROUPS.items():
            with st.container(key=f"card_{group}"):
                st.html(f'<div class="d3-head"><p class="d3-h3"><span class="d3-tile">{ui.icon(GROUP_ICONS[group])}</span>'
                        f'{ui.e(label)}</p>{status(group, view.values)}</div>')
                ui.fields(group, view, reference, LAYOUT[group], gap="small")
        st.html(f'<p class="lab-help">{ui.e(content.REQUIRED_LEGEND)}</p>')
        with st.container(key="actions", horizontal=True, vertical_alignment="center"):
            ui.submit_button(view)
            ui.reset_button()
        ui.blocked_note(view)
    with side:
        with st.container(key="sticky_estimate"):
            estimate(view, reference)
            st.html(payload(view.values))
            st.html(f'<p class="d3-small" style="margin:0 14px">{ui.e(state.unknown_note(view.values))}</p>')


def evaluation() -> None:
    cv = load_cross_validation()
    copy = ui.eval_copy(cv)
    head = f'<h2 class="d3-h2">{ui.e(content.NAV[1])}</h2><p class="d3-lead">{ui.e(content.EVAL_INTRO)}</p>'
    final = (f'<div class="d3-card"><p class="d3-k">{ui.e(content.EVAL_NO_FINAL_LABEL)}</p><p class="d3-v">{ui.e(content.EVAL_NO_FINAL)}</p>'
             f'<p class="d3-small">{ui.e(content.EVAL_NO_FINAL_TEXT)}</p></div>')
    if cv.status != "available":
        st.html(head + f'<div class="d3-grid d3-grid--3">{final}<div class="d3-card"><p class="d3-p">'
                f'{ui.e(cv.problem or content.EVAL_MISSING)}</p></div></div>')
        return
    best = ui.cv_best(cv)
    st.html(head + f'<div class="d3-grid d3-grid--3">{final}'
            f'<div class="d3-card"><p class="d3-k">{ui.e(content.BEST_CAPTION.format(model=best["model"]))}</p>'
            + ui.dl([(content.METRIC_LABELS[k], best[k]) for k in ("mae", "rmse", "r2")]) + '</div>'
            f'<div class="d3-card"><p class="d3-k">{ui.e(content.EVAL_CV_HEADING)}</p><p class="d3-small">{ui.e(content.EVAL_CV_KIND)}</p>'
            f'<p class="d3-small">{ui.e(copy["folds"])}</p></div></div>')
    st.html('<div style="height:.4rem"></div>')
    chart, table = st.columns([7, 5], gap="small")
    with chart:
        with st.container(key="card_cv"):
            st.altair_chart(ui.cv_chart(cv, bar=TOKENS["ACC_A"], text=TOKENS["TEXT"], background="transparent"), width="stretch")
    with table:
        st.html('<div class="d3-card">' + ui.table(content.EVAL_COLUMNS, ui.cv_rows(cv)) + "</div>")
    st.html('<div class="d3-rows">' + "".join(
        f'<div class="d3-rowi"><span class="d3-tile">{ui.icon("info")}</span><p class="d3-small" style="margin:0">'
        f'<strong>{ui.e(k)}</strong>: {ui.e(v)}</p></div>' for k, v in content.METRIC_HELP)
        + f'<div class="d3-rowi"><span class="d3-tile">{ui.icon("description")}</span><p class="d3-small" style="margin:0">'
          f'{ui.e(copy["source"])}</p></div></div>')


def data(reference) -> None:
    facts = "".join(f'<div class="d3-card"><p class="d3-k">{ui.e(k)}</p><p class="d3-p" style="font-size:1.15rem">{ui.e(v)}</p></div>'
                    for k, v in ui.data_facts(reference))
    st.html(f'<h2 class="d3-h2">{ui.e(content.NAV[2])}</h2>'
            f'<p class="d3-lead">{ui.e(content.DATA_INTRO)}</p><div class="d3-grid d3-grid--4">{facts}</div>')
    st.html('<div style="height:.4rem"></div>')
    chart, side = st.columns([7, 5], gap="small")
    with chart:
        with st.container(key="card_hist"):
            st.html(f'<p class="d3-h3">{ui.e(content.DATA_HIST_HEADING)}</p>')
            st.altair_chart(ui.price_hist_chart(reference, bar=TOKENS["ACC_A"], background="transparent", height=280), width="stretch")
    with side:
        st.html('<div class="d3-card">' + f'<p class="d3-k">{ui.e(content.DATA_MISSING_HEADING)}</p>'
                + ui.table(content.DATA_MISSING_COLUMNS, ui.missing_rows(reference)) + "</div>")
    st.html(f'<h3 class="d3-h3" style="margin-top:1.6rem">{ui.e(content.DATA_LIMITS_HEADING)}</h3><div class="d3-rows">' + "".join(
        f'<div class="d3-rowi"><span class="d3-tile">{ui.icon("rule")}</span><p class="d3-p" style="margin:0">{ui.e(t)}</p></div>'
        for t in content.DATA_LIMITS) + "</div>")


st.set_page_config(page_title=f"design_03 · Green — {content.TITLE}", layout="wide")
ui.apply_theme(THEME, CSS)
reference = state.bootstrap()
ui.reference_guard(reference)
view = state.page(reference)

st.html(f'<p class="d3-word">{ui.e(content.TITLE)}</p>')
ui.banner(view)
tab_valuation, tab_evaluation, tab_data = ui.view_tabs()
with tab_valuation:
    valuation(view, reference)
with tab_evaluation:
    evaluation()
with tab_data:
    data(reference)
ui.lab_panel(view)
