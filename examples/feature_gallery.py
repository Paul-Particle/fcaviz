"""Render every fcaviz feature in both profiles, with and without the brand dot.

Run:  uv run --extra export python examples/feature_gallery.py
Writes examples/out/gallery_<profile>_<chart>.html/.png for the profiles
"fca" (standalone) and "fca_slide".
"""

from pathlib import Path

import numpy as np
import plotly.graph_objects as go

from fcaviz import (
    add_look_here_marker, apply_header, build_thin_plus_marker, fca_blue,
    sample_fca_colormap, save_figure,
)

OUTPUT_DIRECTORY = Path(__file__).parent / "out"
FIGURE_WIDTH, FIGURE_HEIGHT = 960, 540
years = np.arange(2020, 2031)


def build_multi_series_line_chart(template_name: str, show_dot: bool) -> go.Figure:
    """Six series: the colorway, the marker cycle, the line weight, look-here and thin plus."""
    fig = go.Figure()
    for i in range(6):
        series_values = 10 + 4 * i + 0.8 * (i + 1) * np.sqrt(years - 2019)
        fig.add_scatter(x=years, y=series_values, mode="lines+markers", name=f"Series {i + 1}")
    fig.update_layout(template=template_name, legend=dict(x=0.02, xanchor="left"))
    fig.update_yaxes(title=None)
    add_look_here_marker(fig, 2027, 10 + 0.8 * np.sqrt(8))
    fig.add_scatter(x=[2024], y=[48], mode="markers", showlegend=False,
                    marker=build_thin_plus_marker(fca_blue, size=14))
    apply_header(fig, title="Six series, default cycle",
                 subtitle="Colorway, markers, look-here diamond and a thin plus (index)",
                 fig_width=FIGURE_WIDTH, fig_height=FIGURE_HEIGHT,
                 show_dot=show_dot)
    return fig


def build_default_colorscale_heatmap(template_name: str) -> go.Figure:
    """A heatmap that sets no colorscale, so it shows the template default."""
    grid_values = np.add.outer(np.arange(8), np.arange(12)) + np.random.default_rng(0).normal(0, 1, (8, 12))
    fig = go.Figure(go.Heatmap(z=grid_values))
    fig.update_layout(template=template_name)
    apply_header(fig, title="Heatmap with no colorscale set", subtitle="Default colormap (a.u.)",
                 fig_width=FIGURE_WIDTH, fig_height=FIGURE_HEIGHT)
    return fig


def build_sampled_colormap_bar_chart(template_name: str) -> go.Figure:
    """Discrete shades taken from the colormap with sample_fca_colormap."""
    sampled_colors = sample_fca_colormap(5)
    fig = go.Figure(go.Bar(x=[f"Step {i + 1}" for i in range(5)], y=[3, 5, 6, 8, 9],
                           marker_color=sampled_colors))
    fig.update_layout(template=template_name)
    fig.update_yaxes(title=None)
    apply_header(fig, title="Five shades from the colormap", subtitle="sample_fca_colormap(5) (index)",
                 fig_width=FIGURE_WIDTH, fig_height=FIGURE_HEIGHT)
    return fig


for template_name in ("fca", "fca_slide"):
    gallery_figures = {
        "lines": build_multi_series_line_chart(template_name, show_dot=False),
        "lines_dot": build_multi_series_line_chart(template_name, show_dot=True),
        "heatmap": build_default_colorscale_heatmap(template_name),
        "sampled": build_sampled_colormap_bar_chart(template_name),
    }
    for chart_name, fig in gallery_figures.items():
        saved_paths = save_figure(fig, OUTPUT_DIRECTORY, f"gallery_{template_name}_{chart_name}")
        print("wrote:", *saved_paths, sep="\n  ")
