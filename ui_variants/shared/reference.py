"""Reference facts read from the training split at run time.

This stands in for the artifact the model should ship with (brief FR-05, FR-11):
the categories and numeric ranges the model was trained on. Only the training
split is read; validation, calibration and test are never opened.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
TRAIN_SPLIT = ROOT / "data" / "processed" / "splits_v1" / "train.csv"
TRAIN_SPLIT_LABEL = "data/processed/splits_v1/train.csv"

NUMERIC = ("Area", "Frontage", "Access Road", "Floors", "Bedrooms", "Bathrooms")
CATEGORICAL = ("House direction", "Balcony direction", "Legal status", "Furniture state")
COMPASS = ("Đông", "Tây", "Nam", "Bắc", "Đông - Bắc", "Đông - Nam", "Tây - Bắc", "Tây - Nam")

# Lab-only rule. The raw location columns contain junk strings and duplicate
# spellings ("Hồ Chí Minh giá 2tỷ380", "TP. HCM", "Quận Bình Tân" next to
# "Bình Tân"). Only city/district pairs with at least this many training rows
# are offered. The production list must come from the model's own artifact.
MIN_ROWS_PER_LOCATION = 10
PRICE_BIN_WIDTH = 0.5


@dataclass(frozen=True)
class Reference:
    ok: bool
    problem: str = ""
    n_rows: int = 0
    cities: tuple[str, ...] = ()
    districts: dict[str, tuple[str, ...]] = field(default_factory=dict)
    ranges: dict[str, tuple[float, float]] = field(default_factory=dict)
    options: dict[str, tuple[str, ...]] = field(default_factory=dict)
    missing: dict[str, float] = field(default_factory=dict)
    price: dict[str, float] = field(default_factory=dict)
    price_hist: tuple[tuple[float, float, int], ...] = ()
    locations_total: int = 0
    locations_offered: int = 0


def normalize_location_name(value: object) -> object:
    """Same rule as notebook 03, cell C03: NFC, collapse spaces, drop a trailing period."""
    if pd.isna(value):
        return value
    text = unicodedata.normalize("NFC", str(value))
    text = re.sub(r"\s+", " ", text).strip()
    return text.rstrip(".").strip()


def _fold(text: str) -> str:
    """Sort key that ignores Vietnamese diacritics."""
    stripped = "".join(c for c in unicodedata.normalize("NFD", text) if not unicodedata.combining(c))
    return stripped.replace("đ", "d").replace("Đ", "D").lower()


@st.cache_data(show_spinner=False)
def load_reference() -> Reference:
    if not TRAIN_SPLIT.is_file():
        return Reference(ok=False, problem=f"Không tìm thấy {TRAIN_SPLIT_LABEL}.")
    try:
        df = pd.read_csv(TRAIN_SPLIT, encoding="utf-8-sig")
    except Exception as exc:  # unreadable file: say so, show no partial numbers
        return Reference(ok=False, problem=f"Không đọc được {TRAIN_SPLIT_LABEL}: {type(exc).__name__}.")

    city = df["City"].map(normalize_location_name)
    district = df["District"].map(normalize_location_name)
    pairs = pd.DataFrame({"city": city, "district": district}).dropna().value_counts()
    kept = pairs[pairs >= MIN_ROWS_PER_LOCATION]

    districts: dict[str, list[str]] = {}
    for (c, d) in kept.index:
        districts.setdefault(c, []).append(d)
    cities = tuple(sorted(districts, key=_fold))

    price = df["Price"]
    edges_lo = (price // PRICE_BIN_WIDTH) * PRICE_BIN_WIDTH
    hist = edges_lo.value_counts().sort_index()

    return Reference(
        ok=True,
        n_rows=len(df),
        cities=cities,
        districts={c: tuple(sorted(v, key=_fold)) for c, v in districts.items()},
        ranges={n: (float(df[n].min()), float(df[n].max())) for n in NUMERIC},
        options={
            n: tuple([v for v in COMPASS if v in set(df[n].dropna())] + sorted(set(df[n].dropna()) - set(COMPASS)))
            for n in CATEGORICAL
        },
        missing={n: float(df[n].isna().mean()) for n in (*NUMERIC, *CATEGORICAL, "City", "District")},
        price={
            "min": float(price.min()),
            "max": float(price.max()),
            "median": float(price.median()),
            "q1": float(price.quantile(0.25)),
            "q3": float(price.quantile(0.75)),
        },
        price_hist=tuple((float(lo), float(lo) + PRICE_BIN_WIDTH, int(n)) for lo, n in hist.items()),
        locations_total=int(len(pairs)),
        locations_offered=int(len(kept)),
    )
