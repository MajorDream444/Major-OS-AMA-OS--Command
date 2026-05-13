# Multi-Chat Handoff Context — AMA OS / MOBS / Command Center

This document gives other ChatGPT, Claude, Codex, OpenClaw, or agent-building chats the necessary context to support the current build without losing the thread.

## Current Objective

We are building an AI-native operating system around Major Dream Williams' AMA / Art Mob / HAMAL ecosystem.

The goal is not to build random bots.

The goal is to build an executable AI workforce civilization made of:

- 12 core MOBS
- 144 eventual specialized agents
- shared memory
- repo-native playbooks
- command-center orchestration
- business workflows
- revenue/event automation
- real-world client deployments

The current phase is foundation and scaffolding.

## Core Repositories

### 1. HAMAL_MOB_PLAYBOOKS

Repo:
`https://github.com/MajorDream444/HAMAL_MOB_PLAYBOOKS.git`

Purpose:
This is the doctrine, SOP, playbook, rubric, and operating-model library.

It should store:

- MOB playbooks
- SOPs
- workflow playbooks
- industry systems
- source notes
- templates
- rubrics
- audit notes
- agent context files

Recently added:

- `03_mobs/MOB_EXECUTION_FRAMEWORK.md`

This file defines how to evolve each Mob from a descriptive concept into an executable operating system.

### 2. agency-agents

Repo:
`https://github.com/MajorDream444/agency-agents.git`

Purpose:
This is the executable agent layer.

It should store:

- individual agents
- agent templates
- division/MOB agent rosters
- installable agent files
- runtime-specific versions for Claude Code, Cursor, OpenClaw, NotebookLM, etc.

Recently added:

- `templates/mob-agent-template.md`

This file defines the standard structure every MOB agent should follow:

- identity
- personality
- mission
- objectives
- inputs
- outputs
- tool stack
- workflow logic
- KPIs
- memory requirements
- escalation rules
- cross-MOB handoffs
- definition of done

### 3. Major-OS-AMA-OS--Command

Repo:
`https://github.com/MajorDream444/Major-OS-AMA-OS--Command.git`

Purpose:
This is the command-center / orchestration repo.

It should store:

- system architecture
- command-center UI/runtime logic
- routing rules
- event schemas
- memory schemas
- orchestration plans
- dashboards
- agent coordination protocols

Recently added:

- `COMMAND_CENTER_ARCHITECTURE_V2.md`
- `HANDOFF_MULTI_CHAT_CONTEXT.md`

The command center should be treated as an orchestration nervous system, not just a dashboard.

## Core Context Plugin — Graphify

Graphify is now considered a **constant core plugin** for AMA OS / HAMAL / Art Mob work.

Repo:
`https://github.com/safishamsi/graphify.git`

Install:

```bash
uv tool install graphifyy && graphify install
# or: pipx install graphifyy && graphify install
# or: pip install graphifyy && graphify install
```

Why it matters:

- It turns mixed project material into a persistent knowledge graph.
- It can read code, markdown, PDFs, images, diagrams, screenshots, and other project files.
- It preserves relationships across files instead of forcing every agent to reread raw folders from scratch.
- It creates `graph.json`, `GRAPH_REPORT.md`, interactive graph views, Obsidian output, optional wiki output, and optional MCP serving.
- It can run in update mode, watch mode, and post-commit hook mode so project context stays current as the system evolves.

How it fits the architecture:

- **Maestros Mob** owns Graphify orchestration and update routines.
- **Artisans Mob** uses the graph for structured insight, dashboards, and scoring.
- **Visionaries Mob** uses the graph for long-range pattern recognition and scenario mapping.
- **Vanguards Mob** should govern provenance, inferred-vs-extracted edges, permissions, and data hygiene.
- The command center should treat Graphify as part of the **shared memory layer**, not as an optional side utility.

Required operating behavior:

1. Major project repos should be graphified regularly.
2. Any repo used as a source of truth should maintain a fresh graph after major structural changes.
3. New chats or agents should be able to consult Graphify outputs before rebuilding context manually.
4. The system should prefer graph queries, wiki navigation, and persistent graph memory before re-reading entire raw corpora.
5. Graphify outputs should eventually feed Obsidian, the command center, and any local-memory layer used by the 144-agent system.

Recommended commands:

```bash
/graphify .
/graphify . --update
/graphify . --watch
/graphify . --wiki
graphify hook install
/graphify query "what connects [concept A] to [concept B]?"
/graphify path "Concept A" "Concept B"
/graphify explain "Concept"
```

Current principle:

> If a repo, notebook, source folder, or project corpus matters enough to influence decisions, it should eventually be graphified.

## Core Doctrine

The MOBS are not just characters or departments.

They are intended to become:

- operational divisions
- behavior systems
- knowledge domains
- economic units
- agent swarms
- memory clusters

Each Mob needs to become executable.

That means every Mob must define:

1. Strategic purpose
2. Core objectives
3. Inputs
4. Outputs
5. Agent hierarchy
6. Tool stack
7. Memory layer
8. KPIs
9. Cross-Mob communication
10. Economic logic

## The 12 MOBS

### 1. Avant-Garde Mob
Innovation, creativity, trend forecasting, market exploration, and risk management in innovation.

### 2. Artisans Mob
Data craftsmanship, analytics, dashboards, trend identification, and insight tailoring.

### 3. Visionaries Mob
Long-term strategy, scenario planning, impact forecasting, opportunity mapping, and resource planning.

### 4. Innovators Mob
Product development, prototyping, market research, agile development, and feedback implementation.

### 5. Maestros Mob
Workflow optimization, data integration, automation, APIs, orchestration, and cross-department coordination.

### 6. Revolutionaries Mob
Transformation, disruption, business model overhaul, change management, and brand reinvention.

### 7. Luminaries Mob
Leadership, mentorship, legacy building, team development, and succession planning.

### 8. Vanguards Mob
Security, compliance, ethical AI, privacy, audits, and governance.

### 9. Provocateurs Mob
Marketing, bold storytelling, campaign strategy, audience engagement, and analytics feedback.

### 10. Dreamweavers Mob
Brand storytelling, immersive experiences, emotional branding, community building, and visual storytelling.

### 11. Guardians Mob
Reputation management, crisis response, public relations, brand protection, and recovery.

### 12. Strategists Mob
Growth planning, competitive positioning, market expansion, operational efficiency, and business model innovation.

## Core MOBS / Nervous System

These five are the central operating layer:

### Maestros
Orchestration, workflow routing, API integration, automation, sync, and infrastructure.

### Artisans
Data intelligence, scoring, dashboards, analytics, model refinement, and feedback loops.

### Visionaries
Forecasting, simulations, strategic foresight, future-state planning.

### Strategists
Growth, monetization, positioning, offer design, and market expansion.

### Vanguards
Security, compliance, ethics, permissions, privacy, contracts, and memory governance.

## Operational MOBS

The remaining MOBS act as specialized force multipliers:

- Dreamweavers: narrative and immersive brand worldbuilding
- Provocateurs: attention, campaigns, and audience capture
- Guardians: reputation defense and crisis response
- Revolutionaries: transformation and disruption
- Luminaries: mentorship, leadership, legacy, and human growth
- Innovators: products, prototypes, and market research
- Avant-Garde: cultural forecasting and frontier ideas

## Current Strategic Decision

Do not build 144 agents immediately.

Build 12 executable MOBS first.

Each Mob should start with:

- 1 lead orchestrator
- 3 to 5 specialist agents
- shared memory rules
- clear workflows
- KPIs
- tools
- cross-MOB handoff logic

Then expand toward 144 total specialized agents.

## Existing Real-World Use Cases

Several prior business concepts should be treated as real-world deployment patterns for the MOBS.

### Global Athlete Launchpad
Human transformation OS for athletes.

Themes:

- athlete business building
- AI/Web3 education
- wellness and mindset
- retreat/community model
- content/reality show layer
- NFT/DAO membership

Relevant MOBS:

- Luminaries
- Dreamweavers
- Strategists
- Provocateurs
- Vanguards
- Maestros

### Mintistry / Caribbean Cultural Ledger
Sovereign cultural preservation and blockchain infrastructure.

Themes:

- cultural preservation
- sovereign ledger
- digital heritage centers
- AI/blockchain education
- VR/AR museums
- programmable cultural assets

Relevant MOBS:

- Dreamweavers
- Vanguards
- Strategists
- Visionaries
- Luminaries
- Maestros

### Jamaican Seafood Venture
Ethical supply chain and direct-market system.

Themes:

- Jamaica-to-NYC seafood supply chain
- fisher coordination
- cold chain logistics
- sustainability
- traceability
- QR/blockchain provenance
- restaurant/market distribution

Relevant MOBS:

- Maestros
- Artisans
- Vanguards
- Strategists
- Provocateurs
- Guardians

### AI Content / Automation JSON Workflows
Several JSON workflows were reviewed as real-world automation patterns.

Patterns identified:

- content distribution OS
- AI clone / influencer factory
- Stripe paid-invoice automation
- Reddit business opportunity analyzer

Key lesson:
Most automations are linear. AMA OS must become adaptive, persistent, memory-based, collaborative, goal-driven, and economically aligned.

## Command Center Concept

The command center is not only a UI.

It is an event-driven orchestration layer.

It should handle:

- intake
- routing
- agent assignment
- memory updates
- workflow triggers
- KPI tracking
- revenue attribution
- alerts
- human review gates
- approval flows

## Event-Driven Architecture

Everything should be treated as an event.

Examples:

- Lead Created
- Lead Qualified
- Proposal Sent
- Invoice Paid
- Client Onboarded
- Content Published
- Campaign Underperforming
- Support Escalated
- Crisis Detected
- Deal Closed
- Churn Risk Detected

Each event can trigger:

- one or more agents
- workflows
- score updates
- notifications
- dashboards
- memory writes
- human approval requests

## Shared Memory Requirement

A key missing layer is shared memory.

Needed memory types:

### Operational Memory
Workflows, execution logs, system state.

### Identity Memory
Brand voice, user preference, agent persona, tone, values.

### Strategic Memory
Decisions, assumptions, forecasts, past outcomes.

### Economic Memory
Revenue attribution, CAC, LTV, deal source, performance metrics.

### Compliance Memory
Permissions, approvals, exclusions, risk flags, legal boundaries.

### Graph Memory
Persistent concept relationships, cross-repo connections, inferred and extracted edges, community structure, and navigable project context generated by Graphify.

## Next Build Priorities

### Priority 1 — Shared Event Schema
Create a canonical event schema for the command center.

Suggested file:
`schemas/event.schema.json`

### Priority 2 — Shared Agent Handoff Schema
Create a standard handoff package that agents use when passing work.

Suggested file:
`schemas/agent-handoff.schema.json`

### Priority 3 — Graphify Operating SOP
Create a standing SOP for when to run Graphify, where outputs live, how often graphs update, and how agents should use the graph before rebuilding context manually.

Suggested file in `HAMAL_MOB_PLAYBOOKS`:
`01_sops/graphify-context-plugin-sop.md`

### Priority 4 — 12 MOB Lead Orchestrator Files
Create one lead orchestrator agent for each Mob.

Suggested path in `agency-agents`:

```text
mobs/01-avant-garde/lead-orchestrator.md
mobs/02-artisans/lead-orchestrator.md
mobs/03-visionaries/lead-orchestrator.md
mobs/04-innovators/lead-orchestrator.md
mobs/05-maestros/lead-orchestrator.md
mobs/06-revolutionaries/lead-orchestrator.md
mobs/07-luminaries/lead-orchestrator.md
mobs/08-vanguards/lead-orchestrator.md
mobs/09-provocateurs/lead-orchestrator.md
mobs/10-dreamweavers/lead-orchestrator.md
mobs/11-guardians/lead-orchestrator.md
mobs/12-strategists/lead-orchestrator.md
```

### Priority 5 — First Three Executable Playbooks
Create three playbooks in HAMAL:

```text
02_playbooks/client-flow-engine.md
02_playbooks/content-distribution-os.md
02_playbooks/opportunity-mining-engine.md
```

### Priority 6 — Command Center State Model
Define state transitions:

```text
New → Triaged → Assigned → In Progress → Human Review → Approved → Executed → Measured → Learned
```

Suggested file:
`COMMAND_CENTER_STATE_MODEL.md`

## Build Rules For Other Chats

Any chat supporting this project should follow these rules:

1. Do not create random agents without mapping them to a Mob.
2. Do not create workflows without defining inputs, outputs, owner, KPIs, and memory writes.
3. Do not add tools unless they serve a playbook.
4. Do not overbuild before defining the event and memory schema.
5. Keep everything repo-native, modular, and easy for another agent to read.
6. Favor markdown and JSON schemas for portable context.
7. Every output should answer: where does this live, who uses it, and what does it trigger?
8. When a project corpus matters, use Graphify as a default context source before rereading everything manually.

## Recommended Prompt For New Chats

Use this prompt when opening a new support chat:

```text
You are supporting Major Dream Williams in building AMA OS / HAMAL / Art Mob MOBS.

The project is an AI-native operating system built around 12 MOBS and eventually 144 specialized agents.

Use this handoff document as the source of truth.

Your job is to help create repo-native scaffolding, playbooks, schemas, agents, workflows, and command-center architecture.

Do not build random bots. Map everything to a Mob, workflow, memory layer, event, KPI, and repo path.

Graphify is a constant core plugin for project context and graph memory. When working inside a meaningful repo or source corpus, prefer Graphify outputs and graph queries before rebuilding context manually from raw files.

Primary repos:
- HAMAL_MOB_PLAYBOOKS: doctrine, SOPs, playbooks, Mob operating models
- agency-agents: executable agent templates and agent files
- Major-OS-AMA-OS--Command: command center, orchestration, schemas, UI/runtime logic

Start by identifying which repo and folder your output belongs in.
```

## Current North Star

The future winner is not the person with the smartest single AI.

The future winner is the one with the best orchestration system.

AMA OS is being designed as that orchestration system.
