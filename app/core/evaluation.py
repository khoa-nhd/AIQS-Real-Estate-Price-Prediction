"""Model evaluation results, read from files in the repository (brief FR-24 to FR-26).

Nothing here is typed in. Two kinds of results exist:
- the cross-validation the team ran while comparing candidate pipelines (notebook 03, Phần A);
- the locked model's own figures: cross-validation, validation and the single evaluation
  on the test split (notebook 03, C63, C64 and C67).
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field

import pandas as pd
import streamlit as st

from .model_interface import MODEL_MANIFEST
from .reference import ROOT

CV_DIR = ROOT / "experiments" / "model_comparison_cv"
CV_SUMMARY = CV_DIR / "recovered_model_cv_summary.csv"
CV_FOLDS = CV_DIR / "recovered_model_cv_folds.csv"
CV_SUMMARY_LABEL = "experiments/model_comparison_cv/recovered_model_cv_summary.csv"

FINAL_DIR = ROOT / "experiments" / "final_selection"
TEST_RESULT = FINAL_DIR / "test_evaluation.json"
TEST_RESULT_LABEL = "experiments/final_selection/test_evaluation.json"
BLEND_SUMMARY = ROOT / "experiments" / "ensemble_oof" / "blend_summary.csv"

REQUIRED_COLUMNS = ("model", "mean_cv_MAE", "mean_cv_RMSE", "mean_cv_R2")


@dataclass(frozen=True)
class CrossValidation:
    status: str  # available | missing | unreadable
    problem: str = ""
    summary: pd.DataFrame | None = None  # one row per candidate, best MAE first
    n_folds: int | None = None


@st.cache_data(show_spinner=False)
def load_cross_validation() -> CrossValidation:
    if not CV_SUMMARY.is_file():
        return CrossValidation("missing")
    try:
        summary = pd.read_csv(CV_SUMMARY)
        if not set(REQUIRED_COLUMNS) <= set(summary.columns):
            raise ValueError("missing columns")
        summary = summary[list(REQUIRED_COLUMNS)].dropna().sort_values("mean_cv_MAE").reset_index(drop=True)
        if summary.empty:
            raise ValueError("no rows")
    except Exception as exc:
        return CrossValidation("unreadable", problem=f"Không đọc được {CV_SUMMARY_LABEL}: {type(exc).__name__}.")

    n_folds = None
    if CV_FOLDS.is_file():
        try:
            n_folds = int(pd.read_csv(CV_FOLDS, usecols=["fold"])["fold"].nunique())
        except Exception:
            n_folds = None
    return CrossValidation("available", summary=summary, n_folds=n_folds)


@dataclass(frozen=True)
class FinalEvaluation:
    """The locked model's figures; each metrics dict holds MAE, RMSE and R2 (tỷ đồng for the first two)."""

    status: str  # available | missing | unreadable
    problem: str = ""
    test: dict[str, float] = field(default_factory=dict)
    test_new: dict[str, float] = field(default_factory=dict)  # test rows with no duplicate listing in training
    validation: dict[str, float] = field(default_factory=dict)
    cv: dict[str, float] = field(default_factory=dict)
    test_rows: int = 0
    twin_share: float = 0.0
    passed: bool = False  # the project's acceptance rule: R² on test of at least 0.7


@st.cache_data(show_spinner=False)
def load_final_evaluation() -> FinalEvaluation:
    if not TEST_RESULT.is_file():
        return FinalEvaluation("missing")
    try:
        test = json.loads(TEST_RESULT.read_text(encoding="utf-8"))
        manifest = json.loads(MODEL_MANIFEST.read_text(encoding="utf-8")) if MODEL_MANIFEST.is_file() else {}
        cv: dict[str, float] = {}
        weight = manifest.get("weights", {}).get("XGBoost")
        if BLEND_SUMMARY.is_file() and weight is not None:
            blend = pd.read_csv(BLEND_SUMMARY)
            row = blend.loc[(blend["xgb_weight"] - weight).abs() < 1e-9]
            if len(row) == 1:
                cv = {"MAE": float(row["mean_cv_MAE"].iloc[0]), "RMSE": float(row["mean_cv_RMSE"].iloc[0]),
                      "R2": float(row["mean_cv_R2"].iloc[0])}
        return FinalEvaluation(
            "available",
            test=test["metrics"],
            test_new=test.get("metrics_without_twins", {}),
            validation=manifest.get("metrics", {}).get("validation", {}),
            cv=cv,
            test_rows=int(test.get("rows", 0)),
            twin_share=float(test.get("twin_share", 0.0)),
            passed=bool(test.get("acceptance_R2_at_least_0_7", False)),
        )
    except Exception as exc:
        return FinalEvaluation("unreadable", problem=f"Không đọc được {TEST_RESULT_LABEL}: {type(exc).__name__}.")
