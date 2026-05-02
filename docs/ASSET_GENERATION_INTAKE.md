# Asset Generation Intake

## Purpose

Mission Control imports `asset_generation_summary.json` from SUBSTACK-AUTOMATION-ENGINE so it can see which external artifacts now have prepared or distribution-ready asset packages.

Mission Control does not generate assets, publish posts, render video, render audio, or call external APIs in this flow.

## Source

Configurable source path:

```text
SUBSTACK_ASSET_SUMMARY_PATH
```

Expected Substack Engine source:

```text
/Users/majordreamwilliams/Documents/SUBSTACK-AUTOMATION-ENGINE/content/logs/workflows/asset_generation_summary.json
```

Default local path:

```text
content/logs/workflows/asset_generation_summary.json
```

Static browser fallback:

```text
fixtures/substack/asset_generation_summary.json
```

## Intake Outputs

The local CLI writes the current Mission Control import handoff:

```text
content/logs/workflows/substack_asset_generation_summary.json
content/logs/workflows/substack_asset_generation_summary.md
content/logs/workflows/substack_asset_summary_handoff.json
```

Legacy intake files may also exist:

```text
content/logs/workflows/asset_generation_intake.json
content/logs/workflows/asset_generation_intake.md
```

These are Mission Control routing summaries only.

The browser UI surfaces `content/logs/workflows/substack_asset_summary_handoff.json` in the read-only `Asset Decision Queue` panel. This panel is for operator visibility only: no approve buttons, no rendering, no publishing, no asset generation, and no duplicated Substack Engine execution logic.

## Routing Rules

Mission Control surfaces one next action and queue for each asset result:

- `asset_state = prepared`: `next_action = review_assets`, `queue = prepared_assets_review`.
- `asset_state = ready_for_distribution`: `next_action = approve_render_or_publish_queue_later`, `queue = distribution_candidate_review`.
- skipped or blocked assets: `next_action = inspect_blocked_reason`, `queue = blocked_asset_review`.

Required files:

- `video_script.md`
- `voice_script.txt`
- `hooks.json`
- `visual_prompts.json`
- `distribution_plan.json`
- `asset_manifest.json`

## Commands

```text
npm run assets:intake
npm run assets:intake -- --file fixtures/substack/asset_generation_summary.json
npm run assets:intake -- --stdin
SUBSTACK_ASSET_SUMMARY_PATH="/Users/majordreamwilliams/Documents/SUBSTACK-AUTOMATION-ENGINE/content/logs/workflows/asset_generation_summary.json" npm run substack:assets:import
```

Browser command input:

```text
refresh assets
refresh asset generation
import asset summary
reload assets
```

## Guardrails

- Mission Control is the authority.
- Substack Engine is the external artifact producer.
- No live publishing.
- No rendering.
- No asset generation inside Mission Control.
- No external API calls.
- No secrets.
