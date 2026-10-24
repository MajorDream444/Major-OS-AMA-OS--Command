# Starting work on the MAIM Academy YouTube channel

**Read this before proposing anything.** The channel plan already exists and is
approved. Writing another one creates a competing document.

**Current as of 24 October 2026, end of day.** An earlier version of this file
said the channel had zero videos and that Drive held usable footage for season
one. Both were true then and are not true now. What follows replaces it.

## Where things actually stand

**The channel has 11 videos, all unlisted.** Nine went up this morning between
02:48 and 03:14, plus a Google Vids `test` from 23 Oct. They run 20 seconds to
2:02 — clips and fragments, staged for tooling, **not season one**. Major hit
YouTube's daily upload cap getting them there.

The cap counts **uploads, not minutes**. A 12-minute video costs the same one
slot as a 20-second clip. Upload the long-form first.

**Season one is recorded fresh.** Decided 24 Oct. There is no footage of the
book's stories and there never was: the dinner party, the wooden boat and the
triangle offense all come from the 23 October intake, which is **audio only**,
and the one real talking-head recording predates that intake by two weeks.
Major is recording the five himself, self-edited in chunks, using **Google Vids
as the edit bay**.

**Google Vids is allowed as an editor, not as a presenter.** Assembling his own
footage, title cards, b-roll and captions is fine. Its AI avatar and synthetic
voiceover are not — that is the synthesised-likeness rule, and it is the one
thing that would undercut a channel whose pitch is being straight with people.

## What is already decided

| File | What |
|---|---|
| `docs/marketing/SEASON_ONE_RECORDING_SHEET.md` | **what Major records from.** One idea and one assignment per video; the rest is his |
| `docs/marketing/YOUTUBE_SEASON_ONE_PLAN.md` | the five, the separation, format reasoning, production and CTA discipline |
| `docs/marketing/ARCHIVE_INVENTORY_HANZO_DRIVE.md` | the 23 archive videos, grouped, with what is absent |
| `docs/marketing/ARCHIVE_AND_VAULT_TRACK.md` | what the archive is for, and why the vault is not an Academy tier |
| `docs/marketing/YOUTUBE_CHANNEL_COPY.md` | channel description, banner and avatar, with upload locations |
| `docs/marketing/COHORT_PRELAUNCH_SEQUENCE.md` | six-email pre-launch sequence, drafted and unsent |
| `docs/handoffs/CLAUDE_TO_CODEX_ACADEMY_BOUNDARY_2026-10-24.md` | why the Academy and the Mindset are separate brands |

## Skills — load these, do not re-derive them

`.claude/skills/` and `.agents/skills/` carry:

- **`maim-channel-operations`** — the two-agent lane split, which accounts belong
  to whom, what each connector can actually do, the vidIQ credit budget, the
  YouTube-unlisted staging pipeline, **the frame rule** and **the Google account
  boundaries**.
- **`maim-brand-production`** — canonical colour tokens, the Inter font pipeline,
  the transparent marks, the builders, and the verification discipline.
- **`maim-integrity-publishing-design`** — the identity lock on the MD mark and
  the author photograph.

## The frame rule

The morning-robe format — robe, hot chocolate, first thing, the 4 W's — is an
established **Major AI Mindset** format with its own thumbnail family. That is
the movement lane. **Do not reuse it for Academy content.** The Academy records
at a desk, with the notebook, with something built on screen. Same man,
different room.

Separation is visual before it is editorial. Two channels that are structurally
distinct still merge in a feed when they are shot identically.

## The channel

`@MAIM_ACADEMY` · `UCAxy4YB0VlQgrmQiKowu04g`

**`channelId` is the only reliable identifier.** vidIQ served a stale handle
(`@maimdreamacademy`) for a full day and it was wrong. Do not trust a handle
from a tool result over YouTube Studio.

Embeds and a videos page stay premature until something is published publicly.

## Google accounts — check before reporting anything missing

| Account | Holds | Connector |
|---|---|---|
| `major@hanzo.ai` | business identity, Substack, the 23 archive videos | **Drive is now here** |
| `majornfts@gmail.com` | older Drive archive, Fathom voice archive | Fathom |
| `artmobagi@gmail.com` | the 23 Oct Volume 1 intake | Fathom, separately |

A file uploaded to one account is invisible to a connector on another, and the
search returns an empty result that looks exactly like "it isn't there." This
cost a day. Check the account before concluding a file is missing.

## Assets ready to use

```
build/banner/maim-academy-banner-2560x1440.png   channel banner
build/avatars/youtube-avatar-800.png             channel avatar
assets/brand/                                     marks, portrait, hashes
assets/fonts/                                     Inter TrueType, embeddable
scripts/build_youtube_banner.py                   regenerate the banner
scripts/build_catalog_images.py                   thumbnails and social exports
```

## Standing constraints

- Production commerce is **disabled**. Founding cohort enrollment is **closed**.
  Nothing may imply a seat can be bought.
- Never synthesize a replacement author likeness; never redraw the MD mark.
- **Fourteen of the 23 archive videos are probably NotebookLM-generated** — the
  ideas are Major's, the delivery is synthetic. Unconfirmed. Until he confirms,
  do not treat any of them as talking-head footage. Separately, several videos
  in the older majornfts Drive are Gemini-generated and carry a synthesised
  likeness; those are out, full stop.
- vidIQ runs on **150 credits a month, resetting 23 November.** Clipping costs
  9 per minute of source, so clipping all five long-form videos would cost
  roughly 500 — more than three months of budget. Clip selectively, or cut
  shorts by hand in Google Vids, which is free. Check `vidiq_balance` first.
- Metricool's Instagram is **`amasolagi`**, not `@maim_academy`. Confirm the
  destination account before scheduling anything to Instagram.

## Open, and Major's to decide

- **Are the fourteen "Unlock / Transform" videos generated delivery, or him on
  camera?** One answer reclassifies all fourteen at once.
- **Which "mindset of major" cut is the keeper** — the 278 MB original or the
  248 MB `Future Proofed` edit. Pick before clipping either.
- **Channel display name** is "Major Dream"; Instagram's is "Major Academy".
  Handles match; names do not.
- The **LA rooftop conversation** and the morning-robe footage are not in Drive
  or on the channel. The rooftop one he named specifically as worth repairing.
