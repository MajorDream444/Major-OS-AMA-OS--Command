# Major OS / AMA OS Command Center

This repository is the command center, dashboard, and operator console for Major OS / AMA OS.

Read these files first:

1. `START_HERE.md`
2. `SYSTEM_CORE.md`
3. `HANDOFF_COMMAND_CENTER.md`
4. `docs/HANDOFF_COMMAND_CENTER.md`

## Repo Role

```text
Command Center = Major-OS-AMA-OS--Command
Reusable AI OS = Major-AI-OS
App Factory = 52in52
Operations DB = Airtable
Human Dashboard = Notion
```

## Operating Stack

- ChatGPT plans.
- Codex builds.
- OpenClaw runs agents.
- GitHub stores truth.
- Airtable tracks operations.
- Notion is the human dashboard.
- Obsidian and Graphify hold deeper memory.

## Current Scope

This repo currently contains the clean boot layer only. Do not build dashboard features until the scaffold, source-of-truth docs, and handoff path are stable.

## Commands

```bash
make start
make dev
```

The scripts currently validate the boot layer and print the next source-of-truth files. They do not start a dashboard app yet.

## Rules

- GitHub is source of truth for code, docs, handoffs, and implementation files.
- No secrets in this repository.
- Airtable remains the operational database.
- Notion remains the human dashboard.
- Command Center references `Major-AI-OS`; it does not duplicate reusable OS logic.
- `52in52` remains the app factory and build tracker.
