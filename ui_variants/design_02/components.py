"""design_02 only: the reference's dotted-column, diamond-marker chart, drawn with real data."""
import altair as alt
import pandas as pd

from shared import formatting as fmt
from shared.reference import Reference

COMMA = "replace(format(datum.value, '.1f'), '.', ',')"


def diamond_distribution(reference: Reference, *, text: str, grid: str, height: int = 300) -> alt.LayerChart:
    """Training-split price distribution: one dotted column per 0.5 tỷ bin, a diamond at its count."""
    data = pd.DataFrame(reference.price_hist, columns=["lo", "hi", "count"])
    data["mid"] = (data["lo"] + data["hi"]) / 2
    data["range"] = [f"{fmt.number(a)} – {fmt.number(b)} tỷ đồng" for a, b in zip(data["lo"], data["hi"])]
    top = float(data["count"].max()) * 1.1
    x = alt.X("mid:Q", title="Giá (tỷ đồng)", axis=alt.Axis(labelExpr=COMMA, grid=False, labelFont="IBM Plex Mono",
                                                            titleFont="IBM Plex Mono", tickCount=10))
    y = alt.Y("count:Q", title="Số căn", scale=alt.Scale(domain=[0, top]),
              axis=alt.Axis(grid=False, labelFont="IBM Plex Mono", titleFont="IBM Plex Mono"))
    base = alt.Chart(data)
    columns = base.mark_rule(color=grid, strokeDash=[1, 3]).encode(x=x, y=alt.datum(0), y2=alt.datum(top))
    whiskers = base.mark_rule(color=text, opacity=0.55, strokeWidth=1.5).encode(
        x=x, y=alt.Y("lo_w:Q"), y2="hi_w:Q").transform_calculate(lo_w="datum.count * 0.82", hi_w="datum.count * 1.08")
    diamonds = base.mark_point(shape="diamond", filled=True, size=110, color=text, opacity=1).encode(
        x=x, y=y, tooltip=[alt.Tooltip("range:N", title="Khoảng giá"), alt.Tooltip("count:Q", title="Số căn")])
    return (columns + whiskers + diamonds).properties(height=height).configure(background="transparent").configure_view(strokeWidth=0)
