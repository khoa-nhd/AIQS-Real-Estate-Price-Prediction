"""Concept C — Modern Fintech.

Run:  streamlit run design_lab/concept_c.py

Input on the left in soft cards; on the right a live check, one large blue
action and a black stage for the figure. A three-part track shows where the
person is between entering details and reading the result. Direction dealt by
the Taste skill ("The product performs", "Sheet and biro"), with Bricolage
Grotesque from the skill's library because the dealt face's Vietnamese support
could not be verified. Only theme, layout and markup live in this file.
"""
from string import Template

import streamlit as st

from lab import content, schema, state, ui
from lab.evaluation import load_cross_validation

TOKENS = dict(INK="#111111", SURFACE="#f4f4f4", MUTED="#5f5f5f", ACCENT="#1a4be0", ACCENT_DARK="#143cb8",
              BORDER="#808080", ERROR="#c21f1f", STAGE_MUTED="#a8a8a8", STAGE_BLOCK="#1f1f1f", AMBER="#ffcf5c")

THEME = {
    "theme.base": "light",
    "theme.primaryColor": TOKENS["ACCENT"],
    "theme.backgroundColor": "#ffffff",
    "theme.secondaryBackgroundColor": "#ffffff",
    "theme.textColor": TOKENS["INK"],
    "theme.linkColor": TOKENS["ACCENT"],
    "theme.borderColor": TOKENS["BORDER"],
    "theme.font": (
        "Bricolage Grotesque:https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:"
        "opsz,wght@12..96,200..800&display=swap, sans-serif"
    ),
    "theme.baseFontSize": 16,
    "theme.baseRadius": "0.75rem",
}

CSS = Template("""
:root{--lab-focus:$ACCENT}
[data-testid="stMainBlockContainer"]{max-width:76rem;padding:2rem 2rem 6rem}
.c-h1{font-size:clamp(2.2rem,4vw,3.2rem);font-weight:600;letter-spacing:-0.045em;line-height:1.12;margin:.25rem 0 0}
.c-lead{font-size:1.125rem;line-height:1.55;margin:.4rem 0 0;max-width:40rem}
.c-h2{font-size:1.25rem;font-weight:600;letter-spacing:-0.02em;line-height:1.3;margin:0}
.c-p{margin:.5rem 0 0;line-height:1.55}
.c-muted,.lab-help{color:$MUTED}
.lab-err,.lab-summary{color:$ERROR}
.lab-summary{background:#fdeeee;padding:1rem 1.15rem;border-radius:1rem}
.lab-summary li{color:$INK}
.lab-banner{background:$SURFACE;padding:.75rem 1.1rem;border-radius:.9rem;line-height:1.5}

/* navigation: one segmented bar */
[role="tablist"]{background:$SURFACE;border-radius:1.7rem;padding:.3rem;gap:.2rem;width:fit-content;max-width:100%;margin:1rem 0 .5rem}
[role="tablist"]::after{display:none}
[data-testid="stTab"]{height:auto;padding:.6rem 1.15rem;border-radius:999px;color:$INK}
[data-testid="stTab"][aria-selected="true"]{background:$INK;color:#fff}
[data-testid="stTab"]>div:last-child:empty,[role="tablist"]>div:not([role="tab"]){display:none}

/* the track from input to result */
.c-steps{list-style:none;display:flex;gap:.5rem;margin-top:1.25rem!important}
.c-steps li{flex:1 1 0;padding:.7rem 1rem;border-radius:.9rem;background:$SURFACE;color:$MUTED;font-weight:500;margin:0}
.c-steps li.is-done{color:$INK}
.c-steps li.is-current{background:$INK;color:#fff}

/* input cards */
[class*="st-key-card_"],.st-key-check{background:$SURFACE;border-radius:1.25rem;padding:1.4rem 1.5rem 1.6rem}
.c-check-line{margin:.6rem 0 0;line-height:1.5}

/* the one action */
[data-testid="stBaseButton-primary"]{background:$ACCENT;color:#fff;border:0;min-height:3.75rem;border-radius:1rem}
[data-testid="stBaseButton-primary"] p{font-size:1.2rem;font-weight:600;letter-spacing:-0.01em}
[data-testid="stBaseButton-primary"]:hover{background:$ACCENT_DARK;color:#fff}
[data-testid="stBaseButton-primary"]:disabled{background:#d9d9d9;color:$MUTED}
[data-testid="stBaseButton-tertiary"]{color:$INK;text-decoration:underline;text-underline-offset:.2em}

/* the stage */
[class*="st-key-stage_"]{background:$INK;color:#fff;border-radius:1.25rem;padding:1.75rem 1.75rem 1.9rem}
.st-key-stage_sample{outline:2px dashed $AMBER;outline-offset:-9px}
.c-tag{display:inline-flex;align-items:center;background:$AMBER;color:$INK;font-weight:600;font-size:.95rem;
  padding:.3rem .8rem;border-radius:999px;margin:0 0 1.1rem}
.c-label{color:$STAGE_MUTED;font-size:1rem;font-weight:500;margin:0}
.c-price{font-size:clamp(4.75rem,8.4vw,7.25rem);font-weight:600;letter-spacing:-0.035em;line-height:1;margin:.1rem 0 0 -.03em;
  font-variant-numeric:tabular-nums}
.c-price span{font-size:.27em;font-weight:500;letter-spacing:-0.01em;margin-left:.35em}
.c-words{font-size:1.15rem;margin:.35rem 0 1rem}
.c-block{background:$STAGE_BLOCK;border-radius:.9rem;padding:1rem 1.15rem;margin-top:.7rem}
.c-block h3{font-size:1rem;font-weight:500;color:$STAGE_MUTED;margin:0 0 .3rem}
.c-block p{margin:0;line-height:1.5}
.c-block .c-big{font-size:1.35rem;font-weight:600;margin:0 0 .25rem}
[class*="st-key-stage_"] .lab-dl dt,[class*="st-key-stage_"] .c-muted{color:$STAGE_MUTED}
.c-state-h{font-size:1.7rem;font-weight:600;letter-spacing:-0.03em;line-height:1.2;margin:0 0 .5rem}
.c-note{background:$AMBER;color:$INK;padding:.65rem .9rem;border-radius:.8rem;margin:0 0 1rem;line-height:1.45}
[class*="st-key-stage_"] [data-testid="stBaseButton-secondary"]{background:#fff;color:$INK;border:0;min-height:3rem}

/* evaluation and data cards */
.c-grid{display:grid;gap:.75rem;grid-template-columns:repeat(4,minmax(0,1fr));margin-top:1.25rem}
.c-card{background:$SURFACE;border-radius:1.25rem;padding:1.25rem 1.35rem;min-width:0}
.c-card--stage{background:$INK;color:#fff}
.c-card--stage .c-k,.c-card--stage .c-c{color:$STAGE_MUTED}
.c-k{font-size:.95rem;font-weight:500;color:$MUTED;margin:0 0 .3rem}
.c-v{font-size:2.1rem;font-weight:600;letter-spacing:-0.04em;line-height:1.15;margin:0;font-variant-numeric:tabular-nums}
.c-c{font-size:.92rem;color:$MUTED;line-height:1.45;margin:.4rem 0 0}
.c-kind{background:$SURFACE;border-radius:.9rem;padding:.75rem 1rem;margin:1rem 0 0;line-height:1.5}
.lab-table thead th{color:$MUTED;font-weight:500}
.lab-table th,.lab-table td{padding:.5rem .6rem}
.lab-table tbody tr:nth-child(odd){background:#fff}
@media (max-width:900px){
  [data-testid="stMainBlockContainer"]{padding:1.1rem 1rem 4rem}
  .c-grid{grid-template-columns:repeat(2,minmax(0,1fr))}
  .c-steps li{padding:.6rem .7rem;font-size:.95rem}
  [data-testid="stTab"]{padding:.5rem .8rem}
}
""").substitute(TOKENS)

COLUMNS = {"location": 2, "size": 3, "structure": 3, "extra": [[1, 1], [1], [1]]}
STEP_OF_KIND = {"initial": 0, "invalid": 1, "fixed": 1}


def steps(view: state.Page) -> str:
    current = STEP_OF_KIND.get(view.kind, 2)
    items = ""
    for index, label in enumerate(content.WORKFLOW):
        if index == current:
            items += f'<li class="is-current" aria-current="step">{ui.e(label)}</li>'
        elif index < current:
            items += f'<li class="is-done">{ui.icon("check")}{ui.e(label)}</li>'
        else:
            items += f"<li>{ui.e(label)}</li>"
    return f'<ol class="c-steps lab-plain">{items}</ol>'


def check(view: state.Page) -> None:
    """Live check of the form, with the one action directly under it."""
    required = [spec for spec in schema.FIELDS if spec.required]
    missing = [spec.label for spec in required if view.values.get(spec.name) is None]
    if missing:
        line = content.CHECK_REQUIRED_MISSING.format(k=len(missing), n=len(required), names=", ".join(missing))
        mark = ui.icon("radio_button_unchecked")
    else:
        line = content.CHECK_REQUIRED_OK.format(n=len(required))
        mark = ui.icon("check_circle")
    with st.container(key="check"):
        st.html(
            f'<h2 class="c-h2">{ui.e(content.CHECK_HEADING)}</h2>'
            f'<p class="c-check-line">{mark}{ui.e(line)}</p>'
            f'<p class="c-check-line c-muted">{ui.e(state.unknown_note(view.values))}</p>'
        )
        ui.submit_button(view, width="stretch")
        ui.blocked_note(view)
        ui.reset_button()


def block(title: str, big: str = "", text: str = "", extra: str = "") -> str:
    return (
        f'<div class="c-block"><h3>{ui.e(title)}</h3>'
        + (f'<p class="c-big">{ui.e(big)}</p>' if big else "")
        + (f"<p>{ui.e(text)}</p>" if text else "") + extra + "</div>"
    )


def stage(view: state.Page, reference) -> None:
    slots = state.result_slots(view, reference)
    kind = slots["kind"]
    with st.container(key=f"stage_{kind}"):
        notes = "".join(
            f'<p class="c-note">{ui.icon("warning")}{ui.e(text)}</p>'
            for text in [slots["stale"], slots["simulated"], *slots["warnings"]] if text
        )
        if kind not in ("sample", "result"):
            st.html(
                f'{notes}<h2 class="c-state-h">{ui.icon(slots["icon"])}{ui.e(slots["heading"])}</h2>'
                f'<p class="c-p">{ui.e(slots["body"])}</p>'
            )
            if kind == "error":
                ui.retry_button()
            return
        st.html(
            f'<p class="c-tag">{ui.icon(slots["icon"])}{ui.e(slots["tag"])}</p>{notes}'
            f'<h2 class="c-label">{ui.e(slots["heading"])}</h2>'
            f'<p class="c-price">{ui.e(slots["price"])}<span>{ui.e(slots["unit"])}</span></p>'
            f'<p class="c-words">{ui.e(slots["words"])}</p>'
            f'<p class="c-p">{ui.e(slots["statement"])}</p>'
            + block(slots["uncertainty_label"], slots["uncertainty"], slots["uncertainty_text"])
            + block(slots["recap_label"], extra=ui.dl(slots["recap"]) + f'<p class="c-muted">{ui.e(slots["unknown"])}</p>')
            + block(slots["provenance_label"], text=slots["provenance"])
        )


def valuation(view: state.Page, reference) -> None:
    st.html(f'<p class="c-lead">{ui.e(content.LEAD)}</p>' + steps(view))
    form, side = st.columns([7, 5], gap="medium")
    with form:
        ui.error_summary(view)
        for group, label in schema.GROUPS.items():
            with st.container(key=f"card_{group}"):
                st.html(f'<h2 class="c-h2">{ui.e(label)}</h2>')
                ui.fields(group, view, reference, COLUMNS[group], choices="segmented")
        st.html(f'<p class="lab-help">{ui.e(content.REQUIRED_LEGEND)}</p>')
    with side:
        check(view)
        stage(view, reference)


def card(label: str, value: str = "", caption: str = "", extra: str = "", cls: str = "") -> str:
    return (
        f'<div class="c-card {cls}"><p class="c-k">{ui.e(label)}</p>'
        + (f'<p class="c-v">{ui.e(value)}</p>' if value else "")
        + (f'<p class="c-c">{ui.e(caption)}</p>' if caption else "") + extra + "</div>"
    )


def evaluation() -> None:
    cv = load_cross_validation()
    copy = ui.eval_copy(cv)
    final = card(content.EVAL_NO_FINAL_LABEL, content.EVAL_NO_FINAL, content.EVAL_NO_FINAL_TEXT, cls="c-card--stage")
    if cv.status != "available":
        st.html(
            f'<p class="c-lead">{ui.e(content.EVAL_INTRO)}</p><div class="c-grid">{final}'
            + card(content.EVAL_CV_HEADING, caption=cv.problem or content.EVAL_MISSING) + "</div>"
        )
        return
    best = ui.cv_best(cv)
    caption = content.BEST_CAPTION.format(model=best["model"])
    metrics = "".join(card(content.METRIC_LABELS[k], best[k], caption) for k in ("mae", "rmse", "r2"))
    st.html(
        f'<p class="c-lead">{ui.e(content.EVAL_INTRO)}</p><div class="c-grid">{final}{metrics}</div>'
        f'<h2 class="c-h2" style="margin-top:2rem">{ui.e(content.EVAL_CV_HEADING)}</h2>'
        f'<p class="c-kind">{ui.icon("info")}{ui.e(content.EVAL_CV_KIND)} {ui.e(copy["folds"])}</p>'
    )
    chart, table = st.columns([7, 5], gap="small")
    with chart:
        with st.container(key="card_cv"):
            st.altair_chart(
                ui.cv_chart(cv, bar=TOKENS["INK"], text=TOKENS["INK"], background=TOKENS["SURFACE"]), width="stretch"
            )
    with table:
        st.html('<div class="c-card">' + ui.table(content.EVAL_COLUMNS, ui.cv_rows(cv)) + "</div>")
    st.html(
        '<div class="c-card">'
        + "".join(f'<p class="c-c"><strong>{ui.e(k)}</strong>: {ui.e(v)}</p>' for k, v in content.METRIC_HELP)
        + f'<p class="c-c">{ui.e(copy["best"])} {ui.e(copy["source"])}</p></div>'
    )


def data(reference) -> None:
    facts = "".join(card(label, value) for label, value in ui.data_facts(reference))
    st.html(f'<p class="c-lead">{ui.e(content.DATA_INTRO)}</p><div class="c-grid">{facts}</div>')
    chart, side = st.columns([7, 5], gap="small")
    with chart:
        with st.container(key="card_hist"):
            st.html(f'<h2 class="c-h2">{ui.e(content.DATA_HIST_HEADING)}</h2>')
            st.altair_chart(
                ui.price_hist_chart(reference, bar=TOKENS["INK"], background=TOKENS["SURFACE"], height=300),
                width="stretch",
            )
    with side:
        st.html(
            card(content.DATA_LIMITS_HEADING, extra=ui.bullets(content.DATA_LIMITS))
            + '<div style="height:.75rem"></div>'
            + card(content.DATA_MISSING_HEADING, extra=ui.table(content.DATA_MISSING_COLUMNS, ui.missing_rows(reference)))
        )


st.set_page_config(page_title=f"C · Fintech — {content.TITLE}", layout="wide")
ui.apply_theme(THEME, CSS)
reference = state.bootstrap()
ui.reference_guard(reference)
view = state.page(reference)

ui.banner(view)
st.html(f'<h1 class="c-h1">{ui.e(content.TITLE)}</h1>')
tab_valuation, tab_evaluation, tab_data = ui.view_tabs()
with tab_valuation:
    valuation(view, reference)
with tab_evaluation:
    evaluation()
with tab_data:
    data(reference)
ui.lab_panel(view)
