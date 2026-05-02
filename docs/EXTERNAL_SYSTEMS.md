# External Systems

## Purpose

Command Center is the authority layer. External systems may produce artifacts, logs, packets, and dry-run summaries, but they do not own final approval, publishing, routing, or operator decisions.

## Registered External Sources

### SUBSTACK_ENGINE

Source repo:

```text
MajorDream444/SUBSTACK-AUTOMATION-ENGINE
```

Role:

- produce Substack/media artifacts
- produce dry-run export files
- expose article packets, scores, confidence, risk, and next actions
- report into Command Center for approval

Boundary:

- no Command Center UI duplication
- no final approval authority
- no live publish authority from Command Center context
- no Airtable write authority from Command Center context

## Expected Import Files

```text
content/logs/workflows/mission_control_export.json
content/logs/workflows/artifacts/*.json
```

Artifact JSON fields:

```text
artifact_id
mission_id
artifact_type
source
status
lane
title
github_path
airtable_record_id
requires_major_review
score
confidence
risk_level
publish_mode
next_action
system_underneath
```

## Current Build

Current implementation uses local fixtures under:

```text
fixtures/substack/
content/logs/workflows/
```

No file watcher, API, webhook, GitHub API, Airtable API, or Substack API is active.

## Import Refresh Flow

```text
Substack Engine export
-> content/logs/workflows/mission_control_export.json
-> Mission Control refresh
-> ARTIFACTS panel
-> hybrid priority ranking
-> NEXT MOVE
```

Mission Control can refresh the local artifact stream with:

```text
refresh artifacts
refresh substack artifacts
reload artifacts
```

The ARTIFACTS panel also exposes `Refresh Artifacts`.

The static fallback path is:

```text
fixtures/substack/mission_control_export.json
```

The ARTIFACTS panel reports the last import:

```text
Import: SUBSTACK_ENGINE · <count> artifacts · <path> · <timestamp> · <status>
```

Supported statuses:

- `loaded`
- `fallback`
- `missing`
- `error`

## Authority Rule

External systems produce artifacts.

Command Center ingests, displays, routes, approves, rejects, requests rewrite, or allows future publish handoff.

## Decision Export

Mission Control records approval decisions locally and exposes exportable JSON for:

```text
content/logs/workflows/mission_control_decisions.json
```

Supported decisions:

- `approved`
- `rejected`
- `rewrite_requested`
- `publish_requested`

Static browser mode cannot write the JSON file directly. Until a local CLI or automation sync is added, the ARTIFACTS panel displays the exportable decision JSON and keeps decisions in local state.

## Substack Asset Summary Import

Substack Engine produces asset files and asset generation summaries.

Mission Control imports only the summary, using:

```text
SUBSTACK_ASSET_SUMMARY_PATH="/Users/majordreamwilliams/Documents/SUBSTACK-AUTOMATION-ENGINE/content/logs/workflows/asset_generation_summary.json" npm run substack:assets:import
```

Mission Control writes:

```text
content/logs/workflows/substack_asset_generation_summary.json
content/logs/workflows/substack_asset_generation_summary.md
content/logs/workflows/substack_asset_summary_handoff.json
```

Mission Control surfaces `substack_asset_summary_handoff.json` in the `Asset Decision Queue` UI panel. The panel shows prepared, ready-for-distribution, and blocked/skipped assets for review.

Mission Control can capture local-only intended decisions into:

```text
content/logs/workflows/asset_queue_decisions.json
content/logs/workflows/asset_queue_decisions.md
```

These decisions do not render, publish, generate assets, call external APIs, or mutate the imported Substack handoff.

Routing rules:

- `prepared` -> `review_assets` in `prepared_assets_review`
- `ready_for_distribution` -> `approve_render_or_publish_queue_later` in `distribution_candidate_review`
- skipped or blocked -> `inspect_blocked_reason` in `blocked_asset_review`

Mission Control does not create assets, change asset content, render video/audio, publish live, or call external APIs.

## Substack Render / Publish Queue Handoff Import

Substack Engine may also export local queue manifests:

```text
content/logs/workflows/render_queue_handoff.json
content/logs/workflows/publish_queue_handoff.json
content/logs/workflows/render_queue_handoff_summary.json
content/logs/workflows/publish_queue_handoff_summary.json
```

Mission Control imports them with:

```text
SUBSTACK_RENDER_QUEUE_HANDOFF_PATH="/Users/majordreamwilliams/Documents/SUBSTACK-AUTOMATION-ENGINE/content/logs/workflows/render_queue_handoff.json" \
SUBSTACK_PUBLISH_QUEUE_HANDOFF_PATH="/Users/majordreamwilliams/Documents/SUBSTACK-AUTOMATION-ENGINE/content/logs/workflows/publish_queue_handoff.json" \
npm run substack:queues:import
```

Mission Control writes:

```text
content/logs/workflows/substack_render_queue_handoff.json
content/logs/workflows/substack_publish_queue_handoff.json
content/logs/workflows/substack_queue_handoffs.md
content/logs/workflows/substack_queue_handoffs_summary.json
```

The dashboard surfaces those records in `Substack Queue Handoffs` as read-only render and publish candidates.

Routing rules:

- render queue item -> `review_render_candidate`
- publish queue item -> `review_publish_candidate`
- execution mode is always `local_only`

This layer does not render, publish, call external APIs, or change Substack Engine asset content.
