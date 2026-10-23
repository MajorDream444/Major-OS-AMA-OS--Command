#!/usr/bin/env python3
"""Catalogue and storefront imagery for a MAIM product, from one cover.

Export sizes come from the canonical tokens in
major-ai-os/data/design-tokens.json. Each format is composed for its own
aspect ratio rather than crudely cropped, because a cover squeezed into a
square loses the thing that made it a cover.

    python3.13 scripts/build_catalog_images.py \
        --cover build/Volume-01-front-cover.pdf \
        --out build/catalog

Produces:
    pdf-cover-1600x2400.png     store/library hero
    stripe-1024x1024.png        Stripe product image (square, safe margins)
    instagram-feed-1080x1350.png
    instagram-square-1080x1080.png
    instagram-story-1080x1920.png
    youtube-thumb-1280x720.png
    open-graph-1200x630.png     link previews
"""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# Canonical MAIM design tokens v2.1
BLACK = (5, 5, 5)
CROWN = (216, 175, 85)
LEGACY = (159, 116, 44)
CLARITY = (247, 244, 234)
SMOKE = (168, 168, 168)

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "assets" / "fonts"
MARK = ROOT / "assets" / "brand" / "MD-Circle-Transparent.png"

TITLE_1, TITLE_2 = "YOU ARE", "THE SYSTEM"
SERIES = "MAJOR MOVES"
AUTHOR = "MAJOR DREAM WILLIAMS"
HOOK = "If everything stops when you stop—\nwhat exactly have you built?"

SPECS = {
    "pdf-cover":         (1600, 2400, "cover"),
    "stripe":            (1024, 1024, "square"),
    "instagram-feed":    (1080, 1350, "portrait"),
    "instagram-square":  (1080, 1080, "square"),
    "instagram-story":   (1080, 1920, "story"),
    "youtube-thumb":     (1280, 720, "wide"),
    "open-graph":        (1200, 630, "wide"),
}


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONTS / name), size)


def render_cover(pdf: Path, dpi: int = 300) -> Image.Image:
    """Rasterise the real cover once, at print resolution."""
    tmp = pdf.parent / "_cover_raster"
    subprocess.run(["pdftoppm", "-png", "-r", str(dpi), "-singlefile",
                    str(pdf), str(tmp)], check=True)
    img = Image.open(tmp.with_suffix(".png")).convert("RGB")
    tmp.with_suffix(".png").unlink(missing_ok=True)
    return img


def tracked(d: ImageDraw.ImageDraw, xy, text, f, fill, track):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f) + track


def centred_tracked(d, cx, y, text, f, fill, track):
    w = sum(d.textlength(c, font=f) + track for c in text) - track
    tracked(d, (cx - w / 2, y), text, f, fill, track)


def compose(cover: Image.Image, w: int, h: int, kind: str) -> Image.Image:
    canvas = Image.new("RGB", (w, h), BLACK)
    d = ImageDraw.Draw(canvas)
    s = min(w, h) / 1000.0  # scale unit

    if kind == "cover":
        # the cover itself, at its own ratio
        c = cover.copy()
        c = c.resize((w, int(w * c.height / c.width)), Image.LANCZOS)
        if c.height > h:
            top = (c.height - h) // 2
            c = c.crop((0, top, w, top + h))
        canvas.paste(c, (0, (h - c.height) // 2))
        return canvas

    if kind in ("square", "portrait"):
        # the cover standing in its own space, with air around it
        pad = int(h * (0.085 if kind == "square" else 0.07))
        ch = h - pad * 2
        cw = int(ch * cover.width / cover.height)
        if cw > w - pad * 2:
            cw = w - pad * 2
            ch = int(cw * cover.height / cover.width)
        c = cover.resize((cw, ch), Image.LANCZOS)
        x, y = (w - cw) // 2, (h - ch) // 2
        # a hairline shadow so the cover reads as an object on the ground
        d.rectangle([x - 1, y - 1, x + cw, y + ch], outline=(26, 22, 16), width=2)
        canvas.paste(c, (x, y))
        return canvas

    # wide + story: the cover beside the words, not squeezed behind them
    if kind == "wide":
        pad = int(h * 0.09)
        ch = h - pad * 2
        cw = int(ch * cover.width / cover.height)
        c = cover.resize((cw, ch), Image.LANCZOS)
        cx = int(w * 0.72) - cw // 2
        canvas.paste(c, (cx, pad))
        tx = int(w * 0.07)
        f_ser = font("Inter-Medium.ttf", int(17 * s))
        f_big = font("Inter-ExtraBold.ttf", int(74 * s))
        f_hook = font("Inter-Regular.ttf", int(21 * s))
        tracked(d, (tx, int(h * 0.16)), SERIES, f_ser, LEGACY, 5 * s)
        d.text((tx, int(h * 0.26)), TITLE_1, font=f_big, fill=CLARITY)
        d.text((tx, int(h * 0.26) + int(80 * s)), TITLE_2, font=f_big, fill=CLARITY)
        d.multiline_text((tx, int(h * 0.68)), HOOK, font=f_hook, fill=SMOKE, spacing=int(9 * s))
        return canvas

    # Story: the cover carries the title already. Repeating it beneath reads
    # as a mistake, so the space below holds the question instead.
    pad = int(w * 0.15)
    cw = w - pad * 2
    ch = int(cw * cover.height / cover.width)
    c = cover.resize((cw, ch), Image.LANCZOS)
    top = int(h * 0.115)
    d.rectangle([pad - 1, top - 1, pad + cw, top + ch], outline=(26, 22, 16), width=2)
    canvas.paste(c, (pad, top))
    f_hook = font("Inter-Regular.ttf", int(27 * s))
    f_aut = font("Inter-Medium.ttf", int(15 * s))
    y = top + ch + int(h * 0.052)
    for i, ln in enumerate(HOOK.split("\n")):
        tw = d.textlength(ln, font=f_hook)
        d.text(((w - tw) / 2, y + i * int(38 * s)), ln, font=f_hook, fill=SMOKE)
    centred_tracked(d, w / 2, y + int(118 * s), AUTHOR, f_aut, LEGACY, 4 * s)
    return canvas


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cover", default="build/Volume-01-front-cover.pdf")
    ap.add_argument("--out", default="build/catalog")
    a = ap.parse_args()

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    cover = render_cover(Path(a.cover))
    print(f"cover rasterised at {cover.size}")

    for name, (w, h, kind) in SPECS.items():
        img = compose(cover, w, h, kind)
        p = out / f"{name}-{w}x{h}.png"
        img.save(p, optimize=True)
        print(f"  {p.name:<34} {p.stat().st_size // 1024:>5} KB")
    print(f"\n{len(SPECS)} images in {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
