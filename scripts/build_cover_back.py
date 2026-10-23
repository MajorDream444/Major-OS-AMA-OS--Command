#!/usr/bin/env python3
"""Major Moves Volume 1 — back cover.

Philosophy: docs/design/PHILOSOPHY_CONSTRICTED_FLOW.md

The front carries the whole constriction. The back carries only what left it —
the release, inverted and quiet, rising from the foot of the page. The same law,
seen after the fact. It never competes with the copy; it is the ground the copy
sits on.

    python3.13 scripts/build_cover_back.py --output build/back.pdf
"""

from __future__ import annotations

import argparse
import math
import random
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as rl_canvas

W, H = 6 * inch, 9 * inch
M = 0.62 * inch

# Canonical MAIM design tokens v2.1
BLACK = colors.HexColor("#050505")
CROWN = colors.HexColor("#D8AF55")
LEGACY = colors.HexColor("#9F742C")
CLARITY = colors.HexColor("#F7F4EA")
SMOKE = colors.HexColor("#A8A8A8")

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "assets" / "fonts"
MARK = ROOT / "assets" / "brand" / "MD-Circle-Transparent.png"
PORTRAIT = ROOT / "assets" / "brand" / "Major-Author-Photo.JPG"

for _n, _f in (("XB", "Inter-ExtraBold.ttf"), ("REG", "Inter-Regular.ttf"),
               ("MED", "Inter-Medium.ttf"), ("IT", "Inter-MediumItalic.ttf")):
    pdfmetrics.registerFont(TTFont(_n, str(FONTS / _f)))

HOOK = "If everything stops when you stop—what exactly have you built?"

BLURB = [
    ("lead", "Most founders think they have a time problem."),
    ("body", "They buy planners. They wake earlier. They get ruthless with the "
             "calendar, and none of it holds — because it was never a time "
             "problem. It is a structure problem."),
    ("body", "There is a difference between being busy and being load-bearing. "
             "Busy means your day is full. Load-bearing means the whole thing "
             "falls down when you step away."),
    ("body", "This is a short book about the second one: why capable people "
             "become the narrowest part of their own business, why it feels like "
             "competence while it happens, and what to hand over first."),
    ("quote", "“You willingly become the bottleneck.”"),
    ("body", "Five chapters, five exercises, and one assignment you can finish "
             "this week."),
]

BIO = ("Major Dream Williams was born in New York City, raised in The Bronx and "
       "Mount Vernon, and shaped by a Jamaican immigrant family. Founder of AMA "
       "Solutions Corp and architect of Foundry OS, he builds systems organised "
       "around one principle: ownership over dependency.")

# --- the released flow -------------------------------------------------

N_LINES = 300
SAMPLES = 110
Y_SRC = 2.62 * inch          # the waist, off the bottom of the page
Y_END = 0.30 * inch
HALF_SRC = 0.075 * inch
HALF_END = 2.90 * inch
TAPER = 1.34


def half_width(t: float) -> float:
    return HALF_SRC + (HALF_END - HALF_SRC) * (t ** TAPER)


def fade(t: float) -> float:
    """Quiet at the source, dissolved before the page edge."""
    return (min(1.0, t / 0.26) ** 1.5) * (min(1.0, (1.0 - t) / 0.34) ** 1.4)


def lerp(a, b, k):
    k = max(0.0, min(1.0, k))
    return colors.Color(a.red + (b.red - a.red) * k,
                        a.green + (b.green - a.green) * k,
                        a.blue + (b.blue - a.blue) * k)


def draw_release(c):
    rnd = random.Random(4471)
    cx = W / 2.0
    span = Y_SRC - Y_END
    for i in range(N_LINES):
        u = (i / (N_LINES - 1)) * 2.0 - 1.0
        drift = rnd.uniform(-0.05, 0.05)
        phase = rnd.uniform(0, math.tau)
        amp = rnd.uniform(0.0012, 0.0048) * inch * 2.0
        edge = abs(u) ** 0.82
        pts = []
        for s in range(SAMPLES + 1):
            t = s / SAMPLES
            hw = half_width(t)
            tremble = amp * math.sin(phase + t * 4.4) * (hw / HALF_END)
            pts.append((cx + (u + drift * (1 - abs(u))) * hw + tremble,
                        Y_SRC - t * span))
        # kept well under the front's brightness: this is a footnote, not a claim
        base = (0.17 + 0.26 * (1 - edge)) * (0.30 + 0.70 * (1 - edge) ** 0.6)
        c.setLineWidth(0.22 + 0.13 * (1 - edge))
        for j in range(SAMPLES):
            t = (j + 0.5) / SAMPLES
            glow = (1.0 - t) ** 2.0
            c.setStrokeColor(lerp(LEGACY, CROWN, glow ** 0.55))
            c.setStrokeAlpha(max(0.0, min(1.0, base * (0.16 + 0.84 * glow) * fade(t))))
            c.line(*pts[j], *pts[j + 1])
    c.setStrokeAlpha(1)


# --- type --------------------------------------------------------------

def wrap(c, text, font, size, width):
    out, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if pdfmetrics.stringWidth(trial, font, size) <= width:
            line = trial
        else:
            out.append(line); line = word
    if line:
        out.append(line)
    return out


def tracked(c, text, font, size, cx, y, track, fill):
    c.setFont(font, size); c.setFillColor(fill)
    total = sum(pdfmetrics.stringWidth(ch, font, size) + track for ch in text) - track
    x = cx - total / 2.0
    for ch in text:
        c.drawString(x, y, ch); x += pdfmetrics.stringWidth(ch, font, size) + track


def draw(c):
    c.setFillColor(BLACK); c.rect(0, 0, W, H, stroke=0, fill=1)
    draw_release(c)

    tracked(c, "MAJOR MOVES", "MED", 6.4, W / 2, H - M - 0.04 * inch, 2.5, LEGACY)

    y = H - M - 0.52 * inch
    c.setFillColor(CROWN); c.setFont("IT", 10.5)
    for ln in wrap(c, HOOK, "IT", 10.5, W - 2 * M):
        c.drawString(M, y, ln); y -= 15.4
    y -= 0.16 * inch

    for kind, para in BLURB:
        if kind == "lead":
            size, fnt, col = 12.6, "XB", CLARITY
        elif kind == "quote":
            y -= 0.07 * inch
            size, fnt, col = 10.6, "IT", CROWN
        else:
            size, fnt, col = 9.3, "REG", SMOKE
        c.setFillColor(col)
        for ln in wrap(c, para, fnt, size, W - 2 * M):
            c.setFont(fnt, size); c.drawString(M, y, ln); y -= size * 1.60
        y -= 0.10 * inch

    # author
    y -= 0.04 * inch
    c.setStrokeColor(LEGACY); c.setStrokeAlpha(0.5); c.setLineWidth(0.5)
    c.line(M, y, W - M, y); c.setStrokeAlpha(1)
    y -= 0.28 * inch

    pw = 0.98 * inch
    if PORTRAIT.is_file():
        from PIL import Image as PILImage
        iw, ih = PILImage.open(PORTRAIT).size
        ph = pw * ih / iw
        c.drawImage(ImageReader(str(PORTRAIT)), M, y - ph, pw, ph,
                    mask="auto", preserveAspectRatio=True)
        tx = M + pw + 0.22 * inch
    else:
        tx = M
    tw = W - M - tx
    ty = y - 0.02 * inch
    c.setFillColor(SMOKE)
    for ln in wrap(c, BIO, "REG", 8.0, tw):
        c.setFont("REG", 8.0); c.drawString(tx, ty, ln); ty -= 11.4

    if MARK.is_file():
        s = 0.46 * inch
        c.drawImage(ImageReader(str(MARK)), W - M - s, M + 0.86 * inch, s, s,
                    mask="auto", preserveAspectRatio=True)

    # reserved, never invented
    bw, bh = 1.75 * inch, 0.62 * inch
    c.setStrokeColor(SMOKE); c.setStrokeAlpha(0.45); c.setLineWidth(0.5)
    c.setDash(2, 2); c.rect(M, M + 0.06 * inch, bw, bh, stroke=1, fill=0)
    c.setDash(); c.setStrokeAlpha(1)
    c.setFillColor(SMOKE); c.setFillAlpha(0.6); c.setFont("REG", 5.4)
    c.drawCentredString(M + bw / 2, M + 0.06 * inch + bh / 2 - 2,
                        "ISBN / BARCODE RESERVED")
    c.setFont("REG", 5.6)
    c.drawRightString(W - M, M + 0.12 * inch, "majoraimindset.com")
    c.setFillAlpha(1)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="build/Volume-01-back-cover.pdf")
    a = ap.parse_args()
    out = Path(a.output); out.parent.mkdir(parents=True, exist_ok=True)
    c = rl_canvas.Canvas(str(out), pagesize=(W, H))
    c.setTitle("You Are the System — back")
    draw(c); c.showPage(); c.save()
    print(f"wrote {out}  ({out.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
