"""Input validation for the form (design_lab brief FR-09 to FR-11).

Blocking errors stop the estimate. Range warnings do not: they flag values
outside what the training split contains.
"""
from __future__ import annotations

from . import content, formatting as fmt
from .reference import Reference, model_key
from .schema import FIELDS

REQUIRED_MESSAGE = {
    "City": "Chọn tỉnh / thành phố.",
    "District": "Chọn quận / huyện.",
    "Ward": "Chọn phường / xã.",
    "Area": "Nhập diện tích.",
}
# Below this many training rows a ward's price level is mostly borrowed from its district.
FEW_WARD_ROWS = 5


def validate(values: dict[str, object], reference: Reference) -> tuple[dict[str, str], dict[str, str]]:
    """Return (errors, warnings), both keyed by dataset field name."""
    errors: dict[str, str] = {}
    warnings: dict[str, str] = {}

    for field in FIELDS:
        value = values.get(field.name)
        if value is None:
            if field.required:
                errors[field.name] = REQUIRED_MESSAGE[field.name]
            continue

        if field.kind == "decimal" and isinstance(value, str):
            example = field.placeholder.removeprefix("Ví dụ: ")
            errors[field.name] = f"Nhập {field.label.lower()} bằng số, ví dụ {example}."
            continue
        if field.kind == "decimal":
            number = float(value)
            if field.name == "Frontage":
                if number < 0:
                    errors[field.name] = "Nhập mặt tiền từ 0 trở lên."
            elif number <= 0:
                errors[field.name] = f"Nhập {field.label.lower()} lớn hơn 0."
        elif field.kind == "count":
            number = float(value)
            if number < 1 or number != int(number):
                errors[field.name] = f"Nhập {field.label.lower()} là số nguyên từ 1 trở lên."

        if field.name in errors or field.name not in reference.ranges:
            continue
        low, high = reference.ranges[field.name]
        if not low <= float(value) <= high:
            unit = f" {field.unit}" if field.unit else ""
            warnings[field.name] = (
                f"{field.label} nằm ngoài khoảng có trong dữ liệu "
                f"({fmt.number(low)} – {fmt.number(high)}{unit}), nên kết quả có thể kém tin cậy."
            )

    ward, district, city = values.get("Ward"), values.get("District"), values.get("City")
    if ward and "Ward" not in errors:
        rows = reference.ward_rows.get((city, district, model_key("ward", str(ward))), 0)
        if rows < FEW_WARD_ROWS:
            warnings["Ward"] = content.WARD_FEW_ROWS.format(n=fmt.count(rows))

    return errors, warnings
