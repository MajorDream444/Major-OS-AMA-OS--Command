# Shoot plan — 24 October 2026

**Subject:** Major Dream Williams · **Channel:** `@MAIM_ACADEMY`
**Record from:** `docs/marketing/SEASON_ONE_RECORDING_SHEET.md`
**Edit bay:** Google Vids · **Backdrop:** `build/backdrop/`

Nobody guesses. This is what is being shot, in what order, and what is not
being shot.

---

## What we are shooting

**Season one. Five long-form videos, 9–12 minutes each.** Each teaches one idea
and ends with one assignment. This is the MAIM Academy lane — the school, not
the movement. The test for every take: does the viewer finish it with something
to do?

**Plus three reusable pieces, shot once and used across all five.** These are
the real time saving and they get shot *first*, while the room is fresh.

---

## Order of the day

Shoot the reusables first, then the videos in this order. If the day runs short,
the cut line is marked.

| # | Piece | Run | Why this position |
|---|---|---|---|
| R1 | **Outro / CTA** | 0:20 | One take, tails all five. **Script is in `CTA_FACTS_LIVE.md`** — say the domain slowly, it is the only thing a viewer has to transcribe by ear |
| R2 | **Cold open sting** | 0:10 | Name, channel, one line. Head of every video |
| R3 | **B-roll** | 5 min | Notebook, pen, hands, the screen with something built on it. Covers every edit seam in Vids |
| 01 | **Your ceiling is a number** (ch 3) | ~9 min | Driest of the five — shoot it while fresh. Also the most immediately useful, so if only one exists it should be this |
| 02 | **The night I found out I was the bottleneck** (ch 1) | ~12 min | The channel's best opening. The dinner party needs you loose, which you will be by now |
| 03 | **What lives in your head is not expertise** (ch 2) | ~10 min | — |
| — | **← realistic cut line for one day** | | 40+ min of finished talking head is a full day. Past here, quality drops and it shows |
| 04 | **Every response correct, and the boat still sinks** (ch 4) | ~12 min | The wooden boat and the 80/20 restaurant. Deserves a fresh head |
| 05 | **Michael Jordan won. Also, the triangle offense.** (ch 5) | ~11 min | Last on purpose — it carries the honest limit about systematising your thinking |

**Three finished videos today is a good day. Five is a stretch, and shooting all
five badly is worse than shooting three well** — the back two can be reshot
tomorrow, but a thin take on the ceiling video wastes the strongest asset.

---

## Setup

**Setting:** desk, notebook visible, something built on screen.
**Not the robe.** The robe, hot chocolate, first-thing-in-the-morning format is
**Major AI Mindset** — the movement lane, with its own thumbnail family. Same
man, different room. Two channels that are structurally separate still merge in
a feed when they are shot identically.

**Backdrop:** `build/backdrop/maim-academy-backdrop-1920x1080.png`
(or the 4K). Use `-mirrored-` **only** if the footage gets flipped in the edit.
Never composite the `-GUIDES-` file — that is framing reference only.

**Framing:** subject centred, inside the 780 px keep-clear box. The gold fields
converge to a waist on either side at ±430 px and must stay visible — that
convergence is the whole point. Do not crop them out.

**Wardrobe:** avoid pure black. The backdrop is maimBlack `#050505` with only a
faint charcoal bloom behind the subject. A black jacket on a black ground
merges. Mid-tone, or anything with edge separation.

---

## Audio — check this before anything else

**Record 10 seconds, play it back, confirm it is clean.** Then shoot.

The reason is on file: the Hollywood Hills clip came back from YouTube's
auto-captioner tagged as Amharic with garbled output at the end. That is what
rough audio looks like downstream. Every minute shot today runs through
`vidiq_video_transcript` for clips and chapters, and a bad transcript makes all
of it worthless. Ten seconds now, or fifty minutes wasted later.

---

## Hard constraints

**Google Vids is the edit bay, not the presenter.** Assembling your own footage,
title cards, b-roll, captions: fine. Its **AI avatar and synthetic voiceover are
out** — that is the synthesised-likeness rule, and it is the one thing that
would undercut a channel whose entire pitch is being straight with people.

**The CTA facts are live and specific — read `CTA_FACTS_LIVE.md` before the
outro.** As of 25 Oct the reserve page is up and states the terms publicly, so
the old "no price, no date" rule no longer applies. You **may** say: reserving
is free, 20 spots, opens 11 November, US$249 paid once, payment link first to
anyone who reserved. You **may not** say anyone can pay today, or quote a
different price or date.

**The address is `academy.majoraimindset.com/reserve` — a subdomain, no `www`.**
`majoraimindset.com/academy` and `/reserve` both 404 right now, so do not say
"slash academy" on camera.

**The episode panel on the backdrop is a placeholder** reading "Episode title
goes here." Fill it per episode in Vids or cover it. Do not ship it as-is.

**Upload unlisted, never private.** Private videos are not fetchable by vidIQ
even with the link, which kills transcripts and clips.

**The daily upload cap counts uploads, not minutes.** A 12-minute video costs the
same one slot as a 20-second clip. **Upload the long-form first.** Yesterday's
cap went on nine short clips, which is why nothing from season one is up.

---

## After the shoot

1. Upload each long-form **unlisted** to `@MAIM_ACADEMY`.
2. `vidiq_video_transcript` → read it. If the captions are garbage, the audio
   is the problem, not the tool.
3. `vidiq_score_title` before committing to a title.
4. Thumbnail via `maim-brand-production` — 1280×720, Constricted Flow language,
   same tokens as the book covers.
5. **Clips: budget first.** `vidiq_generate_clips` costs 9 credits per minute of
   source. 150 credits a month, resetting 23 November, and ~10 are already spent
   today. One 12-minute video costs ~108 — most of the month. **Clip one video
   through vidIQ, cut the rest by hand in Vids**, which is free. Check
   `vidiq_balance` before spending.
6. Instagram scheduling: **confirm the destination account.** Metricool's
   Instagram is `amasolagi`, not `@maim_academy`.

---

## What we are NOT shooting today

- **Anything in the robe.** Wrong lane.
- **Anything using the 23 archive videos as source.** Fourteen are probably
  NotebookLM-generated — Major's ideas, synthetic delivery — and unconfirmed
  either way. They are not talking-head footage until he says so.
- **Nothing public.** Everything today is unlisted. Publishing is Major's call,
  separately, and the 11 clips already on the channel stay unlisted too.
