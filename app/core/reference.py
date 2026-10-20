"""Reference facts read from the training split at run time.

This stands in for the artifact the model should ship with (brief FR-05, FR-11):
the categories and numeric ranges the model was trained on. Only training rows
are read: the training split itself, and the raw Address of those same rows (by
row_id) for the ward, street and project lists. Validation, calibration and test
rows are never used.
"""
from __future__ import annotations

import re
import unicodedata
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
# The final model was trained on splits_v2 (notebook 03, Phần B).
TRAIN_SPLIT = ROOT / "data" / "processed" / "splits_v2" / "train.csv"
TRAIN_SPLIT_LABEL = "data/processed/splits_v2/train.csv"
RAW_DATA = ROOT / "data" / "vietnam_housing_dataset.csv"
RAW_DATA_LABEL = "data/vietnam_housing_dataset.csv"

# Same patterns as notebook 03, C53 (parse_address).
WARD_PATTERN = re.compile(r"^(phường|xã|thị trấn)\b", re.IGNORECASE)
STREET_PATTERN = re.compile(r"^(đường|phố|quốc lộ|tỉnh lộ|đại lộ)\b", re.IGNORECASE)
PROJECT_PATTERN = re.compile(r"^dự án\s+(.+)$", re.IGNORECASE)

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
    price_sorted: tuple[float, ...] = ()  # every training price, ascending: exact "cao hơn X% số căn"
    locations_total: int = 0
    locations_offered: int = 0
    # Address parts seen in training, per (city, district) offered in the form.
    wards: dict[tuple[str, str], tuple[str, ...]] = field(default_factory=dict)
    streets: dict[tuple[str, str], tuple[str, ...]] = field(default_factory=dict)
    projects: dict[tuple[str, str], tuple[str, ...]] = field(default_factory=dict)
    ward_rows: dict[tuple[str, str, str], int] = field(default_factory=dict)  # training rows per ward


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


def address_parts(address: object) -> tuple[str | None, str | None, str | None]:
    """Ward, street and project as written in an address ('[Dự án X,] [Đường Y,] Phường Z, Quận, Tỉnh')."""
    if pd.isna(address):
        return None, None, None
    parts = [re.sub(r"\s+", " ", unicodedata.normalize("NFC", p)).strip() for p in str(address).split(",")]
    ward = parts[-3] if len(parts) >= 3 and WARD_PATTERN.match(parts[-3]) else None
    street = parts[-4] if len(parts) >= 4 and STREET_PATTERN.match(parts[-4]) else None
    project_match = PROJECT_PATTERN.match(parts[0])
    return ward, street, project_match.group(1) if project_match else None


def model_key(kind: str, value: str) -> str:
    """How the model reads a ward, street or project name (notebook 03, C53): lower case;
    a street also drops a leading 'đường' / 'phố', so 'Đường Láng' and 'Phố Láng' are one street."""
    text = value.lower()
    return re.sub(r"^(đường|phố)\s+", "", text) if kind == "street" else text


def _natural(text: str) -> str:
    """Sort key: diacritics ignored, numbers in numeric order ('Phường 2' before 'Phường 10')."""
    return re.sub(r"\d+", lambda m: m.group().zfill(6), _fold(text))


def _options(names: list[str], kind: str) -> tuple[str, ...]:
    """One entry per name the model tells apart, shown in its most common spelling."""
    spellings: dict[str, Counter] = {}
    for name in names:
        spellings.setdefault(model_key(kind, name), Counter())[name] += 1
    return tuple(sorted((c.most_common(1)[0][0] for c in spellings.values()), key=_natural))


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

    # Ward, street and project of the same training rows, from the raw address.
    if not RAW_DATA.is_file():
        return Reference(ok=False, problem=f"Không tìm thấy {RAW_DATA_LABEL} (cần để lấy phường, đường, dự án).")
    try:
        raw_address = pd.read_csv(RAW_DATA, usecols=["Address"], encoding="utf-8-sig")["Address"]
    except Exception as exc:
        return Reference(ok=False, problem=f"Không đọc được {RAW_DATA_LABEL}: {type(exc).__name__}.")
    parsed = pd.DataFrame(
        raw_address.iloc[df["row_id"].to_numpy()].map(address_parts).tolist(),
        columns=["Ward", "Street", "Project"],
    )
    by_location: dict[tuple[str, str], dict[str, list[str]]] = {}
    ward_rows: Counter = Counter()
    for c, d, w, s, p in zip(city, district, parsed["Ward"], parsed["Street"], parsed["Project"]):
        if (c, d) not in kept.index:
            continue
        bucket = by_location.setdefault((c, d), {"ward": [], "street": [], "project": []})
        for kind, value in (("ward", w), ("street", s), ("project", p)):
            if isinstance(value, str):  # a missing part comes back from pandas as NaN
                bucket[kind].append(value)
        if isinstance(w, str):
            ward_rows[(c, d, model_key("ward", w))] += 1

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
        missing={
            **{n: float(df[n].isna().mean()) for n in (*NUMERIC, *CATEGORICAL, "City", "District")},
            **{n: float(parsed[n].isna().mean()) for n in ("Ward", "Street", "Project")},
        },
        price={
            "min": float(price.min()),
            "max": float(price.max()),
            "median": float(price.median()),
            "q1": float(price.quantile(0.25)),
            "q3": float(price.quantile(0.75)),
        },
        price_hist=tuple((float(lo), float(lo) + PRICE_BIN_WIDTH, int(n)) for lo, n in hist.items()),
        price_sorted=tuple(sorted(float(v) for v in price)),
        locations_total=int(len(pairs)),
        locations_offered=int(len(kept)),
        wards={loc: _options(b["ward"], "ward") for loc, b in by_location.items()},
        streets={loc: _options(b["street"], "street") for loc, b in by_location.items()},
        projects={loc: _options(b["project"], "project") for loc, b in by_location.items()},
        ward_rows=dict(ward_rows),
    )
