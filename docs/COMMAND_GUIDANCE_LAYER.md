# Command Guidance Layer

## Purpose

The Command Guidance Layer makes Mission Control easier to read while the system is still local-first. It adds plain-language narration and one recommended next command without creating new workflows, integrations, or agent systems.

This layer explains what already exists in local state:

- missions
- agent statuses
- mission stages
- artifacts
- Major review holds

## System Narrator

The `SYSTEM STATUS` panel turns current runtime state into 3-6 short lines.

It answers:

- What mission is active?
- What stage is the mission in?
- Which agents are working or waiting?
- How many artifacts exist?
- Is the system waiting on Major?

The narrator is generated from local `app.js` state and persists as `state.systemGuidance` in `localStorage`.

## Next Move Logic

The `NEXT MOVE` panel always shows one action:

1. If any artifact has `NEEDS REVIEW`, recommend approving that artifact.
2. Else if any mission has `NEEDS MAJOR`, recommend reviewing missions.
3. Else if the latest mission is content/media, recommend distribution.
4. Otherwise, recommend the next revenue-facing command.

The panel displays:

- `NEXT MOVE`: the single recommended action
- `WHY`: one sentence of rationale
- `COMMAND`: exact command the operator can type

Clicking the panel fills the command input with the recommended command. It does not auto-send.

## Operator Guidance Rule

The system may guide the operator, but it may not execute external actions from this layer.

No API calls. No external writes. No credentials. No integrations.

## Activity Feed

When guidance changes after local state updates, Mission Control logs:

```text
System guidance updated
```

This keeps the guidance layer visible in the same local event stream as missions, artifacts, and agents.
