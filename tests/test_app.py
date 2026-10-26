"""Checks of the Streamlit app in app/, run headless with streamlit.testing (no browser, no server).

From the repository root, in the environment from app/requirements.txt:
    python -m unittest discover -s tests -v
(pytest also runs these.)
"""
import json
import pickle
import re
import sys
import unittest
from pathlib import Path

import pandas as pd
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
APP_DIR = ROOT / "app"
APP = APP_DIR / "streamlit_app.py"
MODEL_DIR = ROOT / "models" / "candidates" / "final_v3_group_2026-10-26"
INTERVAL = ROOT / "experiments" / "group_split" / "prediction_interval.json"
sys.path.insert(0, str(APP_DIR))

from core import model_interface  # noqa: E402

TIMEOUT = 180  # the first run loads the model


def pins(path: Path) -> dict[str, str]:
    """name -> version for every `name==version` line of a requirements file."""
    found = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^\s*([A-Za-z0-9_.\-]+)==([^\s;#]+)", line)
        if match:
            found[match.group(1).lower()] = match.group(2)
    return found


def html_text(at: AppTest) -> str:
    return " ".join(getattr(element, "body", "") or "" for element in at.get("html"))


def widget(at: AppTest, kind: str, key: str):
    return next(w for w in getattr(at, kind) if w.key == key)


class Environment(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads((MODEL_DIR / "manifest.json").read_text(encoding="utf-8"))

    def test_app_requirements_pin_the_model_libraries(self):
        app_pins = pins(APP_DIR / "requirements.txt")
        for name, version in self.manifest["versions"].items():
            self.assertEqual(app_pins.get(name), version, f"app/requirements.txt: {name}")
        self.assertEqual(pins(MODEL_DIR / "requirements-model.txt"),
                         {name: version for name, version in self.manifest["versions"].items()})

    def test_this_environment_matches_the_model(self):
        self.assertEqual(model_interface.environment_problems(self.manifest), [])

    def test_a_different_library_version_is_reported(self):
        problems = model_interface.environment_problems({"versions": {"numpy": "0.0.1"}})
        self.assertEqual(len(problems), 1)
        self.assertIn("numpy 0.0.1", problems[0])


class App(unittest.TestCase):
    def run_app(self, **query) -> AppTest:
        at = AppTest.from_file(str(APP), default_timeout=TIMEOUT)
        for key, value in query.items():
            at.query_params[key] = value
        at.run()
        self.assertFalse(at.exception, at.exception)
        return at

    def test_loads_with_the_real_model(self):
        at = self.run_app()
        text = html_text(at)
        self.assertNotIn("Mô hình chưa sẵn sàng", text)
        self.assertEqual(len(at.tabs), 3)
        self.assertIn("R² = 0,686", text)  # the accuracy tab reads the single test evaluation

    def test_empty_submit_lists_the_required_fields(self):
        at = self.run_app()
        widget(at, "button", "submit").click().run()
        text = html_text(at)
        self.assertEqual(at.session_state["outcome"].kind, "invalid")
        self.assertIn("Chọn phường / xã.", text)

    def estimate_cau_giay(self) -> AppTest:
        at = self.run_app()
        widget(at, "selectbox", "f_city").select("Hà Nội").run()
        widget(at, "selectbox", "f_district").select("Cầu Giấy").run()
        widget(at, "selectbox", "f_ward").select("Phường Dịch Vọng").run()
        widget(at, "text_input", "f_area").input("60").run()
        widget(at, "number_input", "f_floors").set_value(4).run()
        widget(at, "button", "submit").click().run()
        self.assertFalse(at.exception, at.exception)
        self.assertEqual(at.session_state["outcome"].kind, "result")
        return at

    def test_estimate_equals_a_direct_model_call(self):
        at = self.estimate_cau_giay()
        outcome = at.session_state["outcome"]

        model = pickle.loads((MODEL_DIR / "house_price_ensemble.pkl").read_bytes())
        row = {name: None for name in model_interface.MODEL_COLUMNS}
        row.update({"Area": 60.0, "Floors": 4, "City": "Hà Nội", "District": "Cầu Giấy",
                    "Address": "Phường Dịch Vọng, Cầu Giấy, Hà Nội"})
        direct = float(model.predict(pd.DataFrame([row]))[0])
        self.assertAlmostEqual(outcome.prediction.price_ty, direct, places=9)
        self.assertIn("tỷ đồng", html_text(at))

    def test_estimate_comes_with_the_calibrated_range(self):
        record = json.loads(INTERVAL.read_text(encoding="utf-8"))
        manifest = json.loads((MODEL_DIR / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(record["model"]["sha256"], manifest["sha256"])
        at = self.estimate_cau_giay()
        prediction = at.session_state["outcome"].prediction
        low, high, coverage, rows = prediction.interval
        self.assertLessEqual(low, prediction.price_ty)
        self.assertLessEqual(prediction.price_ty, high)
        self.assertEqual((coverage, rows), (record["test"]["coverage"], record["test"]["rows"]))
        text = html_text(at)
        self.assertIn("7,6 – 10,4 tỷ đồng", text)  # notebook 05 model: 7.59 – 10.43
        self.assertIn("d1-market-range", text)
        self.assertIn("Khoảng dao động 80%", text)  # the accuracy tab's team details

    def test_range_rule_matches_notebook_04(self):
        band = model_interface.Interval(
            params={"method": "grouped", "edges": [4.0, 6.0],
                    "groups": [{"q_lo": -1.0, "q_hi": 0.5}, {"q_lo": -1.5, "q_hi": 1.5}, {"q_lo": 0.2, "q_hi": 2.0}]},
            price_range=(1.0, 11.5), coverage=0.8, rows=100, record={})
        self.assertEqual(band.around(3.0), (2.0, 3.5))
        self.assertEqual(band.around(4.0), (2.5, 5.5))  # an edge belongs to the group above it
        self.assertEqual(band.around(1.2), (1.0, 1.7))  # clipped to the training prices
        self.assertEqual(band.around(10.5), (10.5, 11.5))  # always contains the estimate, clipped at the top
        self.assertEqual(band.around(0.8), (0.8, 1.3))  # an estimate below the data keeps itself inside

    def test_changing_the_city_clears_the_address(self):
        at = self.run_app()
        widget(at, "selectbox", "f_city").select("Hồ Chí Minh").run()
        widget(at, "selectbox", "f_district").select("Gò Vấp").run()
        widget(at, "selectbox", "f_ward").select("Phường 12").run()
        widget(at, "selectbox", "f_city").select("Hà Nội").run()
        self.assertIsNone(at.session_state["f_district"])
        self.assertIsNone(at.session_state["f_ward"])

    def test_an_unavailable_model_says_why(self):
        at = self.run_app(state="unavailable")  # the lab's simulated failure
        text = html_text(at)
        self.assertIn("Mô hình chưa sẵn sàng", text)
        self.assertIn("Chi tiết cho người quản trị", text)
        self.assertTrue(widget(at, "button", "submit").disabled)


if __name__ == "__main__":
    unittest.main()
