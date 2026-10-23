---
name: maim-channel-operations
description: Publish, schedule and analyse MAIM social and video. Use before posting, scheduling, uploading, clipping, reading Instagram or YouTube data, or touching any MAIM channel. Carries the two-agent lane split, which accounts belong to whom, what each connector can actually do, and the credit budget. Read it before any channel action so neither agent posts to the other's accounts.
---

# MAIM channel operations

Read `references/lanes.md` before any publish or schedule, and
`references/capabilities.md` before assuming a tool can do something.

Two agents run MAIM channels. **Claude runs the Academy. ChatGPT runs the
Mindset brand.** Posting into the other agent's lane is the failure this skill
exists to prevent.

## The lane split — do not cross it

| | **Claude · Academy** | **ChatGPT · Mindset** |
|---|---|---|
| YouTube | `@MAIM_ACADEMY` — `UCAxy4YB0VlQgrmQiKowu04g` | MAIM / Major AI Mindset |
| Instagram | `@maim_academy` | MAIM main |
| Job | drive founding-cohort enrollment | build the brand and audience |

They cross-link. They do not duplicate, and neither agent publishes to the
other's accounts. If a task would post outside this lane, stop and say so.

**Facebook is out of scope.** The ArtMob page is locked behind a phone number
Major no longer controls. Do not plan around it, and do not present it as a
channel that works.

## Credits are the binding constraint

vidIQ runs on a **150-credit monthly plan**. At 5 credits an Instagram profile
read, that is about 29 lookups a month, and generation costs far more.

- Call `vidiq_balance` (free) before any batch of paid calls.
- Never loop paid calls. One failure, stop and report.
- Prefer free tools: `vidiq_user_channels`, `vidiq_video_transcript`,
  `vidiq_instagram_connected_accounts`, Metricool analytics, Windsor reads.
- Say what a run will cost before spending on Major's behalf.

## What is actually connected

Verified 23 October 2026. Re-verify rather than trust this table if a call fails.

| Capability | Tool | State |
|---|---|---|
| Upload to YouTube | `vidiq_video_upload` | ✅ authorised, `major@hanzo.ai` |
| Clip a long video | `vidiq_generate_clips` | ✅ |
| Transcript, chapters, titles, thumbnails | `vidiq_*` | ✅ |
| Motion graphics, b-roll, media edit | `vidiq_motion_graphics`, `vidiq_generate_broll`, `vidiq_edit_media` | ✅ |
| **Read any public Instagram profile** | `vidiq_ig_profile` | ✅ 5 credits, **needs a handle, does not discover** |
| Publish an Instagram reel | `vidiq_instagram_publish_reel` | ❌ no IG account connected to vidIQ |
| Schedule posts | Metricool `createScheduledPost` | ✅ brand 7610638 |
| Best time to post | Metricool `getBestTimeToPostByNetwork` | ✅ |
| Live streaming, event transcripts, clips | Restream | ✅ |
| YouTube analytics | Windsor `youtube` | ✅ `major@hanzo.ai` |
| Google Vids | — | ❌ no API exists. Export to Drive or YouTube first. |

## The Instagram lead pipeline

`vidiq_ig_profile` reads public profiles but **will not search**. So discovery
and enrichment are separate steps:

1. **Find handles** with web search, podcast directories, awards lists — the
   sources that produced every verified lead so far.
2. **Enrich** each handle with `vidiq_ig_profile`: bio, follower count, post
   count, external link.
3. **Score** against the ICP, then write only 6+ to Airtable GLOBAL_LEADS.

This replaces the Mac-bound social scout, which was blocked on Agent Reach.
Budget it: 8 candidates is 40 credits, roughly a quarter of the month.

`vidiq_instagram_tiktok_outlier_search` and `vidiq_ig_accounts_from_outliers`
may offer real discovery. Untested — test on one call before relying on them.

## Before publishing anything

1. Confirm the target account is in **Claude's lane**.
2. Confirm the asset follows `maim-brand-production` — tokens, marks, fonts.
3. For a first post to a channel, show Major the copy and the asset before it
   goes out. A published post is not a draft.
4. Never invent a metric, a follower count, a testimonial or a result.
5. **Never promise enrollment that is not open.** Live sales are disabled and the
   founding cohort is closed. Build the waitlist instead.
