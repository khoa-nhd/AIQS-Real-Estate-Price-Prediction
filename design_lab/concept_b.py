"""Concept B — Real Estate Analytics.

Run:  streamlit run design_lab/concept_b.py

One dark board. The form is a rail on the left; the canvas holds three labelled
zones of tiles: the estimate for this house, the model's accuracy, and the data.
Palette and type from UI UX Pro Max's dashboard result ("Dark tech + status
green", Fira Sans); the tile-board composition from the Taste skill ("The
well-kept board"). Only theme, layout and markup live in this file.
"""
from string import Template

import streamlit as st

from lab import content, schema, state, ui
from lab.evaluation import load_cross_validation

TOKENS = dict(BG="#0F172A", TILE="#1B2336", TILE2="#243049", WELL="#0B1220", FG="#F8FAFC", MUTED="#94A3B8",
              BORDER="#7C8BA1", GREEN="#22C55E", SKY="#38BDF8", AMBER="#FBBF24", RED="#F87171", SLATE="#94A3B8")

THEME = {
    "theme.base": "dark",
    "theme.primaryColor": TOKENS["GREEN"],
    "theme.backgroundColor": TOKENS["BG"],
    "theme.secondaryBackgroundColor": TOKENS["WELL"],
    "theme.textColor": TOKENS["FG"],
    "theme.linkColor": TOKENS["SKY"],
    "theme.borderColor": TOKENS["BORDER"],
    "theme.font": "Fira Sans:https://fonts.googleapis.com/css2?family=Fira+Sans:wght@400;500;600&display=swap, sans-serif",
    "theme.baseFontSize": 16,
    "theme.baseRadius": "0.375rem",
}

CSS = Template("""
:root{--lab-focus:$SKY}
[data-testid="stMainBlockContainer"]{max-width:108rem;padding:1.1rem 1.5rem 4rem}
.b-title{font-size:1.35rem;font-weight:600;letter-spacing:-0.01em;line-height:1.3;margin:0}
.st-key-nav p{margin:0;text-align:right;line-height:2.4}
.st-key-nav a{color:$FG;text-decoration:none;background:$TILE;padding:.45rem .8rem;border-radius:.375rem;margin-left:.4rem;white-space:nowrap}
.st-key-nav a:hover{background:$TILE2}
.lab-banner{background:$TILE;padding:.65rem 1rem;border-radius:.5rem;line-height:1.5}
.lab-banner .lab-ico{color:$AMBER}
.lab-help{color:$MUTED}
.lab-err{color:$RED}
.lab-summary{background:#3a1c24;color:#FECACA;padding:.9rem 1rem;border-radius:.5rem}

/* rail: the inputs */
.st-key-rail{background:$TILE;border-radius:.6rem;padding:1.2rem 1.25rem 1.4rem}
.b-h2{font-size:1.1rem;font-weight:600;line-height:1.3;margin:0}
.b-h3{font-size:.95rem;font-weight:500;color:$MUTED;line-height:1.3;margin:.9rem 0 0}
[data-testid="stBaseButton-primary"]{background:$GREEN;color:$BG;border:0;min-height:3rem}
[data-testid="stBaseButton-primary"] p{font-weight:600;font-size:1.05rem}
[data-testid="stBaseButton-primary"]:hover{background:#4ADE80;color:$BG}
[data-testid="stBaseButton-primary"]:disabled{background:$TILE2;color:$MUTED}
[data-testid="stBaseButton-tertiary"]{color:$FG;text-decoration:underline;text-underline-offset:.2em}

/* zones: a filled bar and a heading say which scope the tiles belong to */
.b-zone{border-left:.45rem solid $SLATE;padding:.1rem 0 .1rem .9rem;margin:.4rem 0 0}
.b-zone--pred{border-color:$GREEN}
.b-zone--eval{border-color:$SKY}
.b-zone h2{font-size:1.25rem;font-weight:600;line-height:1.3;margin:0;scroll-margin-top:1rem}
.b-zone p{margin:.15rem 0 0;color:$MUTED}
.st-key-zone_eval,.st-key-zone_data{margin-top:1.4rem}

/* tiles */
.b-grid{display:grid;gap:.75rem}
.b-grid--pred{grid-template-columns:7fr 5fr}
.b-grid--4{grid-template-columns:repeat(4,minmax(0,1fr))}
.b-tile{background:$TILE;border-radius:.6rem;padding:1.05rem 1.2rem 1.15rem;min-width:0}
.b-zone-eval .b-tile{background:$TILE2}
.b-wide{grid-column:1/-1}
.b-k{font-size:.9rem;font-weight:500;color:$MUTED;margin:0 0 .3rem}
.b-v{font-size:2rem;font-weight:600;line-height:1.15;margin:0;font-variant-numeric:tabular-nums;letter-spacing:-0.01em}
.b-c{font-size:.9rem;color:$MUTED;line-height:1.45;margin:.4rem 0 0}
.b-p{margin:.5rem 0 0;line-height:1.55;max-width:76ch}
.b-tile>.b-c{max-width:86ch}
.b-price{font-size:clamp(3.75rem,6.4vw,6rem);font-weight:600;letter-spacing:-0.035em;line-height:1;margin:.1rem 0 0;
  font-variant-numeric:tabular-nums}
.b-price span{font-size:.3em;font-weight:500;letter-spacing:0;margin-left:.3em}
.b-words{font-size:1.1rem;margin:.45rem 0 0}
.b-sample{outline:2px dashed $AMBER;outline-offset:-6px}
.b-tag{display:inline-flex;align-items:center;background:$AMBER;color:$BG;font-weight:600;font-size:.9rem;
  padding:.2rem .6rem;border-radius:.3rem;margin:0 0 .8rem}
.b-note{background:#3b2f12;color:#FDE68A;padding:.6rem .8rem;border-radius:.4rem;margin:0 0 .75rem;line-height:1.45}
.b-kind{background:#12324a;color:#BAE6FD;padding:.6rem .8rem;border-radius:.4rem;margin:.75rem 0 0;line-height:1.45}
.b-state-h{font-size:1.5rem;font-weight:600;margin:0 0 .4rem}
.b-recap .lab-dl{columns:2;column-gap:2rem}
.b-recap .lab-dl>div{break-inside:avoid}
.lab-dl dt{color:$MUTED}
[class*="st-key-tile_"]{background:$TILE;border-radius:.6rem;padding:1rem 1.1rem .6rem}
.st-key-tile_cv{background:$TILE2}
.b-grid--facts .b-v{font-size:1.4rem;line-height:1.3}
.lab-table thead th{color:$MUTED;font-weight:500;font-size:.9rem}
.lab-table tbody tr:nth-child(odd){background:rgba(148,163,184,.10)}
.lab-table th,.lab-table td{padding:.45rem .6rem}
@media (max-width:1000px){
  [data-testid="stHorizontalBlock"]:has(>[data-testid="stColumn"] .st-key-rail),
  [data-testid="stHorizontalBlock"]:has(>[data-testid="stColumn"] [class*="st-key-tile_"]){flex-direction:column}
  [data-testid="stHorizontalBlock"]:has(>[data-testid="stColumn"] .st-key-rail)>[data-testid="stColumn"],
  [data-testid="stHorizontalBlock"]:has(>[data-testid="stColumn"] [class*="st-key-tile_"])>[data-testid="stColumn"]{width:100%;flex:1 1 auto}
  [data-testid="stMainBlockContainer"]{padding:.9rem .9rem 3rem}
  .b-grid--pred{grid-template-columns:1fr}
  .b-grid--4{grid-template-columns:repeat(2,minmax(0,1fr))}
  .b-recap .lab-dl{columns:1}
  .st-key-nav p{text-align:left}
  .st-key-nav a{margin:0 .4rem 0 0}
}
""").substitute(TOKENS)

LAYOUT = {"location": [[1, 1]], "size": 2, "structure": 2, "extra": [[1, 1], [1], [1]]}


def tile(label: str, value: str = "", caption: str = "", extra: str = "", cls: str = "") -> str:
    return (
        f'<div class="b-tile {cls}"><p class="b-k">{ui.e(label)}</p>'
        + (f'<p class="b-v">{ui.e(value)}</p>' if value else "")
        + (f'<p class="b-c">{ui.e(caption)}</p>' if caption else "")
        + extra + "</div>"
    )


def zone(view_id: str, cls: str) -> str:
    index = content.VIEW_IDS.index(view_id)
    return (
        f'<div class="b-zone b-zone--{cls}"><h2 id="{view_id}">{ui.e(content.NAV[index])}</h2>'
        f'<p>{ui.e(content.SCOPE_NOTE[view_id])}</p></div>'
    )


def rail(view: state.Page, reference) -> None:
    with st.container(key="rail"):
        st.html(f'<h2 class="b-h2">{ui.e(content.FORM_HEADING)}</h2>')
        ui.error_summary(view)
        for group, label in schema.GROUPS.items():
            st.html(f'<h3 class="b-h3">{ui.e(label)}</h3>')
            ui.fields(group, view, reference, LAYOUT[group], gap="small")
        st.html(f'<p class="lab-help">{ui.e(content.REQUIRED_LEGEND)}</p>')
        ui.submit_button(view, width="stretch")
        ui.blocked_note(view)
        ui.reset_button()


def prediction_zone(view: state.Page, reference) -> None:
    slots = state.result_slots(view, reference)
    kind = slots["kind"]
    with st.container(key="zone_pred"):
        notes = "".join(
            f'<p class="b-note">{ui.icon("warning")}{ui.e(text)}</p>'
            for text in [slots["stale"], slots["simulated"], *slots["warnings"]] if text
        )
        if kind not in ("sample", "result"):
            st.html(
                zone("uoc-tinh", "pred") + '<div class="b-grid" style="margin-top:.9rem">'
                f'<div class="b-tile">{notes}<h3 class="b-state-h">{ui.icon(slots["icon"])}{ui.e(slots["heading"])}</h3>'
                f'<p class="b-p">{ui.e(slots["body"])}</p></div></div>'
            )
            if kind == "error":
                ui.retry_button()
            return
        sample = "b-sample" if kind == "sample" else ""
        price = (
            f'<div class="b-tile {sample}"><p class="b-tag">{ui.icon(slots["icon"])}{ui.e(slots["tag"])}</p>{notes}'
            f'<p class="b-k">{ui.e(slots["heading"])}</p>'
            f'<p class="b-price">{ui.e(slots["price"])}<span>{ui.e(slots["unit"])}</span></p>'
            f'<p class="b-words">{ui.e(slots["words"])}</p><p class="b-p">{ui.e(slots["statement"])}</p></div>'
        )
        st.html(
            zone("uoc-tinh", "pred") + '<div class="b-grid b-grid--pred" style="margin-top:.9rem">' + price
            + tile(slots["uncertainty_label"], slots["uncertainty"], slots["uncertainty_text"])
            + tile(slots["recap_label"], extra=ui.dl(slots["recap"]) + f'<p class="b-c">{ui.e(slots["unknown"])}</p>',
                   cls="b-recap")
            + tile(slots["provenance_label"], caption=slots["provenance"]) + "</div>"
        )


def evaluation_zone() -> None:
    cv = load_cross_validation()
    copy = ui.eval_copy(cv)
    with st.container(key="zone_eval"):
        head = zone("do-chinh-xac", "eval") + f'<p class="b-p" style="color:{TOKENS["MUTED"]}">{ui.e(content.EVAL_INTRO)}</p>'
        final = tile(content.EVAL_NO_FINAL_LABEL, content.EVAL_NO_FINAL, content.EVAL_NO_FINAL_TEXT)
        if cv.status != "available":
            st.html(
                head + f'<div class="b-zone-eval b-grid" style="margin-top:.9rem">{final}'
                + tile(content.EVAL_CV_HEADING, caption=cv.problem or content.EVAL_MISSING) + "</div>"
            )
            return
        best = ui.cv_best(cv)
        caption = content.BEST_CAPTION.format(model=best["model"])
        metrics = "".join(tile(f"{content.METRIC_LABELS[k]}", best[k], caption) for k in ("mae", "rmse", "r2"))
        st.html(
            head + f'<p class="b-kind">{ui.icon("info")}{ui.e(content.EVAL_CV_KIND)} {ui.e(copy["folds"])}</p>'
            f'<div class="b-zone-eval b-grid b-grid--4" style="margin-top:.9rem">{final}{metrics}</div>'
        )
        chart, table = st.columns([1, 1], gap="small")
        with chart:
            with st.container(key="tile_cv"):
                st.altair_chart(
                    ui.cv_chart(cv, bar=TOKENS["SKY"], text=TOKENS["FG"], background=TOKENS["TILE2"]), width="stretch"
                )
        with table:
            st.html(
                '<div class="b-zone-eval"><div class="b-tile">'
                + ui.table(content.EVAL_COLUMNS, ui.cv_rows(cv)) + "</div></div>"
            )
        st.html(
            '<div class="b-tile">'
            + "".join(f'<p class="b-c"><strong>{ui.e(k)}</strong>: {ui.e(v)}</p>' for k, v in content.METRIC_HELP)
            + f'<p class="b-c">{ui.e(copy["best"])} {ui.e(copy["source"])}</p></div>'
        )


def data_zone(reference) -> None:
    with st.container(key="zone_data"):
        facts = "".join(tile(label, value) for label, value in ui.data_facts(reference))
        st.html(
            zone("du-lieu", "data") + f'<p class="b-p" style="color:{TOKENS["MUTED"]}">{ui.e(content.DATA_INTRO)}</p>'
            f'<div class="b-grid b-grid--4 b-grid--facts" style="margin-top:.9rem">{facts}</div>'
        )
        chart, side = st.columns([7, 5], gap="small")
        with chart:
            with st.container(key="tile_hist"):
                st.html(f'<p class="b-k">{ui.e(content.DATA_HIST_HEADING)}</p>')
                st.altair_chart(
                    ui.price_hist_chart(reference, bar=TOKENS["SLATE"], background=TOKENS["TILE"], height=300),
                    width="stretch",
                )
        with side:
            st.html(
                tile(content.DATA_LIMITS_HEADING, extra=ui.bullets(content.DATA_LIMITS))
                + '<div style="height:.75rem"></div>'
                + tile(content.DATA_MISSING_HEADING,
                       extra=ui.table(content.DATA_MISSING_COLUMNS, ui.missing_rows(reference)))
            )


st.set_page_config(page_title=f"B · Phân tích — {content.TITLE}", layout="wide")
ui.apply_theme(THEME, CSS)
reference = state.bootstrap()
ui.reference_guard(reference)
view = state.page(reference)

title, nav = st.columns([3, 6], vertical_alignment="center")
with title:
    st.html(f'<h1 class="b-title">{ui.e(content.TITLE)}</h1>')
with nav:
    with st.container(key="nav"):
        st.markdown(" ".join(f"[{label}](#{view_id})" for label, view_id in zip(content.NAV, content.VIEW_IDS)))
ui.banner(view)

left, canvas = st.columns([5, 11], gap="medium")
with left:
    rail(view, reference)
with canvas:
    prediction_zone(view, reference)
    evaluation_zone()
    data_zone(reference)
ui.lab_panel(view)
