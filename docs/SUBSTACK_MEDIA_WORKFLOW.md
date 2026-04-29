# Substack Media Workflow

## Purpose

This protocol defines the local Command Center workflow for turning a raw thought into a published Substack asset, video script, mock media queue, distribution handoff, and memory update.

Current build: local simulation only.

Do not connect Substack, Remotion, HeyGen, Telegram, Airtable, Notion, Shopify, GitHub APIs, OpenClaw, or any external service yet.

No secrets. No API keys. No external writes.

## Workflow Stages

```text
Raw Thought -> Substack Draft -> Editorial Polish -> Publish -> Hooks -> Video Script -> Remotion Queue -> HeyGen Queue -> Distribution -> Memory Update
```

Mission Control UI labels:

- Raw Thought
- Draft
- Edit
- Publish
- Hooks
- Video Script
- Remotion
- HeyGen
- Distribution
- Memory Update

## Allowed Commands

```text
draft substack <topic>
make video from <topic>
queue remotion <topic>
queue heygen <topic>
publish <topic>
```

Routing:

- `substack`, `article`, `essay`, `draft`, `newsletter` route to `A003 Content Catcher`.
- `remotion`, `video script`, `heygen`, `avatar` route to `A003 Content Catcher` first.
- Media render commands create a follow-up local task. They do not call Remotion or HeyGen.

## Lane Mapping Rule

Every Substack/media item must map to one lane:

- `BWYH`: trust-building
- `Contour`: authority / sales support
- `SAF`: narrative / research
- `Major AI OS`: productization
- `Doctrine`: personal doctrine / 10 Pillars

If a lane is unclear, keep it in `Doctrine` until Major assigns the operating lane.

## No Content Chaos Rule

No asset floats without a lane, stage, next action, assigned agent, and status.

Every item must answer:

- What is the idea?
- Which lane does it serve?
- What stage is it in?
- What is the next action?
- Which agent owns the handoff?
- Is it ready, queued, blocked, or waiting for review?

## Local State

The local workflow persists in browser `localStorage` through the existing Command Center state system.

The reset control clears local workflow state and reloads seed data.

## Future Live Integration Path

Future implementation should happen in this order:

1. Read-only GitHub log view for workflow evidence.
2. Airtable read/write records for content state.
3. Notion human dashboard mirror.
4. Substack draft creation.
5. Remotion queue creation.
6. HeyGen queue creation.
7. Telegram distribution notification.
8. Obsidian / Graphify memory update.
9. OpenClaw execution against the agent contract.

Live integrations must remain opt-in, env-gated, and documented before use.
