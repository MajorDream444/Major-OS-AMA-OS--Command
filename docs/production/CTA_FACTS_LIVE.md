# What you may say on camera — live facts

**Verified against the live site 25 October 2026.** This replaces every earlier
"no price, no date, nothing implying a seat can be bought" instruction in the
shoot plan, the recording sheet and the production skill. Those were correct
while enrollment was closed. The reserve page is now live and states the terms
publicly, so the constraint has changed shape rather than disappeared.

## The address

**`academy.majoraimindset.com/reserve`** — the Academy is a **subdomain**, so
the name goes in front and there is **no `www`**.
`www.academy.majoraimindset.com` does not resolve.

Everything else is a path on the main site and takes `www` or not:
`majoraimindset.com/pillars`, `/library`, `/vault`, `/shop`, `/coaching`.
`pillars.majoraimindset.com` is the one other subdomain.

**Checked 25 Oct:** `academy.majoraimindset.com` and `/reserve` both return 200.
`majoraimindset.com/academy` and `/reserve` **both 404** — the redirect was
offered and has not been added yet. Until it is, **never say "slash academy"
on camera.** Say the full subdomain.

## You MAY say

- Reserve your spot. **Reserving is free.**
- **20 spots.** Founding cohort.
- **Opens 11 November.** Everyone who reserved gets their payment link first.
- **US$249, paid once.** Founding price.
- The 30-Day Major Moves Journey — live sessions Wednesdays **11, 18, 25
  November and 2 December 2026, 10 p.m. Bali time (14:00 UTC).**
- If you change your mind, don't pay. Nothing is charged until you do.

All of the above is on the reserve page in those words. Saying it on camera
matches the page, which is the point — a viewer who hears one thing and reads
another stops trusting both.

## You MAY NOT say

- That anyone can **pay or buy now.** They cannot. Reserving is the action; the
  payment link goes out 11 November.
- A **different price or date** than the ones above. If the page changes, this
  file changes first and the backdrop gets rebuilt.
- That a spot is **held, guaranteed or secured** beyond being in line.
  "Reserving holds your place in line" is the claim; nothing stronger.
- `majoraimindset.com/academy` or `/reserve` — **those 404 today.**

## The outro

Shot once, tails all five videos. Get it right the first time.

> Reserving is free and it takes a minute. Twenty spots, founding cohort, opens
> the eleventh of November — and everyone who reserved gets their payment link
> first. Academy dot major A I mindset dot com, slash reserve.

Say the domain slowly. It is the only thing in the video a viewer has to
transcribe by ear.

## The backdrop carries it too

The CTA bar is **rendered into every frame**, so it cannot be changed after the
shoot:

> Reserve your spot · 20 spots · 11 November      academy.majoraimindset.com/reserve

If any of those facts change, edit `scripts/build_video_backdrop.py`, rerun it,
and reshoot anything already recorded against the old bar.
