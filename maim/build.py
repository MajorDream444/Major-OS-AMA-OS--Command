#!/usr/bin/env python3
"""
Build the deployable MAIM site.

The page sources in maim/ are *fragments* — they open with <title> and <style>
and carry no <!DOCTYPE>, <html>, or <head>. That is correct for Claude Artifacts,
which injects a document skeleton at publish time. Served raw by a static host it
is not correct: no charset, no viewport (mobile renders at desktop width), no
social preview, no favicon.

This script wraps each fragment into a complete document, rewrites internal links
to clean routes, and emits robots.txt + sitemap.xml into maim/dist/.

    python3 maim/build.py

Run it after apply-logo.py, and after any edit to a page source.
"""

import pathlib
import re
import shutil
import sys
from datetime import date

ROOT = pathlib.Path(__file__).resolve().parent
DIST = ROOT / "dist"
ORIGIN = "https://majoraimindset.com"

# source fragment -> (output file, route, description)
PAGES = {
    "majoraimindset_front_door.html": (
        "index.html",
        "/",
        "Learn to think with AI without losing yourself. A free live room for "
        "anyone ready to begin — one letter, one lesson, one action at a time.",
    ),
    "MAIM_Funnel_Landing_Page.html": (
        "pillars.html",
        "/pillars",
        "Five AI moves you can run this week, free. Then the 10 Pillars — the "
        "architecture underneath the A·B·C.",
    ),
    "return.html": (
        "return.html",
        "/return",
        "Your asset is ready. This is not the end of the purchase — it is your "
        "first brick inside MAIM.",
    ),
}

# old relative links -> clean routes
LINK_MAP = {
    "./majoraimindset_front_door.html": "/",
    "./MAIM_Funnel_Landing_Page.html": "/pillars",
    "./return.html": "/return",
}

TITLE_RE = re.compile(r"<title>(.*?)</title>", re.DOTALL)

# Gold medallion mark. Replaced by the real asset when it exists.
FALLBACK_FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">
<circle cx="24" cy="24" r="23" fill="#C9931A"/>
<circle cx="24" cy="24" r="20" fill="#0E0E0E"/>
<text x="24" y="30" font-family="Georgia,serif" font-size="20" font-style="italic"
      font-weight="700" fill="#C9931A" text-anchor="middle">MD</text>
</svg>
"""


def document(title, description, route, body, favicon_href):
    canonical = ORIGIN + route
    social = f"{ORIGIN}/social-preview.png"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#111111">
<link rel="icon" href="{favicon_href}">
<link rel="apple-touch-icon" href="{favicon_href}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Major AI Mindset">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{social}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{social}">
</head>
<body>
{body}
</body>
</html>
"""


def main() -> int:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)

    # favicon: real medallion if present, else the drawn mark
    logo = ROOT / "assets" / "md-medallion.png"
    if logo.exists():
        shutil.copy(logo, DIST / "favicon.png")
        favicon_href = "/favicon.png"
        # double as the social preview until a dedicated card exists
        shutil.copy(logo, DIST / "social-preview.png")
        print("favicon + social preview: md-medallion.png")
    else:
        (DIST / "favicon.svg").write_text(FALLBACK_FAVICON)
        favicon_href = "/favicon.svg"
        print("favicon: drawn fallback (no md-medallion.png yet)")

    routes = []
    for src_name, (out_name, route, description) in PAGES.items():
        src = ROOT / src_name
        if not src.exists():
            print(f"  !! missing source {src_name}")
            return 1

        body = src.read_text()

        m = TITLE_RE.search(body)
        if not m:
            print(f"  !! {src_name} has no <title>")
            return 1
        title = m.group(1).strip()
        body = TITLE_RE.sub("", body, count=1).lstrip()

        for old, new in LINK_MAP.items():
            body = body.replace(old, new)

        (DIST / out_name).write_text(
            document(title, description, route, body, favicon_href)
        )
        routes.append(route)
        print(f"  {src_name} -> dist/{out_name}  ({route})")

    (DIST / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {ORIGIN}/sitemap.xml\n"
    )

    today = date.today().isoformat()
    urls = "\n".join(
        f"  <url><loc>{ORIGIN}{r}</loc><lastmod>{today}</lastmod></url>"
        for r in routes
    )
    (DIST / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n</urlset>\n"
    )

    print(f"\nBuilt {len(routes)} pages + robots.txt + sitemap.xml into maim/dist/")
    print("Deploy that directory. vercel.json already points at it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
