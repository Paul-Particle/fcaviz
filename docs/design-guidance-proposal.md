# Design guidance vs fcaviz: comparison and proposal

Status: approved and implemented for 0.2.0 on the `dot-default-off` branch,
with two adjustments to the original proposal: `highlight_blue` is a soft
highlight that may join the series in busy charts (item 1), and colour usage is
described in prose instead of role constants (item 2). Defaults change directly,
without an opt-in template (see the end). The code sketches below show the
proposal; `src/fcaviz/style.py` is the implementation.

Lightness values below are CIE L* (0 = black, 100 = white), computed from the
palette hex codes. Checks were run against plotly 6.9.0.

## Comparison, rule by rule

| # | Rule | fcaviz today | Verdict |
|---|------|--------------|---------|
| 1 | Mostly blue and greys/black | `fca_colorway` holds only blues and greys; sand, green and magenta are not in it. But the README example and `examples/quickstart.py` colour a series `sand_yellow`. | Follows (colorway); the example contradicts |
| 2 | Highlight blue to draw attention (a soft highlight, case by case) | `highlight_blue` is slot 5 of `fca_colorway`, so any chart with 5+ series uses it for an ordinary series. The brand dot is also `highlight_blue`. | Contradicts |
| 3 | Green as the first extra colour, red if stronger | `green` and `magenta_red` exist as plain constants; no roles, no guidance. `magenta_red` is already the strongest red in the palette. | Not covered |
| 4 | Interleave blues and greys, no false gradient | Order is blue, grey, blue, grey, blue, grey, blue, grey, grey. L* runs 35, 53, 80, 78, 58, 40, 79, 27, 81: not a gradient. Two weak spots: `light_blue` (slot 3) and `turquois` (slot 7) are near-identical light cyans (L* 79.5 vs 79.4); slot 5 is `highlight_blue` (rule 2). | Mostly follows |
| 5 | One continuous colormap, always | `fca_colormap` exists, but the template sets no colorscale defaults. A `go.Heatmap` with no `colorscale` renders blue-to-red (plotly.js default); `px.imshow` renders viridis. | Contradicts by default |
| 6 | Shaped markers: circle, diamond, square, equilateral triangle | No marker sequence; every trace gets `circle`. Plotly's `triangle-up` is not equilateral: height/width = 0.65 instead of 0.87 (its half-width is 2r/sqrt(3) for a height of 1.5r, r = marker radius). Plotly has no custom marker paths. | Not covered; triangle only approximable |
| 7 | Larger diamond as a "look here" marker | Nothing. | Not covered |
| 8 | Thin "+", rarely, where a star would do | Nothing. Plotly's `cross-thin` is a stroke-only plus whose weight is `marker.line.width`. | Not covered |
| 9 | Heavy lines for slide line charts | No line-width default (plotly's 2 px applies); one profile, 960x540, sized for standalone charts. | Not covered |
| 10 | Brand dot off by default, standalone only | Was on by default via `SHOW_DOT = True`. | Fixed on this branch |

## Proposed changes

### 0. Brand dot off by default (implemented)

`SHOW_DOT` is now `False`, and `header_geometry` / `apply_header` take
`show_dot: bool = None` (None falls back to `SHOW_DOT`). `apply_dot` reads
`geom["show_dot"]`, so the title indent and the dot always agree. Without the dot,
title and subtitle start at the same left edge.

### 1. A blue/grey interleaved categorical order without highlight blue

Alternate hue (blue, grey) and lightness (dark, light) so neither hue nor
lightness reads as a ramp, and keep `highlight_blue` out of the default cycle.
It is a soft highlight: in a busy chart it may not work as a highlight but can
add needed contrast, so it may be appended there
(`colorway=fca_colorway + [highlight_blue]`). Existing palette colours only;
implemented as the new `fca_colorway`:

```python
fca_colorway = [
    fca_blue,        # #0A5680  blue  L* 35
    gray,            # #B7C1C8  grey  L* 78
    light_blue,      # #70D2F0  blue  L* 80
    very_dark_gray,  # #525F6A  grey  L* 40
    turquois,        # #83D1DD  blue  L* 79
    blue_gray,       # #8CA5B7  grey  L* 66
]
```

The palette has only three non-reserved blues, and two of them (`light_blue`,
`turquois`) are hard to tell apart. Keeping them four slots apart and giving them
different marker shapes (item 3) helps, but a 6-slot cycle is about the limit.
Past six series, the README should say to use direct labels, small multiples or
grouping rather than more colours. If a longer cycle is wanted anyway, append
`blue_black` (#33434D) and `light_blue_gray` (#BDCCD9); the tail is then
grey-only.

### 2. Colour usage, described rather than named

Decision: no role constants (`highlight_color`, `good`, `bad`), since they would
read as rules. The README describes the suggested usage instead: `green` is the
usual accent for a good or bad aspect or for telling two similar consecutive
slides apart, `magenta_red` when something stronger is needed. The palette names
stay as they are. `green` (L* 74) is pale; on a light-grey series it can be weak,
which is one reason the stronger option exists.

### 3. Marker sequence via the template

Plotly templates cycle `template.data.scatter` entries over scatter traces, and
plotly express reads its default `symbol_sequence` from the same place
(both verified):

```python
fca_marker_symbols = ["circle", "diamond", "square", "triangle-up"]
fca_template.data.scatter = [
    go.Scatter(marker=dict(symbol=symbol_name, size=8), line=dict(width=2))
    for symbol_name in fca_marker_symbols
]
```

Plotly's `triangle-up` is a flattened triangle (see rule 6). Getting a true
equilateral one would mean drawing markers as layout shapes or text glyphs,
which costs more than it is worth. Suggest accepting the plotly triangle and
saying so in the README; I'd like to check that with the person who wrote the
guidance.

### 4. "Look here" and thin-plus helpers

```python
def add_look_here_marker(fig, x, y, *, size: int = 16, **trace_kwargs) -> None:
    """Mark one point with a larger highlight-blue diamond (no legend entry)."""
    fig.add_scatter(x=[x], y=[y], mode="markers", showlegend=False, hoverinfo="skip",
                    marker=dict(symbol="diamond", size=size, color=highlight_color,
                                line=dict(width=0)),
                    **trace_kwargs)

thin_plus_marker = dict(symbol="cross-thin", size=10, line=dict(width=1.5))
# usage: fig.add_scatter(..., marker=dict(thin_plus_marker, line=dict(width=1.5, color=fca_blue)))
```

`cross-thin` is stroke-only, so its colour comes from `marker.line.color`;
set it explicitly.

### 5. A slide profile next to the standalone one

Register `fca_slide` beside `fca` (renamed in docs to "standalone"):

```python
fca_slide_template = go.layout.Template(fca_template)   # copy, then override
fca_slide_template.layout.update(font_size=22, title_font_size=28,
                                 xaxis_linewidth=3, legend_font_size=18)
fca_slide_template.data.scatter = [
    go.Scatter(marker=dict(symbol=symbol_name, size=12), line=dict(width=4.5))
    for symbol_name in fca_marker_symbols
]
pio.templates["fca_slide"] = fca_slide_template
```

Keep the logical size at 960x540 and export with `save_figure(..., scale=2)`,
which gives 1920x1080 pixels without touching the header geometry. Exact sizes
need a look on a real slide. The dot stays off here; slides may also leave the
title to the slide itself, so `apply_header` would accept `title=None`.

Architectural catch: `header_geometry` and `apply_header` read title size,
title y and margins from `fca_template` directly. With two profiles they should
read them from the figure's own template (`fig.layout.template`). That is a small
refactor, but it should land before the slide profile, not be patched around.

### 6. `fca_colormap` as the only continuous scale

Set every default a chart might fall back to (verified for `go.Heatmap` and
`px.imshow`):

```python
fca_template.layout.colorscale.sequential = fca_colormap
fca_template.layout.colorscale.sequentialminus = fca_colormap
fca_template.layout.colorscale.diverging = fca_colormap
fca_template.layout.coloraxis.colorscale = fca_colormap
for trace_type in ("heatmap", "contour", "histogram2d", "histogram2dcontour",
                   "surface", "choropleth", "choroplethmap", "densitymap"):
    fca_template.data[trace_type] = [{"colorscale": fca_colormap}]
```

Setting `diverging` to a sequential map follows "use it in every case", but it
gives diverging data no visual midpoint. Worth confirming that is intended.

Add one sampling helper, so nobody reaches for another colormap when they need N
discrete shades:

```python
def sample_fca_colormap(n_colors: int) -> list[str]:
    """`n_colors` evenly spaced hex colours from fca_colormap, ends included."""
    rgb_array = np.array(cm_data)
    positions = np.linspace(0, len(rgb_array) - 1, n_colors).round().astype(int)
    hex_colors = ["#" + "".join(f"{round(c * 255):02x}" for c in rgb_array[i]) for i in positions]
    return hex_colors
```

This also removes the caveat in `style.py` that `plotly.colors.sample_colorscale`
mishandles the 0-1 `rgb()` strings. fca-sankey already samples `cm_data` this
way in its own code and could use the helper.

### 7. README additions

A short "Colour and marker rules" section: blues and greys by default; highlight
blue only for attention; green then magenta red as accents; one continuous
colormap; the four marker shapes; the look-here diamond; thin plus, rarely; when
to use the slide profile. Change the quickstart and README example from
`sand_yellow` to `fca_blue` + `gray`.

## What breaks, and how to stage it

| Change | Breaking? | Who notices |
|--------|-----------|-------------|
| 0. Dot off | Yes, visually | Every `apply_header` caller loses the dot. Pinned consumers (msc-strategy at v0.1.1; battery-trains, fca-sankey at v0.1.0) are unaffected until they bump; token-cost tracks `main` unpinned and changes on its next lock refresh. |
| 1. New categorical order | Yes, visually | Every chart relying on the default colorway changes colour. |
| 3. Marker sequence | Yes, visually | Traces with markers change shape from the 2nd trace on. |
| 3/5. Template line width | Mild | Only if the standalone width moves off plotly's 2 px. |
| 6. Colormap defaults | Yes, visually | Charts that left `colorscale` unset change, which is the point. |
| 2, 4, 5 (new template), 6 (helper), 7 | No | Additive. |

Decision: change the defaults directly in 0.2.0, with no opt-in template.
Consumers that pin a tag keep the old look until they bump; `CHANGELOG.md`
lists what changes. Item 5's `title=None` for slides was not implemented.
