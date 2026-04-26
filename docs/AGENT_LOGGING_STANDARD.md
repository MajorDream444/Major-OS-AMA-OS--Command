# Agent Logging Standard

## Purpose

Agent logs make the Command Center auditable without relying on chat memory.

## Required Log Fields

Each agent event should include:

- timestamp
- agent id
- agent name
- status
- mission id
- action type
- summary
- next action
- source path or evidence link

## Status Labels

Use these labels consistently:

- IDLE
- WORKING
- WAITING
- READY
- BLOCKED
- DONE
- REVIEW
- ACTION
- SYNCED

## Daily Brief Labels

Use these labels for the 30-day aggressive execution cycle:

- REVENUE ACTION
- CONTENT ACTION
- SYSTEM IMPROVEMENT
- BLOCKER

## Handoff Requirement

Every task must leave a handoff.

Minimum handoff line:

```text
[timestamp] [agent] [status] [mission] [next action] [evidence]
```

## Current Build Boundary

For now, all logs are local/mock and visible in the Command Center UI.

Do not write to Airtable, Notion, GitHub APIs, Gmail, Telegram, HeyGen, Remotion, or n8n yet.
