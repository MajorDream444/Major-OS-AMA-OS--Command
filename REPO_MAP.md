# HAMAL / Major OS Repo Map

## Purpose

This file tells every agent, Codex session, Claude/OpenClaw worker, and future chat which repository owns which layer of the system.

No agent should run without knowing where context, playbooks, and executable tools live.

## Operating Spine

```text
Context → Playbooks → Execution
```

## 1. Command Repo

Repository:

```text
MajorDream444/Major-OS-AMA-OS--Command
```

Role:

```text
Command center / multi-chat context / orchestration doctrine
```

Use this repo for:

- master handoff documents
- command center doctrine
- multi-chat context
- agent civilization architecture
- 12 MOBS structure
- event-driven architecture
- shared memory rules
- repo governance
- bootstrap prompts

Key file:

```text
HANDOFF_MULTI_CHAT_CONTEXT.md
```

Rule:

```text
If an agent needs to understand the whole ecosystem, start here.
```

## 2. Playbook Repo

Repository:

```text
MajorDream444/HAMAL_MOB_PLAYBOOKS
```

Role:

```text
Playbooks / SOPs / skill audits / client systems
```

Use this repo for:

- playbooks
- SOPs
- offer systems
- client onboarding systems
- skill audits
- MCP/tool usage doctrine
- agent operating procedures
- delivery rubrics
- system templates

Important paths:

```text
00_stage_a_foundation/
02_playbooks/
05_templates/
06_audits/
07_rubrics/
```

Current playbooks include:

- Model Brand Pressure Test
- Model Monetization System
- Model / Influencer Outreach Scripts
- Model / Influencer Directory + Platform System
- Client Flow Payment + Signature Engine
- Major AI Mindset Playbook Doctrine
- Generative Media Skill Inventory

Rule:

```text
If an agent needs to know how to execute a repeatable business process, use this repo.
```

## 3. Codex / MCP Execution Repo

Repository:

```text
MajorDream444/hanzo-lux-codex-repo
```

Role:

```text
Executable MCP / Codex / tool layer
```

Use this repo for:

- MCP servers
- integration scripts
- Airtable tools
- Notion tools
- Firecrawl tools
- Telegram tools
- Hanzo tools
- Lux tools
- local execution harnesses
- agent runtime experiments

Known current MCP tool coverage:

```text
Airtable:
- airtable_healthcheck
- airtable_list_tables

Notion:
- notion_healthcheck
- notion_search

Firecrawl:
- firecrawl_healthcheck
- firecrawl_scrape

Telegram:
- telegram_healthcheck
- telegram_send_message

Hanzo:
- hanzo_healthcheck

Lux:
- lux_healthcheck
```

Missing / next needed:

- Airtable create/update records
- Notion create/update pages
- orchestration chain tool
- lead pipeline automation
- payment/signature workflow connectors

Rule:

```text
If an agent needs to touch the outside world or run tools, use this repo.
```

## Agent Startup Rule

Every agent session should identify:

```yaml
source_of_truth_context: Major-OS-AMA-OS--Command
source_of_truth_playbooks: HAMAL_MOB_PLAYBOOKS
source_of_truth_execution: hanzo-lux-codex-repo
assigned_mob: TBD
assigned_workflow: TBD
memory_target: TBD
artifact_target: TBD
kpi: TBD
```

## Repo Relationship

```text
Major-OS-AMA-OS--Command
  ↓ defines mission/context
HAMAL_MOB_PLAYBOOKS
  ↓ defines repeatable execution
hanzo-lux-codex-repo
  ↓ runs tools and automations
Airtable / Notion / Telegram / Firecrawl / Hanzo / Lux
  ↓ receive operational data and outputs
```

## Operating Rule

Do not let agents freestyle in isolation.

Every agent must map to:

- a Mob
- a workflow
- a playbook
- a memory surface
- an artifact output
- a KPI
- an economic purpose

## Bootstrap Prompt For Future Agents

```text
You are operating inside the HAMAL / Major OS ecosystem.

Before acting, read the repo map and identify the correct source of truth:

- Command/context lives in MajorDream444/Major-OS-AMA-OS--Command
- Playbooks/SOPs/skill audits live in MajorDream444/HAMAL_MOB_PLAYBOOKS
- Executable MCP/Codex/tool code lives in MajorDream444/hanzo-lux-codex-repo

Do not operate as an isolated chatbot.
Map every action to a Mob, workflow, playbook, memory target, artifact output, KPI, and economic purpose.

Your job is to reduce manual work for Major and turn ideas into executable systems.
```
