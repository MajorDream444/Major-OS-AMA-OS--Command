---
name: maim-integrity-publishing-design
description: Preserve the approved MAIM Integrity cover family, exact Major Dream MD logos, author photo, front/back layouts and alternate-cover product identity. Use for creating, revising, reviewing or releasing Architecture of Integrity, Integrity Code or Truth Compass covers, interiors, publishing assets or cover variants.
---

# MAIM Integrity Publishing Design

## Read the authority

Read `references/design-canon.md` and `references/approved-assets.json` before visual work. Read `references/release-policy.md` before catalog, cover-rotation or release planning. Treat the 2026-10-20 owner-approved v0.4 visual directions as the baseline; preserve all six, not one winner. Separate design-direction approval from manuscript, back-copy and sales approval.

Follow current owner instructions over this baseline. Record deliberate changes by version; do not silently improvise a new identity. Use Major-AI-OS DESIGN.md as parent brand authority and this family as its Integrity implementation.

## Preserve identity exactly

- Use the archived exact circular MD/woven-hat mark as primary and exact unencircled MD/woven-hat as the approved alternate. Do not draw, trace, reinterpret or regenerate them. Scale proportionately; frame unused margins or the pin caption without changing the mark itself.
- Never introduce a generic crown, crest, seal or substitute monogram. The woven hat in the supplied mark is the asset; the word crown does not authorize a different symbol.
- Keep the supplied author photograph unchanged except proportionate framing/placement. Treat supplied desk images as references unless asked to place them. Do not synthesize a replacement author likeness.
- Spell MAIM, HAMAL and Major Dream Williams correctly. Do not import the old thumbnail wording as a replacement collection name.
- Recover the exact asset directory from the saved v0.4 package, then verify originals with `python scripts/verify_assets.py --asset-dir /absolute/approved-asset-directory`. Recover missing approved assets rather than invent a replacement. Continue unrelated copy work if a source asset is unavailable.

## Produce complete alternatives

Maintain Adult A doorway / B neighborhood; Teen A paths / B court conversation; Child A compass / B bus repair. Keep title, subtitle and age hierarchy. Keep Integrity separate from Lucky Library's 27-volume canon.

Give at least two alternatives for new image samples. Deliver a front AND matching back for each book-cover option, even if only the front is mentioned casually. Include blurb, actual author photo, reviewed short bio and exact marks on the back. Reserve unassigned ISBN/barcode space; invent no identifiers or endorsements.

Use the image-generation skill/tool for new art or raster edits. Place exact logos, portrait and text through deterministic layout composition rather than accepting generated approximations. Mark prior generic-crown drafts superseded.

Restore all nine exact logo, portrait and cover artwork files from the saved v0.4 package using the current Library skill and approved-assets.json. Extract branded-covers/assets into a task directory and verify every assets and archived_cover_art hash. Reuse an existing verified copy if available. Never replace a missing baseline with a newly generated approximation.

Rebuild the baseline using `python scripts/build_covers.py --output-dir /absolute/task-output-directory --asset-dir /absolute/approved-asset-directory`, resolving the script relative to this skill. Require Python, ReportLab, Pillow and DejaVu fonts. Identify missing dependencies instead of claiming successful output. The script writes six two-page front/back PDFs and a six-page review booklet; it does not edit assets or calculate spines.

## Keep authoring and production honest

Follow the Universal Publishing Canon's teaching sequence and preserve original source IDs separately. Pair with Major Voice & Doctrine and Raw Thought Intake for writing: preserve raw words privately; label edits and fiction; invent no biography. Include no private conversations, legal admissions or third-party allegations in this skill or public Git.

Preserve cultural specificity and meaningful tension in adult writing. Independently write teen and child editions rather than simplifying explicit adult cases. Teach honesty with privacy, safe help, boundaries and independent judgment. Assess learning, not moral worth. Claim no external accreditation and enable no minors' AI chat merely because a companion prompt is drafted.

## Verify and deliver

Check exact marks and photo fidelity, spelling, two alternatives, both sides, proportionate placement, readable typography and no invented branding. Render and inspect all review pages; check clipping, embedded fonts and text extraction. Supply editable sources and an asset/version/review manifest. Explain limitations such as flattened art, provisional back copy or untested accessibility.

Do not call a preview print-ready. Require final page count, printer trim, paper, binding, bleed and barcode specifications before calculating a physical spine. The bundled 6x9-inch layout is a review reference only.

Use the current persistence workflow for deliverables; separate private source from reviewer assets. Report outputs, decisions, gaps and three next actions. Save skill changes through its Skills Git workspace; do not package or link the skill itself unless asked.
