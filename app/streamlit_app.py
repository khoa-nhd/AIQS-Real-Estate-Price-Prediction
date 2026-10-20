"""#REP — Vietnamese house price estimator (Streamlit app).

Run from the repository root:
    streamlit run app/streamlit_app.py

The look is the chosen design_01 direction (bento, night violet, mint actions);
its source is design_references/design_01/ (design_spec.md, design_tokens.json).
Theme, layout and markup live here; behaviour comes from app/core.
"""
import sys
from bisect import bisect_left
from pathlib import Path
from string import Template

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))  # so `core` imports however Streamlit is started

import streamlit as st  # noqa: E402

from core import content, formatting as fmt, schema, state, widgets as ui  # noqa: E402
from core.evaluation import load_cross_validation, load_final_evaluation  # noqa: E402

TOKENS = dict(
    GUTTER="#030208", GROUND="#0C0E1D", PANEL_TOP="#151329", PANEL_BOTTOM="#0A121F",
    TEXT="#F2F2F7", MUTED="#A3A2C7", BORDER="#6A6990",
    MINT="#51FAAA", ACTIVE_FILL="#284648", PINK="#FF81FF", TEAL="#51C892",
    # status colours added by the colour pass; the reference has none of its own
    AMBER="#FFC46B", CORAL="#FF8A7A",
)

THEME = {
    "theme.base": "dark",
    "theme.primaryColor": TOKENS["MINT"],
    "theme.backgroundColor": TOKENS["GUTTER"],
    "theme.secondaryBackgroundColor": TOKENS["GROUND"],
    "theme.textColor": TOKENS["TEXT"],
    "theme.borderColor": TOKENS["BORDER"],
    "theme.linkColor": TOKENS["MINT"],
    "theme.font": "'Exo 2':https://fonts.googleapis.com/css2?family=Exo+2:wght@400;500;600;700&display=swap",
    "theme.baseFontSize": 16,
    "theme.baseRadius": "0.625rem",
}

CSS = Template((HERE / "styles.css").read_text(encoding="utf-8")).substitute(TOKENS)
# location: city | district, ward | street, project
LAYOUT = {"location": [[1, 1], [1, 1], [1]], "size": 3, "structure": 3, "extra": [[1, 1], [1], [1]]}


def ring(view: state.Page) -> str:
    """A gauge for a real quantity: how many required fields are filled."""
    required = [spec for spec in schema.FIELDS if spec.required]
    done = sum(view.values.get(spec.name) is not None for spec in required)
    deg = round(360 * done / len(required))
    # The arc sweeps from the fill it showed last run (styles.css draws it from --deg and animates from --from).
    previous = st.session_state.get("ring_deg", deg)
    st.session_state["ring_deg"] = deg
    return (
        '<div class="d1-ring">'
        f'<div class="d1-ring-arc" style="--deg:{deg}deg;--from:{previous}deg" role="img" '
        f'aria-label="Đã điền {done} trên {len(required)} mục bắt buộc"></div>'
        f'<div><p class="d1-ring-n">{done}/{len(required)}</p><p class="d1-k">mục bắt buộc đã điền</p>'
        # which optional fields are «Không rõ» matters once someone is filling in; on an empty form it is a list of everything
        + (f'<p class="d1-small">{ui.e(state.unknown_note(view.values))}</p>' if done else "") + "</div></div>"
    )


def bands(values: dict) -> str:
    """The entered property as banded rows, after the reference's swatch panel."""
    def value(name: str) -> str:
        return dict(state.recap(values))[schema.BY_NAME[name].label]

    location = ", ".join(str(v) for v in (values.get("Street"), values.get("Ward"), values.get("District"),
                                          values.get("City")) if v) or schema.UNKNOWN
    # whole words, not listing shorthand (PN, PT); counts the person left unknown are simply not listed
    # each count stays whole ("2\u00a0phòng\u00a0ngủ"); the line may break only between them, at " · "
    structure = " · ".join(f"{fmt.count(int(values[n]))}\u00a0{label}".replace(" ", "\u00a0") for n, label in
                           (("Floors", "tầng"), ("Bedrooms", "phòng ngủ"), ("Bathrooms", "phòng tắm"))
                           if values.get(n) is not None) or schema.UNKNOWN
    rows = [("Vị trí", location), ("Diện tích", value("Area")), ("Kết cấu", structure), ("Pháp lý", value("Legal status"))]
    return '<div class="d1-bands">' + "".join(
        f'<div class="d1-band"><span>{ui.e(k)}</span><span>{ui.e(v)}</span></div>' for k, v in rows
    ) + "</div>"


def market(price_ty: float, reference) -> str:
    """Where this estimate sits among the training prices: the real histogram, a pin, and one sentence
    saying what share of the houses cost less. No second pair of numbers sits next to the price.

    The pin starts from the estimate shown before this one (styles.css animates from --from-pin), so a new
    estimate visibly moves from the old one along the market.
    """
    bins, p = reference.price_hist, reference.price
    lo, hi = bins[0][0], bins[-1][1]

    def at(x: float) -> float:
        return max(0.0, min(100.0, (x - lo) / (hi - lo) * 100))

    pin = at(price_ty)
    previous = st.session_state.get("market_pin", 0.0)
    st.session_state["market_pin"] = pin
    share = bisect_left(reference.price_sorted, price_ty) / len(reference.price_sorted)
    if price_ty < p["min"] or price_ty > p["max"]:
        note = content.MARKET_OUTSIDE.format(low=fmt.number(p["min"]), high=fmt.number(p["max"]))
    elif share < 0.005:
        note = content.MARKET_LOWEST
    else:
        note = content.MARKET_SHARE.format(pct=fmt.percent(share))
    label = content.MARKET_LABEL.format(n=fmt.count(reference.n_rows))
    top = max(n for _, _, n in bins)
    last = len(bins) - 1
    cells = "".join(
        f'<span class="d1-bin{" d1-bin--hit" if a <= price_ty < b or (k == last and price_ty == b) else ""}" '
        f'style="--h:{n / top * 100:.1f}%" '
        f'title="{ui.e(content.MARKET_BIN.format(low=fmt.number(a), high=fmt.number(b), n=fmt.count(n)))}"></span>'
        for k, (a, b, n) in enumerate(bins)
    )
    return (
        f'<div class="d1-market"><p class="d1-k">{ui.e(label)}</p>'
        f'<div class="d1-market-plot" role="img" aria-label="{ui.e(label)}. {ui.e(note)}." '
        f'style="--pin:{pin:.2f}%;--from-pin:{previous:.2f}%">'
        f'<div class="d1-market-bars">{cells}</div><div class="d1-market-pin"></div></div>'
        # the axis names the data's real lowest and highest prices, at their places (the last bin runs past the max)
        f'<div class="d1-market-axis"><span style="left:{at(p["min"]):.2f}%">{ui.e(content.MARKET_AXIS.format(value=fmt.number(p["min"])))}</span>'
        f'<span style="right:{100 - at(p["max"]):.2f}%">{ui.e(content.MARKET_AXIS.format(value=fmt.number(p["max"])))}</span></div>'
        f'<p class="d1-market-note">{ui.e(note)}</p></div>'
    )


def result_panel(view: state.Page, reference) -> None:
    slots = state.result_slots(view, reference)
    kind = slots["kind"]
    arrived = st.session_state.pop("arrived", False)
    if arrived:  # a new id, so a repeated identical result is announced again
        st.session_state["announce_n"] = st.session_state.get("announce_n", 0) + 1
    with st.container(key=f"panel_result_{kind}"):
        # amber for things the person should check; pink only for the lab's simulated state
        flagged = [(slots["stale"], ""), (slots["simulated"], " d1-note--lab"), *((w, "") for w in slots["warnings"])]
        notes = "".join(f'<p class="d1-note{cls}">{ui.icon("warning")}{ui.e(t)}</p>' for t, cls in flagged if t)
        if kind not in ("sample", "result"):
            # no estimate on screen: the next one's pin travels from the strip's start
            st.session_state.pop("market_pin", None)
            # an invalid form is announced by its error summary (role="alert"); other outcomes by a11y.js
            say = (f' data-announce="{ui.e(slots["heading"])}. {ui.e(slots["body"])}" '
                   f'data-announce-id="{st.session_state.get("announce_n", 0)}"' if arrived and kind != "invalid" else "")
            st.html(f'<div{say}>{notes}<h2 class="d1-state-h">{ui.icon(slots["icon"])}{ui.e(slots["heading"])}</h2>'
                    f'<p class="d1-p">{ui.e(slots["body"])}</p></div>')
            if kind == "error":
                ui.retry_button()
            return
        # Reading order answers the person's questions in turn: what is the price, what kind of number is it,
        # how far can I trust it (range, then the recorded average error), where does it come from, and
        # how does it compare with the data. d1-arrive plays the arrival once, right after someone asked.
        absent = " d1-absent" if slots["uncertainty"] == content.UNCERTAINTY_NONE else ""
        price_ty = view.outcome.prediction.price_ty
        said = f'{slots["heading"]}: {slots["price"]} {slots["unit"]}, {slots["words"]}. {slots["tag"]}.'
        say = (f' data-announce="{ui.e(said)}" data-announce-id="{st.session_state.get("announce_n", 0)}"'
               if arrived else "")
        st.html(
            f'<div class="d1-result{" d1-arrive" if arrived else ""}"{say}>'
            f'<p class="d1-tag">{ui.icon(slots["icon"])}{ui.e(slots["tag"])}</p>{notes}'
            f'<h2 class="d1-k">{ui.e(slots["heading"])}</h2>'
            f'<p class="d1-price">{ui.e(slots["price"])}<span class="d1-unit">{ui.e(slots["unit"])}</span></p>'
            f'<p class="d1-words">{ui.e(slots["words"])}</p>'
            f'<p class="d1-small d1-statement">{ui.e(slots["statement"])}</p>'
            '<div class="d1-facts">'
            f'<div><p class="d1-k">{ui.e(slots["uncertainty_label"])}</p><p class="d1-fact-v{absent}">{ui.e(slots["uncertainty"])}</p>'
            f'<p class="d1-small">{ui.e(slots["uncertainty_text"])}</p></div>'
            + trust() +
            f'<div class="d1-fact--wide"><p class="d1-k">{ui.e(slots["provenance_label"])}</p><p class="d1-small">{ui.e(slots["provenance"])}</p></div>'
            "</div>"
            + market(price_ty, reference) +
            "</div>"
        )


def trust() -> str:
    """The model's average error on the test split, read from the team's results file."""
    final = load_final_evaluation()
    if final.status != "available":
        return (f'<div><p class="d1-k">{ui.e(content.TRUST_LABEL)}</p><p class="d1-fact-v d1-absent">{ui.e(content.TRUST_NONE)}</p>'
                f'<p class="d1-small">{ui.e(content.TRUST_NONE_TEXT)}</p></div>')
    mae = final.test["MAE"]
    return (f'<div><p class="d1-k">{ui.e(content.TRUST_LABEL)}</p>'
            f'<p class="d1-fact-v">{ui.e(content.TRUST_VALUE.format(mae=fmt.number(mae, 2, trim=False)))}</p>'
            f'<p class="d1-small">{ui.e(content.TRUST_TEXT.format(n=fmt.count(final.test_rows)))}</p></div>')


def page_head(title: str, lead: str) -> None:
    """Each view opens with its title at display size, set on the ground rather than in a panel."""
    st.html(f'<header class="d1-head"><h1 class="d1-h1">{ui.e(title)}</h1><p class="d1-lead">{ui.e(lead)}</p></header>')


def valuation(view: state.Page, reference) -> None:
    ui.banner(view)  # preview and model notices are about this tab's prices; the other tabs show real figures
    page_head(content.TITLE, content.LEAD)
    form, out = st.columns([2.1, 2], gap="small")
    with form:
        with st.container(key="panel_form"):
            ui.error_summary(view)
            for i, (group, label) in enumerate(schema.GROUPS.items()):
                st.html(f'<h2 class="d1-h2{" d1-h2--first" if i == 0 else ""}">{ui.e(label)}</h2>')
                ui.fields(group, view, reference, LAYOUT[group], gap="small")
            st.html(f'<p class="lab-help">{ui.e(content.REQUIRED_LEGEND)}</p>')
            # how complete the form is belongs next to the button it gates, not beside the answer
            st.html(ring(view))
            with st.container(key="actions", horizontal=True, vertical_alignment="center"):
                ui.submit_button(view)
                ui.reset_button()
            ui.blocked_note(view)
    with out:
        # the right half holds the answer and nothing else; it follows the form while the page scrolls
        with st.container(key="result_column"):
            result_panel(view, reference)
        # what the estimate was based on: on a phone the form is far above, so it is repeated here;
        # side by side (styles.css hides it) the form itself is the record
        if view.kind in ("sample", "result"):
            with st.container(key="panel_summary"):
                st.html(f'<p class="d1-k">{ui.e(content.RECAP_LABEL)}</p>' + bands(view.outcome.snapshot))


def evaluation(reference) -> None:
    """For the public: how far off the estimates run, and the final test result. For the team (behind a
    disclosure): every measurement of the model in use, the candidate comparison and the source files."""
    final = load_final_evaluation()
    cv = load_cross_validation()
    copy = ui.eval_copy(cv)
    page_head(content.NAV[1], content.EVAL_INTRO)
    answer, status = st.columns([2.1, 2], gap="small")
    with status:
        with st.container(key="panel_final"):
            if final.status == "available":
                verdict = content.EVAL_FINAL_PASS if final.passed else content.EVAL_FINAL_FAIL
                st.html(f'<p class="d1-k">{ui.e(content.EVAL_FINAL_LABEL)}</p>'
                        f'<p class="d1-ring-n">{ui.e(content.EVAL_FINAL_VALUE.format(r2=fmt.number(final.test["R2"], 3, trim=False)))}</p>'
                        f'<p class="d1-small">{ui.e(content.EVAL_FINAL_TEXT.format(n=fmt.count(final.test_rows), verdict=verdict))}</p>')
            else:
                st.html(f'<p class="d1-k">{ui.e(content.EVAL_FINAL_LABEL)}</p><p class="d1-ring-n d1-absent">{ui.e(content.EVAL_NO_FINAL)}</p>'
                        f'<p class="d1-small">{ui.e(final.problem or content.EVAL_NO_FINAL_TEXT)}</p>')
    with answer:
        with st.container(key="panel_answer"):
            if final.status != "available":
                st.html(f'<p class="d1-k">{ui.e(content.TRUST_LABEL)}</p><p class="d1-figure d1-absent">{ui.e(content.TRUST_NONE)}</p>'
                        f'<p class="d1-p">{ui.e(final.problem or content.EVAL_MISSING)}</p>')
            else:
                mae, median = final.test["MAE"], reference.price["median"]
                mae_text = fmt.number(mae, 2, trim=False)
                note = content.ACC_NOTE.format(twin=fmt.percent(final.twin_share),
                                               mae_new=fmt.number(final.test_new.get("MAE", mae), 2, trim=False))
                st.html(f'<p class="d1-k">{ui.e(content.TRUST_LABEL)}</p>'
                        f'<p class="d1-figure">{ui.e(content.TRUST_VALUE.format(mae=mae_text))}</p>'
                        f'<p class="d1-p d1-measure">{ui.e(content.ACC_TEXT.format(n=fmt.count(final.test_rows), mae=mae_text, median=fmt.price(median), share=fmt.percent(mae / median)))}</p>'
                        f'<p class="d1-small">{ui.e(note)}</p>')
    if cv.status != "available" or cv.summary is None or cv.summary.empty:
        return
    # every measurement of the model in use, then the course's candidate comparison, one click away
    with st.expander(content.TEAM_DETAILS.format(n=len(cv.summary)), icon=":material/table_chart:"):
        with st.container(key="cv_detail"):  # not a panel: the expander is already the container
            if final.status == "available":
                rows = [[content.EVAL_MODEL_ROWS[k], fmt.number(m["MAE"], 3, False), fmt.number(m["RMSE"], 3, False),
                         fmt.number(m["R2"], 3, False)]
                        for k, m in (("cv", final.cv), ("validation", final.validation), ("test", final.test),
                                     ("test_new", final.test_new)) if m]
                st.html(f'<h2 class="d1-h2" style="margin-top:0">{ui.e(content.EVAL_MODEL_HEADING)}</h2>'
                        + '<div class="d1-model-table">' + ui.table(content.EVAL_MODEL_COLUMNS, rows) + "</div>"
                        + f'<p class="d1-small">{ui.e(content.EVAL_SOURCE.format(path=content.EVAL_MODEL_SOURCE))}</p>')
            st.html(f'<h2 class="d1-h2">{ui.e(content.EVAL_CV_HEADING)}</h2>'
                    f'<p class="d1-small">{ui.e(content.EVAL_CV_KIND)} {ui.e(copy["folds"])}</p>')
            # teal marks the lowest-error candidate in the chart and its row in the table
            st.altair_chart(ui.cv_chart(cv, bar=TOKENS["BORDER"], highlight=TOKENS["TEAL"], text=TOKENS["TEXT"],
                                        row_height=34, background="transparent"), width="stretch")
            st.html(ui.table(content.EVAL_COLUMNS, ui.cv_rows(cv))
                    + "".join(f'<p class="d1-small"><strong>{ui.e(k)}</strong>: {ui.e(v)}</p>' for k, v in content.METRIC_HELP)
                    + f'<p class="d1-small">{ui.e(copy["source"])}</p>')


def data(reference) -> None:
    page_head(content.NAV[2], content.DATA_INTRO)
    wide, narrow = st.columns([2.1, 2], gap="small")
    # left: the price distribution and the limits on reading it; right: what the dataset holds and what it lacks
    with wide:
        with st.container(key="stack_data_main"):
            with st.container(key="panel_hist"):
                st.html(f'<h2 class="d1-h2" style="margin-top:0">{ui.e(content.DATA_HIST_HEADING)}</h2>')
                st.altair_chart(ui.price_hist_chart(reference, bar=TOKENS["TEAL"], background="transparent", height=330,
                                                    band=TOKENS["MUTED"], band_text=TOKENS["MUTED"]), width="stretch")
            with st.container(key="panel_limits"):
                st.html(f'<p class="d1-k">{ui.e(content.DATA_LIMITS_HEADING)}</p>' + ui.bullets(content.DATA_LIMITS))
    with narrow:
        with st.container(key="stack_data_side"):
            with st.container(key="panel_facts"):
                st.html('<div class="d1-bands d1-bands--flush">' + "".join(
                    f'<div class="d1-band"><span>{ui.e(k)}</span><span>{ui.e(v)}</span></div>'
                    for k, v in ui.data_facts(reference)) + "</div>")
            with st.container(key="panel_missing"):
                st.html(f'<p class="d1-k">{ui.e(content.DATA_MISSING_HEADING)}</p>'
                        + ui.table(content.DATA_MISSING_COLUMNS, ui.missing_rows(reference)))


st.set_page_config(page_title=content.TITLE, layout="wide")
ui.apply_theme(THEME, CSS)
ui.enhance_accessibility()
reference = state.bootstrap()
ui.reference_guard(reference)
view = state.page(reference)

tab_valuation, tab_evaluation, tab_data = ui.view_tabs()
with tab_valuation:
    valuation(view, reference)
with tab_evaluation:
    evaluation(reference)
with tab_data:
    data(reference)
ui.lab_panel(view)
