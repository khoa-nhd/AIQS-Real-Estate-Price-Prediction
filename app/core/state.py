"""Session state and the submit flow, identical for every variant.

The app runs on the real model by default. The lab switch (shown with ?lab=1)
keeps the design-review states: it selects which gateway scenario runs and
which preset fills the form.
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass, field

import streamlit as st

from . import content, formatting as fmt, schema
from .model_interface import InferenceError, ModelUnavailable, Prediction, gateway_for
from .reference import Reference, load_reference
from .schema import FIELDS, UNKNOWN
from .validation import validate

# Lab state -> (label, gateway scenario, form preset)
LAB_STATES: dict[str, tuple[str, str, dict[str, object]]] = {
    "real": ("Mô hình thật (mặc định)", "project", {}),
    "real_sample": ("Mô hình thật với căn nhà mẫu", "project", schema.SAMPLE_PROPERTY),
    "invalid": ("Dữ liệu chưa hợp lệ", "project", schema.INVALID_PROPERTY),
    "sample": ("Kết quả mẫu (xem trước, không chạy mô hình)", "preview", schema.SAMPLE_PROPERTY),
    "unavailable": ("Mô hình chưa sẵn sàng (mô phỏng)", "unavailable", schema.SAMPLE_PROPERTY),
    "error": ("Lỗi khi ước tính (mô phỏng)", "error", schema.SAMPLE_PROPERTY),
}
DEFAULT_STATE = "real"


@dataclass
class Outcome:
    kind: str = "initial"  # initial | invalid | unavailable | sample | result | error
    snapshot: dict[str, object] = field(default_factory=dict)
    prediction: Prediction | None = None
    warnings: dict[str, str] = field(default_factory=dict)


@dataclass
class Page:
    """Everything a variant needs to draw the current state."""

    values: dict[str, object]
    errors: dict[str, str]  # live blocking errors, shown only after a submit attempt
    outcome: Outcome
    kind: str  # outcome kind, or "fixed" once every error has been corrected
    stale: bool
    preview: bool  # lab preview mode: sample figures, never a real prediction
    blocked: bool  # the real model is unavailable and no preview is running
    simulated: bool  # the outcome was produced by a simulated failure
    model_reason: str


def _to_widget(spec: schema.Field, value: object) -> object:
    if spec.kind in ("direction", "choice", "street", "project"):
        return UNKNOWN if value is None else value
    if spec.kind == "count" and value is not None:
        return int(value)
    if spec.kind == "decimal":  # typed text, written the Vietnamese way ("4,1")
        return "" if value is None else fmt.number(float(value), 1)
    return value


def parse_decimal(text: object) -> object:
    """A typed decimal: comma or point ("4,1" or "4.1"), spaces and a trailing unit (m, m2, m²) allowed.
    Empty is None (not filled). Text that is not a number comes back unchanged, so validation can say so."""
    if text is None or isinstance(text, (int, float)):
        return None if text is None else float(text)
    raw = str(text).strip()
    cleaned = re.sub(r"(m²|m2|m)$", "", raw.lower().replace(" ", "")).replace(",", ".")
    if not cleaned:
        return None
    try:
        number = float(cleaned)
    except ValueError:
        return raw
    return number if math.isfinite(number) else raw


def read_values() -> dict[str, object]:
    """Current form values keyed by dataset field name. Unknown is None; an unreadable decimal is its text."""
    values: dict[str, object] = {}
    for spec in FIELDS:
        value = st.session_state.get(spec.key)
        if spec.kind == "decimal":
            values[spec.name] = parse_decimal(value)
        else:
            values[spec.name] = None if value in (None, UNKNOWN) else value
    return values


def _fill(values: dict[str, object]) -> None:
    for spec in FIELDS:
        st.session_state[spec.key] = _to_widget(spec, values.get(spec.name))


def scenario() -> str:
    return LAB_STATES[st.session_state["lab_state"]][1]


def submit() -> None:
    """Validate, then ask the gateway. Used as the primary button's callback."""
    ss = st.session_state
    reference = load_reference()
    values = read_values()
    errors, warnings = validate(values, reference)
    ss.pop("reset_backup", None)  # a new estimate replaces what a reset could bring back
    ss["attempted"] = True
    ss["arrived"] = True  # a person asked for an estimate: the next run may mark the answer's arrival
    if errors:
        ss["outcome"] = Outcome("invalid", values)
        return
    try:
        prediction = gateway_for(scenario(), reference).predict(values)
    except ModelUnavailable:
        ss["outcome"] = Outcome("unavailable", values)
    except InferenceError:
        ss["outcome"] = Outcome("error", values)
    else:
        ss["outcome"] = Outcome("sample" if prediction.is_sample else "result", values, prediction, warnings)


def apply_preset() -> None:
    """Fill the form and reach the chosen lab state. Callback of the lab switch."""
    ss = st.session_state
    preset = LAB_STATES[ss["lab_state"]][2]
    _fill(preset)
    ss["attempted"] = False
    ss["outcome"] = Outcome("initial")
    if not gateway_for(scenario(), load_reference()).status().available:
        ss["outcome"] = Outcome("unavailable")
    elif preset:  # an empty form waits for the person; a filled preset shows its outcome
        submit()
        ss.pop("arrived", None)  # a preset is not someone asking; it should not play the arrival


def reset_form() -> None:
    """Clear the form, keeping what was there so one click can bring it back (reset sits next to submit)."""
    ss = st.session_state
    if any(ss.get(spec.key) not in (None, "", UNKNOWN) for spec in FIELDS):
        ss["reset_backup"] = ({spec.key: ss.get(spec.key) for spec in FIELDS}, ss.get("outcome"), ss.get("attempted", False))
    _fill({})
    ss["attempted"] = False
    available = gateway_for(scenario(), load_reference()).status().available
    ss["outcome"] = Outcome("initial" if available else "unavailable")


def undo_reset() -> None:
    """Put back the form, result and error state the last reset cleared."""
    ss = st.session_state
    if "reset_backup" not in ss:
        return
    widgets, outcome, attempted = ss.pop("reset_backup")
    for key, value in widgets.items():
        ss[key] = value
    ss["outcome"], ss["attempted"] = outcome, attempted


def fill_sample() -> None:
    _fill(schema.SAMPLE_PROPERTY)


def _clear(names: tuple[str, ...]) -> None:
    for name in names:
        spec = schema.BY_NAME[name]
        st.session_state[spec.key] = _to_widget(spec, None)


def city_changed() -> None:
    """A new city: its districts, wards, streets and projects are different lists."""
    _clear(schema.LOCATION_DETAIL)


def district_changed() -> None:
    _clear(schema.ADDRESS_FIELDS)


def bootstrap() -> Reference:
    """Call once per run, before any widget. Returns the reference data."""
    ss = st.session_state
    if "lab_state" not in ss:
        wanted = st.query_params.get("state", DEFAULT_STATE)
        ss["lab_state"] = wanted if wanted in LAB_STATES else DEFAULT_STATE
        apply_preset()
    return load_reference()


def page(reference: Reference) -> Page:
    ss = st.session_state
    values = read_values()
    outcome: Outcome = ss["outcome"]
    errors = validate(values, reference)[0] if ss.get("attempted") else {}
    kind = outcome.kind
    if kind == "invalid" and not errors:
        kind = "fixed"
    model_status = gateway_for(scenario(), reference).status()
    preview = scenario() in ("preview", "error")  # sample figures or a simulated failure, never the real model
    return Page(
        values=values,
        errors=errors,
        outcome=outcome,
        kind=kind,
        stale=kind in ("sample", "result", "error") and outcome.snapshot != values,
        preview=preview,
        blocked=not model_status.available,
        simulated=scenario() == "error" and kind == "error",
        model_reason=model_status.reason,
    )


def recap(values: dict[str, object]) -> list[tuple[str, str]]:
    """The inputs as label/value pairs, in schema order."""
    rows: list[tuple[str, str]] = []
    for spec in FIELDS:
        value = values.get(spec.name)
        if value is None:
            rows.append((spec.label, UNKNOWN))
        elif spec.kind in ("decimal", "count"):
            unit = f" {spec.unit}" if spec.unit else ""
            rows.append((spec.label, f"{fmt.number(float(value))}{unit}"))
        else:
            rows.append((spec.label, schema.display_value(spec, value)))
    return rows


def unknown_note(values: dict[str, object]) -> str:
    """Optional fields left as unknown. Missing required fields are errors, not unknowns."""
    names = [spec.label for spec in FIELDS if not spec.required and values.get(spec.name) is None]
    if not names:
        return content.UNKNOWN_NONE
    return content.UNKNOWN_SOME.format(n=len(names), names=", ".join(names))


def result_slots(view: Page, reference: Reference) -> dict[str, object]:
    """The text of the result panel, slot by slot. Variants only lay it out."""
    kind = view.kind
    slots: dict[str, object] = {
        "kind": kind,
        "icon": content.STATE_ICON[kind],
        "stale": content.STALE if view.stale else "",
        "simulated": content.SIMULATED_NOTE if view.simulated else "",
        "warnings": list(view.outcome.warnings.values()),
    }
    if kind not in ("sample", "result"):
        heading, body = content.STATE_TEXT[kind]
        slots.update(heading=heading, body=body)
        return slots

    prediction = view.outcome.prediction
    assert prediction is not None
    sample = prediction.is_sample
    snapshot = view.outcome.snapshot
    if prediction.interval:
        low, high, coverage = prediction.interval
        uncertainty = content.UNCERTAINTY_INTERVAL.format(low=fmt.price(low), high=fmt.price(high))
        uncertainty_text = content.UNCERTAINTY_INTERVAL_TEXT.format(coverage=fmt.percent(coverage))
    else:
        uncertainty, uncertainty_text = content.UNCERTAINTY_NONE, content.UNCERTAINTY_NONE_TEXT
    slots.update(
        heading=content.RESULT_LABEL,
        tag=content.SAMPLE_TAG if sample else content.REAL_TAG,
        price=fmt.price(prediction.price_ty),
        unit=content.PRICE_UNIT,
        words=fmt.price_words(prediction.price_ty),
        statement=content.SAMPLE_STATEMENT if sample else content.REAL_STATEMENT,
        uncertainty_label=content.UNCERTAINTY_LABEL,
        uncertainty=uncertainty,
        uncertainty_text=uncertainty_text,
        recap_label=content.RECAP_LABEL,
        recap=recap(snapshot),
        unknown=unknown_note(snapshot),
        provenance_label=content.PROVENANCE_LABEL,
        provenance=(
            content.PROVENANCE_SAMPLE.format(n=fmt.count(reference.n_rows))
            if sample
            else (prediction.source or content.PROVENANCE_UNKNOWN)
        ),
    )
    return slots
