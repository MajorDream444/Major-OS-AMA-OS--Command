# Substack Queue Handoff Intake

## Purpose

Mission Control imports Substack Engine render and publish queue handoffs so Major can review downstream candidates without triggering execution.

Command Center remains the authority. SUBSTACK-AUTOMATION-ENGINE remains an external artifact producer.

## Source Files

Substack Engine may export:

```text
content/logs/workflows/render_queue_handoff.json
content/logs/workflows/publish_queue_handoff.json
content/logs/workflows/render_queue_handoff_summary.json
content/logs/workflows/publish_queue_handoff_summary.json
```

Mission Control reads the JSON handoffs from configurable local paths:

```text
SUBSTACK_RENDER_QUEUE_HANDOFF_PATH
SUBSTACK_PUBLISH_QUEUE_HANDOFF_PATH
```

## Local Import

Run:

```text
npm run substack:queues:import
```

With explicit paths:

```text
SUBSTACK_RENDER_QUEUE_HANDOFF_PATH="/Users/majordreamwilliams/Documents/SUBSTACK-AUTOMATION-ENGINE/content/logs/workflows/render_queue_handoff.json" \
SUBSTACK_PUBLISH_QUEUE_HANDOFF_PATH="/Users/majordreamwilliams/Documents/SUBSTACK-AUTOMATION-ENGINE/content/logs/workflows/publish_queue_handoff.json" \
npm run substack:queues:import
```

Mission Control writes local copies and a combined summary:

```text
content/logs/workflows/substack_render_queue_handoff.json
content/logs/workflows/substack_publish_queue_handoff.json
content/logs/workflows/substack_queue_handoffs.md
content/logs/workflows/substack_queue_handoffs_summary.json
```

## Routing

Render queue items are normalized as:

```text
queue_type = render
next_action = review_render_candidate
execution_mode = local_only
```

Publish queue items are normalized as:

```text
queue_type = publish
next_action = review_publish_candidate
execution_mode = local_only
```

## UI

The Command Center dashboard shows a read-only panel:

```text
Substack Queue Handoffs
```

It displays:

- render queue count
- publish queue count
- blocked/skipped count
- artifact ID
- mission ID
- title
- lane
- queue type
- recommended renderer or platforms
- source asset folder
- execution mode
- next action

## Guardrails

Mission Control does not:

- render video or audio
- publish live
- call external APIs
- generate assets
- mutate Substack Engine production files
- duplicate Substack Engine production logic

This intake is review-only. Execution comes later through explicit approved handoffs.
