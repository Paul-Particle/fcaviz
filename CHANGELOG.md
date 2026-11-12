# Changelog

## 0.2.1

- **`fca_colormap` renders in colour everywhere.** Its rgb() strings are now 0-255
  (from the unchanged 0-1 `cm_data`). The 0-1 strings rendered near-black on plotly 7,
  and on plotly 6 for markers using the layout default. Where they did render, output
  is pixel-identical.

## 0.2.0

Changes the default look of existing charts.

- **Brand dot off by default.** `apply_header(..., show_dot=True)` turns it on per
  chart, `fcaviz.style.SHOW_DOT = True` for a whole project. Without it, title and
  subtitle sit flush left.
- **New default colour cycle.** `fca_colorway` is now `fca_blue, gray, light_blue,
  very_dark_gray, turquois, blue_gray`: blues and greys interleaved, no
  `highlight_blue` (add it for contrast in busy charts).
- **Marker cycle.** Scatter traces cycle circle, diamond, square, triangle-up
  (`fca_marker_symbols`).
- **`fca_colormap` is the default for every colorscale**, in `go.*` traces and
  plotly express. New `sample_fca_colormap(n)` for discrete shades.
- **Slide profile.** New `fca_slide_template`, registered as `"fca_slide"`:
  heavier lines (4.5 px), bigger markers and fonts, larger bottom margin.
- **New helpers.** `add_look_here_marker` (large highlight-blue diamond) and
  `build_thin_plus_marker` (thin "+").
- **Header API.** `header_geometry` now takes the figure as its first argument and
  reads sizes from the figure's template; `apply_header` raises if the figure has
  no fca template. `margin_b` is optional and defaults to the template's.
  Standalone line width is explicit at 2 px.
- Requires plotly >= 5.24.
