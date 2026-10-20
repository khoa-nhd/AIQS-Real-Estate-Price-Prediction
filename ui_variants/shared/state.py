"""Session state and the submit flow, identical for every variant.

The lab adds one thing the product will not have: a state switch, so reviewers
can see each UI state without a model. It selects which gateway scenario runs
and which preset fills the form.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import streamlit as st

from . import content, formatting as fmt, schema
from .model_interface import InferenceError, ModelUnavailable, Prediction, ProjectModelGateway, gateway_for
from .reference import Reference, load_reference
from .schema import FIELDS, UNKNOWN
from .validation import validate

# Lab state -> (label, gateway scenario, form preset)
LAB_STATES: dict[str, tuple[str, str, dict[str, object]]] = {
    "sample": ("Kết quả mẫu (xem trước)", "preview", schema.SAMPLE_PROPERTY),
    "initial": ("Ban đầu", "preview", {}),
    "invalid": ("Dữ liệu chưa hợp lệ", "preview", schema.INVALID_PROPERTY),
    "unavailable": ("Mô hình chưa sẵn sàng", "project", schema.SAMPLE_PROPERTY),
    "error": ("Lỗi khi ước tính (mô phỏng)", "error", schema.SAMPLE_PROPERTY),
}
DEFAULT_STATE = "sample"


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
    if spec.kind in ("direction", "choice"):
        return UNKNOWN if value is None else value
    if spec.kind == "count" and value is not None:
        return int(value)
    return value


def read_values() -> dict[str, object]:
    """Current form values keyed by dataset field name. Unknown is None."""
    values: dict[str, object] = {}
    for spec in FIELDS:
        value = st.session_state.get(spec.key)
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
    ss["attempted"] = True
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
    _fill(LAB_STATES[ss["lab_state"]][2])
    ss["attempted"] = False
    ss["outcome"] = Outcome("initial")
    if ss["lab_state"] == "unavailable":
        ss["outcome"] = Outcome("unavailable")
    elif ss["lab_state"] != "initial":
        submit()


def reset_form() -> None:
    _fill({})
    st.session_state["attempted"] = False
    st.session_state["outcome"] = Outcome("unavailable" if scenario() == "project" else "initial")


def fill_sample() -> None:
    _fill(schema.SAMPLE_PROPERTY)


def city_changed() -> None:
    st.session_state[schema.BY_NAME["District"].key] = None


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
    project_status = ProjectModelGateway().status()
    preview = scenario() != "project"
    return Page(
        values=values,
        errors=errors,
        outcome=outcome,
        kind=kind,
        stale=kind in ("sample", "result", "error") and outcome.snapshot != values,
        preview=preview,
        blocked=not preview and not project_status.available,
        simulated=scenario() == "error" and kind == "error",
        model_reason=project_status.reason,
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
