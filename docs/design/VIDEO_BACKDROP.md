# MAIM Academy video backdrop

**Built:** 24 October 2026 · `scripts/build_video_backdrop.py` ·
**Philosophy:** `PHILOSOPHY_CONSTRICTED_FLOW.md`

```bash
python3.13 scripts/build_video_backdrop.py --out build/backdrop
```

## The idea

Two filament fields flow in from the left and right edges and converge to a
waist on either side of the subject. The frame says what the series says:
everything narrows to one person. He **is** the constriction.

The waists land at ±430 px from centre, outside the 780 px subject zone, so
nothing crosses his silhouette. The fields read as flow, not as beams — the
brightness peaks short of each waist and eases off, because peaking on the apex
produced two cones that looked like headlights.

Behind the subject sits a wide charcoal bloom, barely above the ground. Without
it the centre is a void and anyone in dark clothing vanishes into it.

## On inverting

The layout is **left–right symmetric by construction**, so a horizontal flip
does not break the composition. Type is the exception: flipped type is
backwards.

So two variants ship. If you mirror your footage in the edit, use the
**`-mirrored-`** file — flipping it puts the type the right way round. If you
do not mirror, use the plain file. Nothing else changes between them.

## Files

| File | Use |
|---|---|
| `maim-academy-backdrop-1920x1080.png` | the backdrop |
| `maim-academy-backdrop-mirrored-1920x1080.png` | for footage you will flip |
| `maim-academy-backdrop-GUIDES-1920x1080.png` | **reference only — never composite this.** Shows the keep-clear subject zone and centreline |
| `maim-academy-backdrop-3840x2160.png` | 4K |
| `maim-academy-backdrop-mirrored-3840x2160.png` | 4K, pre-mirrored |

## Zones

| Zone | Position | For |
|---|---|---|
| **Subject** | centre, 780 px wide, y 96 → 770 | keep clear |
| **Channel strip** | top, above the rule | MAIM ACADEMY · the positioning line |
| **Episode panel** | lower left, 430 × 172 | episode title and one line of context |
| **Name lockup** | lower right | MD seal, name, role |
| **CTA bar** | bottom, under the gold rule | free guide · majoraimindset.com |

The episode panel is a **placeholder** reading "Episode title goes here." Fill it
per episode in Google Vids, or cover it. Do not ship it as-is.

## Constraints held

- Tokens only: maimBlack `#050505`, crownGold `#D8AF55`, legacyGold `#9F742C`,
  clarityWhite `#F7F4EA`, smokeGray `#A8A8A8`, darkSurface `#18181B`,
  borderDark `#27272A`. Guides use systemLime `#A3E635`.
- Inter throughout — ExtraBold for display, Regular and Medium for body.
- The MD seal is placed from `MD-Circle-Transparent.png`, scaled only. Not
  redrawn, traced or regenerated.
- The CTA names the free guide and the cohort **list**. Enrollment is closed and
  live sales are disabled; nothing here implies a seat can be bought. When
  enrollment opens, change the CTA in one pass and rebuild.
- Every output was rendered and inspected. The first pass was rejected for
  reading as headlights over a dead centre.
