"""The one seam between the interface and the model.

Every UI variant calls the model through this module and nowhere else. No
model is loaded here: the repository has no saved artifact and no agreed
artifact format (brief OD-3), so the project gateway reports "unavailable".
When the team ships a pipeline, its loader goes in ProjectModelGateway and the
variants need no change.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from .reference import ROOT, Reference

MODELS_DIR = ROOT / "models"


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


def _artifact_names(folder: Path = MODELS_DIR) -> list[str]:
    if not folder.is_dir():
        return []
    return sorted(p.name for p in folder.iterdir() if p.is_file() and p.name.lower() != "readme.md")


class ProjectModelGateway:
    """The real project model. Today it can only report that there is none."""

    def status(self) -> ModelStatus:
        names = _artifact_names()
        if not names:
            return ModelStatus(False, "Thư mục models/ chưa có tệp mô hình nào.")
        # Files exist but nothing here knows how to load them safely yet.
        return ModelStatus(False, "Đã có tệp trong models/ nhưng chưa có bộ nạp mô hình được nhóm thống nhất.")

    def predict(self, features: dict[str, object]) -> Prediction:
        raise ModelUnavailable(self.status().reason)


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


def gateway_for(scenario: str, reference: Reference) -> ModelGateway:
    """scenario: 'project' (the real thing), 'preview' or 'error'."""
    if scenario == "preview":
        return PreviewGateway(reference)
    if scenario == "error":
        return SimulatedErrorGateway()
    return ProjectModelGateway()
