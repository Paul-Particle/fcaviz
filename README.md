# fcaviz

The **FCA house plotting style for Plotly** — palette, layout template, continuous
colormap, and brand "chrome" (leading dot, dot-aligned title + subtitle, corner
monogram) — packaged so you or a colleague can just install it.

```python
import plotly.graph_objects as go
from fcaviz import fca_template, apply_header, save_figure

fig = go.Figure(go.Bar(x=[2022, 2023, 2024], y=[19, 24, 31]))
fig.update_layout(template=fca_template)   # or template="fca" (registered on import)
fig.update_yaxes(title=None)               # house convention: units go in the subtitle
apply_header(fig, title="Capacity additions", subtitle="Annual (GW)",
             fig_width=960, fig_height=540, margin_b=64)
save_figure(fig, "out", "capacity")        # font-embedded HTML (+ PNG with [export])
```

See [`examples/quickstart.py`](examples/quickstart.py) for a runnable demo.

## Install

Private repo — install straight from GitHub:

```sh
# pip
pip install "git+https://github.com/Paul-Particle/fcaviz.git"
# uv
uv add "git+https://github.com/Paul-Particle/fcaviz.git"
```

Add the `export` extra for static PNG/SVG output via `save_figure` (pulls Kaleido):

```sh
pip install "fcaviz[export] @ git+https://github.com/Paul-Particle/fcaviz.git"
```

## What you get

- **Palette** — named brand colors (`fca_blue`, `highlight_blue`, `sand_yellow`, …)
  and the discrete `fca_colorway` used as the template's trace cycle.
- **`fca_template`** — the house Plotly layout (fonts, axes, legend, sizing). Also
  registered by name, so `fig.update_layout(template="fca")` works after import.
- **`fca_colormap`** — a continuous blue-grey → teal → sand scale for heatmaps etc.
- **Chrome** — `apply_header` (dot-aligned title + subtitle + corner logo),
  `add_trace_label` (solid-chip legend replacement), and lower-level
  `apply_dot` / `apply_logo` / `header_geometry`.
- **`save_figure`** — writes a self-contained, **font-embedded** HTML plus a retina PNG.
- **Helpers** — `lighten`, `contrast_shades` (stacked-bar shade ordering),
  `inject_titillium_font`.

## Notes

- **House convention:** no rotated y-axis title — state the quantity + units in the
  subtitle and set `yaxis_title=None`.
- **Fonts.** The brand font is **Titillium Web**. `save_figure` embeds it into HTML
  from the bundled `woff2` files (renders offline, no network). For static PNG/SVG
  via Kaleido the font must also be **installed on the OS**, otherwise Plotly falls
  back to a default sans-serif (colors/layout are unaffected).
- **Provenance.** Ported from the canonical `lcox-steel` `viz/style.py`.

## Licensing

Internal FCA package (brand palette, logo, house style). The bundled **Titillium
Web** font (`src/fcaviz/assets/*.woff2`) is licensed under the SIL Open Font
License 1.1 and redistributed under those terms.
