"""Pixel measurements for an image reference.

Stands in for the Taste skill's DOM extractor (references/extract.js), which
needs a live page. Everything here is measured from pixels of a compressed,
possibly downscaled capture, so colours are approximate and sizes are in
capture pixels, not CSS pixels.

    python measure_image.py palette <image> [--colors 12] [--box x0,y0,x1,y1]
    python measure_image.py sample  <image> x,y [x,y ...]
    python measure_image.py crop    <image> x0,y0,x1,y1 <out.png> [--scale 2]
"""
from __future__ import annotations

import json
import sys

from PIL import Image


def _hex(rgb: tuple[int, int, int]) -> str:
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def _box(arg: str) -> tuple[int, int, int, int]:
    x0, y0, x1, y1 = (int(v) for v in arg.split(","))
    return x0, y0, x1, y1


def palette(path: str, colors: int = 12, box: str | None = None) -> dict:
    image = Image.open(path).convert("RGB")
    if box:
        image = image.crop(_box(box))
    quantized = image.quantize(colors=colors, method=Image.Quantize.MEDIANCUT)
    lut = quantized.getpalette()[: colors * 3]
    counts = sorted(quantized.getcolors(), reverse=True)
    total = image.width * image.height
    return {
        "image": path,
        "box": box,
        "size": [image.width, image.height],
        "colors": [
            {"hex": _hex(tuple(lut[i * 3: i * 3 + 3])), "areaPct": round(100 * n / total, 1)}
            for n, i in counts
        ],
    }


def sample(path: str, points: list[str]) -> dict:
    image = Image.open(path).convert("RGB")
    out = []
    for point in points:
        x, y = (int(v) for v in point.split(","))
        patch = image.crop((max(0, x - 2), max(0, y - 2), x + 3, y + 3))
        pixels = sorted(getattr(patch, "get_flattened_data", patch.getdata)(), key=sum)
        out.append({"at": [x, y], "hex": _hex(pixels[len(pixels) // 2])})
    return {"image": path, "samples": out}


def crop(path: str, box: str, out: str, scale: float = 2.0) -> dict:
    image = Image.open(path).convert("RGB").crop(_box(box))
    image = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    image.save(out)
    return {"image": path, "box": box, "out": out}


if __name__ == "__main__":
    mode, path, *rest = sys.argv[1:]
    if mode == "palette":
        n = int(rest[rest.index("--colors") + 1]) if "--colors" in rest else 12
        b = rest[rest.index("--box") + 1] if "--box" in rest else None
        result = palette(path, n, b)
    elif mode == "sample":
        result = sample(path, rest)
    elif mode == "crop":
        s = float(rest[rest.index("--scale") + 1]) if "--scale" in rest else 2.0
        result = crop(path, rest[0], rest[1], s)
    else:
        raise SystemExit(__doc__)
    print(json.dumps(result, ensure_ascii=False))
