"""Building blocks every prototype uses, with no look of their own.

Widgets here carry the shared keys and behaviour. Markup helpers emit plain
semantic HTML with `lab-` class names, which each concept styles in its own CSS.
"""
from __future__ import annotations

import html

import altair as alt
import pandas as pd
import streamlit as st
from streamlit import config

from . import content, formatting as fmt, schema, state
from .evaluation import CrossValidation
from .reference import Reference
from .schema import FIELDS, UNKNOWN, Field

# Prototype-only technique: each concept sets its theme from inside the script,
# so `streamlit run design_lab/concept_x.py` needs no flags. A production app
# would put these options in .streamlit/config.toml instead.
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
[data-testid="stNumberInputField"],input[role="combobox"],[data-testid="stRadioOption"] p,[data-testid="stTab"] p{font-size:1rem}
[data-testid="stNumberInputContainer"],.react-aria-ComboBox>[role="group"]{min-height:2.75rem}
.lab-dl>div{display:flex;justify-content:space-between;gap:1.25rem;padding:.3rem 0}
.lab-dl dt,.lab-dl dd{margin:0}
.lab-dl dd{text-align:right}
.lab-list{margin:0;padding-left:1.15rem}
.lab-list li{margin:.3rem 0}
button:focus-visible,[role="tab"]:focus-visible{outline:3px solid var(--lab-focus,currentColor);outline-offset:2px}
[data-testid="stHtml"] p,[data-testid="stHtml"] li{overflow-wrap:anywhere}
[data-testid="stButtonGroup"] [role="radiogroup"]{flex-wrap:wrap;row-gap:.35rem}
@media (max-width:640px){[role="tablist"]{flex-wrap:wrap;overflow:visible;row-gap:.25rem}}
"""


def apply_theme(options: dict[str, object], css: str) -> None:
    """Set this concept's theme options, then add its CSS. Call right after set_page_config."""
    changed = False
    for key, value in {**BASE_OPTIONS, **options}.items():
        if config.get_option(key) != value:
            config.set_option(key, value)
            changed = True
    if changed and not st.session_state.get("_theme_applied"):
        st.session_state["_theme_applied"] = True
        st.rerun()  # the theme is sent to the browser at the start of a run
    st.html(f"<style>{BASE_CSS}{css}</style>")


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
                     placeholder=spec.placeholder if city else "Chọn tỉnh / thành phố trước")
    elif spec.kind == "decimal":
        st.number_input(label, value=None, step=0.1, format="%.1f", placeholder=spec.placeholder, key=spec.key)
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
        unit = f" {spec.unit}" if spec.unit else ""
        notes.append(
            f'<p class="lab-help">{e(content.RANGE_HELP.format(low=fmt.number(low), high=fmt.number(high), unit=unit))}</p>'
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
    items = "".join(
        f"<li><strong>{e(spec.label)}:</strong> {e(view.errors[spec.name])}</li>"
        for spec in FIELDS if spec.name in view.errors
    )
    heading = content.SUMMARY_HEADING.format(n=len(view.errors))
    st.html(
        f'<div class="lab-summary" role="alert">{icon("error")}'
        f'<div><p class="lab-summary-h"><strong>{e(heading)}</strong></p><ul>{items}</ul></div></div>'
    )


def banner(view: state.Page) -> None:
    """System banner: model unavailable, or lab preview mode."""
    if view.blocked:
        kind, name, text = "unavailable", "cloud_off", content.BANNER_UNAVAILABLE
    elif view.preview:
        kind, name, text = "preview", "science", content.BANNER_PREVIEW
    else:
        return
    st.html(f'<div class="lab-banner lab-banner--{kind}" role="status">{icon(name)}<p>{e(text)}</p></div>')


def submit_button(view: state.Page, **kwargs) -> None:
    st.button(content.SUBMIT, type="primary", key="submit", on_click=state.submit, disabled=view.blocked, **kwargs)


def blocked_note(view: state.Page) -> None:
    """Says why the action is disabled, so the button is never silently inert."""
    if view.blocked:
        st.html(f'<p class="lab-help lab-blocked">{icon("lock")}{e(content.DISABLED_REASON)}</p>')


def reset_button(**kwargs) -> None:
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


def cv_chart(cv: CrossValidation, *, bar: str, text: str, row_height: int = 30,
             background: str | None = None) -> alt.Chart:
    assert cv.summary is not None
    data = cv.summary.assign(label=[fmt.number(v, 3, False) for v in cv.summary["mean_cv_MAE"]])
    base = alt.Chart(data).encode(
        y=alt.Y("model:N", sort=None, title=None, axis=alt.Axis(labelLimit=240, ticks=False, domain=False)),
        x=alt.X("mean_cv_MAE:Q", title=content.EVAL_CHART_AXIS,
                scale=alt.Scale(domain=[0, float(data["mean_cv_MAE"].max()) * 1.18]),
                axis=alt.Axis(labelExpr=_DECIMAL_COMMA, tickCount=6)),
        tooltip=[alt.Tooltip("model:N", title="Ứng viên"), alt.Tooltip("label:N", title="MAE (tỷ đồng)")],
    )
    bars = base.mark_bar(color=bar, size=row_height * 0.58)
    labels = base.mark_text(align="left", dx=6, color=text, fontSize=13).encode(text="label:N")
    chart = (bars + labels).properties(height=row_height * len(data) + 44)
    return chart.configure(background=background) if background else chart


def price_hist_chart(reference: Reference, *, bar: str, height: int = 240,
                     background: str | None = None) -> alt.Chart:
    data = pd.DataFrame(reference.price_hist, columns=["lo", "hi", "count"])
    data["range"] = [f"{fmt.number(a)} – {fmt.number(b)} tỷ đồng" for a, b in zip(data["lo"], data["hi"])]
    chart = alt.Chart(data).mark_bar(color=bar).encode(
        x=alt.X("lo:Q", bin=alt.Bin(binned=True), title=content.DATA_HIST_X, axis=alt.Axis(labelExpr=_DECIMAL_COMMA)),
        x2="hi:Q",
        y=alt.Y("count:Q", title=content.DATA_HIST_Y),
        tooltip=[alt.Tooltip("range:N", title="Khoảng giá"), alt.Tooltip("count:Q", title="Số căn")],
    ).properties(height=height)
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

    copy = {"folds": "", "best": "", "source": content.EVAL_SOURCE.format(path=CV_SUMMARY_LABEL)}
    if cv.status == "available":
        copy["best"] = content.EVAL_BEST.format(model=cv_best(cv)["model"])
        if cv.n_folds:
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
    """Reviewer controls. Same in every prototype, and not part of the product design."""
    with st.expander("Công cụ phòng thiết kế (không thuộc giao diện sản phẩm)", icon=":material/construction:"):
        st.selectbox("Trạng thái giao diện để xem", list(state.LAB_STATES), key="lab_state",
                     format_func=lambda k: state.LAB_STATES[k][0], on_change=state.apply_preset)
        st.button("Điền căn nhà mẫu", key="lab_fill", on_click=state.fill_sample)
        st.caption(f"Mô hình thật: {view.model_reason} Mọi con số giá trong phòng thiết kế là dữ liệu mẫu.")
    st.html('<div id="lab-ready"></div>')
