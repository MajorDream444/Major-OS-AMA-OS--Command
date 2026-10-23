#!/usr/bin/env python3
"""Text-led cover directions for Major Moves Volume 1.

Two alternatives, front and back for each, as the MAIM Integrity design lock
requires. No illustration: the typography, the brand colours and the exact MD
mark carry it. Integrity's six artworks are NOT used here — they belong to the
Integrity collection.

The mark and the portrait are placed from the verified v0.4 originals,
unaltered except for proportionate scaling. Nothing is redrawn or regenerated.

Review reference at 6x9in. NOT print-ready: a physical cover needs final page
count, printer trim, paper, binding, bleed and a real barcode before a spine
can be calculated. Barcode space is reserved, never invented.

    python3.13 scripts/build_cover.py --output build/covers.pdf
"""

from __future__ import annotations

import argparse
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as rl_canvas

W, H = 6 * inch, 9 * inch
M = 0.62 * inch

# Canonical MAIM design tokens v2.1 — major-ai-os/data/design-tokens.json
GROUND = colors.HexColor("#050505")   # maimBlack
GOLD = colors.HexColor("#D8AF55")     # crownGold
GOLD_DEEP = colors.HexColor("#9F742C")  # legacyGold
TEXT = colors.HexColor("#F7F4EA")     # clarityWhite
MUTED = colors.HexColor("#A8A8A8")    # smokeGray

# Inter ExtraBold is on DESIGN.md's canonical display list and ships here, so
# the brand faces are used directly rather than substituted.
# ReportLab cannot read Inter's CFF-outline OTFs, so TrueType builds are
# committed alongside, converted from the system OTFs with fontTools.
_INTER = Path(__file__).resolve().parent.parent / "assets" / "fonts"
for _name, _file in (("Inter-XB", "Inter-ExtraBold.ttf"),
                     ("Inter", "Inter-Regular.ttf"),
                     ("Inter-Med", "Inter-Medium.ttf"),
                     ("Inter-It", "Inter-MediumItalic.ttf")):
    pdfmetrics.registerFont(TTFont(_name, str(_INTER / _file)))

DISPLAY = "Inter-XB"
BODY = "Inter"
BODY_I = "Inter-It"
MONO = "Inter-Med"

ASSETS = Path(__file__).resolve().parent.parent / "assets" / "brand"
MARK = ASSETS / "MD-Circle-Original.png"
PORTRAIT = ASSETS / "Major-Author-Photo.JPG"

TITLE_1, TITLE_2 = "YOU ARE", "THE SYSTEM"
SERIES = "MAJOR MOVES   ·   VOLUME ONE"
AUTHOR = "MAJOR DREAM WILLIAMS"
QUESTION = ("If everything stops when you stop—", "what exactly have you built?")

BLURB = [
    "Most founders think they have a time problem.",
    "",
    "They buy planners. They wake earlier. They get ruthless with the calendar,"
    " and none of it holds, because it was never a time problem. It is a"
    " structure problem.",
    "",
    "There is a difference between being busy and being load-bearing. Busy"
    " means your day is full. Load-bearing means the whole thing falls down"
    " when you step away.",
    "",
    "This is a short book about the second one — why capable people become"
    " the narrowest part of their own business, why it feels like competence"
    " while it happens, and what to hand over first.",
    "",
    "It comes with a workbook, five exercises and one assignment you can"
    " finish this week.",
]

BIO = ("Major Dream Williams was born in New York City, raised in The Bronx and "
       "Mount Vernon, and shaped by a Jamaican immigrant family. Founder of AMA "
       "Solutions Corp and architect of Foundry OS, he builds systems organised "
       "around one principle: ownership over dependency.")


def wrap(c, text, font, size, width):
    c.setFont(font, size)
    out, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if c.stringWidth(trial, font, size) <= width:
            line = trial
        else:
            out.append(line)
            line = word
    if line:
        out.append(line)
    return out


def ground(c):
    c.setFillColor(GROUND)
    c.rect(0, 0, W, H, stroke=0, fill=1)


def mark(c, x, y, size):
    if MARK.is_file():
        c.drawImage(ImageReader(str(MARK)), x, y, size, size,
                    mask="auto", preserveAspectRatio=True)


# ----------------------------------------------------------------- fronts

def front_a(c):
    """Direction A — The Neck. A gold rule that narrows, then releases."""
    ground(c)
    mark(c, (W - 1.0 * inch) / 2, H - M - 1.0 * inch, 1.0 * inch)

    c.setFillColor(GOLD)
    c.setFont(MONO, 7)
    c.drawCentredString(W / 2, H - M - 1.42 * inch, SERIES)

    c.setFillColor(TEXT)
    c.setFont(DISPLAY, 42)
    c.drawCentredString(W / 2, H / 2 + 0.52 * inch, TITLE_1)
    c.drawCentredString(W / 2, H / 2 - 0.08 * inch, TITLE_2)

    # the bottleneck, drawn: wide, pinched, wide again
    cy = H / 2 - 0.72 * inch
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.1)
    for i, (x0, x1) in enumerate([(W / 2 - 1.5 * inch, W / 2 - 0.22 * inch),
                                  (W / 2 + 0.22 * inch, W / 2 + 1.5 * inch)]):
        c.line(x0, cy, x1, cy)
    c.setFillColor(GOLD)
    c.circle(W / 2, cy, 2.4, stroke=0, fill=1)

    c.setFillColor(MUTED)
    c.setFont(BODY_I, 11)
    c.drawCentredString(W / 2, cy - 0.52 * inch, QUESTION[0])
    c.drawCentredString(W / 2, cy - 0.76 * inch, QUESTION[1])

    c.setFillColor(TEXT)
    c.setFont(DISPLAY, 10.5)
    c.drawCentredString(W / 2, M + 0.18 * inch, AUTHOR)
    c.showPage()


def front_b(c):
    """Direction B — The Question. The question leads; the title answers."""
    ground(c)
    c.setFillColor(GOLD)
    c.setFont(MONO, 7)
    c.drawString(M, H - M - 0.1 * inch, SERIES)
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.8)
    c.line(M, H - M - 0.3 * inch, W - M, H - M - 0.3 * inch)

    c.setFillColor(TEXT)
    y = H - M - 1.35 * inch
    for ln in ["If everything", "stops when", "you stop —"]:
        c.setFont(BODY_I, 27)
        c.drawString(M, y, ln)
        y -= 0.44 * inch
    c.setFillColor(GOLD)
    for ln in ["what exactly", "have you built?"]:
        c.setFont(BODY_I, 27)
        c.drawString(M, y, ln)
        y -= 0.44 * inch

    mark(c, W - M - 0.82 * inch, M + 1.52 * inch, 0.82 * inch)

    c.setFillColor(TEXT)
    c.setFont(DISPLAY, 29)
    c.drawString(M, M + 0.86 * inch, TITLE_1)
    c.drawString(M, M + 0.44 * inch, TITLE_2)

    c.setFillColor(MUTED)
    c.setFont(DISPLAY, 9.5)
    c.drawString(M, M - 0.02 * inch, AUTHOR)
    c.showPage()


# ------------------------------------------------------------------ backs

def back(c, label):
    ground(c)
    c.setFillColor(GOLD)
    c.setFont(MONO, 7)
    c.drawString(M, H - M + 0.04 * inch, f"{SERIES}    ·    BACK {label}")

    y = H - M - 0.42 * inch
    for para in BLURB:
        if not para:
            y -= 0.1 * inch
            continue
        first = para.startswith("Most founders")
        c.setFillColor(TEXT if first else MUTED)
        size = 11.5 if first else 9.6
        for ln in wrap(c, para, BODY, size, W - 2 * M):
            c.setFont(BODY, size)
            c.drawString(M, y, ln)
            y -= size * 1.52
        y -= 0.04 * inch

    # author block
    y -= 0.12 * inch
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.6)
    c.line(M, y, W - M, y)
    y -= 0.26 * inch

    px, pw = M, 0.92 * inch
    if PORTRAIT.is_file():
        from PIL import Image as PILImage
        iw, ih = PILImage.open(PORTRAIT).size
        ph = pw * ih / iw
        c.drawImage(ImageReader(str(PORTRAIT)), px, y - ph, pw, ph,
                    mask="auto", preserveAspectRatio=True)
        tx, tw = px + pw + 0.2 * inch, W - M - (px + pw + 0.2 * inch)
    else:
        tx, tw = M, W - 2 * M

    ty = y - 0.04 * inch
    c.setFillColor(MUTED)
    for ln in wrap(c, BIO, BODY, 8.2, tw):
        c.setFont(BODY, 8.2)
        c.drawString(tx, ty, ln)
        ty -= 11.6

    mark(c, W - M - 0.52 * inch, M + 0.92 * inch, 0.52 * inch)

    # Reserved barcode area. No identifier is invented.
    bw, bh = 1.75 * inch, 0.62 * inch
    c.setStrokeColor(MUTED)
    c.setLineWidth(0.5)
    c.setDash(2, 2)
    c.rect(M, M + 0.1 * inch, bw, bh, stroke=1, fill=0)
    c.setDash()
    c.setFillColor(MUTED)
    c.setFont(MONO, 5.6)
    c.drawCentredString(M + bw / 2, M + 0.1 * inch + bh / 2 - 2, "ISBN / BARCODE RESERVED")

    c.setFillColor(MUTED)
    c.setFont(MONO, 5.6)
    c.drawRightString(W - M, M + 0.16 * inch, "majoraimindset.com")
    c.showPage()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="build/Volume-01-cover-directions.pdf")
    a = ap.parse_args()
    out = Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)

    c = rl_canvas.Canvas(str(out), pagesize=(W, H))
    c.setTitle("You Are the System — cover directions")
    front_a(c); back(c, "A")
    front_b(c); back(c, "B")
    c.save()

    print(f"wrote {out}  ({out.stat().st_size // 1024} KB)")
    print("Two text-led directions, front and back each. Review reference, not print-ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
