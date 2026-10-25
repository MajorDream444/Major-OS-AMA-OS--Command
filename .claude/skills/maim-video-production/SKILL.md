---
name: maim-video-production
description: Plan and run a MAIM video shoot — what gets shot, in what order, how it is framed, lit, miked and edited, and what must never appear on camera. Use before any MAIM recording session, shot list, call sheet, backdrop placement, or Google Vids edit, and before advising Major or a creative team on production. Covers the shoot itself; maim-channel-operations covers everything after upload.
---

# MAIM video production

Read `references/setup.md` before a shoot and `references/edit.md` before an
edit. This skill covers **production** — getting footage made. Publishing,
scheduling, clipping and analytics belong to `maim-channel-operations`. Colour,
type, marks and exports belong to `maim-brand-production`.

## Authority, in order

1. **Owner instruction**, always first.
2. `maim-brand-production` — tokens, marks, type, the likeness lock.
3. `maim-channel-operations` — lanes, accounts, connectors, credit budget.
4. This skill.

## The lane decides the frame

Separation is visual before it is editorial. Two channels that are structurally
distinct still merge in a feed when they are shot the same way.

| Lane | Format | Setting |
|---|---|---|
| **Major AI Mindset** — the movement | *Major Morning AI Mindset.* Robe, hot chocolate, first thing. The 4 W's | morning chair |
| **MAIM Academy** — the school | teach one idea, end with one assignment | desk, notebook, something built on screen |

**Never shoot Academy content in the robe.** Before any shoot, ask which lane
the *setting* reads as, not just the script. A borrowed frame undoes the
separation faster than a borrowed topic.

## Absolute — on camera

- **The presenter is Major, filmed.** Never an AI avatar, never a synthetic
  voiceover, never a generated likeness. Google Vids, HeyGen, Higgsfield and
  every similar tool are **edit bays, not presenters.** A channel whose pitch is
  being straight with people cannot open with a synthetic face.
- **Never redraw, trace or regenerate the MD mark.** Place
  `MD-Circle-Transparent.png`, scaled proportionately.
- **Never synthesize a replacement author likeness.** Use the supplied photo.
- Several archive videos are Gemini-generated and carry a synthesised likeness.
  **Do not use them,** as source or as b-roll.

## Absolute — what is said

**Read `docs/production/CTA_FACTS_LIVE.md` before writing or shooting any CTA.**
It holds the verified live facts and is the file that changes first when the
site does.

As of 25 October the reserve page is live and public. Takes, titles,
descriptions, end screens and on-screen graphics **may** state: reserving is
free, 20 spots, opens 11 November, US$249 paid once, payment link first to
anyone who reserved, sessions Wednesdays 11/18/25 Nov and 2 Dec at 10 p.m. Bali.
They **may not** say anyone can pay today, quote any other price or date, or
claim a spot is held or guaranteed beyond being in line.

The address is **`academy.majoraimindset.com/reserve`** — a subdomain, **no
`www`**. `majoraimindset.com/academy` and `/reserve` 404 today.

Shoot the outro **once** and tail it onto everything. Five separate outros are
five chances to say something that has to be reshot.

## Order of a shoot day

1. **Audio test.** Ten seconds, played back, confirmed clean. Before anything.
2. **Reusables** — outro, cold-open sting, b-roll. Shot while the room is fresh,
   used across every video in the set.
3. **The driest piece**, while concentration is highest.
4. **The most human piece**, once the subject is loose.
5. The rest.

**Three finished long-form videos is a full day.** Forty minutes of finished
talking head is more than it sounds. Shooting five badly is worse than shooting
three well — a thin take on the strongest asset cannot be un-shot.

## Framing against the backdrop

`scripts/build_video_backdrop.py` → `build/backdrop/`.

- Subject **centred**, inside the 780 px keep-clear zone.
- The gold fields converge to a waist at **±430 px** from centre. Keep them in
  frame — the convergence is the argument.
- Use `-mirrored-` **only** when the footage is flipped in the edit. The layout
  is symmetric so a flip survives; type is the exception.
- **Never composite the `-GUIDES-` file.** Framing reference only.
- **Avoid pure black wardrobe.** The ground is maimBlack `#050505` with only a
  faint charcoal bloom behind the subject; black on black merges.
- The episode panel ships as a placeholder. Fill it per episode or cover it.

## Audio is the known weak point

Check it first, every time. The evidence is on file: a clip came back from
YouTube's auto-captioner tagged **Amharic** with garbled output, because the
source audio was rough. Every minute shot runs through
`vidiq_video_transcript` for clips and chapters, so bad audio does not just
sound bad — it makes the whole post-production chain worthless.

After upload, **read the transcript.** Garbage captions mean the audio, not the
tool.

## Upload discipline

- **Unlisted, never private.** Private videos are not fetchable by vidIQ even
  with the link.
- **The daily cap counts uploads, not minutes.** A 12-minute video costs the
  same slot as a 20-second clip. **Long-form goes up first.** A day's cap was
  once spent entirely on short clips while the main recordings waited.
- Nothing goes public without the owner saying so. Unlisted is a staging state,
  not a publishing decision.

## Never

- Call a rough cut finished without watching it end to end.
- Carry one lane's format into the other.
- Shoot five pieces of an outro when one will serve.
- Treat unconfirmed archive footage as talking head. Ask first; one answer can
  reclassify a whole set.
