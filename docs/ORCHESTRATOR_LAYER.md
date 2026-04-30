# Orchestrator Layer

## Purpose

The Orchestrator turns an operator command into a local mission plan, assigns mock agents, runs the plan in simulation, and updates Mission Control.

Current build: A only.

No artifacts beyond simple placeholder output. No agent evaluation. No sandbox/browser execution. No external services.

## Mission Object

```text
mission = {
  id,
  command,
  intent,
  status,
  created_at,
  updated_at,
  assigned_agents,
  plan,
  current_step,
  steps_completed,
  next_action,
  needs_major,
  output_summary
}
```

## Intent Detection

- `lead`, `find`, `scout`, `contour leads`, `SAF leads` -> `lead_generation`
- `audit`, `diagnose`, `review business` -> `audit`
- `content`, `substack`, `article`, `video`, `remotion`, `heygen` -> `content_media`
- `email`, `outreach`, `follow up`, `dm` -> `outreach`
- `shopify`, `gumroad`, `product`, `store` -> `commerce`
- `daily brief`, `report`, `status` -> `operations`
- fallback -> `operations`

## Agent Assignment

- `lead_generation`: A001 Scout, A002 Audit, A006 Outreach
- `audit`: A002 Audit, A004 Ops Watcher
- `content_media`: A003 Content Catcher, A007 Offer Builder
- `outreach`: A006 Outreach, A002 Audit
- `commerce`: A009 Storefront Operator, A007 Offer Builder
- `operations`: A004 Ops Watcher

## Mission Statuses

- PLANNED
- RUNNING
- NEEDS MAJOR
- REVIEW
- DONE
- BLOCKED

## Local-Only Behavior

The Orchestrator currently:

1. Creates a local mission.
2. Assigns local mock agents.
3. Steps through the plan with timed simulation.
4. Updates the Mission Board and Activity Feed.
5. Persists mission state through `localStorage`.
6. Ends most missions in `NEEDS MAJOR` so Major can approve the next move.

Commands containing `auto`, `status`, or `daily brief` can finish as `DONE`.

## Future Integration Path

Future live execution can connect in this order:

1. Kimi or another model proposes richer plans.
2. Hanzo enriches agent/system intelligence.
3. OpenClaw executes approved agent workflows.
4. Hyperbrowser or browser sandbox handles browser-only tasks.
5. Airtable and Notion mirror approved state.
6. GitHub stores durable logs and handoffs.

## Guardrail

The Orchestrator plans and simulates now.

Real execution comes later, after explicit approval, credentials, scopes, and logging rules exist.

No secrets. No API calls. No external writes.
