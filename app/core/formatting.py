"""Vietnamese number formatting: decimal comma, dot for thousands."""
from __future__ import annotations


def number(value: float, digits: int = 1, trim: bool = True) -> str:
    text = f"{value:,.{digits}f}"
    if trim and "." in text:
        text = text.rstrip("0").rstrip(".")
    return text.replace(",", "\u0000").replace(".", ",").replace("\u0000", ".")


def count(value: int) -> str:
    return number(value, 0)


def percent(share: float) -> str:
    return f"{number(share * 100, 0)}%"


def price(ty: float) -> str:
    """Price in tỷ đồng at the display precision (one decimal, brief FR-19)."""
    return number(round(ty, 1), 1, trim=False)


def price_words(ty: float) -> str:
    """The same rounded figure spelled out in tỷ and triệu ("tức": "khoảng" is kept for ranges)."""
    rounded = round(ty, 1)
    whole = int(rounded)
    trieu = int(round((rounded - whole) * 1000))
    parts = []
    if whole:
        parts.append(f"{count(whole)} tỷ")
    if trieu:
        parts.append(f"{trieu} triệu")
    return "tức " + " ".join(parts or ["0"]) + " đồng"
