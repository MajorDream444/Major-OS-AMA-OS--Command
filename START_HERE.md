# Start Here

## First Read Order

1. `ECOSYSTEM_BOUNDARY.md`
2. `STAGE.md`
3. `SYSTEM_CORE.md`
4. `52IN52_AND_KNOWLEDGE_CENTER.md`
5. `HANDOFF_COMMAND_CENTER.md`
6. `docs/HANDOFF_COMMAND_CENTER.md`
7. `README.md`
8. `.env.example`

## What This Repo Is

`MajorDream444/Major-OS-AMA-OS--Command` is the Command Center / dashboard / operator console repo.

It coordinates the system. It should not absorb every system into itself.

Canonical boundary:

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

## What To Do First

1. Confirm the handoff exists at the root and in `docs/`.
2. Confirm no secrets are present.
3. Confirm the repo separation is preserved.
4. Run `make start`.
5. Run `make dev`.

## Builder Boundary

Do not build dashboard features yet. The current job is to keep the repo easy for Codex, OpenClaw, and human operators to enter cleanly.

No live integrations, Airtable writes, Notion writes, OpenClaw execution, Hanzo source changes, Lux implementation, or secrets.

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

Before choosing that build, review whether the next approved layer is the dashboard scaffold, 52-in-52 app registry view, Knowledge Center view, or sync/status visibility.
