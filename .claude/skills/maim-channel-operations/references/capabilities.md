# What each connector can and cannot do

Checked 23 October 2026 by calling the tools, not by reading descriptions. A
capability table is a claims table until someone runs it.

## vidIQ — the main engine

Authorised as `major@hanzo.ai`. **150 renewable credits a month**, resets 23 Nov.
`vidiq_balance` is free; call it before spending.

**Free (0 credits):** `vidiq_user_channels`, `vidiq_balance`,
`vidiq_instagram_connected_accounts`.

**Paid — check cost in the tool description before calling.** `vidiq_ig_profile`
is 5. Generation (video, clips, thumbnails, voiceover, motion graphics) costs
considerably more.

**Works now:** upload, clip, transcript, chapters, titles and title scoring,
thumbnail generate/score/refine/update, b-roll, motion graphics, media edit,
keyword research, outliers, competitor and channel analytics.

**Does not work yet:** `vidiq_instagram_publish_reel` — no Instagram account is
connected to vidIQ. Connect at app.vidiq.com, then re-check
`vidiq_instagram_connected_accounts`.

**Reads public Instagram by handle.** Confirmed working. It explicitly will not
search or discover, so pair it with web search for the handle.

## Metricool

Brand `7610638`, owner `major@hanzo.ai`, timezone Asia/Makassar, created 23 Oct.
Networks: Facebook `467809073092442`, Instagram `amasolagi`, YouTube
`UCAxy4YB0VlQgrmQiKowu04g`.

Scheduling, analytics and best-time-to-post. **Its Instagram is not
`@maim_academy`** — see `lanes.md` before scheduling anything to Instagram.

## Restream

Live to 30+ destinations, with event transcripts, recordings, chat history and
clips projects. This is the Knowledge Vault Live infrastructure.

Per its own instructions: discover IDs with list/get calls, never invent them,
never show internal IDs in a reply, and ask which event type before creating one.

## Windsor.ai

Read-only analytics. Connected: `youtube` (`major@hanzo.ai`), `instagram` and
`instagram_public` (`fix_your_business_system`, `artmobagi`), `linkedin_organic`
(ART MOB AGINT Solutions Inc).

Own-account performance data only. It cannot read other people's profiles, so it
does not serve lead research.

## Google Vids

**No API exists**, so no connector can be built. Drive sees the file as an opaque
`application/vnd.google-apps.video` and cannot read its timeline, transcript or
edits. The export is the integration: Vids → Drive or YouTube → then work on it.

## Google Drive — a hard size limit

Downloads arrive base64-encoded inside a tool result. **Anything above roughly
2–3 MB kills the connection.** An 8.6 MB file brought the server down on 23 Oct.

Do not try to inspect large video from Drive. Ask Major what is in it, or have
the file exported somewhere that streams.

## Programmable editing

`ffmpeg` and `ffprobe` are installed in the container. Combined with timestamped
Fathom transcripts this gives edit-by-transcript: a line of text maps to an in
and out point, so a cut list is text rather than a timeline.
