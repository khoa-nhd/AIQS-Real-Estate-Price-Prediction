"""design_03 only: the payload panel (show the machine) and the field-group strip."""
import html
import json

from shared import schema
from shared.schema import FIELDS


def payload(values: dict[str, object]) -> str:
    """The exact feature dict the model gateway receives, as highlighted JSON."""
    lines = ['<span class="c">// Dữ liệu gửi cho mô hình (12 trường)</span>', "{"]
    for i, spec in enumerate(FIELDS):
        value = values.get(spec.name)
        if value is None:
            shown = '<span class="z">null</span>'
        elif isinstance(value, (int, float)):
            shown = f'<span class="n">{json.dumps(value)}</span>'
        else:
            shown = f'<span class="s">{html.escape(json.dumps(value, ensure_ascii=False))}</span>'
        comma = "," if i < len(FIELDS) - 1 else ""
        lines.append(f'  <span class="k">"{html.escape(spec.name)}"</span>: {shown}{comma}')
    lines.append("}")
    return '<pre class="d3-code" aria-label="Dữ liệu gửi cho mô hình">' + "\n".join(lines) + "</pre>"


GROUP_ICONS = {"location": "location_on", "size": "straighten", "structure": "stairs", "extra": "tune"}


def group_status(group: str, values: dict[str, object]) -> tuple[str, bool]:
    """A real per-group state: required fields missing, or how many optional ones are unknown."""
    specs = schema.fields_in(group)
    missing = [s for s in specs if s.required and values.get(s.name) is None]
    if missing:
        return f"Thiếu {len(missing)} mục bắt buộc", False
    unknown = [s for s in specs if values.get(s.name) is None]
    if unknown:
        return f"Đủ · {len(unknown)} mục «Không rõ»", True
    return "Đủ", True
