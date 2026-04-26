# Agents

## Runtime

OpenClaw is the intended agent runtime.

The current Command Center uses local/mock agent simulation only.

## Active Mock Agent Roster

- A001 Scout
- A002 Audit
- A003 Content Catcher
- A004 Ops Watcher
- A005 Grant Hunter
- A006 Outreach
- A007 Offer Builder
- A008 Deck Builder
- A009 Storefront Operator
- A010 Meeting Synthesizer

## Agent Rule

Agents must support the daily loop:

```text
Plan -> Build -> Run -> Log -> Improve
```

## Daily Outputs

Every day needs:

- one revenue action
- one content action
- one logged system improvement

## Logging

Use `docs/AGENT_LOGGING_STANDARD.md`.

No agent should rely on chat memory as the record.
