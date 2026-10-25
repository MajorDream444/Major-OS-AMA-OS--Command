#!/usr/bin/env python3
"""MAIM Academy — video backdrop.

Philosophy: docs/design/PHILOSOPHY_CONSTRICTED_FLOW.md
Tokens: .claude/skills/maim-brand-production/references/tokens.md

The subject sits in the centre. Two mirrored filament fields flow in from the
left and right edges and converge to a waist on either side of him, so the
frame says the thing the series says: everything narrows to one person. The
waists land outside the subject zone, so nothing crosses his silhouette.

The layout is left-right symmetric by construction, which means a horizontal
flip does not break it. Text is the exception, so a pre-mirrored variant is
built alongside: flip that one and the type reads correctly.

    python3.13 scripts/build_video_backdrop.py --out build/backdrop
"""

from __future__ import annotations

import argparse
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "assets" / "fonts"
MARK = ROOT / "assets" / "brand" / "MD-Circle-Transparent.png"

# Canonical MAIM design tokens v2.1
MAIM_BLACK = (5, 5, 5)
CROWN = (216, 175, 85)
LEGACY = (159, 116, 44)
CLARITY = (247, 244, 234)
SMOKE = (168, 168, 168)
SURFACE = (24, 24, 27)
BORDER = (39, 39, 42)

W, H = 1920, 1080
SS = 2                      # supersample factor

SUBJECT_HALF = 390          # keep-clear zone: 780px wide, centred
WAIST_OFFSET = 430          # where each field pinches, clear of the subject
WAIST_HALF = 26
EDGE_HALF = 470
TAPER = 1.55
N_LINES = 210
SAMPLES = 64


def lerp(a, b, k):
    k = max(0.0, min(1.0, k))
    return tuple(round(a[i] + (b[i] - a[i]) * k) for i in range(3))


def fade(t: float) -> float:
    """Dim at the frame edge, gathering toward the waist, then easing off.

    The peak sits short of the waist rather than on it. Peaking at the apex
    made two cones that read as headlights; easing off keeps it a flow.
    """
    head = min(1.0, t / 0.26) ** 1.2
    tail = 1.0 - 0.42 * max(0.0, (t - 0.80) / 0.20) ** 1.4
    return head * (0.20 + 0.80 * t ** 1.35) * tail


def draw_field(d: ImageDraw.ImageDraw, side: int, cy: float) -> None:
    """side -1 = flows in from the left, +1 = from the right."""
    rnd = random.Random(8821 if side < 0 else 8822)
    x_edge = 0 if side < 0 else W * SS
    x_waist = (W / 2 + side * WAIST_OFFSET) * SS
    span = x_waist - x_edge
    for i in range(N_LINES):
        u = (i / (N_LINES - 1)) * 2.0 - 1.0
        drift = rnd.uniform(-0.06, 0.06)
        phase = rnd.uniform(0, math.tau)
        amp = rnd.uniform(0.6, 2.6) * SS
        edge = abs(u) ** 0.8
        pts = []
        for s in range(SAMPLES + 1):
            t = s / SAMPLES
            half = (EDGE_HALF + (WAIST_HALF - EDGE_HALF) * (t ** TAPER)) * SS
            tremble = amp * math.sin(phase + t * 4.1) * (half / (EDGE_HALF * SS))
            pts.append((x_edge + t * span,
                        cy * SS + (u + drift * (1 - abs(u))) * half + tremble))
        base = (0.17 + 0.30 * (1 - edge)) * (0.34 + 0.66 * (1 - edge) ** 0.55)
        width = max(1, round((1.0 + 0.7 * (1 - edge)) * SS))
        for j in range(SAMPLES):
            t = (j + 0.5) / SAMPLES
            a = base * fade(t)
            if a <= 0.004:
                continue
            col = lerp(LEGACY, CROWN, t ** 0.6)
            d.line([pts[j], pts[j + 1]],
                   fill=col + (max(0, min(255, round(a * 255))),), width=width)


def tracked(d, text, font, cx, y, track, fill, anchor="c"):
    widths = [d.textlength(ch, font=font) for ch in text]
    total = sum(widths) + track * (len(text) - 1)
    x = cx - total / 2 if anchor == "c" else (cx if anchor == "l" else cx - total)
    for ch, w in zip(text, widths):
        d.text((x, y), ch, font=font, fill=fill)
        x += w + track
    return total


def panel(d, box, label, lines, font_l, font_b):
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, radius=10, fill=SURFACE + (190,), outline=BORDER + (255,), width=2)
    d.line([(x0 + 18, y0 + 46), (x0 + 58, y0 + 46)], fill=CROWN + (255,), width=3)
    d.text((x0 + 18, y0 + 16), label, font=font_l, fill=CROWN + (255,))
    y = y0 + 62
    for ln in lines:
        d.text((x0 + 18, y), ln, font=font_b, fill=CLARITY + (235,))
        y += 34


def build(mirror_text: bool, guides: bool) -> Image.Image:
    base = Image.new("RGB", (W * SS, H * SS), MAIM_BLACK)
    layer = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer, "RGBA")

    cy = H * 0.52            # the eye falls slightly below true centre
    draw_field(d, -1, cy)
    draw_field(d, +1, cy)

    base = Image.alpha_composite(base.convert("RGBA"), layer)
    img = base.resize((W, H), Image.LANCZOS).convert("RGBA")

    # A wide charcoal bloom behind the subject. Without it the centre is a
    # void and anyone in dark clothing disappears into it.
    bloom = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bloom, "RGBA")
    bcx, bcy, rad = W / 2, H * 0.60, 760
    for i in range(86):
        k = 1.0 - i / 86
        r = rad * (i + 1) / 86
        a = round(26 * (k ** 2.1))
        if a <= 0:
            continue
        bd.ellipse([(bcx - r, bcy - r * 0.86), (bcx + r, bcy + r * 0.86)],
                   fill=(34, 32, 28, a))
    img = Image.alpha_composite(img, bloom)

    # a soft floor so the lower thirds read as solid ground
    floor = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fd = ImageDraw.Draw(floor, "RGBA")
    for i in range(300):
        a = round(200 * (i / 300) ** 1.7)
        fd.line([(0, H - 300 + i), (W, H - 300 + i)], fill=(5, 5, 5, a))
    img = Image.alpha_composite(img, floor)

    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov, "RGBA")

    f_eyebrow = ImageFont.truetype(str(FONTS / "Inter-Medium.ttf"), 19)
    f_label = ImageFont.truetype(str(FONTS / "Inter-ExtraBold.ttf"), 17)
    f_body = ImageFont.truetype(str(FONTS / "Inter-Regular.ttf"), 23)
    f_name = ImageFont.truetype(str(FONTS / "Inter-ExtraBold.ttf"), 30)
    f_role = ImageFont.truetype(str(FONTS / "Inter-Regular.ttf"), 19)
    f_cta = ImageFont.truetype(str(FONTS / "Inter-Medium.ttf"), 24)

    # top rule and channel mark
    d.line([(72, 74), (W - 72, 74)], fill=BORDER + (255,), width=2)
    tracked(d, "MAIM ACADEMY", f_eyebrow, 72, 44, 5.0, CROWN + (255,), anchor="l")
    tracked(d, "BUILD SOMETHING THAT RUNS", f_eyebrow, W - 72, 44, 4.0,
            SMOKE + (215,), anchor="r")

    # name lockup, lower right — the one asymmetric element, and the reason
    # a mirrored variant exists
    if MARK.is_file():
        m = Image.open(MARK).convert("RGBA").resize((104, 104), Image.LANCZOS)
        ov.alpha_composite(m, (W - 72 - 104, H - 286))
    d.text((W - 72, H - 170), "MAJOR DREAM WILLIAMS", font=f_name,
           fill=CLARITY + (255,), anchor="ra")
    d.text((W - 72, H - 132), "Founder · AMA Solutions Corp", font=f_role,
           fill=SMOKE + (225,), anchor="ra")

    # information panel, lower left — fill or delete per episode
    panel(d, (72, H - 300, 72 + 430, H - 128), "THIS EPISODE",
          ["Episode title goes here", "One line of context"], f_label, f_body)

    # call to action, bottom rule
    d.line([(72, H - 96), (W - 72, H - 96)], fill=CROWN + (120,), width=2)
    # Reserve, not buy. Reserving is free; the payment link goes out 11 Nov.
    d.text((72, H - 76), "Reserve your spot  ·  20 spots  ·  11 November",
           font=f_cta, fill=CLARITY + (240,))
    d.text((W - 72, H - 76), "academy.majoraimindset.com/reserve", font=f_cta,
           fill=CROWN + (255,), anchor="ra")

    if mirror_text:
        ov = ov.transpose(Image.FLIP_LEFT_RIGHT)

    img = Image.alpha_composite(img, ov)

    if guides:
        g = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        gd = ImageDraw.Draw(g, "RGBA")
        gd.rectangle([(W // 2 - SUBJECT_HALF, 96), (W // 2 + SUBJECT_HALF, H - 310)],
                     outline=(163, 230, 53, 210), width=3)
        gd.line([(W // 2, 0), (W // 2, H)], fill=(163, 230, 53, 90), width=1)
        gf = ImageFont.truetype(str(FONTS / "Inter-Medium.ttf"), 20)
        gd.text((W // 2, 112), "KEEP CLEAR — SUBJECT", font=gf,
                fill=(163, 230, 53, 230), anchor="ma")
        img = Image.alpha_composite(img, g)

    return img.convert("RGB")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="build/backdrop")
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)

    jobs = [
        ("maim-academy-backdrop-1920x1080.png", False, False),
        ("maim-academy-backdrop-mirrored-1920x1080.png", True, False),
        ("maim-academy-backdrop-GUIDES-1920x1080.png", False, True),
    ]
    for name, mirror, guides in jobs:
        img = build(mirror, guides)
        img.save(out / name)
        print(f"wrote {out / name}  ({(out / name).stat().st_size // 1024} KB)")

    # 4K, no guides
    for name, mirror in (("maim-academy-backdrop-3840x2160.png", False),
                         ("maim-academy-backdrop-mirrored-3840x2160.png", True)):
        img = build(mirror, False).resize((3840, 2160), Image.LANCZOS)
        img.save(out / name)
        print(f"wrote {out / name}  ({(out / name).stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
