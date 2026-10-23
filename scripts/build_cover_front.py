#!/usr/bin/env python3
"""Major Moves Volume 1 — front cover.

Philosophy: docs/design/PHILOSOPHY_CONSTRICTED_FLOW.md

The bottleneck is not described, it is drawn. Four hundred filaments descend
the page under one law, each with its own small deviation, and are forced
through a single narrowing placed above true centre. What leaves the waist is
narrower than what entered it, because nothing passes through a constriction
unchanged.

Tokens are canonical MAIM v2.1. The MD seal is the approved original, scaled
proportionately and never redrawn.

    python3.13 scripts/build_cover_front.py --output build/front.pdf
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

# Canonical MAIM design tokens v2.1
BLACK = colors.HexColor("#050505")      # maimBlack
CROWN = colors.HexColor("#D8AF55")      # crownGold
LEGACY = colors.HexColor("#9F742C")     # legacyGold
CLARITY = colors.HexColor("#F7F4EA")    # clarityWhite
SMOKE = colors.HexColor("#A8A8A8")      # smokeGray

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "assets" / "fonts"
MARK = ROOT / "assets" / "brand" / "MD-Circle-Transparent.png"

for _n, _f in (("XB", "Inter-ExtraBold.ttf"), ("REG", "Inter-Regular.ttf"),
               ("MED", "Inter-Medium.ttf"), ("IT", "Inter-MediumItalic.ttf")):
    pdfmetrics.registerFont(TTFont(_n, str(FONTS / _f)))

# --- the field ---------------------------------------------------------

N_LINES = 420
SAMPLES = 150

Y_TOP = H - 1.62 * inch          # field begins below the seal and series line
Y_BOT = 2.28 * inch              # and ends above the title plinth
T_WAIST = 0.455                  # above true centre: the eye falls, never rests
HALF_TOP = 2.18 * inch
HALF_BOT = 1.46 * inch           # the release is narrower than the origin
HALF_WAIST = 0.030 * inch
TAPER = 1.72                     # how urgently breadth is surrendered


def half_width(t: float) -> float:
    """Breadth of the field at parametric depth t, 0 = top, 1 = bottom."""
    if t <= T_WAIST:
        p = ((T_WAIST - t) / T_WAIST) ** TAPER
        return HALF_WAIST + (HALF_TOP - HALF_WAIST) * p
    p = ((t - T_WAIST) / (1.0 - T_WAIST)) ** TAPER
    return HALF_WAIST + (HALF_BOT - HALF_WAIST) * p


def lerp_colour(a, b, k: float):
    """Blend two tokens smoothly. A hard switch leaves a seam across the field."""
    k = max(0.0, min(1.0, k))
    return colors.Color(a.red + (b.red - a.red) * k,
                        a.green + (b.green - a.green) * k,
                        a.blue + (b.blue - a.blue) * k)


def fade(t: float) -> float:
    """Dissolve the field into the ground at both ends.

    Without this the filaments stop on a straight line and the bounding box
    becomes visible, which reads as a clipped rectangle rather than a form
    emerging from darkness."""
    head = min(1.0, t / 0.17) ** 1.25
    tail = min(1.0, (1.0 - t) / 0.21) ** 1.15
    return head * tail


def draw_field(c: rl_canvas.Canvas) -> None:
    rnd = random.Random(1123)          # deterministic: the same hand every time
    cx = W / 2.0
    span = Y_TOP - Y_BOT

    for i in range(N_LINES):
        u = (i / (N_LINES - 1)) * 2.0 - 1.0          # -1 .. 1
        # Each filament obeys the law with its own small deviation.
        drift = rnd.uniform(-0.055, 0.055)
        phase = rnd.uniform(0, math.tau)
        amp = rnd.uniform(0.0016, 0.0062) * inch * 2.2
        edge = abs(u) ** 0.82                        # outer paths carry more air

        pts = []
        for s in range(SAMPLES + 1):
            t = s / SAMPLES
            y = Y_TOP - t * span
            hw = half_width(t)
            # breathe, but fall silent at the waist where there is no room
            tremble = amp * math.sin(phase + t * 5.1) * (hw / HALF_TOP)
            x = cx + (u + drift * (1.0 - abs(u))) * hw + tremble
            pts.append((x, y))

        # Light behaves like metal: brightest where compression is greatest.
        # Outer filaments carry less light, so the field has no hard flank.
        base = (0.34 + 0.50 * (1.0 - edge)) * (0.30 + 0.70 * (1.0 - edge) ** 0.6)
        c.setLineWidth(0.24 + 0.17 * (1.0 - edge))

        # draw in segments so alpha can follow depth
        for j in range(SAMPLES):
            t = (j + 0.5) / SAMPLES
            d = abs(t - T_WAIST) / max(T_WAIST, 1 - T_WAIST)
            glow = (1.0 - d) ** 2.3
            a = base * (0.14 + 0.86 * glow) * fade(t)
            c.setStrokeColor(lerp_colour(LEGACY, CROWN, glow ** 0.55))
            c.setStrokeAlpha(max(0.0, min(1.0, a)))
            x0, y0 = pts[j]
            x1, y1 = pts[j + 1]
            c.line(x0, y0, x1, y1)

    c.setStrokeAlpha(1)


# --- typography --------------------------------------------------------

def tracked(c, text, font, size, cx, y, track, fill):
    c.setFont(font, size)
    c.setFillColor(fill)
    total = sum(pdfmetrics.stringWidth(ch, font, size) + track for ch in text) - track
    x = cx - total / 2.0
    for ch in text:
        c.drawString(x, y, ch)
        x += pdfmetrics.stringWidth(ch, font, size) + track


def draw(c: rl_canvas.Canvas) -> None:
    c.setFillColor(BLACK)
    c.rect(0, 0, W, H, stroke=0, fill=1)

    draw_field(c)

    # seal — approved original, proportionate, never redrawn
    if MARK.is_file():
        s = 0.74 * inch
        c.drawImage(ImageReader(str(MARK)), (W - s) / 2, H - 1.12 * inch, s, s,
                    mask="auto", preserveAspectRatio=True)

    tracked(c, "MAJOR MOVES", "MED", 6.6, W / 2, H - 1.33 * inch, 2.5, LEGACY)

    # the plinth: type as architecture, holding the base of the field
    c.setFillColor(CLARITY)
    c.setFont("XB", 40)
    c.drawCentredString(W / 2, 1.42 * inch, "YOU ARE")
    c.drawCentredString(W / 2, 0.98 * inch, "THE SYSTEM")

    # a hairline, the width of the released flow
    c.setStrokeColor(LEGACY)
    c.setStrokeAlpha(0.55)
    c.setLineWidth(0.5)
    c.line(W / 2 - 0.42 * inch, 0.80 * inch, W / 2 + 0.42 * inch, 0.80 * inch)
    c.setStrokeAlpha(1)

    tracked(c, "MAJOR DREAM WILLIAMS", "MED", 6.4, W / 2, 0.58 * inch, 2.2, SMOKE)

    # specimen annotation, as if from a discipline that does not exist
    c.setFont("REG", 5.2)
    c.setFillColor(LEGACY)
    c.setFillAlpha(0.68)
    c.drawString(0.42 * inch, 0.40 * inch, "VOL. I")
    c.drawRightString(W - 0.42 * inch, 0.40 * inch, "FIG. 1 — CONSTRICTED FLOW")
    c.setFillAlpha(1)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="build/Volume-01-front-cover.pdf")
    a = ap.parse_args()
    out = Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)

    c = rl_canvas.Canvas(str(out), pagesize=(W, H))
    c.setTitle("You Are the System")
    draw(c)
    c.showPage()
    c.save()
    print(f"wrote {out}  ({out.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
