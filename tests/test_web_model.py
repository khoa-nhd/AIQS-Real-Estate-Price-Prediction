"""The web app's model (web/public/model.js + data/model.json) must give the prices of the pickled model.

Runs model.js under Node on every validation and calibration row, plus form-like rows with
optional fields left unknown, and compares with the pickle. Needs Node (skipped without it) and
web/public/data/*.json from web/scripts/export_web_data.py.
    python -m unittest tests.test_web_model -v
"""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"
MODEL_JSON = WEB / "public" / "data" / "model.json"
REFERENCE_JSON = WEB / "public" / "data" / "reference.json"
sys.path.insert(0, str(ROOT / "app"))

from core import model_interface  # noqa: E402

NODE = shutil.which("node")
# XGBoost adds its trees in float32: the two sides may differ in the last float32 digit (~1e-6 tỷ).
TOLERANCE = 1e-5


def as_input(prepared: pd.DataFrame) -> list[dict]:
    """Rows as model.js receives them: the 12 fields and the parsed address parts, None for missing."""
    frame = prepared.astype(object).where(prepared.notna(), None)
    return [{k: (float(v) if isinstance(v, (int, float, np.floating, np.integer)) else v) for k, v in row.items()}
            for row in frame.to_dict("records")]


@unittest.skipUnless(NODE, "Node.js is needed to run web/public/model.js")
class WebModelParity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        loaded = model_interface.load_project_model()
        assert loaded.model is not None, loaded.problem
        cls.model = loaded.model
        cls.band = model_interface.load_interval()
        assert cls.band is not None, "experiments/calibration/prediction_interval.json missing (notebook 04)"
        cls.exported = json.loads(MODEL_JSON.read_text(encoding="utf-8"))

    def run_node(self, rows: list[dict]) -> list[dict]:
        with tempfile.TemporaryDirectory() as tmp:
            src, out = Path(tmp) / "rows.json", Path(tmp) / "out.json"
            src.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
            subprocess.run([NODE, str(WEB / "scripts" / "predict.mjs"), str(MODEL_JSON), str(src), str(out)],
                           check=True, capture_output=True, text=True)
            return json.loads(out.read_text(encoding="utf-8"))

    def compare(self, frame: pd.DataFrame, label: str) -> None:
        prepared = self.model.prepare(frame)
        expected = self.model.predict(frame)
        parts = {name: pipe.predict(prepared) for name, pipe in self.model.components.items()}
        got = self.run_node(as_input(prepared))
        for name, values in parts.items():
            diff = np.abs(np.array([g[name] for g in got]) - values)
            self.assertLess(diff.max(), TOLERANCE, f"{label}, {name}: largest difference {diff.max():.2e}")
        diff = np.abs(np.array([g["price"] for g in got]) - expected)
        self.assertLess(diff.max(), TOLERANCE, f"{label}: largest difference {diff.max():.2e}")
        # the 80% range (notebook 04) around each price, as the Streamlit app computes it
        ranges = np.array([self.band.around(float(p)) for p in expected])
        for i, end in enumerate(("low", "high")):
            diff = np.abs(np.array([g[end] for g in got]) - ranges[:, i])
            self.assertLess(diff.max(), TOLERANCE, f"{label}, interval {end}: largest difference {diff.max():.2e}")
        # what the person sees: the price rounded to 0,1 tỷ
        shown = np.round(np.array([g["price"] for g in got]), 1) != np.round(expected, 1)
        self.assertLessEqual(int(shown.sum()), 0, f"{label}: rounded price differs on {int(shown.sum())} rows")

    def split_rows(self, name: str) -> pd.DataFrame:
        raw = pd.read_csv(ROOT / "data" / "vietnam_housing_dataset.csv", usecols=["Address"])
        split = pd.read_csv(ROOT / "data" / "processed" / "splits_v2" / f"{name}.csv")
        frame = split[self.model.features].copy()
        frame["Address"] = raw["Address"].iloc[split["row_id"].to_numpy()].to_numpy()
        return frame

    def test_validation_rows(self):
        self.compare(self.split_rows("validation"), "validation")

    def test_calibration_rows(self):
        self.compare(self.split_rows("calibration"), "calibration")

    def test_form_rows_with_unknown_fields(self):
        """Rows as the form makes them: every offered ward, with only the required fields filled in."""
        reference = json.loads(REFERENCE_JSON.read_text(encoding="utf-8"))
        rows = []
        for loc in reference["locations"]:
            for i, ward in enumerate(loc["wards"]):
                values = {"City": loc["city"], "District": loc["district"], "Ward": ward["label"], "Area": 40.0 + i % 90}
                if i % 3 == 0 and loc["streets"]:
                    values["Street"] = loc["streets"][i % len(loc["streets"])]["label"]
                if i % 7 == 0 and loc["projects"]:
                    values["Project"] = loc["projects"][0]["label"]
                if i % 2:
                    values.update({"Floors": 1 + i % 5, "Frontage": 3.5, "Legal status": "Have certificate"})
                rows.append(model_interface.model_frame(values))
        self.compare(pd.concat(rows, ignore_index=True), "form rows")

    def test_exported_from_the_locked_model(self):
        manifest = json.loads(model_interface.MODEL_MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(self.exported["sha256"], manifest["sha256"])
        self.assertEqual([c["name"] for c in self.exported["components"]], list(self.model.weights))

    def test_self_checks_are_the_pickle_prices(self):
        for check in self.exported["checks"]:
            frame = pd.DataFrame([{**check["input"], "Address": None}])
            prepared_like = self.model.predict(frame.drop(columns="Address").assign(
                Ward=check["input"]["Ward"], Project=check["input"]["Project"], Street=check["input"]["Street"]))
            self.assertAlmostEqual(float(prepared_like[0]), check["price"], places=9)
            self.assertEqual(tuple(check["interval"]), self.band.around(check["price"]))

    def test_exported_range_is_the_calibrated_one(self):
        exported = self.exported["interval"]
        self.assertEqual(exported["params"], self.band.params)
        self.assertEqual((exported["coverage"], exported["rows"]), (self.band.coverage, self.band.rows))


if __name__ == "__main__":
    unittest.main()
