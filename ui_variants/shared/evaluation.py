"""Model evaluation results, read from files in the repository (brief FR-24 to FR-26).

Nothing here is typed in. What exists today is cross-validation on the training
split, recorded while the team compared candidate pipelines. There is no final
test evaluation and no locked model.
"""
from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
import streamlit as st

from .reference import ROOT

CV_DIR = ROOT / "experiments" / "model_comparison_cv"
CV_SUMMARY = CV_DIR / "recovered_model_cv_summary.csv"
CV_FOLDS = CV_DIR / "recovered_model_cv_folds.csv"
CV_SUMMARY_LABEL = "experiments/model_comparison_cv/recovered_model_cv_summary.csv"

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


def final_test_evaluation() -> None:
    """No final test evaluation exists, and no file format for one is agreed (brief OD-3)."""
    return None
