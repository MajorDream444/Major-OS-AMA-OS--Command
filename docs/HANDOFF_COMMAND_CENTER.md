# Command Center Handoff

The canonical handoff currently lives at the repository root:

- `HANDOFF_COMMAND_CENTER.md`

This `docs/` entrypoint exists because the builder priorities reference `/docs/HANDOFF_COMMAND_CENTER.md` as a required path. Keep this file in sync with the root handoff or replace it with a full copy when the handoff becomes stable enough to duplicate.

## Required Operating Rule

```text
AMA Command Center coordinates.
MAIM teaches.
HAMAL provides doctrine and orchestration standards.
Major-AI-OS holds reusable product/system layer.
52in52 builds weekly apps.
Hanzo provides AI infrastructure.
Lux provides sovereignty.
Airtable tracks operations.
Notion presents the human dashboard.
```

## Builder Instruction

Read `ECOSYSTEM_BOUNDARY.md`, `STAGE.md`, and the root `HANDOFF_COMMAND_CENTER.md` first. Do not build dashboard features until the clean boot layer and repo entrypoints are present.

Stage A safety:

- No dashboard features.
- No live integrations.
- No Airtable writes.
- No Notion writes.
- No OpenClaw execution.
- No Hanzo source changes.
- No Lux implementation.
- No secrets.
