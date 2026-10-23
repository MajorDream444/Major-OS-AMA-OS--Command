#!/usr/bin/env python3
"""MAIM Academy YouTube channel banner.

Philosophy: docs/design/PHILOSOPHY_CONSTRICTED_FLOW.md

YouTube crops this three ways. TV sees the whole 2560x1440, desktop sees a
centre strip, phones see only the 1235x338 safe area. So the constriction runs
the full width for the people who see it, and every legible element sits inside
the safe box for everyone else.

    python3.13 scripts/build_youtube_banner.py --out build/banner
"""
from __future__ import annotations
import argparse, math, random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 2560, 1440
SAFE_W, SAFE_H = 1235, 338
SAFE = ((W - SAFE_W) // 2, (H - SAFE_H) // 2, (W + SAFE_W) // 2, (H + SAFE_H) // 2)

BLACK, CROWN, LEGACY = (5, 5, 5), (216, 175, 85), (159, 116, 44)
CLARITY, SMOKE = (247, 244, 234), (168, 168, 168)

ROOT = Path(__file__).resolve().parent.parent
FONTS, SEAL = ROOT / "assets" / "fonts", ROOT / "assets" / "brand" / "MD-Circle-Transparent.png"
F = lambda n, s: ImageFont.truetype(str(FONTS / n), s)


def flow(img):
    """The constriction, laid on its side and run across the full width."""
    d = ImageDraw.Draw(img, "RGBA")
    rnd = random.Random(90210)
    cy, cx = H / 2, W / 2
    half_end, half_waist, taper = H * 0.50, 5.0, 2.05
    for i in range(460):
        u = (i / 459) * 2 - 1
        drift, phase = rnd.uniform(-.05, .05), rnd.uniform(0, math.tau)
        amp, edge = rnd.uniform(1.4, 5.2), abs(u) ** .82
        pts = []
        for s in range(121):
            t = s / 120
            x = t * W
            p = abs(t - .5) / .5
            hw = half_waist + (half_end - half_waist) * (p ** taper)
            pts.append((x, cy + (u + drift * (1 - abs(u))) * hw
                        + amp * math.sin(phase + t * 5.1) * (hw / half_end)))
        base = (.62 + .78 * (1 - edge)) * (.34 + .66 * (1 - edge) ** .6)
        for j in range(120):
            t = (j + .5) / 120
            glow = (1 - abs(t - .5) / .5) ** 2.3
            # fade into the ground at both ends so no bounding edge shows
            fade = (min(1, t / .14) ** 1.3) * (min(1, (1 - t) / .14) ** 1.3)
            a = int(255 * max(0, min(1, base * (.14 + .86 * glow) * fade)))
            k = glow ** .55
            col = (int(LEGACY[0] + (CROWN[0] - LEGACY[0]) * k),
                   int(LEGACY[1] + (CROWN[1] - LEGACY[1]) * k),
                   int(LEGACY[2] + (CROWN[2] - LEGACY[2]) * k), a)
            d.line([pts[j], pts[j + 1]], fill=col, width=3)


def tracked(d, text, font, fill, cx, y, track):
    w = sum(d.textlength(c, font=font) + track for c in text) - track
    x = cx - w / 2
    for c in text:
        d.text((x, y), c, font=font, fill=fill)
        x += d.textlength(c, font=font) + track


def build(guides=False):
    img = Image.new("RGB", (W, H), BLACK)
    flow(img)
    d = ImageDraw.Draw(img)

    # The waist is already the emptiest part of the field, so the type sits in a
    # clearing rather than on a slab. A soft radial pool only deepens what is
    # there; a hard band would hide the constriction, which is the whole image.
    from PIL import ImageFilter
    pool = Image.new("L", (W, H), 0)
    ImageDraw.Draw(pool).ellipse([W // 2 - 760, H // 2 - 250, W // 2 + 760, H // 2 + 250],
                                 fill=200)
    pool = pool.filter(ImageFilter.GaussianBlur(120))
    img = Image.composite(Image.new("RGB", (W, H), BLACK), img, pool)
    d = ImageDraw.Draw(img)

    cx = W // 2
    s = Image.open(SEAL).convert("RGBA"); sz = 108
    s = s.resize((sz, sz), Image.LANCZOS)
    img.paste(s, (cx - sz // 2, SAFE[1] - 4), s)

    tracked(d, "MAIM ACADEMY", F("Inter-ExtraBold.ttf", 74), CLARITY, cx, SAFE[1] + 110, 7)
    tracked(d, "FIX THE SYSTEM.  FIX THE INCOME.", F("Inter-Medium.ttf", 26), CROWN,
            cx, SAFE[1] + 198, 5)

    # The banner has to do a job, so it carries the one honest ask. Enrollment is
    # closed, so it points at the guide and the waitlist rather than a checkout.
    d.line([cx - 300, SAFE[1] + 242, cx + 300, SAFE[1] + 242], fill=LEGACY, width=2)
    tracked(d, "FREE GUIDE  ·  FOUNDING COHORT LIST", F("Inter-Medium.ttf", 21),
            SMOKE, cx, SAFE[1] + 258, 4)
    tracked(d, "MAJORAIMINDSET.COM", F("Inter-ExtraBold.ttf", 30), CROWN,
            cx, SAFE[1] + 288, 6)

    if guides:
        g = ImageDraw.Draw(img)
        g.rectangle(SAFE, outline=(230, 60, 60), width=4)
        g.rectangle([0, (H - 423) // 2, W - 1, (H + 423) // 2], outline=(60, 140, 230), width=4)
        g.text((SAFE[0] + 10, SAFE[1] - 46), "SAFE AREA 1235x338 — all devices",
               font=F("Inter-Medium.ttf", 28), fill=(230, 60, 60))
        g.text((20, (H - 423) // 2 + 10), "desktop crop 2560x423",
               font=F("Inter-Medium.ttf", 28), fill=(60, 140, 230))
    return img


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--out", default="build/banner")
    a = ap.parse_args(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    build(False).save(out / "maim-academy-banner-2560x1440.png", optimize=True)
    build(True).save(out / "_safe-area-check.png", optimize=True)
    for p in sorted(out.glob("*.png")):
        print(f"  {p.name:<42} {p.stat().st_size // 1024:>5} KB")
