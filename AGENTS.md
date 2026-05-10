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

## graphify

Graphify is installed locally and should be treated as the persistent context layer for this repo.

Primary reference: https://github.com/safishamsi/graphify

Rules:
- If `graphify-out/GRAPH_REPORT.md` exists, read it before broad source-file searches or codebase architecture answers.
- If `graphify-out/wiki/index.md` exists, navigate it before reading raw files.
- For cross-module "how does X relate to Y" questions, prefer `graphify query "<question>"`, `graphify path "<A>" "<B>"`, or `graphify explain "<concept>"` over raw grep when a graph exists.
- If no graph exists yet, do not pretend it does. Continue with normal repo inspection and note that Graphify has not been initialized for this checkout.
- After meaningful code changes, run `graphify update .` only when a graph already exists or when the user has approved creating/updating the graph.
- Do not let Graphify replace source-of-truth docs. Use it as navigation/context over `README.md`, `SYSTEM_CORE.md`, `HANDOFF_COMMAND_CENTER.md`, and project docs.
