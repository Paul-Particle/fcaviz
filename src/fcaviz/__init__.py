"""fcaviz — the FCA house plotting style for Plotly.

Importing this package registers the FCA layout template with Plotly (so
``fig.update_layout(template="fca")`` works anywhere) and re-exports the palette,
template, colormap, and brand-chrome helpers.

    import plotly.graph_objects as go
    from fcaviz import fca_template, fca_colormap, apply_header, save_figure

    fig = go.Figure(...)
    fig.update_layout(template=fca_template)
    apply_header(fig, title="…", subtitle="… (units)",
                 fig_width=960, fig_height=540, margin_b=64)
    save_figure(fig, "out", "my_chart")   # HTML (font-embedded) + PNG
"""

from .style import (
    # palette
    fca_blue, highlight_blue, light_blue, sand_yellow, green, magenta_red,
    turquois, blue_black, very_dark_gray, dark_gray, blue_gray, gray,
    light_blue_gray, light_gray,
    # tokens / config
    BRAND_FONT, PLOTLY_CONFIG, SHOW_DOT, SHOW_LOGO,
    # core style objects (importing .style registers template "fca" with Plotly)
    fca_colorway, fca_template, fca_colormap,
    # color helpers
    lighten, contrast_shades,
    # brand chrome + output
    fca_logo, inject_titillium_font, save_figure, add_trace_label,
    header_geometry, apply_dot, apply_logo, apply_header,
)

__version__ = "0.1.1"

__all__ = [
    "fca_blue", "highlight_blue", "light_blue", "sand_yellow", "green",
    "magenta_red", "turquois", "blue_black", "very_dark_gray", "dark_gray",
    "blue_gray", "gray", "light_blue_gray", "light_gray",
    "BRAND_FONT", "PLOTLY_CONFIG", "SHOW_DOT", "SHOW_LOGO",
    "fca_colorway", "fca_template", "fca_colormap",
    "lighten", "contrast_shades",
    "fca_logo", "inject_titillium_font", "save_figure", "add_trace_label",
    "header_geometry", "apply_dot", "apply_logo", "apply_header",
    "__version__",
]
