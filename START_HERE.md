# Start Here

## First Read Order

1. `HANDOFF_COMMAND_CENTER.md`
2. `docs/HANDOFF_COMMAND_CENTER.md`
3. `SYSTEM_CORE.md`
4. `README.md`
5. `.env.example`

## What This Repo Is

`MajorDream444/Major-OS-AMA-OS--Command` is the Command Center / dashboard / operator console repo.

It coordinates the system. It should not absorb every system into itself.

## What To Do First

1. Confirm the handoff exists at the root and in `docs/`.
2. Confirm no secrets are present.
3. Confirm the repo separation is preserved.
4. Run `make start`.
5. Run `make dev`.

## Builder Boundary

Do not build dashboard features yet. The current job is to keep the repo easy for Codex, OpenClaw, and human operators to enter cleanly.

## Canonical Split

```text
Command Center = Major-OS-AMA-OS--Command
Reusable AI OS = Major-AI-OS
App Factory = 52in52
Operations DB = Airtable
Human Dashboard = Notion
```

## Next Layer After Boot

After this boot layer is stable, the next layer should be the UI scaffold for the command center dashboard.
