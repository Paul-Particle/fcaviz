# fcaviz

The **FCA house plotting style for Plotly** — palette, standalone and slide layout
templates, the continuous colormap, marker helpers, and brand "chrome" (left-aligned
title + subtitle, corner monogram, optional leading dot) — packaged so you or a
colleague can just install it.

```python
import plotly.graph_objects as go
from fcaviz import fca_template, apply_header, save_figure

fig = go.Figure(go.Bar(x=[2022, 2023, 2024], y=[19, 24, 31]))
fig.update_layout(template=fca_template)   # or "fca"; "fca_slide" for slides
fig.update_yaxes(title=None)               # house convention: units go in the subtitle
apply_header(fig, title="Capacity additions", subtitle="Annual (GW)",
             fig_width=960, fig_height=540)
save_figure(fig, "out", "capacity")        # font-embedded HTML (+ PNG with [export])
```

See [`examples/quickstart.py`](examples/quickstart.py) for a runnable demo and
[`examples/feature_gallery.py`](examples/feature_gallery.py) for every feature in
both profiles.

## Install

Install straight from GitHub (public repo — no auth needed):

```sh
# pip
pip install "git+https://github.com/Paul-Particle/fcaviz.git"
# uv
uv add "git+https://github.com/Paul-Particle/fcaviz.git"
```

By default that tracks the `main` branch. For reproducible installs, **pin to a
released tag** (see [Releasing](#releasing) for the tag list):

```sh
# pip — pinned to a tag
pip install "git+https://github.com/Paul-Particle/fcaviz.git@v0.2.1"
# uv — pinned to a tag
uv add "git+https://github.com/Paul-Particle/fcaviz.git@v0.2.1"
```

Add the `export` extra for static PNG/SVG output via `save_figure` (pulls Kaleido):

```sh
pip install "fcaviz[export] @ git+https://github.com/Paul-Particle/fcaviz.git"
```

### Using conda

`fcaviz` is a pure-Python package — there is no conda package and you don't need
one. Create the conda env as usual, then **pip-install `fcaviz` into it**. The only
rule when mixing the two: install conda packages first, pip packages last. The
clean, reproducible way is to declare it in `environment.yml` (the `pip:` block runs
last automatically on `conda env create`):

```yaml
name: my-env
channels: [conda-forge]
dependencies:
  - python=3.12
  - plotly          # let conda manage the heavy deps
  - numpy
  - pip
  - pip:
      - "fcaviz @ git+https://github.com/Paul-Particle/fcaviz.git@v0.2.1"
      # for PNG/SVG export, use fcaviz[export] instead (pulls Kaleido)
```

Or into an already-active env: `conda activate my-env` then the `pip install …`
command above. Do **not** run `conda install` *after* pip-installing `fcaviz` in the
same env — conda can overwrite pip-managed packages; put pip last.

## What you get

- **Palette** — named brand colors (`fca_blue`, `highlight_blue`, `sand_yellow`, …),
  the discrete `fca_colorway` (blues and greys, interleaved) and the marker cycle
  `fca_marker_symbols`, both used by the templates.
- **Two profiles** — `fca_template` for standalone charts and `fca_slide_template`
  for slides (heavier lines, bigger markers and fonts). Both are registered by
  name, so `fig.update_layout(template="fca")` or `template="fca_slide"` works
  after import. The header chrome takes its sizes from whichever the figure uses.
- **`fca_colormap`** — the corporate design's continuous blue-grey → teal → sand
  scale. Both templates make it the default for every colorscale (heatmaps,
  contours, maps, colour axes, plotly express), and `sample_fca_colormap(n)`
  returns `n` discrete shades from it.
- **Markers** — `add_look_here_marker` (a larger highlight-blue diamond on one
  point) and `build_thin_plus_marker` (a thin, stroke-only "+").
- **Chrome** — `apply_header` (title + subtitle + corner logo, with an optional
  leading dot via `show_dot=True`), `add_trace_label` (solid-chip legend
  replacement; its white text needs a dark chip colour), and lower-level
  `apply_dot` / `apply_logo` / `header_geometry`.
- **`save_figure`** — writes a self-contained, **font-embedded** HTML plus a retina PNG.
- **Helpers** — `lighten`, `contrast_shades` (stacked-bar shade ordering),
  `inject_titillium_font`.

## Colour, marker and line guidance

- **Blues and greys first.** The default cycle alternates blue and grey, and dark
  and light, so successive series never suggest a gradient:
  `fca_blue, gray, light_blue, very_dark_gray, turquois, blue_gray`. `light_blue`
  and `turquois` are close; past about six series, prefer direct labels, small
  multiples or grouping over more colours.
- **`highlight_blue` is a soft highlight.** Use it to draw attention to something,
  so it is not in the default cycle. In a busy chart, where it would not stand out
  anyway, it may be added among the series for contrast:
  `fig.update_layout(colorway=fca_colorway + [highlight_blue])`.
- **One accent colour, when needed.** To mark something as good or bad, or to tell
  two similar-looking consecutive slides apart, `green` is the usual choice;
  `magenta_red` when something stronger is needed. Other palette colours such as
  `sand_yellow` are not part of the default chart look.
- **One continuous colormap.** Wherever a colormap is needed, use `fca_colormap`
  (the templates' default) or `sample_fca_colormap(n)`; similar-looking colormaps
  from other libraries are not a substitute, diverging data included.
- **Shaped markers alongside colour.** Scatter traces cycle circle, diamond,
  square and triangle (Plotly's triangle is slightly wider than equilateral).
  A larger diamond makes a good "look here" marker (`add_look_here_marker`; add
  it after the series traces). A thin "+" may stand where a star could, but
  rarely (`build_thin_plus_marker`).
- **Line weights.** Standalone charts use 2 px lines; the slide profile uses
  4.5 px. Slides keep the 960x540 logical size: `save_figure` exports at
  `scale=2`, i.e. 1920x1080 pixels.

## Notes

- **House convention:** no rotated y-axis title — state the quantity + units in the
  subtitle and set `yaxis_title=None`.
- **Brand dot is off by default.** The leading dot before the title is an
  experimental device for standalone charts and is not used on slides. Without it,
  title and subtitle sit flush left. Turn it on per chart with
  `apply_header(..., show_dot=True)` (the title then shifts right to clear the dot),
  or for a whole project with `fcaviz.style.SHOW_DOT = True`.
- **Fonts.** The brand font is **Titillium Web**. `save_figure` embeds it into HTML
  from the bundled `woff2` files (renders offline, no network). For static PNG/SVG
  via Kaleido the font must also be **installed on the OS**, otherwise Plotly falls
  back to a default sans-serif (colors/layout are unaffected).
- **Provenance.** Ported from the canonical `lcox-steel` `viz/style.py`.

## Releasing

The version lives in **one place** — `__version__` in `src/fcaviz/__init__.py`.
`pyproject.toml` reads it dynamically (via `[tool.hatch.version]`), so a release is
just: bump that line, commit, tag, push.

```sh
# 1. bump the single source of truth, e.g. 0.1.0 -> 0.2.0
#    edit src/fcaviz/__init__.py:  __version__ = "0.2.0"

# 2. sanity-check the build picks it up
uv build --wheel            # -> dist/fcaviz-0.2.0-py3-none-any.whl

# 3. commit, tag (tag == "v" + __version__), push both
git commit -am "fcaviz 0.2.0"
git tag -a v0.2.0 -m "fcaviz 0.2.0"
git push && git push --tags
```

Consumers then pin with `...git@v0.2.0` (see [Install](#install)). Use
[semantic versioning](https://semver.org): patch for fixes, minor for additions,
major for breaking API changes.

## Licensing

Internal FCA package (brand palette, logo, house style). The bundled **Titillium
Web** font (`src/fcaviz/assets/*.woff2`) is licensed under the SIL Open Font
License 1.1 and redistributed under those terms.
