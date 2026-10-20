"""Concept A — Premium Real Estate.

Run:  streamlit run design_lab/concept_a.py

An editorial spread: one light news serif for everything, a rose-grey page, and
the price set as the monument on an inverted plate beside the form. Direction
dealt by the Taste skill ("The name as a monument", "Rose grey, green"), with
Newsreader from the skill's own library because the dealt faces have no
Vietnamese glyphs. Only theme, layout and markup live in this file.
"""
from string import Template

import streamlit as st

from lab import content, schema, state, ui
from lab.evaluation import load_cross_validation

TOKENS = dict(BG="#ebe5e3", SURFACE="#e1dad7", INK="#2b2622", MUTED="#5e5551", ACCENT="#0f7d45",
              ACCENT_DARK="#0c6b3a", BORDER="#756a65", ERROR="#a3231f", PLATE_MUTED="#b9aeaa")

THEME = {
    "theme.base": "light",
    "theme.primaryColor": TOKENS["ACCENT"],
    "theme.backgroundColor": TOKENS["BG"],
    "theme.secondaryBackgroundColor": TOKENS["SURFACE"],
    "theme.textColor": TOKENS["INK"],
    "theme.linkColor": TOKENS["INK"],
    "theme.borderColor": TOKENS["BORDER"],
    "theme.font": (
        "Newsreader:https://fonts.googleapis.com/css2?family=Newsreader:"
        "ital,opsz,wght@0,6..72,200..800;1,6..72,200..800&display=swap, serif"
    ),
    "theme.baseFontSize": 18,
    "theme.baseRadius": "0.125rem",
}

CSS = Template("""
:root{--lab-focus:$ACCENT}
[data-testid="stMainBlockContainer"]{max-width:80rem;padding:2rem 3rem 6rem}
.a-h1{font-size:clamp(2.4rem,4.2vw,3.5rem);font-weight:300;letter-spacing:-0.035em;line-height:1.15;margin:1.25rem 0 0}
.a-lead{font-size:1.25rem;font-weight:300;line-height:1.5;margin:1rem 0 .5rem;max-width:33rem}
.a-h2{font-size:1.55rem;font-style:italic;font-weight:400;line-height:1.3;margin:2rem 0 0}
.a-h3{font-size:1rem;font-style:italic;font-weight:400;line-height:1.4;margin:1.9rem 0 .35rem}
.a-p{margin:0 0 .6rem;line-height:1.6}
.a-muted,.lab-help{color:$MUTED}
.lab-help,.lab-err{font-size:.9rem}
.lab-err,.lab-summary{color:$ERROR}
.lab-summary{background:$SURFACE;padding:1.1rem 1.25rem}
.lab-summary li{color:$INK}
.lab-banner{background:$SURFACE;padding:.7rem 1.1rem;line-height:1.5;font-size:.9rem}

/* navigation: three words, the current one carries the accent */
[role="tablist"]{gap:2.5rem;margin-top:1rem}
[role="tablist"]::after{display:none}
[data-testid="stTab"]{padding:0 0 .45rem;height:auto;color:$MUTED}
[data-testid="stTab"][aria-selected="true"]{color:$INK}

/* the single action: flat, square, green */
[data-testid="stBaseButton-primary"]{background:$ACCENT;color:#fff;border:0;border-radius:0;min-height:3.5rem;padding:0 2.4rem}
[data-testid="stBaseButton-primary"]:hover{background:$ACCENT_DARK;color:#fff}
[data-testid="stBaseButton-primary"]:disabled{background:$SURFACE;color:$MUTED}
[data-testid="stBaseButton-tertiary"]{color:$INK;text-decoration:underline;text-underline-offset:.22em;min-height:3.5rem}
.st-key-actions{margin-top:1.25rem;gap:1.5rem}

/* the plate: ground and ink inverted, the price as the monument */
[class*="st-key-plate_"]{background:$INK;color:$BG;padding:2.75rem 2.5rem 2.5rem;min-height:34rem}
[data-testid="stColumn"]:has([class*="st-key-plate_"]){position:sticky;top:1.5rem;align-self:flex-start}
.st-key-plate_sample{outline:2px dashed $PLATE_MUTED;outline-offset:-12px}
.a-tag{margin:0 0 2.25rem;font-size:1rem;font-weight:500}
.a-price{font-size:clamp(6.5rem,12.5vw,11.5rem);font-weight:300;letter-spacing:-0.055em;line-height:1;margin:0 0 0 -.04em;
  font-variant-numeric:lining-nums}
.a-unit{font-size:1.55rem;font-weight:300;letter-spacing:-0.01em;margin:0}
.a-words{font-size:1.25rem;font-weight:300;margin:.6rem 0 2rem}
[class*="st-key-plate_"] .a-h3{color:$PLATE_MUTED}
[class*="st-key-plate_"] .a-muted,[class*="st-key-plate_"] .lab-dl dt{color:$PLATE_MUTED}
.a-state-h{font-size:clamp(2.4rem,4.2vw,3.5rem);font-weight:300;letter-spacing:-0.03em;line-height:1.15;margin:0 0 1rem}
.a-note{background:#f1dfb8;color:#5a3a00;padding:.7rem .9rem;margin:0 0 1.25rem;font-size:.9rem}
[class*="st-key-plate_"] [data-testid="stBaseButton-secondary"]{background:$BG;color:$INK;border:0;border-radius:0;min-height:3rem;padding:0 1.5rem}

/* side facts beside a wide column */
.a-fact{margin:0 0 1.6rem}
.a-fact dt{font-size:.9rem;font-style:italic;color:$MUTED}
.a-fact dd{margin:0;font-size:1.55rem;font-weight:300;letter-spacing:-0.025em;line-height:1.2}
.a-fact dd small{display:block;font-size:.9rem;letter-spacing:0;color:$MUTED;line-height:1.45;margin-top:.2rem}
.lab-table thead th{font-style:italic;color:$MUTED}
.lab-table tbody tr:nth-child(odd){background:$SURFACE}
.lab-table th,.lab-table td{padding-left:.7rem}
.lab-table .num{padding-right:.7rem}
@media (max-width:900px){
  [data-testid="stMainBlockContainer"]{padding:1.25rem 1.1rem 4rem}
  [class*="st-key-plate_"]{padding:2rem 1.5rem;min-height:0}
  [data-testid="stColumn"]:has([class*="st-key-plate_"]){position:static}
  [role="tablist"]{gap:1.25rem}
}
""").substitute(TOKENS)

COLUMNS = {"location": 2, "size": 3, "structure": 3, "extra": [[1, 1], [1], [1]]}


def plate(view: state.Page, reference) -> None:
    slots = state.result_slots(view, reference)
    kind = slots["kind"]
    with st.container(key=f"plate_{kind}"):
        notes = "".join(
            f'<p class="a-note">{ui.icon("warning")}{ui.e(text)}</p>'
            for text in [slots["stale"], slots["simulated"], *slots["warnings"]] if text
        )
        if kind not in ("sample", "result"):
            st.html(
                f'{notes}<h2 class="a-state-h">{ui.e(slots["heading"])}</h2>'
                f'<p class="a-p">{ui.icon(slots["icon"])}{ui.e(slots["body"])}</p>'
            )
            if kind == "error":
                ui.retry_button()
            return
        st.html(
            f'<p class="a-tag">{ui.icon(slots["icon"])}{ui.e(slots["tag"])}</p>{notes}'
            f'<h2 class="lab-sr">{ui.e(slots["heading"])}</h2>'
            f'<p class="a-price">{ui.e(slots["price"])}</p>'
            f'<p class="a-unit">{ui.e(slots["unit"])}</p>'
            f'<p class="a-words">{ui.e(slots["heading"])}: {ui.e(slots["words"])}</p>'
            f'<p class="a-p">{ui.e(slots["statement"])}</p>'
            f'<h3 class="a-h3">{ui.e(slots["uncertainty_label"])}</h3>'
            f'<p class="a-p"><strong>{ui.e(slots["uncertainty"])}.</strong> {ui.e(slots["uncertainty_text"])}</p>'
            f'<h3 class="a-h3">{ui.e(slots["recap_label"])}</h3>{ui.dl(slots["recap"])}'
            f'<p class="a-p a-muted">{ui.e(slots["unknown"])}</p>'
            f'<h3 class="a-h3">{ui.e(slots["provenance_label"])}</h3>'
            f'<p class="a-p a-muted">{ui.e(slots["provenance"])}</p>'
        )


def valuation(view: state.Page, reference) -> None:
    form, result = st.columns([7, 5], gap="large")
    with form:
        st.html(f'<h1 class="a-h1">{ui.e(content.TITLE)}</h1><p class="a-lead">{ui.e(content.LEAD)}</p>')
        ui.error_summary(view)
        for group, label in schema.GROUPS.items():
            st.html(f'<h2 class="a-h2">{ui.e(label)}</h2>')
            ui.fields(group, view, reference, COLUMNS[group])
        st.html(f'<p class="lab-help">{ui.e(content.REQUIRED_LEGEND)}</p>')
        with st.container(key="actions", horizontal=True, vertical_alignment="center"):
            ui.submit_button(view)
            ui.reset_button()
        ui.blocked_note(view)
    with result:
        plate(view, reference)


def facts(rows: list[tuple[str, str, str]]) -> str:
    return "".join(
        f'<dl class="a-fact"><dt>{ui.e(label)}</dt><dd>{ui.e(value)}'
        f'{f"<small>{ui.e(note)}</small>" if note else ""}</dd></dl>'
        for label, value, note in rows
    )


def evaluation() -> None:
    cv = load_cross_validation()
    copy = ui.eval_copy(cv)
    side, wide = st.columns([4, 8], gap="large")
    rows = [(content.EVAL_NO_FINAL_LABEL, content.EVAL_NO_FINAL, content.EVAL_NO_FINAL_TEXT)]
    if cv.status == "available":
        best = ui.cv_best(cv)
        caption = content.BEST_CAPTION.format(model=best["model"])
        rows += [(content.METRIC_LABELS[k], best[k], caption) for k in ("mae", "rmse", "r2")]
    with side:
        st.html(f'<h1 class="a-h1">{ui.e(content.NAV[1])}</h1><div style="height:1.5rem"></div>' + facts(rows))
    with wide:
        st.html(f'<p class="a-lead" style="max-width:40rem;margin-top:1.6rem">{ui.e(content.EVAL_INTRO)}</p>')
        if cv.status != "available":
            st.html(f'<p class="a-p">{ui.icon("info")}{ui.e(cv.problem or content.EVAL_MISSING)}</p>')
            return
        st.html(
            f'<h2 class="a-h2">{ui.e(content.EVAL_CV_HEADING)}</h2>'
            f'<p class="a-note" style="margin-top:.8rem">{ui.icon("info")}{ui.e(content.EVAL_CV_KIND)}</p>'
            f'<p class="a-p">{ui.e(copy["folds"])} {ui.e(copy["best"])}</p>'
        )
        st.altair_chart(ui.cv_chart(cv, bar=TOKENS["INK"], text=TOKENS["INK"]), width="stretch")
        st.html(
            ui.table(content.EVAL_COLUMNS, ui.cv_rows(cv))
            + "".join(f'<p class="a-p a-muted"><em>{ui.e(k)}</em>: {ui.e(v)}</p>' for k, v in content.METRIC_HELP)
            + f'<p class="a-p a-muted">{ui.e(copy["source"])}</p>'
        )


def data(reference) -> None:
    side, wide = st.columns([4, 8], gap="large")
    with side:
        st.html(
            f'<h1 class="a-h1">{ui.e(content.NAV[2])}</h1><div style="height:1.5rem"></div>'
            + facts([(label, value, "") for label, value in ui.data_facts(reference)])
        )
    with wide:
        st.html(
            f'<p class="a-lead" style="max-width:40rem;margin-top:1.6rem">{ui.e(content.DATA_INTRO)}</p>'
            f'<h2 class="a-h2">{ui.e(content.DATA_HIST_HEADING)}</h2>'
        )
        st.altair_chart(ui.price_hist_chart(reference, bar=TOKENS["INK"]), width="stretch")
        st.html(
            f'<h2 class="a-h2">{ui.e(content.DATA_LIMITS_HEADING)}</h2>{ui.bullets(content.DATA_LIMITS)}'
            f'<h2 class="a-h2">{ui.e(content.DATA_MISSING_HEADING)}</h2>'
            + ui.table(content.DATA_MISSING_COLUMNS, ui.missing_rows(reference))
        )


st.set_page_config(page_title=f"A · Bất động sản cao cấp — {content.TITLE}", layout="wide")
ui.apply_theme(THEME, CSS)
reference = state.bootstrap()
ui.reference_guard(reference)
view = state.page(reference)

ui.banner(view)
tab_valuation, tab_evaluation, tab_data = ui.view_tabs()
with tab_valuation:
    valuation(view, reference)
with tab_evaluation:
    evaluation()
with tab_data:
    data(reference)
ui.lab_panel(view)
