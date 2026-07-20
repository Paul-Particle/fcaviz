"""Minimal fcaviz demo: a house-styled grouped bar chart with full brand chrome.

Run:  uv run python examples/quickstart.py
Writes examples/out/quickstart.html (+ .png if a Kaleido engine is installed).
"""

from pathlib import Path

import plotly.graph_objects as go

from fcaviz import (
    apply_header, fca_blue, fca_template, sand_yellow, save_figure,
    add_trace_label,
)

years = [2020, 2021, 2022, 2023, 2024]
fig = go.Figure()
fig.add_bar(x=years, y=[12, 15, 19, 24, 31], name="Solar", marker_color=sand_yellow)
fig.add_bar(x=years, y=[20, 22, 25, 27, 30], name="Wind", marker_color=fca_blue)

fig.update_layout(template=fca_template, barmode="group", showlegend=False)
fig.update_yaxes(title=None)

# the FCA legend replacement: solid color chips
add_trace_label(fig, "Solar", color=sand_yellow, x=0.30, y=0.92)
add_trace_label(fig, "Wind", color=fca_blue, x=0.30, y=0.80)

apply_header(
    fig,
    title="Renewable capacity additions",
    subtitle="Annual additions (GW)",
    fig_width=960, fig_height=540, margin_b=64,
)

out = Path(__file__).parent / "out"
paths = save_figure(fig, out, "quickstart")
print("wrote:", *paths, sep="\n  ")
