# AMA / Major OS Command Center Handoff

## Purpose

This handoff gives the Command Center builder full context on where the system stands, why recent architecture decisions were made, and how GitHub, Notion, Airtable, Codex, OpenClaw, Hanzo, Lux, media tools, commerce tools, and automation should connect.

The mission is not to rebuild from zero. The mission is to integrate what already exists, make it easier to operate, and turn the internal system into a productized AI operating system that can be used by Major and sold to clients.

## Latest Update - 2026-05-02

Mission Control now has a local-only intake for SUBSTACK-AUTOMATION-ENGINE `asset_generation_summary.json`.

Mission Control also surfaces `content/logs/workflows/substack_asset_summary_handoff.json` as a read-only Asset Decision Queue panel.

What changed:

- `npm run assets:intake` imports asset generation summaries from a file or stdin.
- The browser Artifacts panel can refresh asset summaries with `Refresh Assets`.
- The Asset Decision Queue panel shows prepared, ready-for-distribution, and blocked/skipped asset handoff rows.
- Mission Control ranks asset packages into `hold`, `review assets`, `request rewrite`, `approve for rendering queue later`, or `approve for publishing queue later`.
- Matching artifacts are annotated with `asset_state`, route decision, generated files, and routing notes.
- Asset-only summary rows are visible even if the main artifact export has not been refreshed yet.

Boundary:

- Command Center does not generate assets.
- Command Center does not render video/audio.
- Command Center does not publish live.
- Command Center only imports, surfaces, ranks, and routes the external producer summary.
- The Asset Decision Queue is read-only. It has no approve, render, publish, or generation controls.

## Core Intention

Major is building an AI-powered operating system that can:

- Track and build apps / mini-apps
- Run agents and workflows
- Generate leads
- Create content
- Build media assets
- Manage commerce flows
- Update Airtable and Notion
- Keep GitHub as the source of truth
- Package the system into a sellable AI Business OS

The long-term product idea is simple:

> We install an AI team that helps a business find leads, create content, build products, automate workflows, and turn scattered operations into a usable command center.

## Why This Decision Happened

Major had been using Claude Code and Claude CoWork in earlier workflows. The Claude subscription lapsed, so the system needed to move toward an OpenAI-centered stack without losing the value already built.

The decision:

- Keep existing agents and system work.
- Do not rebuild unnecessarily.
- Use ChatGPT as the strategy/planning layer.
- Use Codex as the build/repo execution layer.
- Keep OpenClaw as the agent runtime.
- Keep Hanzo as the agent intelligence/ecosystem layer.
- Keep Airtable as the operational database.
- Keep Notion as the human dashboard.
- Keep GitHub as the truth vault.

Operating sentence:

> ChatGPT plans it. Codex builds it. OpenClaw runs the agents. Hanzo gives the ecosystem intelligence. GitHub stores the truth. Airtable tracks the business. Notion gives the dashboard. Obsidian and Graphify store deep memory.

## Current Repo Roles

There are now three important GitHub repos in this architecture.

### 1. Major-OS-AMA-OS--Command

Repo: `MajorDream444/Major-OS-AMA-OS--Command`

This is the Command Center repo. It should become the main builder workspace for the dashboard, command console, sync logic, operating views, and the bridge between systems.

Use this repo for:

- Command center UI
- Dashboard build
- App registry views
- Sync interfaces
- Airtable/Notion/GitHub coordination
- Operator console
- Admin workflows
- Navigation layer across AMA / Major OS

### 2. Major-AI-OS

Repo: `MajorDream444/Major-AI-OS`

This is the reusable AI OS/product repo.

Use this repo for:

- System core files
- Reusable skills
- Agent instructions
- Workflow templates
- Productized documentation
- Sellable AI OS packaging

Already seeded there:

- `README.md`
- `SYSTEM_CORE.md`

Recommended next files:

- `CODEX.md`
- `AGENTS.md`
- `SYSTEM_MAP.md`
- `WORKFLOWS.md`
- `/skills`
- `/docs/SYNC_MAP.md`

### 3. 52in52

Repo: `MajorDream444/52in52`

This is the app factory and build tracker.

Use this repo for:

- App experiments
- Mini-app scaffolds
- 52-in-52 build records
- Specific app implementations

Important note: this repo is private and its default branch is currently `claude/notebooklm-skill-setup-waVBR`, which caused confusion because files were not visible where expected. Early OS files and skills were first placed there before the cleaner separation was made.

Current architecture:

- Command Center repo = dashboard/control layer
- Major-AI-OS repo = reusable OS/product layer
- 52in52 repo = app factory/build layer

## System Stack

### ChatGPT
Strategy, thinking, writing, research, architecture, product framing, prompts.

### Codex
Builder, executor, repo worker, PR machine, local/cloud implementation agent.

### OpenClaw
Agent runtime and orchestration layer. Should remain in the stack. Do not replace it with Codex; Codex should help build and maintain it.

### Hanzo
Agent intelligence and ecosystem identity layer.

### Lux
Rails, trust, settlement, blockchain/tokenization layer.

### GitHub
Source of truth for code, docs, skills, tasks, workflows, handoffs, and versioned system knowledge.

### Airtable
Operational data layer: apps, engines, workflows, tools, agents, marketing, audience, forms, and pipeline records.

### Notion
Human dashboard: command pages, app registry, readable planning, high-level operational views.

### Obsidian + Graphify
Deep memory and context graph. Intended to reduce repeated context and make agents more aware of prior decisions.

### n8n
Automation layer: triggers, scheduled jobs, webhooks, Telegram alerts, Airtable sync, Notion updates, content flows.

### NotebookLM
Research vault and source synthesis layer.

### Media / Commerce Stack
- HeyGen = avatar/video generation
- Remotion = programmatic video rendering
- Generative Media Skills = image/video/lip sync/media generation
- Gumroad = digital product sales
- Shopify CLI = ecommerce store operations
- Marketing skills = content/funnel/distribution layer

## Current Airtable Source

Base ID: `appSMmnuKy6GYfBPu`

The user provided:

- Apps table: `tblGGRGbc0rJYc2OX`
- View: `viwFjJP1Usx3YGeLN`

The base is already robust. Do not recreate it.

### Key Airtable Tables

#### 52 in 52 - Apps
Table ID: `tblGGRGbc0rJYc2OX`

Purpose: Master operating table for the 52-in-52 initiative.

Important fields:

- Name
- App ID
- Week #
- Development Status
- Notes
- Pillar
- Archetype
- Core Engine Type
- Audience
- Hook
- CTA / Next Step
- Route Type
- Data Captured
- Result Delivered
- Offer Path
- Select

#### 52 in 52 - Engines
Reusable engine patterns that power apps.

Important fields:

- Engine Name
- Engine Category
- Description
- Input Type
- Output Type
- Reusable Logic
- Prompt Template
- Primary Model
- Notes

#### 52 in 52 - Workflows
Automation workflows and system processes.

Important fields:

- Workflow Name
- Related App
- Trigger
- Tool Used
- Steps
- Output
- Status
- Notes

#### 52 in 52 - Tools
Tools, MCPs, models, and services.

Important fields:

- Tool Name
- Category
- Use Case
- Connected Apps
- API / Access
- Notes

#### 52 in 52 - Agents
AI agents and MOB workflows.

Important fields:

- Agent Name
- Mob Group
- Role
- Assigned Apps
- Tasks
- Schedule
- Tools Used
- Output Type
- Notes

#### 52 in 52 - Marketing
Campaigns, assets, funnels.

Important fields:

- Campaign Name
- Related App
- Channel
- Asset Type
- Link
- Funnel Type
- Status
- Notes

#### 52 in 52 - Audience
Leads, users, and audience segments.

Important fields:

- Email
- Name
- Segment
- Source App
- Score
- Interest
- Last Action
- Opt-in Status
- Notes
- Archetype
- Latest Score
- Role
- Location
- Main Goal
- Bottleneck
- Strength
- Lifecycle Stage
- WhatsApp

#### Substack Pipeline
Editorial workflow for Substack posts and content repurposing.

This matters because Major wants a Substack skill where voice/article input can become:

- Substack post
- Video script
- Podcast outline
- Tweets
- Social assets
- Marketing campaign

#### Systems Audit Intake
Lead intake table from the Systems World CTA.

Can feed the AI OS product/client funnel.

#### Fix Up Score Tables
Diagnostic responses and outreach pipeline. These can feed lead scoring, archetypes, follow-up, and content campaigns.

## Current Notion State

A matching Notion page was found and updated.

### 52in52 Notion Page

Title: `52in52`

Purpose: Human command center for the `52in52` app factory and its connection to GitHub/Airtable.

It now includes:

- Purpose
- Canonical references
- Current stack
- Active skill packs
- Seed app/system list
- Sync rules
- Immediate next actions

### Notion App Registry

A database was created under the 52in52 page:

Title: `52in52 App Registry`

Purpose: Visual dashboard/index for apps, mini-apps, skills, workflows, and systems.

Fields:

- App Name
- Status
- Priority
- Category
- GitHub Repo
- Airtable Base ID
- Airtable Table ID
- Airtable View ID
- Airtable Record
- Owner Agent
- Revenue Path
- Next Action
- Source
- Notes

Important: Notion registry is a dashboard, not the operational source. Airtable remains the operational source.

## Skills / Repos to Integrate

### HeyGen Skill
Source repo: `MajorDream444/heygen-com-skills`

Purpose:

- Avatar videos
- UGC-style clips
- Explainer content
- Product launch videos

### Remotion Skill
Source repo: `MajorDream444/remotion`

Purpose:

- Programmatic video rendering
- Captions
- Composition
- Social video formatting
- Batch content generation

### Shopify CLI Skill
Current user version: 3.50.0
Update available: 3.51.0
Update command:

```bash
npm install -g @shopify/cli@latest
```

Purpose:

- Manage Shopify products
- Theme work
- Store operations
- Drop launches
- CLI-driven automation

### Gumroad Skill
Source reference: MCPMarket Gumroad Automation

Purpose:

- Digital product listings
- Pricing
- Funnels
- Launch copy
- Sales tracking

### Marketing Skills
Source repos:

- `MajorDream444/mpos-marketing`
- `MajorDream444/marketingskills`

Purpose:

- Content strategy
- Funnel copy
- Campaign planning
- Viral scripts
- Audience targeting

### Generative Media Skills
Source repo: `Dream-AI-4444/Generative-Media-Skills`

Purpose:

- Image generation
- Video generation
- Lip sync
- Audio
- Upscaling
- Face swap
- Cinematic scenes
- Agent-native media workflows through `muapi-cli`

### Open Generative AI
Source repo: `Anil-matcha/Open-Generative-AI`

Purpose:

- Full generative AI studio similar to Higgsfield/Krea style workflows
- Image Studio
- Video Studio
- Lip Sync Studio
- Cinema Studio
- Workflow Studio
- 200+ model access

This should be treated as a future media arsenal layer, not the immediate first money workflow unless required.

## Seed App/System List

The system currently recognizes at least these 25 seeds:

1. Major AI OS / 52in52 Command Center
2. Hip-Hop Trivia App
3. Gumroad Product Engine
4. Shopify Store Automation Skill
5. HeyGen Avatar Content Engine
6. Remotion Video Engine
7. Generative Media Studio / Higgsfield-style stack
8. UGC Ad Generator
9. Substack Article-to-Media Machine
10. Marketing Engine
11. Lead Scout / Customer Finder
12. Airtable Sync Engine
13. Obsidian + Graphify Memory Layer
14. OpenClaw Agent Runtime Pack
15. Hanzo Agent Ecosystem Pack
16. AI Growth OS Productized Offer
17. T-Shirt / Invisible Mannequin Product Visual Engine
18. Podcast Repurposing Engine
19. Tweet / Social Posting Agent
20. App Builder Workflow
21. Customer Dashboard / Operator Console
22. NotebookLM Research Vault Skill
23. 52 Apps in 52 Weeks Tracker
24. Media Asset Library
25. Client Install Template

These should be reconciled with Airtable, Notion, and GitHub.

## First Money Workflow Recommendation

Recommended first focused workflow:

> Content → Product → Sale

Suggested flow:

1. ChatGPT creates product strategy and positioning.
2. Gumroad skill creates the digital product page, sales copy, pricing, and offer structure.
3. HeyGen creates avatar/promo video.
4. Remotion formats final clips for IG/TikTok/YouTube.
5. Marketing engine turns the offer into posts, tweets, emails, IG copy, and campaign assets.
6. Shopify CLI supports ecommerce/product drops where relevant.
7. Airtable tracks app/product/campaign state.
8. Notion shows the command dashboard.
9. GitHub stores handoffs, skills, prompts, workflows, and implementation files.

Do not build everything at once. Start with one money workflow and make it repeatable.

## Builder Priorities

### Priority 1: Initialize Command Center Repo

In `Major-OS-AMA-OS--Command`, create:

```text
README.md
SYSTEM_MAP.md
SYNC_MAP.md
DASHBOARD_PLAN.md
COMMAND_CENTER_SPEC.md
.env.example
/docs/HANDOFF_COMMAND_CENTER.md
```

### Priority 2: Connect to Major-AI-OS

`Major-AI-OS` should own reusable skills and OS logic.

Command Center should reference it, not duplicate everything.

### Priority 3: Connect to Airtable

Use Airtable base and tables above. Do not create duplicate tables unless needed.

### Priority 4: Connect to Notion

Use the existing 52in52 page and App Registry database.

### Priority 5: Build Dashboard

Dashboard should show:

- Apps
- Status
- Priority
- Next Action
- GitHub Repo
- Airtable record
- Notion record
- Assigned Agent
- Revenue Path
- Current workflow

### Priority 6: Build Sync Logic

At minimum, create a sync plan:

- Airtable Apps → Notion App Registry
- GitHub repo/folder → Airtable app record
- Codex handoff → GitHub docs and Notion notes

### Priority 7: Productize

The same system should become sellable as Major AI OS / AI Growth OS.

## Non-Negotiable Rules

1. Do not rebuild what already exists.
2. Do not scatter app ideas across chats only.
3. Every meaningful app idea must land in Airtable, Notion, or GitHub.
4. GitHub is the source of truth for code/docs.
5. Airtable is the source of truth for operational app records.
6. Notion is the human dashboard.
7. Every task must leave a handoff.
8. Every skill must map to a workflow.
9. Every workflow must connect to revenue, audience growth, automation, or internal leverage.
10. Never commit API keys or secrets.

## Next Builder Action

Start in `MajorDream444/Major-OS-AMA-OS--Command`.

Build the command center scaffold, then connect it to:

- `MajorDream444/Major-AI-OS`
- `MajorDream444/52in52`
- Airtable 52-in-52 base
- Notion 52in52 page and App Registry

The system is now properly split into:

```text
Command Center = Major-OS-AMA-OS--Command
Reusable AI OS = Major-AI-OS
App Factory = 52in52
Operations DB = Airtable
Human Dashboard = Notion
```
