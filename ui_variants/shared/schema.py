"""The property schema shared by every variant.

The 12 fields are the model's features from the notebooks (01, cell C02). Field
names are the dataset column names and are sent to the model unchanged.
"""
from __future__ import annotations

from dataclasses import dataclass

UNKNOWN = "Không rõ"


@dataclass(frozen=True)
class Field:
    name: str  # dataset column
    key: str  # widget and session-state key
    label: str
    group: str
    kind: str  # city | district | decimal | count | direction | choice
    required: bool = False
    unit: str = ""
    placeholder: str = ""


# Required set is provisional (design brief OD-2): the five features that have
# no missing values in the training split. The team's model contract decides.
# Units are provisional too (OD-1): the repository does not document them.
FIELDS: tuple[Field, ...] = (
    Field("City", "f_city", "Tỉnh / Thành phố", "location", "city", True, placeholder="Chọn tỉnh / thành phố"),
    Field("District", "f_district", "Quận / Huyện", "location", "district", True, placeholder="Chọn quận / huyện"),
    Field("Area", "f_area", "Diện tích", "size", "decimal", True, "m²", "Ví dụ: 54.0"),
    Field("Frontage", "f_frontage", "Mặt tiền", "size", "decimal", True, "m", "Ví dụ: 4.1"),
    Field("Access Road", "f_access", "Đường vào", "size", "decimal", True, "m", "Ví dụ: 3.5"),
    Field("Floors", "f_floors", "Số tầng", "structure", "count", placeholder="Ví dụ: 2"),
    Field("Bedrooms", "f_bedrooms", "Số phòng ngủ", "structure", "count", placeholder="Ví dụ: 2"),
    Field("Bathrooms", "f_bathrooms", "Số phòng tắm", "structure", "count", placeholder="Ví dụ: 3"),
    Field("House direction", "f_house_dir", "Hướng nhà", "extra", "direction"),
    Field("Balcony direction", "f_balcony_dir", "Hướng ban công", "extra", "direction"),
    Field("Legal status", "f_legal", "Pháp lý", "extra", "choice"),
    Field("Furniture state", "f_furniture", "Nội thất", "extra", "choice"),
)

BY_NAME = {f.name: f for f in FIELDS}

GROUPS: dict[str, str] = {
    "location": "Vị trí",
    "size": "Kích thước",
    "structure": "Kết cấu",
    "extra": "Thông tin thêm (không bắt buộc)",
}

# Display labels only. The dataset value is what goes to the model (brief OD-8).
CHOICE_LABELS: dict[str, dict[str, str]] = {
    "Legal status": {"Have certificate": "Đã có sổ", "Sale contract": "Hợp đồng mua bán"},
    "Furniture state": {"Full": "Đầy đủ", "Basic": "Cơ bản"},
}

# One sample property for every variant, so comparisons are like for like.
# Balcony direction is left unknown on purpose, to show how unknowns are reported.
SAMPLE_PROPERTY: dict[str, object] = {
    "City": "Hồ Chí Minh",
    "District": "Gò Vấp",
    "Area": 54.0,
    "Frontage": 4.1,
    "Access Road": 3.5,
    "Floors": 2,
    "Bedrooms": 2,
    "Bathrooms": 3,
    "House direction": "Tây - Nam",
    "Balcony direction": None,
    "Legal status": "Have certificate",
    "Furniture state": "Full",
}

# The same property with three blocking errors, for the invalid-input state.
INVALID_PROPERTY: dict[str, object] = {**SAMPLE_PROPERTY, "District": None, "Area": 0.0, "Access Road": None}


def fields_in(group: str) -> list[Field]:
    return [f for f in FIELDS if f.group == group]


def widget_label(field: Field) -> str:
    """Label with unit, and an asterisk on required fields."""
    text = f"{field.label} ({field.unit})" if field.unit else field.label
    return f"{text} \\*" if field.required else text


def display_value(field: Field, value: object) -> str:
    """How a dataset value is shown to the person."""
    if value is None:
        return UNKNOWN
    return CHOICE_LABELS.get(field.name, {}).get(str(value), str(value))
