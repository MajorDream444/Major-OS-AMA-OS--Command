# Command Center Handoff

The canonical handoff currently lives at the repository root:

- `HANDOFF_COMMAND_CENTER.md`

This `docs/` entrypoint exists because the builder priorities reference `/docs/HANDOFF_COMMAND_CENTER.md` as a required path. Keep this file in sync with the root handoff or replace it with a full copy when the handoff becomes stable enough to duplicate.

## Required Operating Rule

```text
Command Center = Major-OS-AMA-OS--Command
Reusable AI OS = Major-AI-OS
App Factory = 52in52
Operations DB = Airtable
Human Dashboard = Notion
```

## Builder Instruction

Read the root `HANDOFF_COMMAND_CENTER.md` first. Do not build dashboard features until the clean boot layer and repo entrypoints are present.
