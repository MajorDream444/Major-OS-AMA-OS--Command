---
name: maim-brand-production
description: Produce MAIM-branded visual output — book interiors, covers, catalogue and storefront imagery, Stripe product images, social exports. Use for any MAIM artwork, typesetting, logo placement, export sizing or brand colour decision, and before writing any script that draws, typesets or exports a MAIM asset. Carries the canonical tokens, the font pipeline, the transparent-mark derivations and the verification discipline, so none of it is re-derived.
---

# MAIM brand production

Read `references/tokens.md` before any colour or type decision, and
`references/pipeline.md` before writing or running a builder.

This skill exists because all of it was worked out once, painfully, and must not
be worked out again. Where it states a value, use that value. Do not approximate
from memory — every approximation in the first pass was close enough to look
right and wrong enough to be off-brand.

## Authority, in order

1. **Owner instruction**, always first.
2. `major-ai-os/DESIGN.md` — the canonical design system. It says every agent
   must read it before visual decisions. Do that.
3. `major-ai-os/data/design-tokens.json` — the real values, v2.1.
4. `maim-integrity-publishing-design` skill — the Integrity collection's lock.
   Its identity rules bind everywhere; its cover directions bind Integrity only.
5. This skill — the production mechanics underneath all of the above.

## Use the brand's own vocabulary

Colours have names: **maimBlack, crownGold, sovereignGold, legacyGold,
jamaicanLegacyGreen, championBlue, championOrange, clarityWhite, smokeGray.**
Use them. Do not invent a parallel vocabulary — calling `#F7F4EA` "cream"
creates a second naming system beside the canonical one and the drift compounds.

## Identity assets — absolute

- The MD/woven-hat seal is **the** asset. **Never redraw, trace, reinterpret,
  vectorise or regenerate it.** Scale proportionately only.
- **Never synthesize a replacement author likeness.** Use the supplied photo.
- No generic crown, crest, seal or substitute monogram. The word "crown" does
  not authorise a different symbol.
- Framing out unused margins or the pin caption is permitted. Changing the mark
  is not.
- Verify against hashes before use. `verify_assets.py` in the Integrity skill
  checks the approved set. Recover a missing original; never substitute a
  generated approximation.

## Transparent marks

The approved originals carry flat near-black grounds, so unprocessed they can
only be placed on black. Two derivations exist in `assets/brand/`, recorded with
their own hashes and method in `transparent-derivation.json`:

| File | Method | Why |
|---|---|---|
| `MD-Circle-Transparent.png` | circular alpha mask on the seal's own outer ring, 4× supersampled | the seal has a **black interior** — a luminance key would hollow it |
| `MD-Hat-Transparent.png` | luminance key, then **un-premultiplied** | gaps between strokes must drop out; un-premultiplying stops a dark halo on light grounds |

Use the transparent versions for placement. The originals remain the approved
assets and must stay byte-identical: `MD-Circle-Original.png` = `4fde85eb…`,
`MD-Hat-Original.png` = `97d66750…`.

## Builders

All live in `scripts/`. All require **`python3.13`** — `python3` is 3.11 here
and the packages are installed for 3.13.

| Script | Produces |
|---|---|
| `build_interior.py` | 6×9 book interior from manuscript markdown |
| `build_cover_front.py` | front cover, the Constricted Flow field |
| `build_catalog_images.py` | 7 catalogue/storefront/social exports from one cover |
| Integrity skill's `build_covers.py` | the six approved Integrity cover pairs |

## Verification — not optional

A build that has not been looked at is not finished. Every time:

1. **Render it to PNG and actually look at it.** `pdftoppm -png -r 110
   -singlefile file.pdf out`. Describing intent is not inspecting output. A
   cover was once shipped "drawn as a narrowing" that was two horizontal rules
   and a dot.
2. **`pdffonts`** — brand faces must show `emb yes`. A silent fallback to
   Helvetica looks fine and is wrong.
3. **`pdftotext`** — text must extract, and production scaffolding must *not*
   appear. An approval record once typeset itself into page 2 of a book.
4. **`pdfimages -list`** — placed assets ≥ 300 ppi for print.
5. **Re-read your own colophon.** If it still claims assets are unverified
   after they were verified, that is also an inaccuracy.

## Never

- Call a preview print-ready. A spine needs final page count, printer trim,
  paper, binding, bleed and barcode first.
- Invent an ISBN, barcode, endorsement or review quote. Reserve the space empty.
- Carry one collection's artwork into another. Integrity's six illustrations are
  Integrity's.
- Promise an outcome, a price or an enrollment that the repositories do not show
  as open.
