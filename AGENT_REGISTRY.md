# Agent Registry

## Purpose

This registry defines the current Mission Control agent roster for local/mock operation and future OpenClaw execution.

Mission Control is the authority layer. Agents may simulate work locally, report state, and leave handoffs. They must not execute external writes or live integrations until an approved workflow explicitly allows it.

## Registry Fields

```text
agent_id:
agent_name:
assigned_mob:
primary_role:
allowed_tools:
workflows_supported:
memory_target:
artifact_target:
kpi:
economic_purpose:
status:
```

## Agents

| agent_id | agent_name | assigned_mob | primary_role | allowed_tools | workflows_supported | memory_target | artifact_target | kpi | economic_purpose | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A001 | Scout | Revenue Mob | Lead discovery and first-pass sourcing | Local command simulation, mission board, activity feed, GitHub docs | lead_generation, client_clarity_intake | Obsidian / Graphify lead memory | lead_list, client_blueprint input notes | Qualified leads found | Creates revenue opportunities by feeding pipeline with real targets | READY |
| A002 | Audit | Revenue Mob | Qualification, diagnosis, and business analysis | Local command simulation, artifacts panel, mission board, GitHub docs | lead_generation, audit, outreach, client_clarity_intake | Obsidian / Graphify analysis memory | audit_report, client_blueprint review notes | Audits completed and reviewed | Improves close quality by turning raw prospects into clear problems and offers | READY |
| A003 | Content Catcher | Media Mob | Capture, shape, and route content/media ideas | Local command simulation, Substack / Media Engine, distribution queue, artifacts panel | content_media, substack_reaction_doctrine, daily_brief | Obsidian / Graphify content memory | substack_draft, video_script, memory_note | Content artifacts ready for review | Builds authority and demand through publishable content assets | READY |
| A004 | Ops Watcher | Command Mob | System monitoring, registry review, blockers, and operating rhythm | Local command simulation, app registry, GitHub logs, activity feed, localStorage | operations, daily_brief, design_system_build | GitHub docs, Obsidian / Graphify system memory | workflow_plan, daily_brief, handoff note | Blockers surfaced and daily loop logged | Keeps the operating system coherent so revenue and content do not drift | READY |
| A005 | Grant Hunter | Revenue Mob | Grant, funding, and institutional opportunity scanning | Local command simulation, mission board, activity feed, GitHub docs | lead_generation, audit, operations | Obsidian / Graphify opportunity memory | lead_list, workflow_plan | Funding opportunities qualified | Opens non-client revenue and partnership paths | IDLE |
| A006 | Outreach | Revenue Mob | Draft outreach, follow-up, and relationship moves | Local command simulation, mission board, artifacts panel, activity feed | lead_generation, outreach, client_clarity_intake | Obsidian / Graphify relationship memory | outreach_draft, client_blueprint follow-up | Outreach drafts approved | Converts qualified attention into conversations and revenue actions | READY |
| A007 | Offer Builder | Product Mob | Package offers, angles, and commercial next steps | Local command simulation, artifacts panel, mission board, GitHub docs | content_media, commerce, audit, design_system_build | GitHub docs, Obsidian / Graphify offer memory | workflow_plan, product_page, action_plan | Offer assets prepared | Turns insight and content into sellable offers | READY |
| A008 | Deck Builder | Product Mob | Convert strategy into decks and presentation assets | Local command simulation, artifacts panel, GitHub docs | audit, commerce, client_clarity_intake, design_system_build | GitHub docs, Obsidian / Graphify presentation memory | workflow_plan, client_blueprint, action_plan | Deck-ready artifacts prepared | Supports sales, onboarding, and authority presentations | IDLE |
| A009 | Storefront Operator | Commerce Mob | Commerce, product listing, storefront, and sales surface planning | Local command simulation, app registry, mission board, artifacts panel | commerce, content_media | GitHub docs, Obsidian / Graphify commerce memory | product_page, workflow_plan | Commerce actions prepared | Turns assets and offers into buyable paths | READY |
| A010 | Meeting Synthesizer | Command Mob | Meeting notes, handoffs, and decision summaries | Local command simulation, activity feed, GitHub docs | operations, daily_brief, client_clarity_intake | GitHub docs, Obsidian / Graphify meeting memory | daily_brief, memory_note, client_blueprint summary | Handoffs logged | Preserves decisions so sessions become reusable operating knowledge | IDLE |

## Operating Rules

- Every agent supports `Plan -> Build -> Run -> Log -> Improve`.
- Every agent leaves a handoff when it changes mission state.
- Agents use GitHub docs as durable truth and Obsidian / Graphify as memory targets.
- Airtable, Notion, Substack, Stripe, n8n, OpenClaw, and external APIs remain future integration targets unless explicitly enabled.
- Mission Control owns final approval.
