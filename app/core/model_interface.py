"""The one seam between the interface and the model.

Every UI variant calls the model through this module and nowhere else.
ProjectModelGateway loads the locked model exported by notebook 03 (C68):
models/candidates/final_v2_2026-10-20/house_price_ensemble.pkl, an equal-weight
XGBoost + LightGBM ensemble. The file is a pickle, so it is only loaded when its
SHA-256 matches the manifest written next to it.
"""
from __future__ import annotations

import hashlib
import json
import math
import pickle
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

import pandas as pd
import streamlit as st

from . import content, formatting as fmt
from .reference import ROOT, Reference

MODELS_DIR = ROOT / "models"
MODEL_DIR = MODELS_DIR / "candidates" / "final_v2_2026-10-20"
MODEL_FILE = MODEL_DIR / "house_price_ensemble.pkl"
MODEL_MANIFEST = MODEL_DIR / "manifest.json"
MODEL_LABEL = "models/candidates/final_v2_2026-10-20"

# The 12 dataset columns the model reads, plus "Address" built from the ward, street and project.
MODEL_COLUMNS = (
    "Area", "Frontage", "Access Road", "House direction", "Balcony direction", "Floors",
    "Bedrooms", "Bathrooms", "Legal status", "Furniture state", "City", "District",
)


@dataclass(frozen=True)
class ModelStatus:
    available: bool
    reason: str = ""


@dataclass(frozen=True)
class Prediction:
    price_ty: float  # total price in tỷ đồng
    is_sample: bool  # True for lab preview figures; never shown as a prediction
    source: str  # provenance line shown with the figure
    interval: tuple[float, float, float] | None = None  # low, high, coverage; only from a calibration artifact


class ModelUnavailable(Exception):
    """The model cannot be used at all."""


class InferenceError(Exception):
    """The model was called and failed."""


class ModelGateway(Protocol):
    def status(self) -> ModelStatus: ...

    def predict(self, features: dict[str, object]) -> Prediction: ...


@dataclass(frozen=True)
class LoadedModel:
    model: object | None
    manifest: dict = field(default_factory=dict)
    problem: str = ""


@st.cache_resource(show_spinner="Đang nạp mô hình…")
def load_project_model() -> LoadedModel:
    """Load the locked model once per server process, after checking its file against the manifest."""
    if not MODEL_FILE.is_file() or not MODEL_MANIFEST.is_file():
        return LoadedModel(None, problem=f"Chưa có tệp mô hình trong {MODEL_LABEL}.")
    try:
        manifest = json.loads(MODEL_MANIFEST.read_text(encoding="utf-8"))
    except Exception as exc:
        return LoadedModel(None, problem=f"Không đọc được manifest.json của mô hình: {type(exc).__name__}.")
    payload = MODEL_FILE.read_bytes()
    if hashlib.sha256(payload).hexdigest() != manifest.get("sha256"):
        # A pickle can run code when loaded: never load a file the manifest does not vouch for.
        return LoadedModel(None, manifest, "Tệp mô hình không khớp mã kiểm tra trong manifest.json nên không được nạp.")
    try:
        model = pickle.loads(payload)
    except Exception as exc:
        return LoadedModel(
            None, manifest,
            f"Không nạp được mô hình ({type(exc).__name__}). Cài thư viện theo {MODEL_LABEL}/requirements-model.txt.",
        )
    if not callable(getattr(model, "predict", None)):
        return LoadedModel(None, manifest, "Tệp mô hình không có hàm dự đoán.")
    return LoadedModel(model, manifest)


def build_address(features: dict[str, object]) -> str | None:
    """The address in the dataset's own order, which is how the model reads it:
    '[Dự án X, ][Đường Y, ]Phường Z, Quận, Tỉnh'."""
    ward, district, city = features.get("Ward"), features.get("District"), features.get("City")
    if not (ward and district and city):
        return None
    parts = []
    if features.get("Project"):
        parts.append(f"Dự án {features['Project']}")
    if features.get("Street"):
        parts.append(str(features["Street"]))
    return ", ".join([*parts, str(ward), str(district), str(city)])


def model_frame(features: dict[str, object]) -> pd.DataFrame:
    """One row as the model expects it; a field left unknown is None."""
    row = {name: features.get(name) for name in MODEL_COLUMNS}
    row["Address"] = build_address(features)
    return pd.DataFrame([row])


class ProjectModelGateway:
    """The real project model: the locked ensemble exported by notebook 03."""

    def status(self) -> ModelStatus:
        loaded = load_project_model()
        if loaded.model is None:
            return ModelStatus(False, loaded.problem)
        return ModelStatus(True, f"Đang dùng mô hình đã khoá trong {MODEL_LABEL}.")

    def predict(self, features: dict[str, object]) -> Prediction:
        loaded = load_project_model()
        if loaded.model is None:
            raise ModelUnavailable(loaded.problem)
        try:
            price = float(loaded.model.predict(model_frame(features))[0])
        except Exception as exc:  # any failure inside the pipeline is an inference error, shown as such
            raise InferenceError(type(exc).__name__) from exc
        if not math.isfinite(price):
            raise InferenceError("non-finite prediction")
        return Prediction(price_ty=price, is_sample=False, source=provenance(loaded.manifest))


def provenance(manifest: dict) -> str:
    """The line shown under a real estimate: which model, trained on what, tested how."""
    test = manifest.get("metrics", {}).get("test", {})
    if not test:
        return content.PROVENANCE_UNKNOWN
    created = str(manifest.get("created", "?"))
    if len(created) == 10 and created[4] == created[7] == "-":  # 2026-10-20 -> 20/10/2026
        created = "/".join(reversed(created.split("-")))
    return content.PROVENANCE_REAL.format(
        created=created,
        mae=fmt.number(test["MAE"], 2, trim=False),
        r2=fmt.number(test["R2"], 3, trim=False),
    )


class PreviewGateway:
    """Design-review stand-in. Returns one fixed, labelled sample figure.

    The figure is the median price of the training split. It ignores the input,
    so it cannot be read as a prediction for the property on screen.
    """

    def __init__(self, reference: Reference):
        self._reference = reference

    def status(self) -> ModelStatus:
        return ModelStatus(True, "Chế độ xem trước: không có mô hình nào chạy.")

    def predict(self, features: dict[str, object]) -> Prediction:
        if not self._reference.ok:
            raise ModelUnavailable(self._reference.problem)
        return Prediction(price_ty=self._reference.price["median"], is_sample=True, source="preview")


class SimulatedErrorGateway:
    """Design-review stand-in for a model that fails during inference."""

    def status(self) -> ModelStatus:
        return ModelStatus(True, "Chế độ xem trước: lỗi được mô phỏng.")

    def predict(self, features: dict[str, object]) -> Prediction:
        raise InferenceError("simulated")


class SimulatedUnavailableGateway:
    """Design-review stand-in for a model that cannot be loaded."""

    def status(self) -> ModelStatus:
        return ModelStatus(False, "Chế độ xem trước: mô phỏng mô hình chưa sẵn sàng.")

    def predict(self, features: dict[str, object]) -> Prediction:
        raise ModelUnavailable("simulated")


def gateway_for(scenario: str, reference: Reference) -> ModelGateway:
    """scenario: 'project' (the real model), 'preview', 'error' or 'unavailable' (the last three are lab-only)."""
    if scenario == "preview":
        return PreviewGateway(reference)
    if scenario == "error":
        return SimulatedErrorGateway()
    if scenario == "unavailable":
        return SimulatedUnavailableGateway()
    return ProjectModelGateway()
