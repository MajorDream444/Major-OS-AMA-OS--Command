#!/usr/bin/env python3
"""
Inject the real MD medallion into every MAIM page.

Artifacts are served under a strict CSP that blocks external images, so the
logo has to be inlined as a data URI rather than linked. That would mean
hand-editing every page each time the asset changes — this script does it
instead.

Usage:
    1. Put the real logo at  maim/assets/md-medallion.png
    2. python3 maim/apply-logo.py

Every <!--MD-LOGO size--> ... <!--/MD-LOGO--> block in the pages listed below
is replaced with an <img> carrying the encoded asset. Run it again whenever
the logo changes; the markers survive, so it is safe to re-run.
"""

import base64
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
LOGO = ROOT / "assets" / "md-medallion.png"

PAGES = [
    ROOT / "majoraimindset_front_door.html",
    ROOT / "MAIM_Funnel_Landing_Page.html",
    ROOT / "return.html",
]

# <!--MD-LOGO 36--> anything <!--/MD-LOGO-->   →  36px square <img>
BLOCK = re.compile(
    r"<!--MD-LOGO\s+(\d+)-->.*?<!--/MD-LOGO-->",
    re.DOTALL,
)


def main() -> int:
    if not LOGO.exists():
        print(f"error: no logo at {LOGO.relative_to(ROOT.parent)}", file=sys.stderr)
        print(
            "Drop the medallion PNG there, then re-run. Pages keep their\n"
            "placeholder until you do — nothing else needs editing.",
            file=sys.stderr,
        )
        return 1

    encoded = base64.b64encode(LOGO.read_bytes()).decode("ascii")
    uri = f"data:image/png;base64,{encoded}"
    print(f"logo: {LOGO.name} → {len(encoded) // 1024} KB encoded")

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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
