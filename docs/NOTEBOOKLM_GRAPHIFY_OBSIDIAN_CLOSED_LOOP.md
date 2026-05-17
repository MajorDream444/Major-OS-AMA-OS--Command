# NotebookLM + Graphify + Obsidian Closed Loop

## Purpose
This document defines the memory and synthesis loop for Major OS / AMA OS Command Center.

We are not building isolated apps, isolated chats, or isolated agents. We are building a living organization where every meaningful input can be preserved, routed, graphed, synthesized, and reused.

## Canonical Stack

```text
GitHub      = source of truth for code, docs, specs, handoffs, implementation files
Airtable    = operational state and structured tracking
Notion      = human dashboard and client-facing workspace
Obsidian    = local linked memory vault
Graphify    = relationship graph, context compression, and agent-navigable wiki
NotebookLM  = source-grounded synthesis studio for briefs, decks, audio, and document Q&A
Command Center = operational coordination and routing
HAMAL_MOB_PLAYBOOKS = reusable doctrine, SOPs, playbooks, rubrics, agent operating models
```

## The Closed Loop

```text
New source / breakthrough / client artifact / conversation / meeting note
    -> durable source-of-truth storage
    -> human dashboard or operational tracker updated where relevant
    -> Obsidian note or local knowledge link created when it changes memory
    -> Graphify update or scheduled graph refresh
    -> NotebookLM notebook updated when synthesis or client-facing artifacts are useful
    -> reusable lesson abstracted into HAMAL_MOB_PLAYBOOKS when applicable
    -> command center handoff updated so agents enter with current context
```

## Graphify Role
Graphify is the context graph layer. It should be treated as standing infrastructure, not an optional analysis tool.

It supports:
- knowledge graphs across code, PDFs, markdown, screenshots, diagrams, and images
- persistent `graph.json`
- agent-navigable wiki output
- graph reports, god nodes, surprising connections, and suggested questions
- update/watch modes so the graph can stay current as files change
- MCP mode where useful

Recommended usage patterns:

```bash
/graphify ./path --update
/graphify ./path --wiki
/graphify ./path --mcp
graphify hook install
```

## Obsidian Role
Obsidian is the local linked memory vault. It is where deeper narrative, conceptual, and cross-project context can live in a graph-friendly markdown structure.

Use Obsidian skills to create and maintain:
- linked markdown notes
- Bases
- JSON Canvas diagrams
- agent-readable vault organization
- clean extraction from web pages when appropriate

## NotebookLM Role
NotebookLM is the synthesis and artifact studio. It is not the source of truth, but it is essential for:
- source-grounded document Q&A
- client update briefs
- audio overviews / podcasts
- decks and reports
- milestone summaries
- handover recaps
- structured synthesis from large source packs

NotebookLM should receive curated source packs, not become a dumping ground without routing discipline.

## Agent Awareness Standard
Every agent should know:
1. its own job,
2. what adjacent agents do,
3. what tools it may use,
4. where its outputs belong,
5. when to hand off,
6. when to update shared context.

The organization is agentive only when memory and handoffs are explicit.

## No-Leak Doctrine
No meaningful artifact is complete until it has:
- a durable home,
- a clear owner,
- a routing note if cross-system relevant,
- a memory update if it changes operating understanding,
- a playbook abstraction if reusable.

## Client-Specific vs Shared Doctrine
Client-specific material remains in the client lane. Reusable standards are abstracted before entering shared doctrine.

Example:
- Theo's revised SOW = client-specific
- Serious Client Due-Diligence Response Protocol = reusable playbook

## Theo as First Live Pressure Test
Theo / Howling MUNE demonstrates the closed loop in practice:

```text
Theo close package
    -> GitHub source docs / handoff
    -> Notion Theo workspace
    -> NotebookLM Theo notebook
    -> Obsidian local project note
    -> Graphify context graph
    -> HAMAL playbook extraction of reusable doctrine
```

## Final Principle

```text
Nothing meaningful is lost.
Nothing reusable stays isolated.
Every agent gets smarter through the organism.
```
