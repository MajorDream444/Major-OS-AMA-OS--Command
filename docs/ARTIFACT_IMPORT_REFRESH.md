# Artifact Import Refresh

## Purpose

Mission Control ingests external artifacts from local export files. External systems produce artifacts; Command Center ranks, displays, routes, and approves them.

## Current Source

```text
content/logs/workflows/mission_control_export.json
```

Static browser fallback:

```text
fixtures/substack/mission_control_export.json
```

## Asset Summary Intake

Mission Control also imports SUBSTACK-AUTOMATION-ENGINE asset summaries from:

```text
SUBSTACK_ASSET_SUMMARY_PATH
```

The expected source path is:

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

This does not create assets. It only tells Mission Control which artifacts have prepared or ready-for-distribution asset packages and which next decision should surface.

Current local import outputs:

```text
content/logs/workflows/substack_asset_generation_summary.json
content/logs/workflows/substack_asset_generation_summary.md
content/logs/workflows/substack_asset_summary_handoff.json
```

## Refresh Flow

```text
Substack Engine export
-> Mission Control refresh
-> ARTIFACTS panel
-> hybrid priority ranking
-> NEXT MOVE
```

## Commands

```text
refresh artifacts
refresh substack artifacts
reload artifacts
refresh assets
refresh asset generation
import asset summary
reload assets
```

## UI Control

The ARTIFACTS panel includes:

```text
Refresh Artifacts
Refresh Assets
```

Clicking it reloads the local export, preserves the active source filter, re-runs ranking, updates NEXT MOVE, and appends:

```text
Refreshed SUBSTACK_ENGINE artifacts from export
```

## Import Status Line

The ARTIFACTS panel shows the last import status:

```text
Import: SUBSTACK_ENGINE · 3 artifacts · content/logs/workflows/mission_control_export.json · 13:42 · loaded
```

Asset summary line:

```text
Assets: SUBSTACK_ENGINE · 3 artifacts · 1 prepared · 1 distribution-ready · 1 skipped · fixtures/substack/asset_generation_summary.json · 13:42 · fallback
```

Fields:

- source
- artifact count
- file path used
- timestamp
- status

Statuses:

- `loaded`: primary export file loaded
- `fallback`: static fixture loaded after primary export failed
- `missing`: primary export and fallback fixture were not found
- `error`: refresh failed for another local parsing or fetch reason

## Missing Export Behavior

If the export cannot be loaded from the local path or fallback fixture, Mission Control must not crash.

It should:

- keep local artifacts visible
- add a blocked fallback artifact
- show Needs Major: `Substack export missing`
- log the missing export in Activity Feed

## Guardrails

- No live APIs.
- No secrets.
- No external writes.
- No Substack content generation inside Command Center.
- No asset generation, rendering, or live publishing inside Command Center.
- Command Center owns approval and publish handoff.
