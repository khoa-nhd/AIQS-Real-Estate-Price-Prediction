"""Building blocks for the app, with no look of their own.

Widgets here carry the keys and behaviour. Markup helpers emit plain semantic
HTML with `lab-` class names, which app/styles.css styles.
"""
from __future__ import annotations

import html
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st
from streamlit import config

from . import content, formatting as fmt, schema, state
from .evaluation import CrossValidation
from .reference import Reference
from .schema import FIELDS, UNKNOWN, Field

# The app sets its theme from inside the script, so `streamlit run app/streamlit_app.py`
# needs no flags or config file. Moving these options to .streamlit/config.toml would
# also work, but that file applies to every Streamlit app run from the same folder.
BASE_OPTIONS = {"client.toolbarMode": "minimal", "theme.showWidgetBorder": True}

BASE_CSS = """
.lab-ico{font-family:'Material Symbols Rounded';font-weight:400;font-style:normal;font-size:1.25em;line-height:1;
  display:inline-block;vertical-align:-0.22em;letter-spacing:normal;text-transform:none;white-space:nowrap;
  font-feature-settings:'liga';-webkit-font-smoothing:antialiased;margin-right:.4em;flex:none}
#lab-ready{display:none}
.lab-sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}
[data-testid="stElementToolbar"]{box-shadow:none}
[data-testid="stElementContainer"]:has(.lab-note){margin-top:-0.8rem}
.lab-help,.lab-err{margin:0;font-size:.875rem;line-height:1.45}
.lab-err{font-weight:600}
.lab-banner,.lab-summary{display:flex;align-items:flex-start}
.lab-banner p,.lab-summary p{margin:0}
.lab-summary ul{margin:.35rem 0 0;padding-left:1.15rem}
.lab-summary li{margin:.15rem 0}
.lab-table-wrap{overflow-x:auto}
.lab-table{width:100%;border-collapse:collapse;font-variant-numeric:tabular-nums}
.lab-table th,.lab-table td{text-align:left;padding:.55rem 1rem .55rem 0;vertical-align:top;font-weight:400}
.lab-table thead th{font-weight:600}
.lab-table .num{text-align:right;padding-right:0}
.lab-table td.num{white-space:nowrap}
[data-testid="stHtml"] dl,[data-testid="stHtml"] ol.lab-plain{margin:0!important;padding:0!important}
[data-testid="stNumberInputField"],[data-testid="stTextInputRootElement"] input,input[role="combobox"],[data-testid="stRadioOption"] p,[data-testid="stTab"] p{font-size:1rem}
[data-testid="stNumberInputContainer"],[data-testid="stTextInputRootElement"],.react-aria-ComboBox>[role="group"]{min-height:2.75rem}
.lab-dl>div{display:flex;justify-content:space-between;gap:1.25rem;padding:.3rem 0}
.lab-dl dt,.lab-dl dd{margin:0}
.lab-dl dd{text-align:right}
.lab-list{margin:0;padding-left:1.15rem}
.lab-list li{margin:.3rem 0}
button:focus-visible,[role="tab"]:focus-visible{outline:3px solid var(--lab-focus,currentColor);outline-offset:2px}
[data-testid="stHtml"] p,[data-testid="stHtml"] li{overflow-wrap:anywhere}
[data-testid="stButtonGroup"] [role="radiogroup"]{flex-wrap:wrap;row-gap:.35rem}
/* fields: steppers only where a step of one means something (counts), clear buttons on demand */
[data-testid="stNumberInputContainer"]:has(input[step="0.1"]) :is([data-testid="stNumberInputStepDown"],[data-testid="stNumberInputStepUp"]){display:none}
@media (hover:hover){
  [data-testid="stNumberInputClearButton"],.react-aria-ComboBox button:is([aria-label="Clear value"],[aria-label="Xoá giá trị"]){opacity:0;transition:opacity .15s ease-out}
  [data-testid="stNumberInputContainer"]:is(:hover,:focus-within) [data-testid="stNumberInputClearButton"],
  .react-aria-ComboBox>[role="group"]:is(:hover,:focus-within) button:is([aria-label="Clear value"],[aria-label="Xoá giá trị"]){opacity:1}
}
/* browser surfaces carry the variant's palette */
::selection{background:var(--lab-select-bg,Highlight);color:var(--lab-select-fg,HighlightText)}
input,textarea{caret-color:var(--lab-caret,auto)}
[data-testid="stMain"]{scrollbar-width:thin;scrollbar-color:var(--lab-scroll,auto) transparent}
@media (max-width:640px){
  [role="tablist"]{flex-wrap:nowrap;overflow-x:auto;overscroll-behavior-x:contain;scrollbar-width:none;justify-content:flex-start;max-width:100%}
  [role="tablist"]::-webkit-scrollbar{display:none}
  [data-testid="stTab"]{flex:none}
  [data-testid^="stTabsScroll"]{display:none}  /* sits misaligned on styled tab bars; the cut-off tab already signals scrolling */
}
"""


def apply_theme(options: dict[str, object], css: str) -> None:
    """Set this variant's theme options, then add its CSS. Call right after set_page_config."""
    changed = False
    for key, value in {**BASE_OPTIONS, **options}.items():
        if config.get_option(key) != value:
            config.set_option(key, value)
            changed = True
    if changed and not st.session_state.get("_theme_applied"):
        st.session_state["_theme_applied"] = True
        st.rerun()  # the theme is sent to the browser at the start of a run
    st.html(f"<style>{BASE_CSS}{css}</style>")


def enhance_accessibility() -> None:
    """Run core/a11y.js in the page: Vietnamese page language, Vietnamese names for Streamlit's controls,
    required and invalid states on inputs, error-summary links that move focus, and a live region."""
    script = (Path(__file__).with_name("a11y.js")).read_text(encoding="utf-8")
    st.html(f"<script>{script}</script>", unsafe_allow_javascript=True)


def load_fonts(*urls: str) -> None:
    """Load extra web fonts beyond the theme's body, heading and code fonts."""
    if urls:
        st.html("<style>" + "".join(f"@import url('{u}');" for u in urls) + "</style>")


def e(text: object) -> str:
    return html.escape(str(text))


def icon(name: str) -> str:
    """A Material Symbols icon (the family Streamlit ships), hidden from screen readers."""
    return f'<span class="lab-ico" aria-hidden="true">{name}</span>'


# ---------------------------------------------------------------- form


def field(spec: Field, view: state.Page, reference: Reference, *, choices: str = "radio") -> None:
    """One form field: widget, range helper and, after a submit attempt, its error."""
    label = schema.widget_label(spec)
    if spec.kind == "city":
        st.selectbox(label, reference.cities, index=None, placeholder=spec.placeholder, key=spec.key,
                     on_change=state.city_changed)
    elif spec.kind == "district":
        city = st.session_state.get(schema.BY_NAME["City"].key)
        st.selectbox(label, reference.districts.get(city, ()), index=None, key=spec.key, disabled=not city,
                     placeholder=spec.placeholder if city else "Chọn tỉnh / thành phố trước",
                     on_change=state.district_changed)
    elif spec.kind in ("ward", "street", "project"):
        city = st.session_state.get(schema.BY_NAME["City"].key)
        district = st.session_state.get(schema.BY_NAME["District"].key)
        lists = {"ward": reference.wards, "street": reference.streets, "project": reference.projects}[spec.kind]
        names = lists.get((city, district), ())
        if spec.kind == "ward":
            st.selectbox(label, names, index=None, key=spec.key, disabled=not district,
                         placeholder=spec.placeholder if district else "Chọn quận / huyện trước")
        else:  # optional: «Không rõ» first, then the names seen in this district
            st.selectbox(label, (UNKNOWN, *names), key=spec.key, disabled=not district,
                         help=content.ADDRESS_HELP[spec.kind])
    elif spec.kind == "decimal":
        # text, not a number field: browsers' number fields refuse "4,1", the way Vietnamese write decimals
        st.text_input(label, placeholder=spec.placeholder, key=spec.key, max_chars=12, autocomplete="off")
    elif spec.kind == "count":
        st.number_input(label, value=None, step=1, format="%d", placeholder=spec.placeholder, key=spec.key)
    else:
        options = (UNKNOWN, *reference.options.get(spec.name, ()))
        show = lambda value, spec=spec: schema.display_value(spec, None if value == UNKNOWN else value)
        if spec.kind == "direction":
            st.selectbox(label, options, format_func=show, key=spec.key)
        elif choices == "segmented":
            st.segmented_control(label, options, format_func=show, required=True, key=spec.key)
        else:
            st.radio(label, options, format_func=show, horizontal=True, key=spec.key)

    notes = []
    if spec.name in reference.ranges:
        low, high = reference.ranges[spec.name]
        unit = f"\u00a0{spec.unit}" if spec.unit else ""  # keep "4 – 595 m²" on one line (the dash also needs a word joiner)
        notes.append(
            f'<p class="lab-help">{e(content.RANGE_HELP.format(low=fmt.number(low), high=fmt.number(high), unit=unit).replace(" – ", "\u00a0–\u2060\u00a0"))}</p>'
        )
    if spec.name in view.errors:
        notes.append(f'<p class="lab-err">{icon("error")}{e(view.errors[spec.name])}</p>')
    if notes:
        st.html(f'<div class="lab-note">{"".join(notes)}</div>')


def fields(group: str, view: state.Page, reference: Reference, layout: int | list[list[int]], *,
           choices: str = "radio", gap: str = "medium") -> None:
    """A field group. `layout` is fields per row, or one list of column weights per row."""
    specs = iter(schema.fields_in(group))
    total = len(schema.fields_in(group))
    rows = layout if isinstance(layout, list) else [[1] * layout] * -(-total // layout)
    for weights in rows:
        for cell in st.columns(weights, gap=gap):
            spec = next(specs, None)
            if spec is None:
                break
            with cell:
                field(spec, view, reference, choices=choices)


def error_summary(view: state.Page) -> None:
    """The summary above the form after a failed submit (brief FR-12)."""
    if not view.errors:
        return
    # each item links to its field; a11y.js moves focus there (the href is the no-script fallback)
    items = "".join(
        f'<li><a class="lab-jump" href="#{spec.key}" data-focus="{spec.key}"><strong>{e(spec.label)}</strong></a>: '
        f"{e(view.errors[spec.name])}</li>"
        for spec in FIELDS if spec.name in view.errors
    )
    heading = content.SUMMARY_HEADING.format(n=len(view.errors))
    st.html(
        f'<div class="lab-summary" role="alert">{icon("error")}'
        f'<div><p class="lab-summary-h"><strong>{e(heading)}</strong></p><ul>{items}</ul></div></div>'
    )


def banner(view: state.Page) -> None:
    """System banner: model unavailable (with the technical reason, which whoever deploys needs), or lab preview mode."""
    detail = ""
    if view.blocked:
        kind, name, text = "unavailable", "cloud_off", content.BANNER_UNAVAILABLE
        if view.model_reason:
            detail = f'<p class="d1-small">{e(content.BANNER_DETAIL.format(reason=view.model_reason))}</p>'
    elif view.preview:
        kind, name, text = "preview", "science", content.BANNER_PREVIEW
    else:
        return
    st.html(f'<div class="lab-banner lab-banner--{kind}" role="status">{icon(name)}<div><p>{e(text)}</p>{detail}</div></div>')


def submit_button(view: state.Page, **kwargs) -> None:
    st.button(content.SUBMIT, type="primary", key="submit", on_click=state.submit, disabled=view.blocked, **kwargs)


def blocked_note(view: state.Page) -> None:
    """Says why the action is disabled, so the button is never silently inert."""
    if view.blocked:
        st.html(f'<p class="lab-help lab-blocked">{icon("lock")}{e(content.DISABLED_REASON)}</p>')


def reset_button(**kwargs) -> None:
    """Clears the form; right after a reset it becomes the way back."""
    if "reset_backup" in st.session_state:  # set by state.reset_form; "undo" is the button's own key
        st.button(content.UNDO, type="tertiary", key="undo", on_click=state.undo_reset, icon=":material/undo:", **kwargs)
    else:
        st.button(content.RESET, type="tertiary", key="reset", on_click=state.reset_form, **kwargs)


def retry_button(**kwargs) -> None:
    st.button(content.RETRY, key="retry", on_click=state.submit, icon=":material/refresh:", **kwargs)


def view_tabs():
    """The three destinations as tabs. `?view=do-chinh-xac` opens a given one."""
    wanted = st.query_params.get("view")
    default = content.NAV[content.VIEW_IDS.index(wanted)] if wanted in content.VIEW_IDS else None
    return st.tabs(list(content.NAV), default=default)


# ---------------------------------------------------------------- markup


def table(headers: tuple[str, ...] | list[str], rows: list[list[str]], numeric_from: int = 1) -> str:
    def cls(index: int) -> str:
        return ' class="num"' if index >= numeric_from else ""

    head = "".join(f'<th scope="col"{cls(i)}>{e(h)}</th>' for i, h in enumerate(headers))
    body = "".join(
        "<tr>" + "".join(
            (f'<th scope="row">{e(cell)}</th>' if i == 0 else f"<td{cls(i)}>{e(cell)}</td>")
            for i, cell in enumerate(row)
        ) + "</tr>"
        for row in rows
    )
    return f'<div class="lab-table-wrap"><table class="lab-table"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def dl(rows: list[tuple[str, str]], cls: str = "") -> str:
    items = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in rows)
    return f'<dl class="lab-dl {cls}">{items}</dl>'


def bullets(items: tuple[str, ...] | list[str]) -> str:
    return '<ul class="lab-list">' + "".join(f"<li>{e(i)}</li>" for i in items) + "</ul>"


# ---------------------------------------------------------------- evaluation and data


def cv_rows(cv: CrossValidation) -> list[list[str]]:
    assert cv.summary is not None
    return [
        [str(r.model), fmt.number(r.mean_cv_MAE, 3, False), fmt.number(r.mean_cv_RMSE, 3, False),
         fmt.number(r.mean_cv_R2, 3, False)]
        for r in cv.summary.itertuples()
    ]


def cv_best(cv: CrossValidation) -> dict[str, str]:
    """The candidate with the lowest cross-validated MAE, straight from the file."""
    model, mae, rmse, r2 = cv_rows(cv)[0]
    return {"model": model, "mae": mae, "rmse": rmse, "r2": r2}


_DECIMAL_COMMA = "replace(format(datum.value, '.1f'), '.', ',')"
_THOUSANDS_DOT = "replace(format(datum.value, ',d'), ',', '.')"  # 1.800, as Vietnamese write it


def cv_chart(cv: CrossValidation, *, bar: str, text: str, row_height: int = 30,
             background: str | None = None, highlight: str | None = None) -> alt.Chart:
    """MAE per candidate. With `highlight`, the candidate cv_best() names gets that colour."""
    assert cv.summary is not None
    data = cv.summary.assign(label=[fmt.number(v, 3, False) for v in cv.summary["mean_cv_MAE"]])
    base = alt.Chart(data).encode(
        y=alt.Y("model:N", sort=None, title=None, axis=alt.Axis(labelLimit=240, ticks=False, domain=False)),
        x=alt.X("mean_cv_MAE:Q", title=content.EVAL_CHART_AXIS,
                scale=alt.Scale(domain=[0, float(data["mean_cv_MAE"].max()) * 1.18]),
                axis=alt.Axis(labelExpr=_DECIMAL_COMMA, tickCount=6)),
        tooltip=[alt.Tooltip("model:N", title="Ứng viên"), alt.Tooltip("label:N", title="MAE (tỷ đồng)")],
    )
    bars = base.mark_bar(size=row_height * 0.58)
    if highlight:
        best = cv_best(cv)["model"]
        bars = bars.encode(color=alt.condition(alt.datum.model == best, alt.value(highlight), alt.value(bar)))
    else:
        bars = bars.encode(color=alt.value(bar))
    labels = base.mark_text(align="left", dx=6, color=text, fontSize=13).encode(text="label:N")
    chart = (bars + labels).properties(height=row_height * len(data) + 44)
    return chart.configure(background=background) if background else chart


def price_hist_chart(reference: Reference, *, bar: str, height: int = 240,
                     background: str | None = None, band: str | None = None,
                     band_text: str | None = None) -> alt.Chart:
    """Training-split price histogram. With `band`, the middle half (Q1 to Q3) is shaded in that colour."""
    data = pd.DataFrame(reference.price_hist, columns=["lo", "hi", "count"])
    data["range"] = [f"{fmt.number(a)} – {fmt.number(b)} tỷ đồng" for a, b in zip(data["lo"], data["hi"])]
    data["count_text"] = [fmt.count(n) for n in data["count"]]
    chart = alt.Chart(data).mark_bar(color=bar).encode(
        x=alt.X("lo:Q", bin=alt.Bin(binned=True), title=content.DATA_HIST_X, axis=alt.Axis(labelExpr=_DECIMAL_COMMA)),
        x2="hi:Q",
        y=alt.Y("count:Q", title=content.DATA_HIST_Y, axis=alt.Axis(labelExpr=_THOUSANDS_DOT)),
        tooltip=[alt.Tooltip("range:N", title="Khoảng giá"), alt.Tooltip("count_text:N", title="Số căn")],
    ).properties(height=height)
    if band:
        p = reference.price
        middle = pd.DataFrame({"q1": [p["q1"]], "q3": [p["q3"]], "mid": [(p["q1"] + p["q3"]) / 2],
                               "label": [content.DATA_MIDDLE_LABEL]})
        x = alt.X("q1:Q", scale=alt.Scale(zero=False))  # keep the bars' axis; a rect would pull it to 0
        shade = alt.Chart(middle).mark_rect(color=band, opacity=0.22).encode(x=x, x2="q3:Q")
        note = alt.Chart(middle).mark_text(baseline="top", dy=4, fontSize=12, color=band_text or band).encode(
            x=alt.X("mid:Q", scale=alt.Scale(zero=False)), y=alt.value(0), text="label:N")
        chart = alt.layer(shade, chart, note).properties(height=height)
    return chart.configure(background=background) if background else chart


def data_facts(reference: Reference) -> list[tuple[str, str]]:
    p = reference.price
    return [
        (content.DATA_FACTS["source"], content.DATA_SOURCE),
        (content.DATA_FACTS["rows"], fmt.count(reference.n_rows)),
        (content.DATA_FACTS["range"], content.DATA_RANGE.format(low=fmt.number(p["min"]), high=fmt.number(p["max"]))),
        (content.DATA_FACTS["middle"], content.DATA_RANGE.format(low=fmt.number(p["q1"]), high=fmt.number(p["q3"]))),
    ]


def missing_rows(reference: Reference) -> list[list[str]]:
    """Fields that are missing in at least 1% of training rows, most-missing first."""
    rows = [(spec.label, reference.missing.get(spec.name, 0.0)) for spec in FIELDS]
    return [[label, fmt.percent(share)] for label, share in sorted(rows, key=lambda r: -r[1]) if share >= 0.01]


def eval_copy(cv: CrossValidation) -> dict[str, str]:
    """Sentences for the accuracy view that depend on the files found."""
    from .evaluation import CV_SUMMARY_LABEL

    copy = {"folds": "", "source": content.EVAL_SOURCE.format(path=CV_SUMMARY_LABEL)}
    if cv.status == "available" and cv.n_folds:
        copy["folds"] = content.EVAL_CV_FOLDS.format(k=cv.n_folds)
    return copy


def reference_guard(reference: Reference) -> None:
    """Stop with a plain message when the reference data cannot be read."""
    if not reference.ok:
        st.error(content.DATA_PROBLEM.format(problem=reference.problem), icon=":material/error:")
        st.html('<div id="lab-ready"></div>')
        st.stop()


# ---------------------------------------------------------------- lab controls


def lab_panel(view: state.Page) -> None:
    """Reviewer controls, only with ?lab=1: they are not part of the product."""
    if st.query_params.get("lab") == "1":
        with st.expander("Công cụ phòng thiết kế (không thuộc giao diện sản phẩm)", icon=":material/construction:"):
            st.selectbox("Trạng thái giao diện để xem", list(state.LAB_STATES), key="lab_state",
                         format_func=lambda k: state.LAB_STATES[k][0], on_change=state.apply_preset)
            st.button("Điền căn nhà mẫu", key="lab_fill", on_click=state.fill_sample)
            st.caption(f"Trạng thái mô hình: {view.model_reason}")
    st.html('<div id="lab-ready"></div>')
