# Graphify Context Layer

## Status

Graphify is a required persistent context layer for the HAMAL / Major OS ecosystem.

It should be treated as a constant plugin, not an optional add-on.

## Source

- Upstream repo: `https://github.com/safishamsi/graphify.git`
- Local install command used by Major:

```bash
uv tool install graphifyy && graphify install
# or
pipx install graphifyy && graphify install
# or
pip install graphifyy && graphify install
```

Graphify is a Claude Code skill that reads mixed files, builds a persistent knowledge graph, and outputs an interactive graph, Obsidian vault, wiki, graph report, graph JSON, and update cache. It can process code, markdown, PDFs, and images; supports update mode, watch mode, wiki export, git hooks, and an MCP stdio server. It is especially valuable for reducing repeated raw-file reads and preserving cross-session structure.

## Why HAMAL Needs It

HAMAL is too large to run from isolated chat memory.

The ecosystem includes:

- multiple repos
- 12 MOBS
- 144 specialist agents
- skills
- MCPs
- tools
- playbooks
- SOPs
- client systems
- documents
- PDFs
- voice-note-derived doctrine
- market signals
- Hanzo and Lux infrastructure

Without a graph layer, agents repeatedly re-read files, miss relationships, and work in silos.

Graphify gives the system:

- persistent cross-repo context
- concept relationships
- surprise-link discovery
- token-efficient querying
- Obsidian-compatible knowledge structure
- agent-crawlable wiki output
- honest provenance on edges: `EXTRACTED`, `INFERRED`, or `AMBIGUOUS`

## Operating Doctrine

```text
Graphify is not a one-time scan.
Graphify is the connective tissue of the OS.
```

Every serious repo should eventually have:

```text
graphify-out/
├── graph.html
├── obsidian/
├── wiki/
├── GRAPH_REPORT.md
├── graph.json
└── cache/
```

## Where Graphify Fits

```text
Raw files / repos / docs / images
        ↓
Graphify knowledge graph
        ↓
Obsidian + wiki + graph.json
        ↓
Agents query shared context
        ↓
Playbooks improve / workflows execute
```

## Required First Targets

### 1. Command Context Repo

```text
MajorDream444/Major-OS-AMA-OS--Command
```

Purpose:
- graph command doctrine
- 12 MOB architecture
- multi-chat handoffs
- orchestration rules

### 2. Playbook Repo

```text
MajorDream444/HAMAL_MOB_PLAYBOOKS
```

Purpose:
- graph playbooks
- SOPs
- skill audits
- client systems
- Stage A doctrine

### 3. Codex / MCP Repo

```text
MajorDream444/hanzo-lux-codex-repo
```

Purpose:
- graph MCP servers
- tools
- integrations
- executable capability layer

### 4. Major Personal Vault Later

```text
Obsidian / local archive / selected transcripts / docs
```

Purpose:
- graph Major's ideas, decisions, signals, and dormant opportunities

## Recommended Local Commands

### Initial scan

```bash
/graphify .
```

### Update after files change

```bash
/graphify . --update
```

### Deep relationship extraction

```bash
/graphify . --mode deep
```

### Build agent-readable wiki

```bash
/graphify . --wiki
```

### Keep graph synced while active work happens

```bash
/graphify . --watch
```

### Rebuild after every commit

```bash
graphify hook install
```

### Expose graph as MCP server later

```bash
/graphify . --mcp
```

## Mandatory Agent Rule

Before an agent begins a substantial repo, system, or architecture task, it should check whether a current Graphify output exists.

If it exists:
- read `GRAPH_REPORT.md`
- read `wiki/index.md` if available
- query graph before rereading many raw files

If it does not exist:
- request or create a graph pass before deep work, when local execution access allows it

## Mandatory Repo Rule

Every core HAMAL repo should eventually include a small pointer file such as:

```text
GRAPHIFY.md
```

that states:

- whether Graphify has been run
- where outputs live
- last graph update date
- recommended queries
- whether hook/watch/MCP is active

## Suggested Graph Questions

For the OS:

```text
What connects MOBS, playbooks, agents, and economic outputs?
Which playbooks depend on which tools and skills?
Which repositories overlap or duplicate each other?
What dormant ideas connect to active markets now?
Which agents touch the same memory surfaces?
Which skills appear in multiple playbooks?
```

For skills:

```text
Which skills are wrappers versus original capabilities?
Which skills have no playbook attachment?
Which tools are used by the most playbooks?
Which skills should be merged to reduce token use?
```

For client systems:

```text
What onboarding steps recur across clients?
Which deliverables repeat across offers?
Which client pain points map to the same internal playbook?
```

## Graphify + Obsidian Rule

Graphify's `obsidian/` export should be treated as a bridge into the long-term Major OS knowledge vault.

Obsidian is where the human reads and navigates.
Graphify is how the system discovers relationships.

## Graphify + Agent Registry Rule

When the agent registry is built, each agent should be graphable through:

- Mob
- skills
- tools
- workflows
- memory targets
- KPIs
- economic purpose
- related playbooks

The graph should make it visible when agents are isolated, redundant, or missing shared context.

## Graphify + Signal Intake Rule

Every major idea, voice note, market signal, repo, and opportunity should eventually be able to enter the graph so dormant ideas can resurface when conditions change.

This is essential to Major's operating style:

```text
Signal now → graph now → opportunity later
```

## Immediate Next Actions

1. Add `GRAPHIFY.md` pointer files to:
   - `Major-OS-AMA-OS--Command`
   - `HAMAL_MOB_PLAYBOOKS`
   - `hanzo-lux-codex-repo`
2. Add Graphify to all future Codex handoff prompts.
3. Run Graphify locally on the three core repos.
4. Export wiki outputs for agent navigation.
5. Add git hooks where appropriate.
6. Later, evaluate Graphify MCP mode as a shared context service for agents.

## Bootstrap Language For Future Agents

```text
Graphify is a required context layer in the HAMAL / Major OS ecosystem.
Before deep work, inspect current Graphify outputs when present: `GRAPH_REPORT.md`, `graph.json`, and `wiki/index.md`.
Prefer graph queries over repeated raw-file rereads when the graph is current.
When working in a core repo without a current graph, flag that Graphify should be run or updated locally.
```
