# Distribution Queue

## Purpose

The Distribution Queue shows where a local Substack/media item should go next after it reaches Publish, Remotion Queue, HeyGen Queue, or Distribution stage.

This is an operator visibility layer only. It prepares local handoffs for channels without publishing, syncing, rendering, or sending anything externally.

## Local-Only Behavior

Current build: local mock state only.

The queue persists in browser `localStorage` through the existing Command Center state system.

The reset control clears local distribution state and reloads seed data.

## Supported Channels

- Substack
- X
- Instagram
- YouTube Shorts
- LinkedIn
- Telegram
- GitHub / Obsidian Memory

## Asset Types

- article
- hook
- short script
- avatar video
- remotion render
- memory note

## Commands

```text
distribute <topic>
send to x <topic>
send to substack <topic>
save to memory <topic>
```

Command behavior:

- `distribute <topic>` creates or updates local rows for Substack article, X hook, Instagram short, YouTube short, and GitHub / Obsidian memory note.
- `send to x <topic>` marks the local X item as `QUEUED`.
- `send to substack <topic>` marks the local Substack item as `QUEUED`.
- `save to memory <topic>` marks the local GitHub / Obsidian Memory item as `READY`.

All commands route to `A003 Content Catcher` and update the Activity Feed.

## No External Publish Rule

No distribution command may publish, post, send, render, sync, or write to an external service in this build.

Do not connect:

- Telegram
- Substack
- Remotion
- HeyGen
- Airtable
- Notion
- Shopify
- GitHub APIs
- OpenClaw

No secrets. No API keys. No webhook URLs.

## Future Live Path

Future implementation should happen in this order:

1. Keep local queue as the visible source of operator intent.
2. Add read-only status checks for completed assets.
3. Add env-gated draft creation for Substack.
4. Add env-gated render queue creation for Remotion and HeyGen.
5. Add env-gated notification drafts for Telegram.
6. Add Airtable/Notion mirrors only after the local queue contract is stable.
7. Add OpenClaw execution only after each agent returns structured handoffs.

Every live path must be opt-in, documented, and reversible.
