# Build pipeline — traps and fixes

Every item below cost time to find. None should be rediscovered.

## Interpreter

Use **`python3.13`**. `python3` is 3.11 on this container and the packages are
installed for 3.13 — a `pip install` that reports success will still fail to
import under `python3`.

```
pip install --break-system-packages reportlab pillow fonttools
python3.13 -c "import reportlab, PIL, fontTools; print('ok')"
```

## Fonts

Inter ships as **OTF with CFF outlines**, which ReportLab's `TTFont` cannot
read. Registration fails, and the build silently falls back to Helvetica —
which renders fine and is wrong.

TrueType builds are committed at `assets/fonts/`, converted with fontTools:

```python
from fontTools.ttLib import TTFont as FT, newTable
from fontTools.pens.ttGlyphPen import TTGlyphPen
f = FT("Inter-ExtraBold.otf"); gs = f.getGlyphSet()
glyf = {}
for g in f.getGlyphOrder():
    pen = TTGlyphPen(gs); gs[g].draw(pen); glyf[g] = pen.glyph()
t = newTable("glyf"); t.glyphOrder = f.getGlyphOrder(); t.glyphs = glyf
f["glyf"] = t; f["loca"] = newTable("loca")
f["head"].indexToLocFormat = 0
f["maxp"].tableVersion = 0x00010000   # plus zeroed max* fields
del f["CFF "]
f.sfntVersion = "\x00\x01\x00\x00"
f.save("Inter-ExtraBold.ttf")
```

Always confirm with `pdffonts`: the brand faces must show `emb yes`.

Inter sets larger than Times at the same point size. Dropping body copy from
10.5pt to ~9.6pt keeps a 6×9 page honest.

## Manuscript boundaries

Manuscript files carry production scaffolding — approval records at the top,
production status at the bottom. **Set explicit content boundaries**, or it
typesets into the book. `build_interior.py` runs from `## A Word from Major` to
`## Production status`.

## Glyphs

Base-14 PDF fonts have no emoji. A `✅` renders as a tofu box. Strip emoji
before typesetting.

## Transparent marks

Treatment depends on the mark's structure, not on preference:

- **A mark with a black interior** (the circular seal) needs a **geometric
  mask** — find its own outer ring and mask outside it. A luminance key hollows
  it out.
- **A mark that is only strokes** (unencircled MD/hat) needs a **luminance key**,
  then **un-premultiply**: `rgb = rgb * 255/alpha` for partial pixels. Without
  that, edge pixels keep their dark values and leave a halo on light grounds.

Supersample masks 4× and resize down; a hard ellipse edge aliases badly.

## Drawing a metaphor

If the brief says a form means something, **draw the form and then look at it**.
A bottleneck tapers — converging paths through a waist — it is not a line with a
dot on it. Two failures to watch for in generated fields:

- a field that stops on a straight line exposes its bounding box; fade the
  alpha to zero at both ends
- a hard switch between two colours leaves a visible seam; interpolate

## Verification

```
pdftoppm -png -r 110 -singlefile out.pdf preview   # then LOOK at it
pdffonts out.pdf        # brand faces, emb yes
pdftotext out.pdf -     # text extracts; no scaffolding leaked
pdfimages -list out.pdf # placed assets >= 300 ppi
```

A crude check produces confident wrong answers. Grepping push output for the
word "error" once reported a repository as write-denied when the real message
was a stale local branch.
