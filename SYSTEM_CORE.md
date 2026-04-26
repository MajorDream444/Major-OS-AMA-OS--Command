# System Core

## Identity

This repo is the Command Center for Major OS / AMA OS. It is the operator-facing coordination layer for apps, agents, workflows, dashboards, handoffs, and sync surfaces.

## Source Of Truth Map

```text
Command Center = Major-OS-AMA-OS--Command
Reusable AI OS = Major-AI-OS
App Factory = 52in52
Operations DB = Airtable
Human Dashboard = Notion
```

## Responsibilities

The Command Center owns:

- Operator entrypoints
- Dashboard shell and navigation
- App registry views
- Airtable, Notion, and GitHub coordination surfaces
- Codex and OpenClaw handoff files
- Admin workflows
- Sync planning and status visibility

The Command Center does not own:

- Reusable AI OS skill logic
- Productized OS templates that belong in `Major-AI-OS`
- Individual app implementations that belong in `52in52`
- Operational records that belong in Airtable
- Human-readable planning dashboards that belong in Notion

## Operating Sentence

ChatGPT plans it. Codex builds it. OpenClaw runs the agents. GitHub stores the truth. Airtable tracks the business. Notion gives the dashboard. Obsidian and Graphify store deep memory.

## Build Rule

Start with the boot layer. Do not add dashboard features until the entrypoint files, handoff docs, environment template, and repo commands are stable.

## Security Rule

Never commit API keys, access tokens, database credentials, Airtable tokens, Notion tokens, OpenAI keys, or private webhook URLs.
