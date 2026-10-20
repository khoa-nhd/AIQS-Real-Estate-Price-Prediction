"""Basic checks for the four prototypes. No browser needed.

Run from the repository root:

    design_lab/.venv/Scripts/python.exe design_lab/check_prototypes.py

Each prototype is run headlessly with Streamlit's own test harness in every lab
state, then driven through one real interaction. The checks are about behaviour
and honesty of the states, not about how anything looks.
"""
from __future__ import annotations

import sys
from pathlib import Path

from streamlit.testing.v1 import AppTest

LAB = Path(__file__).resolve().parent
sys.path.insert(0, str(LAB))

from lab import content, schema  # noqa: E402
from lab.gateway import ProjectModelGateway  # noqa: E402
from lab.state import LAB_STATES  # noqa: E402

CONCEPTS = ("concept_a.py", "concept_b.py", "concept_c.py", "concept_d.py")
EXPECTED_KIND = {"sample": "sample", "initial": "initial", "invalid": "invalid", "unavailable": "unavailable", "error": "error"}


def page_text(app: AppTest) -> str:
    """Everything the prototype wrote as HTML or Markdown."""
    parts = [str(getattr(element, "body", "") or getattr(element, "value", "")) for element in app.main]
    return "\n".join(parts)


def run(path: Path, state: str | None = None) -> AppTest:
    app = AppTest.from_file(str(path), default_timeout=60)
    if state:
        app.query_params["state"] = state
    return app.run()


def check_concept(name: str) -> list[str]:
    problems: list[str] = []
    path = LAB / name

    def expect(condition: bool, message: str) -> None:
        if not condition:
            problems.append(message)

    for state, expected in EXPECTED_KIND.items():
        app = run(path, state)
        expect(not app.exception, f"{state}: exception {[e.value for e in app.exception]}")
        if app.exception:
            continue
        expect(not app.warning and not app.error, f"{state}: unexpected Streamlit alert")
        expect(app.session_state["outcome"].kind == expected, f"{state}: outcome is {app.session_state['outcome'].kind}")
        missing = [spec.name for spec in schema.FIELDS if spec.key not in app.session_state]
        expect(not missing, f"{state}: fields missing from the form: {missing}")
        text = page_text(app)
        submit = app.button(key="submit")
        if state == "unavailable":
            expect(submit.disabled, "unavailable: the action is not disabled")
            expect(content.BANNER_UNAVAILABLE in text, "unavailable: banner missing")
            expect(content.PRICE_UNIT not in text or content.SAMPLE_TAG not in text, "unavailable: a figure is shown")
        else:
            expect(content.BANNER_PREVIEW in text, f"{state}: preview banner missing")
        if state == "sample":
            expect(content.SAMPLE_TAG in text, "sample: the sample label is missing")
            expect(content.REAL_TAG not in text, "sample: labelled as a model result")
            expect(content.UNCERTAINTY_NONE in text, "sample: uncertainty is not shown as unavailable")
        if state == "invalid":
            expect(content.SUMMARY_HEADING.format(n=3) in text, "invalid: error summary missing")
        if state == "error":
            expect(content.SIMULATED_NOTE in text, "error: not marked as simulated")

    # One real interaction: start empty, submit, fix the form, submit again, then edit.
    app = run(path, "initial")
    if app.exception:
        return problems
    app.button(key="submit").click().run()
    expect(app.session_state["outcome"].kind == "invalid", "empty submit did not fail validation")
    app.selectbox(key="f_city").select("Hà Nội").run()
    expect(app.session_state["f_district"] is None, "district was not cleared when the city changed")
    district = app.selectbox(key="f_district").options[0]
    app.selectbox(key="f_district").select(district).run()
    app.number_input(key="f_area").set_value(60.0).run()
    app.number_input(key="f_frontage").set_value(4.0).run()
    app.number_input(key="f_access").set_value(700.0).run()  # outside the training range on purpose
    app.button(key="submit").click().run()
    outcome = app.session_state["outcome"]
    expect(outcome.kind == "sample", f"valid submit gave {outcome.kind}")
    expect("Access Road" in outcome.warnings, "out-of-range value produced no warning")
    expect(outcome.snapshot["City"] == "Hà Nội", "the estimate was not based on the submitted input")
    app.number_input(key="f_area").set_value(75.0).run()
    expect(content.STALE in page_text(app), "editing after a result did not mark it as out of date")
    expect(not app.exception, "exception during interaction")
    return problems


def main() -> int:
    status = ProjectModelGateway().status()
    print(f"Project model: available={status.available} ({status.reason})")
    failed = 0
    for name in CONCEPTS:
        problems = check_concept(name)
        failed += bool(problems)
        print(f"{'FAIL' if problems else 'PASS'}  {name}  ({len(LAB_STATES)} states + interaction)")
        for problem in problems:
            print(f"      - {problem}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
