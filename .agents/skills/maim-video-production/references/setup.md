# Shoot setup

## Before the camera rolls

| Check | Pass condition |
|---|---|
| Audio | 10 s recorded, played back, clean — no room hum, no clipping |
| Lane | setting matches the channel (desk for Academy, robe for Mindset) |
| Backdrop | correct variant loaded; `-GUIDES-` **not** in the comp |
| Framing | subject inside the 780 px centre box; waists visible at ±430 px |
| Wardrobe | not pure black against maimBlack |
| Episode panel | filled for this episode, or covered |
| Script | the recording sheet open — one idea, one assignment per piece |

## Backdrop variants

| File | Use |
|---|---|
| `maim-academy-backdrop-1920x1080.png` | standard |
| `maim-academy-backdrop-mirrored-1920x1080.png` | footage flipped in the edit |
| `maim-academy-backdrop-3840x2160.png` | 4K |
| `maim-academy-backdrop-mirrored-3840x2160.png` | 4K, flipped |
| `maim-academy-backdrop-GUIDES-1920x1080.png` | **reference only** |

Zones: channel strip top · episode panel lower left (430 × 172) · name lockup
lower right · CTA bar bottom · subject centre, keep clear.

Regenerate after any copy change:

```bash
python3.13 scripts/build_video_backdrop.py --out build/backdrop
```

## Reusables, shot once per set

| Piece | Run | Notes |
|---|---|---|
| Outro / CTA | ~0:20 | free guide + founding cohort **list**. No price, no date, no seat |
| Cold open sting | ~0:10 | name, channel, one line |
| B-roll | ~5 min | notebook, pen, hands, screen showing something built |

B-roll covers every edit seam. Without it, chunked self-editing shows every cut.

## Recording in chunks

Major records in passes rather than takes, speaking past the page wherever the
thought goes further. The **assignment** and **one idea** are fixed; the route
through them is not. A story that belongs to chapter 4 and surfaces while
recording chapter 2 stays where it landed — the series is ordered by what the
viewer does at the end, not by chapter number.
