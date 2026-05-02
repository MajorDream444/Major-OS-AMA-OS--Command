# Asset Queue Decisions

## Purpose

Mission Control records Major's intended next action for Substack-generated asset packages.

Substack Automation Engine remains the external artifact producer. Mission Control does not generate assets, render video, render audio, publish live, or call external APIs.

## Source Handoff

```text
content/logs/workflows/substack_asset_summary_handoff.json
```

This imported handoff is preserved as raw source context and must not be mutated by browser decision controls.

## Decision Outputs

```text
content/logs/workflows/asset_queue_decisions.json
content/logs/workflows/asset_queue_decisions.md
```

In the static browser app, decisions are captured in local state and shown as exportable JSON in the Asset Decision Queue panel. The repo files are local handoff targets.

Sync browser-exported decisions into the repo handoff files with:

```text
npm run asset-queue:decisions:sync -- --file fixtures/substack/sample_asset_queue_decisions_export.json
```

## Schema

```json
{
  "asset_decision_id": "AD-YYYYMMDD-HHMMSS-XXXX",
  "artifact_id": "",
  "mission_id": "",
  "title": "",
  "lane": "",
  "asset_state": "",
  "decision": "hold | review_assets | request_asset_rewrite | approve_for_render_queue | approve_for_publish_queue_later | block_asset",
  "decided_by": "Major",
  "decided_at": "",
  "reason": "",
  "source": "MISSION_CONTROL",
  "execution_mode": "local_only"
}
```

## Allowed Decisions

- `hold`
- `review_assets`
- `request_asset_rewrite`
- `approve_for_render_queue`
- `approve_for_publish_queue_later`
- `block_asset`

## Guardrails

- Buttons only write a local decision log.
- No rendering.
- No publishing.
- No external API calls.
- No Substack Engine asset generation.
- No mutation of the imported handoff file.
- Preserve raw summary always.
