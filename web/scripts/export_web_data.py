"""Build the data files of the static web app (web/public/data/) from the locked model.

The Vercel app runs the model in the browser: this script writes every fitted parameter
of the two pipelines (scalers, imputers, one-hot categories, target encodings) and every
tree of XGBoost and LightGBM to model.json, and the facts the interface shows to
reference.json. web/public/model.js applies them exactly as scikit-learn, XGBoost and
LightGBM do; tests/test_web_model.py checks that both give the same prices.

Run from the repository root with the project environment (Python 3.14, app/requirements.txt):
    python web/scripts/export_web_data.py
"""
from __future__ import annotations

import bisect
import hashlib
import json
import sys
from dataclasses import asdict
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "app"))

from core import content, model_interface, schema  # noqa: E402
from core.evaluation import CV_SUMMARY_LABEL, load_cross_validation, load_final_evaluation  # noqa: E402
from core.reference import load_reference, model_key  # noqa: E402
from core.validation import FEW_WARD_ROWS, REQUIRED_MESSAGE  # noqa: E402

OUT = ROOT / "web" / "public" / "data"
MISSING_LABEL = "__MISSING__"
# Location keys the model builds from City, District and the parsed address (notebook 03, C54).
KEY_PARTS = {
    "City_District_Ward": ("City", "District", "Ward"),
    "City_Project": ("City", "Project"),
    "City_District_Street": ("City", "District", "Street"),
}


def floats(values) -> list[float]:
    return [float(v) for v in np.asarray(values, dtype=float)]


def export_preprocessing(pipe) -> list[dict]:
    """The ColumnTransformer's blocks, in output order, with their fitted parameters."""
    pre = pipe.named_steps["preprocessing"]
    assert [name for name, _ in pre.steps] == ["features", "columns"]
    columns = pre.named_steps["columns"]
    assert columns.sparse_output_, "model.js assumes the sparse output the model was trained on"
    blocks = []
    for name, transformer, cols in columns.transformers_:
        if name == "remainder":
            assert transformer == "drop"
            continue
        steps = dict(transformer.steps)
        if name in ("num", "fa"):
            scaler, imputer = steps["scaler"], steps.get("imputer")
            assert scaler.with_mean and scaler.with_std
            assert imputer is None or not imputer.add_indicator
            blocks.append({
                "kind": "scale", "columns": list(cols),
                "mean": floats(scaler.mean_), "scale": floats(scaler.scale_),
                # None: missing values stay missing for the trees (LightGBM's frontage and access road)
                "fill": floats(imputer.statistics_) if imputer is not None else None,
            })
        elif name == "cat":
            imputer, onehot = steps["imputer"], steps["onehot"]
            assert imputer.strategy == "most_frequent" and onehot.drop is None
            assert onehot.handle_unknown == "ignore" and not onehot._infrequent_enabled
            blocks.append({
                "kind": "onehot", "columns": list(cols),
                "fill": [str(v) for v in imputer.statistics_],
                "categories": [[str(c) for c in cats] for cats in onehot.categories_],
            })
        elif name == "target":
            imputer, encoder = steps["imputer"], steps["encoder"]
            assert imputer.fill_value == MISSING_LABEL and encoder.target_type_ == "continuous"
            blocks.append({
                "kind": "target", "columns": list(cols),
                "parts": [list(KEY_PARTS[c]) for c in cols], "fill": MISSING_LABEL,
                "encodings": [dict(zip((str(c) for c in cats), floats(enc)))
                              for cats, enc in zip(encoder.categories_, encoder.encodings_)],
                "default": float(encoder.target_mean_),
            })
        else:
            raise AssertionError(f"unexpected block {name}")
    width = sum(len(b["columns"]) if b["kind"] != "onehot" else sum(map(len, b["categories"])) for b in blocks)
    assert width == len(columns.get_feature_names_out())
    return blocks


def export_xgboost(model) -> dict:
    booster = model.get_booster()
    raw = json.loads(booster.save_raw("json"))
    learner = raw["learner"]
    gbm = learner["gradient_booster"]
    assert gbm["name"] == "gbtree" and learner["objective"]["name"] == "reg:squarederror"
    # no early stopping in the final fit, so predict() uses every tree
    assert booster.num_boosted_rounds() == model.n_estimators
    base =float(np.float32(float(learner["learner_model_param"]["base_score"].strip("[]"))))
    trees = []
    for tree in gbm["model"]["trees"]:
        left = tree["left_children"]
        trees.append({
            "left": left, "right": tree["right_children"],
            "feature": [f if l != -1 else -1 for f, l in zip(tree["split_indices"], left)],
            # split value of a node, or the leaf value of a leaf; stored as float32 by XGBoost
            "value": [float(np.float32(v)) for v in tree["split_conditions"]],
            "defaultLeft": [int(bool(d)) for d in tree["default_left"]],
        })
    assert len(trees) == booster.num_boosted_rounds()
    return {"kind": "xgboost", "base": base, "trees": trees}


def export_lightgbm(model) -> dict:
    dump = model.booster_.dump_model()
    assert dump["objective"].startswith("regression") and not dump["average_output"]
    assert model.best_iteration_ in (0, None)
    trees = []
    for info in dump["tree_info"]:
        tree = {"left": [], "right": [], "feature": [], "value": [], "defaultLeft": [], "missingNaN": []}

        def add(node) -> int:
            index = len(tree["left"])
            for key in tree:
                tree[key].append(0)
            if "split_index" not in node:
                tree["feature"][index], tree["value"][index] = -1, float(node["leaf_value"])
                tree["left"][index] = tree["right"][index] = -1
                return index
            assert node["decision_type"] == "<=" and node["missing_type"] in ("None", "NaN")
            tree["feature"][index], tree["value"][index] = int(node["split_feature"]), float(node["threshold"])
            tree["defaultLeft"][index] = int(node["default_left"])
            tree["missingNaN"][index] = int(node["missing_type"] == "NaN")
            tree["left"][index] = add(node["left_child"])
            tree["right"][index] = add(node["right_child"])
            return index

        add(info["tree_structure"])
        trees.append(tree)
    assert len(trees) == model.booster_.num_trees()
    return {"kind": "lightgbm", "trees": trees}


def export_model(loaded) -> dict:
    model, manifest = loaded.model, loaded.manifest
    components = []
    for name, weight in model.weights.items():
        pipe = model.components[name]
        estimator = pipe.named_steps["model"]
        trees = export_xgboost(estimator) if name == "XGBoost" else export_lightgbm(estimator)
        components.append({"name": name, "weight": float(weight), "preprocessing": export_preprocessing(pipe), **trees})
    band = load_band()
    return {
        "source": model_interface.MODEL_LABEL,
        "sha256": manifest["sha256"],
        "created": manifest.get("created"),
        "versions": manifest.get("versions", {}),
        "features": list(model.features),
        "components": components,
        # the 80% range of notebook 04, applied by model.js exactly as model_interface.Interval.around
        "interval": {"params": band.params, "priceRange": list(band.price_range),
                     "coverage": band.coverage, "rows": band.rows},
        "checks": self_checks(model),
    }


def load_band():
    """The calibration result the Streamlit app uses (checked against the model's SHA-256)."""
    band = model_interface.load_interval()
    assert band is not None, f"{model_interface.INTERVAL_LABEL} missing or made for another model (run notebook 04)"
    return band


def model_input(values: dict) -> dict:
    """What model.js receives for a form: the dataset fields, plus the address parts as the model parses them."""
    frame = model_interface.model_frame(values)
    parsed = load_project().model.prepare(frame).iloc[0]
    row = {name: (None if pd.isna(values.get(name)) else values.get(name)) for name in model_interface.MODEL_COLUMNS}
    row.update({part: (None if pd.isna(parsed[part]) else str(parsed[part])) for part in ("Ward", "Project", "Street")})
    return row


def self_checks(model) -> list[dict]:
    """Prices the browser recomputes when it loads the model; a mismatch stops the app."""
    cases = [
        schema.SAMPLE_PROPERTY,
        {"City": "Hà Nội", "District": "Cầu Giấy", "Ward": "Phường Dịch Vọng", "Area": 60.0, "Floors": 4},
        {"City": "Đà Nẵng", "District": "Hải Châu", "Ward": "Phường Hòa Cường Bắc", "Area": 85.0},
    ]
    checks = []
    for values in cases:
        price = float(model.predict(model_interface.model_frame(values))[0])
        checks.append({"input": model_input(values), "price": price, "interval": list(load_band().around(price))})
    return checks


def options_with_keys(names: tuple[str, ...], kind: str, counts: dict | None = None, where: tuple = ()) -> list[dict]:
    out = []
    for name in names:
        item = {"label": name, "key": model_key(kind, name)}
        if counts is not None:
            item["rows"] = int(counts.get((*where, item["key"]), 0))
        out.append(item)
    return out


def check_address_keys(reference) -> None:
    """The keys the interface sends must be what the model's own address parser makes of the same choice."""
    rows, expected = [], []
    for (city, district), wards in reference.wards.items():
        ward = wards[0] if wards else None
        for w in wards:
            rows.append({"City": city, "District": district, "Ward": w})
            expected.append(("Ward", model_key("ward", w)))
        for s in reference.streets.get((city, district), ()):
            rows.append({"City": city, "District": district, "Ward": ward, "Street": s})
            expected.append(("Street", model_key("street", s)))
        for p in reference.projects.get((city, district), ()):
            rows.append({"City": city, "District": district, "Ward": ward, "Project": p})
            expected.append(("Project", model_key("project", p)))
    frame = pd.concat([model_interface.model_frame(r) for r in rows], ignore_index=True)
    parsed = load_project().model.prepare(frame)
    bad = [(rows[i], part, key, parsed[part].iloc[i]) for i, (part, key) in enumerate(expected) if parsed[part].iloc[i] != key]
    assert not bad, f"{len(bad)} address keys differ from the model's parser, e.g. {bad[:3]}"
    print(f"address keys: {len(rows)} choices parse to the keys the web app sends")


def export_reference() -> dict:
    reference = load_reference()
    assert reference.ok, reference.problem
    check_address_keys(reference)
    final, cv = load_final_evaluation(), load_cross_validation()
    assert final.status == "available", final.problem
    loaded = load_project()
    prices = sorted(reference.price_sorted)
    unique = sorted(set(prices))
    locations = []
    for city in reference.cities:
        for district in reference.districts[city]:
            loc = (city, district)
            locations.append({
                "city": city, "district": district,
                "wards": options_with_keys(reference.wards.get(loc, ()), "ward", reference.ward_rows, loc),
                "streets": options_with_keys(reference.streets.get(loc, ()), "street"),
                "projects": options_with_keys(reference.projects.get(loc, ()), "project"),
            })
    copy = {k: v for k, v in vars(content).items() if k.isupper() and isinstance(v, (str, tuple, dict))}
    return {
        "nRows": reference.n_rows,
        "locations": locations,
        "ranges": {k: list(v) for k, v in reference.ranges.items()},
        "options": {k: list(v) for k, v in reference.options.items()},
        "missing": reference.missing,
        "price": reference.price,
        "priceHist": [list(b) for b in reference.price_hist],
        # every training price once, with how many prices lie below it: "cao hơn giá của X% số căn"
        "priceBelow": [[p, bisect.bisect_left(prices, p)] for p in unique],
        "locationsTotal": reference.locations_total,
        "locationsOffered": reference.locations_offered,
        "evaluation": {
            "test": final.test, "testNew": final.test_new, "validation": final.validation, "cv": final.cv,
            "testRows": final.test_rows, "newShare": final.new_share, "passed": final.passed,
        },
        "candidates": {
            "rows": cv.summary.to_dict("records") if cv.status == "available" else [],
            "folds": cv.n_folds,
            "source": CV_SUMMARY_LABEL,
        },
        "provenance": model_interface.provenance(loaded.manifest),
        "interval": interval_summary(load_band().record),
        "schema": {
            "fields": [asdict(f) for f in schema.FIELDS],
            "groups": schema.GROUPS,
            "choiceLabels": schema.CHOICE_LABELS,
            "unknown": schema.UNKNOWN,
            "sample": schema.SAMPLE_PROPERTY,
            "requiredMessage": REQUIRED_MESSAGE,
            "fewWardRows": FEW_WARD_ROWS,
        },
        "copy": copy,
    }


def interval_summary(record: dict) -> dict:
    """What the accuracy view says about the range (same figures as streamlit_app.interval_summary)."""
    return {
        "calibrationRows": record["fit_on"]["rows"],
        "validationCoverage": record["validation"]["results"][record["method"]]["coverage"],
        "testCoverage": record["test"]["coverage"],
        "testNewCoverage": record["test"]["coverage_new_listings"],
        "testRows": record["test"]["rows"],
        "meanWidth": record["test"]["mean_width"],
        "source": model_interface.INTERVAL_LABEL,
    }


_loaded = None


def load_project():
    """The model, loaded the way the Streamlit app loads it (SHA-256 and environment checked)."""
    global _loaded
    if _loaded is None:
        _loaded = model_interface.load_project_model()
        assert _loaded.model is not None, _loaded.problem
    return _loaded


def write(name: str, data: dict) -> None:
    path = OUT / name
    text = json.dumps(data, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
    path.write_text(text, encoding="utf-8")
    print(f"{path.relative_to(ROOT)}: {len(text.encode('utf-8')) / 1e6:.1f} MB, sha256 {hashlib.sha256(text.encode('utf-8')).hexdigest()[:12]}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    write("model.json", export_model(load_project()))
    write("reference.json", export_reference())


if __name__ == "__main__":
    main()
