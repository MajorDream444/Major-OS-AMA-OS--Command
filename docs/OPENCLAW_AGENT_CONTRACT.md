# OpenClaw Agent Contract

## Purpose

This contract defines how Command Center agents should be represented before OpenClaw executes real work.

Current build: local/mock only.

Do not connect Airtable, Notion, GitHub APIs, Substack, Telegram, HeyGen, Remotion, Shopify, or OpenClaw yet.

## What An Agent Is

An agent is a named operating module with:

- a stable ID
- a role
- an allowed workflow
- visible status
- a current task
- a last reported event
- a handoff format
- a list of allowed tools

Agents do not perform external actions in this build. They simulate work and report state back to Mission Control.

## Required Agent Fields

```text
id:
name:
role:
status:
current_task:
last_event:
needs_major:
tools:
workflow:
```

## Allowed Statuses

```text
IDLE
READY
WORKING
WAITING
BLOCKED
DONE
SYNCED
```

## Required Handoff Format

Every agent task must leave a handoff line:

```text
[timestamp] [agent_id] [agent_name] [status] [mission_id] [current_task] [last_event] [next_action]
```

## Command Routing Rules

Local Mission Control routing:

```text
lead / find / scout -> A001 Scout
audit / diagnose -> A002 Audit
content / video / remotion / heygen / substack -> A003 Content Catcher
email / outreach / follow up -> A006 Outreach
shopify / gumroad / store / product -> A009 Storefront Operator
show agents -> A004 Ops Watcher registry review
fallback -> A004 Ops Watcher
```

## Logging Requirements

Each simulated event should update:

- Activity Feed
- agent `status`
- agent `current_task`
- agent `last_event`
- `needs_major` when the task waits for Major review
- Top 3 Actions when Major review is needed

## Reporting Back To Mission Control

Agents report by updating local state.

Mission Control must show:

- current status
- current task
- last event
- Needs Major indicator
- visible working animation
- persisted state after refresh

## Future OpenClaw Execution Path

When approved, OpenClaw should:

1. Read the agent registry contract.
2. Load the command routing rules.
3. Receive a mission object from Mission Control.
4. Execute only allowed workflow steps.
5. Return a structured handoff.
6. Let Mission Control decide whether to log, escalate, or request Major review.

## Boundary

OpenClaw execution is not implemented here.

This file only prepares the local contract and UI state model.
