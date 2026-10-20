"""design_05 — #REP interface after the "Finotive" page (centre line, violet action, spotlight on the result).

Run from the repository root:
    streamlit run ui_variants/design_05/app.py

Design source: design_references/design_05/ (design_spec.md, design_tokens.json).
Only theme, layout and markup live here; behaviour comes from ui_variants/shared.
"""
import sys
from pathlib import Path
from string import Template

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import streamlit as st  # noqa: E402

from shared import content, schema, state, widgets as ui  # noqa: E402
from shared.evaluation import load_cross_validation  # noqa: E402
from shared.reference import MIN_ROWS_PER_LOCATION  # noqa: E402

TOKENS = dict(HERO="#17161C", FLOOR="#000000", CARD="#1D1C24", CARD_RAISED="#221E2F", BORDER="#38373C", TEXT="#FDFDFF",
              SECONDARY="#9E9AA6", ACCENT="#6F47C2", ACCENT_LIGHT="#815CCE", FIELD_BORDER="#6A6773")

THEME = {
    "theme.base": "dark",
    "theme.primaryColor": TOKENS["ACCENT_LIGHT"],
    "theme.backgroundColor": TOKENS["FLOOR"],
    "theme.secondaryBackgroundColor": "#121117",
    "theme.textColor": TOKENS["TEXT"],
    "theme.borderColor": TOKENS["FIELD_BORDER"],
    "theme.linkColor": TOKENS["ACCENT_LIGHT"],
    "theme.font": "'Inter Tight':https://fonts.googleapis.com/css2?family=Inter+Tight:wght@300;400;500;600&display=swap",
    "theme.baseFontSize": 16,
    "theme.baseRadius": "0.625rem",
}

CSS = Template((HERE / "styles.css").read_text(encoding="utf-8")).substitute(TOKENS)
LAYOUT = {"location": 2, "size": 3, "structure": 3, "extra": [[1, 1], [1], [1]]}


def card(label: str, body: str, cls: str = "") -> str:
    return f'<div class="d5-card {cls}"><p class="d5-k">{ui.e(label)}</p>{body}</div>'


def result(view: state.Page, reference) -> None:
    slots = state.result_slots(view, reference)
    kind = slots["kind"]
    with st.container(key=f"result_{kind}"):
        notes = "".join(f'<p class="d5-note">{ui.icon("warning")}{ui.e(t)}</p>'
                        for t in [slots["stale"], slots["simulated"], *slots["warnings"]] if t)
        if kind not in ("sample", "result"):
            st.html(f'<div class="d5-state">{notes}<p class="d5-state-h">{ui.icon(slots["icon"])}{ui.e(slots["heading"])}</p>'
                    f'<p class="d5-small">{ui.e(slots["body"])}</p></div>')
            if kind == "error":
                ui.retry_button()
            return
        price = (f'<p class="d5-tag">{ui.icon(slots["icon"])}{ui.e(slots["tag"])}</p>{notes}'
                 f'<p class="d5-price">{ui.e(slots["price"])}<span>{ui.e(slots["unit"])}</span></p>'
                 f'<p class="d5-small">{ui.e(slots["words"])}</p><p class="d5-small">{ui.e(slots["statement"])}</p>')
        # price on the left over two rows; interval and source stacked beside it; the recap runs full width below
        st.html(
            '<div class="d5-bento">' + card(slots["heading"], price, "d5-card--price")
            + card(slots["uncertainty_label"], f'<p class="d5-v">{ui.e(slots["uncertainty"])}</p><p class="d5-small">{ui.e(slots["uncertainty_text"])}</p>')
            + card(slots["provenance_label"], f'<p class="d5-small">{ui.e(slots["provenance"])}</p><p class="d5-small">{ui.e(slots["unknown"])}</p>')
            + card(slots["recap_label"], ui.dl(slots["recap"]), "d5-card--recap") + "</div>"
        )


def valuation(view: state.Page, reference) -> None:
    st.html(f'<h1 class="d5-h1">{ui.e(content.TITLE)}</h1><p class="d5-lead">{ui.e(content.LEAD)}</p>')
    with st.container(key="card_form"):
        ui.error_summary(view)
        for group, label in schema.GROUPS.items():
            st.html(f'<p class="d5-h3" style="margin-top:1rem">{ui.e(label)}</p>')
            ui.fields(group, view, reference, LAYOUT[group], gap="small")
        st.html(f'<p class="lab-help">{ui.e(content.REQUIRED_LEGEND)}</p>')
    with st.container(key="cta", horizontal=True, vertical_alignment="center"):
        ui.submit_button(view)
        ui.reset_button()
    ui.blocked_note(view)
    st.html('<div class="d5-beam" aria-hidden="true"></div>')
    result(view, reference)


def evaluation() -> None:
    cv = load_cross_validation()
    copy = ui.eval_copy(cv)
    st.html(f'<h2 class="d5-h2">{ui.e(content.NAV[1])}</h2><p class="d5-lead">{ui.e(content.EVAL_INTRO)}</p><div style="height:1.6rem"></div>')
    final = card(content.EVAL_NO_FINAL_LABEL, f'<p class="d5-v">{ui.e(content.EVAL_NO_FINAL)}</p><p class="d5-small">{ui.e(content.EVAL_NO_FINAL_TEXT)}</p>')
    if cv.status != "available":
        st.html(f'<div class="d5-bento">{card(content.EVAL_CV_HEADING, f"<p class=d5-p>{ui.e(cv.problem or content.EVAL_MISSING)}</p>")}{final}</div>')
        return
    chart, side = st.columns([3, 2], gap="small")
    with chart:
        with st.container(key="card_cv"):
            st.html(f'<p class="d5-k">{ui.e(content.EVAL_CV_HEADING)}</p><p class="d5-small">{ui.e(content.EVAL_CV_KIND)} {ui.e(copy["folds"])}</p>')
            st.altair_chart(ui.cv_chart(cv, bar=TOKENS["ACCENT"], text=TOKENS["TEXT"], background="transparent"), width="stretch")
    with side:
        best = ui.cv_best(cv)
        st.html(final + '<div style="height:10px"></div>' + card(content.BEST_CAPTION.format(model=best["model"]),
                ui.dl([(content.METRIC_LABELS[k], best[k]) for k in ("mae", "rmse", "r2")])))
    st.html('<div class="d5-bento d5-bento--b">' + card(content.EVAL_CV_HEADING, ui.table(content.EVAL_COLUMNS, ui.cv_rows(cv)))
            + card("Giải thích", "".join(f'<p class="d5-small"><strong>{ui.e(k)}</strong>: {ui.e(v)}</p>' for k, v in content.METRIC_HELP)
                   + f'<p class="d5-small">{ui.e(copy["source"])}</p>') + "</div>")


def data(reference) -> None:
    st.html(f'<h2 class="d5-h2">{ui.e(content.NAV[2])}</h2><p class="d5-lead">{ui.e(content.DATA_INTRO)}</p><div style="height:1.6rem"></div>')
    chart, side = st.columns([3, 2], gap="small")
    with chart:
        with st.container(key="card_hist"):
            st.html(f'<p class="d5-k">{ui.e(content.DATA_HIST_HEADING)}</p>')
            st.altair_chart(ui.price_hist_chart(reference, bar=TOKENS["ACCENT"], background="transparent", height=280), width="stretch")
    with side:
        st.html(card(content.DATA_FACTS["source"], ui.dl(ui.data_facts(reference)[1:]) + f'<p class="d5-small">{ui.e(content.DATA_SOURCE)}</p>')
                + '<div style="height:10px"></div>'
                + card(content.DATA_LIMITS_HEADING, '<ul class="d5-checks lab-plain">'
                       + "".join(f"<li>{ui.e(t)}</li>" for t in content.DATA_LIMITS) + "</ul>"))
    st.html(f'<h2 class="d5-h2" style="font-size:clamp(1.6rem,3vw,2.2rem)">Câu hỏi thường gặp</h2><div style="height:1rem"></div>')
    facts = {"min_rows": MIN_ROWS_PER_LOCATION, "offered": reference.locations_offered, "cities": len(reference.cities)}
    for question, answer in content.FAQ:
        with st.expander(question):
            st.html(f'<p class="d5-p">{ui.e(answer.format(**facts))}</p>')
    st.html('<div style="height:1rem"></div><div style="max-width:44rem;margin:0 auto">'
            + card(content.DATA_MISSING_HEADING, ui.table(content.DATA_MISSING_COLUMNS, ui.missing_rows(reference))) + "</div>")


st.set_page_config(page_title=f"design_05 · Centre — {content.TITLE}", layout="wide")
ui.apply_theme(THEME, CSS)
reference = state.bootstrap()
ui.reference_guard(reference)
view = state.page(reference)

st.html(f'<p class="d5-word">{ui.icon("auto_awesome")}{ui.e(content.TITLE)}</p>')
ui.banner(view)
tab_valuation, tab_evaluation, tab_data = ui.view_tabs()
with tab_valuation:
    valuation(view, reference)
with tab_evaluation:
    evaluation()
with tab_data:
    data(reference)
ui.lab_panel(view)
