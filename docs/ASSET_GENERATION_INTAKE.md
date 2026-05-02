# Asset Generation Intake

## Purpose

Mission Control imports `asset_generation_summary.json` from SUBSTACK-AUTOMATION-ENGINE so it can see which external artifacts now have prepared or distribution-ready asset packages.

Mission Control does not generate assets, publish posts, render video, render audio, or call external APIs in this flow.

## Source

Primary local path:

```text
content/logs/workflows/asset_generation_summary.json
```

Static browser fallback:

```text
fixtures/substack/asset_generation_summary.json
```

## Intake Outputs

The local CLI writes:

```text
content/logs/workflows/asset_generation_intake.json
content/logs/workflows/asset_generation_intake.md
```

These are Mission Control routing summaries only.

## Ranking Rules

Mission Control surfaces one next decision for each asset result:

- `request rewrite` when asset generation was skipped or blocked.
- `hold` when required generated files are missing.
- `review assets` when the asset state is unclear.
- `approve for rendering queue later` when `asset_state = prepared`.
- `approve for publishing queue later` when `asset_state = ready_for_distribution`.

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
