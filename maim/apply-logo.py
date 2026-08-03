#!/usr/bin/env python3
"""
Inject the MD medallion into every MAIM page.

There is exactly ONE logo source in this repo:

    maim/assets/md-medallion.png   <- the real photographic seal. Preferred.
    maim/assets/md-medallion.svg   <- drawn stand-in, used only until the PNG lands.

Artifacts and the deployed site both run under a strict CSP that blocks external
images, so the logo must be inlined as a data URI rather than linked. Doing that by
hand across every page is how pages drift apart, so this script does it instead.

Usage:
    python3 maim/apply-logo.py

Every <!--MD-LOGO size--> ... <!--/MD-LOGO--> block in the pages below is replaced
with an <img> carrying the encoded asset. The markers survive, so it is safe to
re-run any time the asset changes.

To install the real logo:
    cp <your-file>.png maim/assets/md-medallion.png
    python3 maim/apply-logo.py
    python3 maim/build.py
"""

import base64
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
PNG = ROOT / "assets" / "md-medallion.png"
SVG = ROOT / "assets" / "md-medallion.svg"

PAGES = [
    ROOT / "majoraimindset_front_door.html",
    ROOT / "MAIM_Funnel_Landing_Page.html",
    ROOT / "return.html",
]

# <!--MD-LOGO 36--> anything <!--/MD-LOGO-->   ->  36px square <img>
BLOCK = re.compile(r"<!--MD-LOGO\s+(\d+)-->.*?<!--/MD-LOGO-->", re.DOTALL)


def load_asset():
    """Return (data_uri, label). Real PNG wins; drawn SVG is the fallback."""
    if PNG.exists():
        encoded = base64.b64encode(PNG.read_bytes()).decode("ascii")
        return f"data:image/png;base64,{encoded}", f"md-medallion.png ({len(encoded)//1024} KB encoded)"
    if SVG.exists():
        encoded = base64.b64encode(SVG.read_bytes()).decode("ascii")
        return f"data:image/svg+xml;base64,{encoded}", "md-medallion.svg (drawn stand-in)"
    return None, None


def main() -> int:
    uri, label = load_asset()
    if uri is None:
        print(f"error: no logo asset in {(ROOT / 'assets').relative_to(ROOT.parent)}", file=sys.stderr)
        return 1

    print(f"logo: {label}")
    if not PNG.exists():
        print("       (drop the real PNG at maim/assets/md-medallion.png and re-run)")

    total = 0
    for page in PAGES:
        if not page.exists():
            print(f"  skip {page.name} (not found)")
            continue

        def swap(m: re.Match) -> str:
            size = m.group(1)
            return (
                f"<!--MD-LOGO {size}-->"
                f'<img src="{uri}" width="{size}" height="{size}" '
                f'alt="MD medallion" style="display:block;flex-shrink:0">'
                f"<!--/MD-LOGO-->"
            )

        text = page.read_text()
        swapped, n = BLOCK.subn(swap, text)
        if n:
            page.write_text(swapped)
            total += n
        print(f"  {page.name}: {n} marker(s)")

    if total == 0:
        print("\nNo markers found — check the pages still carry <!--MD-LOGO n-->.")
        return 1

    print(f"\nDone. {total} logo(s) updated across {len(PAGES)} pages.")
    print("Run `python3 maim/build.py` to rebuild the deployable site.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
