"""Concept D — Minimalist.

Run:  streamlit run design_lab/concept_d.py

A single narrow column, one typeface at regular weight, navy on white and one
tangerine button. Direction dealt by the Taste skill ("The quiet instrument",
Archivo, "Navy on white"). Only theme, layout and markup live in this file.
"""
import streamlit as st

from lab import content, schema, state, ui
from lab.evaluation import load_cross_validation

INK, MUTED, SURFACE, ACCENT, BORDER, ERROR = "#1f2b4d", "#5f667b", "#f4f4f2", "#f7941d", "#767d90", "#b3261e"

THEME = {
    "theme.base": "light",
    "theme.primaryColor": INK,
    "theme.backgroundColor": "#ffffff",
    "theme.secondaryBackgroundColor": SURFACE,
    "theme.textColor": INK,
    "theme.linkColor": INK,
    "theme.borderColor": BORDER,
    "theme.font": "Archivo:https://fonts.googleapis.com/css2?family=Archivo:wght@400;600&display=swap, sans-serif",
    "theme.baseFontSize": 17,
    "theme.baseRadius": "0.25rem",
}

CSS = f"""
:root{{--lab-focus:{INK}}}
[data-testid="stMainBlockContainer"]{{max-width:44rem;padding:4rem 1.25rem 6rem}}
.d-h1{{font-size:1.75rem;font-weight:400;letter-spacing:-0.02em;line-height:1.3;margin:0 0 .5rem}}
.d-lead{{font-size:1.0625rem;line-height:1.6;margin:1.25rem 0 0;max-width:36rem}}
.d-h2{{font-size:1.25rem;font-weight:400;letter-spacing:-0.01em;line-height:1.35;margin:1.75rem 0 0}}
.d-h3{{font-size:1rem;font-weight:600;line-height:1.4;margin:1.75rem 0 .3rem}}
.d-p{{margin:0 0 .5rem;line-height:1.6}}
.d-muted,.lab-help{{color:{MUTED}}}
.lab-err,.lab-summary{{color:{ERROR}}}
.lab-summary{{background:#fdf3f2;padding:1rem 1.1rem;border-radius:4px}}
.lab-summary li{{color:{INK}}}
.lab-banner{{background:{SURFACE};padding:.8rem 1rem;border-radius:4px;line-height:1.5}}
[data-testid="stWidgetLabel"] p{{font-size:1rem}}

/* navigation: plain words, the current one in full ink */
[role="tablist"]::after{{display:none}}
[role="tablist"]{{gap:1.75rem;margin:1.25rem 0 .25rem}}
[data-testid="stTab"]{{padding:0 0 .45rem;height:auto;color:{MUTED}}}
[data-testid="stTab"][aria-selected="true"]{{color:{INK}}}

/* the one accent on the page */
[data-testid="stBaseButton-primary"]{{background:{ACCENT};color:{INK};border:2px solid {INK};min-height:3rem;padding:0 1.6rem}}
[data-testid="stBaseButton-primary"] p{{font-weight:600}}
[data-testid="stBaseButton-primary"]:hover{{background:#ffa93d;color:{INK};border-color:{INK}}}
[data-testid="stBaseButton-primary"]:disabled{{background:{SURFACE};color:{MUTED};border-color:{BORDER}}}
[data-testid="stBaseButton-tertiary"]{{color:{INK};text-decoration:underline;text-underline-offset:.2em;min-height:3rem}}
.st-key-actions{{margin-top:1rem}}

/* result: no panel, only type */
[class*="st-key-result_"]{{margin-top:2.5rem}}
.st-key-result_sample{{background:{SURFACE};outline:2px dashed {BORDER};padding:1.6rem 1.75rem}}
.d-tag{{font-weight:600;margin:0 0 1.25rem}}
.d-label{{font-size:1rem;font-weight:400;color:{MUTED};margin:0}}
.d-price{{font-size:clamp(2.75rem,9vw,4.25rem);font-weight:400;letter-spacing:-0.03em;line-height:1.1;margin:.15rem 0 0;
  font-variant-numeric:tabular-nums}}
.d-price span{{font-size:.38em;letter-spacing:0;margin-left:.15em}}
.d-words{{font-size:1.125rem;margin:.3rem 0 1.25rem}}
.d-state-h{{font-size:1.25rem;font-weight:400;margin:0 0 .4rem}}
.d-note{{background:#fff4e2;padding:.7rem .9rem;border-radius:4px;margin:0 0 1rem}}
.lab-dl>div{{padding:.35rem 0}}
.lab-dl dt{{color:{MUTED}}}
.lab-table thead th{{color:{MUTED};font-weight:400}}
.lab-table tbody tr:nth-child(odd){{background:{SURFACE}}}
.lab-table th,.lab-table td{{padding-left:.6rem}}
.lab-table .num{{padding-right:.6rem}}
"""

COLUMNS = {"location": 2, "size": 3, "structure": 3, "extra": [[1, 1], [1], [1]]}


def result(view: state.Page, reference) -> None:
    slots = state.result_slots(view, reference)
    kind = slots["kind"]
    with st.container(key=f"result_{kind}"):
        notes = "".join(
            f'<p class="d-note">{ui.icon("warning")}{ui.e(text)}</p>'
            for text in [slots["stale"], slots["simulated"], *slots["warnings"]] if text
        )
        if kind not in ("sample", "result"):
            st.html(
                f'{notes}<h2 class="d-state-h">{ui.icon(slots["icon"])}{ui.e(slots["heading"])}</h2>'
                f'<p class="d-p">{ui.e(slots["body"])}</p>'
            )
            if kind == "error":
                ui.retry_button()
            return
        st.html(
            f'<p class="d-tag">{ui.icon(slots["icon"])}{ui.e(slots["tag"])}</p>{notes}'
            f'<h2 class="d-label">{ui.e(slots["heading"])}</h2>'
            f'<p class="d-price">{ui.e(slots["price"])}<span>{ui.e(slots["unit"])}</span></p>'
            f'<p class="d-words">{ui.e(slots["words"])}</p>'
            f'<p class="d-p">{ui.e(slots["statement"])}</p>'
            f'<h3 class="d-h3">{ui.e(slots["uncertainty_label"])}</h3>'
            f'<p class="d-p"><strong>{ui.e(slots["uncertainty"])}.</strong> {ui.e(slots["uncertainty_text"])}</p>'
            f'<h3 class="d-h3">{ui.e(slots["recap_label"])}</h3>{ui.dl(slots["recap"])}'
            f'<p class="d-p d-muted">{ui.e(slots["unknown"])}</p>'
            f'<h3 class="d-h3">{ui.e(slots["provenance_label"])}</h3>'
            f'<p class="d-p d-muted">{ui.e(slots["provenance"])}</p>'
        )


def valuation(view: state.Page, reference) -> None:
    st.html(f'<p class="d-lead">{ui.e(content.LEAD)}</p>')
    ui.error_summary(view)
    for group, label in schema.GROUPS.items():
        st.html(f'<h2 class="d-h2">{ui.e(label)}</h2>')
        ui.fields(group, view, reference, COLUMNS[group])
    st.html(f'<p class="lab-help">{ui.e(content.REQUIRED_LEGEND)}</p>')
    with st.container(key="actions", horizontal=True, vertical_alignment="center"):
        ui.submit_button(view)
        ui.reset_button()
    ui.blocked_note(view)
    result(view, reference)


def evaluation() -> None:
    cv = load_cross_validation()
    copy = ui.eval_copy(cv)
    st.html(
        f'<p class="d-lead">{ui.e(content.EVAL_INTRO)}</p>'
        f'<h2 class="d-h2">{ui.e(content.EVAL_NO_FINAL_LABEL)}</h2>'
        f'<p class="d-p"><strong>{ui.e(content.EVAL_NO_FINAL)}.</strong> {ui.e(content.EVAL_NO_FINAL_TEXT)}</p>'
    )
    if cv.status != "available":
        st.html(f'<p class="d-p">{ui.icon("info")}{ui.e(cv.problem or content.EVAL_MISSING)}</p>')
        return
    best = ui.cv_best(cv)
    st.html(
        f'<h2 class="d-h2">{ui.e(content.EVAL_CV_HEADING)}</h2>'
        f'<p class="d-note">{ui.icon("info")}{ui.e(content.EVAL_CV_KIND)}</p>'
        f'<p class="d-p">{ui.e(copy["folds"])} {ui.e(copy["best"])}</p>'
        + ui.dl([(f'{content.METRIC_LABELS[k]}', best[k]) for k in ("mae", "rmse", "r2")])
    )
    st.altair_chart(ui.cv_chart(cv, bar=INK, text=INK), width="stretch")
    st.html(
        ui.table(content.EVAL_COLUMNS, ui.cv_rows(cv))
        + "".join(f'<p class="d-p d-muted"><strong>{ui.e(k)}</strong>: {ui.e(v)}</p>' for k, v in content.METRIC_HELP)
        + f'<p class="d-p d-muted">{ui.e(copy["source"])}</p>'
    )


def data(reference) -> None:
    st.html(f'<p class="d-lead">{ui.e(content.DATA_INTRO)}</p>' + ui.dl(ui.data_facts(reference)))
    st.html(f'<h2 class="d-h2">{ui.e(content.DATA_HIST_HEADING)}</h2>')
    st.altair_chart(ui.price_hist_chart(reference, bar=INK), width="stretch")
    st.html(
        f'<h2 class="d-h2">{ui.e(content.DATA_LIMITS_HEADING)}</h2>{ui.bullets(content.DATA_LIMITS)}'
        f'<h2 class="d-h2">{ui.e(content.DATA_MISSING_HEADING)}</h2>'
        + ui.table(content.DATA_MISSING_COLUMNS, ui.missing_rows(reference))
    )


st.set_page_config(page_title=f"D · Tối giản — {content.TITLE}", layout="centered")
ui.apply_theme(THEME, CSS)
reference = state.bootstrap()
ui.reference_guard(reference)
view = state.page(reference)

st.html(f'<h1 class="d-h1">{ui.e(content.TITLE)}</h1>')
ui.banner(view)
tab_valuation, tab_evaluation, tab_data = ui.view_tabs()
with tab_valuation:
    valuation(view, reference)
with tab_evaluation:
    evaluation()
with tab_data:
    data(reference)
ui.lab_panel(view)
