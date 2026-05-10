# Graphify Context Layer

Graphify is the persistent context layer for this Command Center repo.

Install reference:

```bash
uv tool install graphifyy && graphify install
# or
pipx install graphifyy && graphify install
# or
pip install graphifyy && graphify install
```

Repository reference: `https://github.com/safishamsi/graphify`

## Role

Graphify helps agents navigate the repo through a local knowledge graph. It should provide context, relationships, and architecture paths before agents spend time reading disconnected files.

It is not a product feature, a CRM, a CMS, or an external integration.

## Codex Hook

This repo has Graphify registered for Codex through:

- `AGENTS.md`
- `.codex/hooks.json`

The hook points to the local Graphify command at:

```text
/Users/majordreamwilliams/.local/bin/graphify
```

## Operating Rule

If `graphify-out/GRAPH_REPORT.md` exists, read it before broad repo exploration.

If `graphify-out/wiki/index.md` exists, use it as the graph navigation entrypoint.

If no graph exists, continue normal repo inspection and say plainly that Graphify has not been initialized for this checkout.

Do not run write-back, sync, or automation behavior just because Graphify exists. It is context infrastructure first.
