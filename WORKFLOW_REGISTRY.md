# Workflow Registry

## Purpose

This registry defines the current Mission Control workflow map for local/mock operation, governance, and future OpenClaw routing.

Mission Control owns workflow visibility, approval state, and handoff discipline. External subsystems may produce artifacts, but Mission Control decides what gets reviewed, approved, routed, or blocked.

## Registry Fields

```text
workflow_id:
workflow_name:
mob_owner:
trigger:
playbook_source:
tools_required:
output_artifacts:
memory_target:
approval_required:
kpi:
economic_purpose:
```

## Workflows

| workflow_id | workflow_name | mob_owner | trigger | playbook_source | tools_required | output_artifacts | memory_target | approval_required | kpi | economic_purpose |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| lead_generation | Lead Generation | Revenue Mob | Commands containing `lead`, `find`, `scout`, `contour leads`, or `SAF leads` | `docs/ORCHESTRATOR_LAYER.md`, `docs/OPENCLAW_AGENT_CONTRACT.md` | Local orchestrator, A001 Scout, A002 Audit, A006 Outreach, mission board | lead_list, outreach_draft | Obsidian / Graphify lead memory | Yes, before outreach execution | Qualified leads and review-ready outreach drafts | Produces revenue pipeline |
| audit | Audit | Revenue Mob | Commands containing `audit`, `diagnose`, or `review business` | `docs/ORCHESTRATOR_LAYER.md`, `docs/ARTIFACT_SYSTEM.md` | Local orchestrator, A002 Audit, A004 Ops Watcher, artifacts panel | audit_report, workflow_plan | Obsidian / Graphify analysis memory | Yes, before client-facing recommendations | Audits completed and review-ready | Converts business context into offers, fixes, and next actions |
| content_media | Content / Media | Media Mob | Commands containing `content`, `substack`, `article`, `video`, `remotion`, or `heygen` | `docs/SUBSTACK_MEDIA_WORKFLOW.md`, `docs/ORCHESTRATOR_LAYER.md` | Local orchestrator, A003 Content Catcher, A007 Offer Builder, Substack / Media Engine | substack_draft, video_script, memory_note | Obsidian / Graphify content memory | Yes, before publishing or distribution | Review-ready content assets | Builds authority and monetizable attention |
| outreach | Outreach | Revenue Mob | Commands containing `email`, `outreach`, `follow up`, or `dm` | `docs/ORCHESTRATOR_LAYER.md`, `docs/OPENCLAW_AGENT_CONTRACT.md` | Local orchestrator, A006 Outreach, A002 Audit, artifacts panel | outreach_draft | Obsidian / Graphify relationship memory | Yes, before sending | Approved outreach drafts | Converts leads into conversations |
| commerce | Commerce | Commerce Mob | Commands containing `shopify`, `gumroad`, `product`, or `store` | `docs/ORCHESTRATOR_LAYER.md`, `docs/DISTRIBUTION_QUEUE.md` | Local orchestrator, A009 Storefront Operator, A007 Offer Builder, artifacts panel | product_page, workflow_plan | Obsidian / Graphify commerce memory | Yes, before live listing or publishing | Product actions prepared | Turns offers into sellable surfaces |
| operations | Operations | Command Mob | Status, repo, dashboard, blocker, registry, or fallback commands | `SYSTEM_CORE.md`, `HANDOFF_COMMAND_CENTER.md`, `docs/ORCHESTRATOR_LAYER.md` | A004 Ops Watcher, GitHub docs, app registry, activity feed | workflow_plan, daily_brief, handoff note | GitHub docs, Obsidian / Graphify system memory | Conditional, required for changes that affect authority boundaries | Blockers surfaced and system state clarified | Keeps execution coherent and reduces repeated context loss |
| client_clarity_intake | Client Clarity Intake | Revenue Mob | External artifact stream from `CLIENT_CLARITY_INTAKE_OS` or commands around client blueprint review | `docs/CLIENT_CLARITY_SUBSYSTEM.md`, `docs/EXTERNAL_SYSTEMS.md` | External subsystem export contract, A001 Scout, A002 Audit, A006 Outreach, A010 Meeting Synthesizer | client_blueprint, audit_report, outreach_draft | Obsidian / Graphify client memory | Yes, approval mode `REVIEW` | Client blueprints reviewed and routed | Turns intake into diagnosis, offer fit, and revenue action |
| substack_reaction_doctrine | Substack Reaction Doctrine | Media Mob | External Substack artifact import or commands around reaction doctrine content | `docs/SUBSTACK_MEDIA_WORKFLOW.md`, `docs/EXTERNAL_SYSTEMS.md`, `docs/RISK_GOVERNANCE.md` | SUBSTACK-AUTOMATION-ENGINE export, A003 Content Catcher, artifacts panel, risk governance | substack_draft, video_script, memory_note | Obsidian / Graphify doctrine memory | Yes, especially for risk or missing system-underneath checks | Approved or rewritten doctrine artifacts | Converts cultural moments into authority assets without chasing noise |
| design_system_build | Design System Build | Product Mob | Commands containing `design system`, UI governance, visual rules, or component standardization | `docs/ORCHESTRATOR_LAYER.md`, `docs/COMMAND_GUIDANCE_LAYER.md` | A004 Ops Watcher, A007 Offer Builder, A008 Deck Builder, GitHub docs | workflow_plan, action_plan, memory_note | GitHub docs, Obsidian / Graphify design memory | Yes, before broad UI changes | Approved design rules and implementation plan | Makes the OS more reusable, sellable, and easier to extend |
| daily_brief | Daily Brief | Command Mob | Commands containing `daily brief`, `report`, `status`, or daily operating loop review | `docs/DAILY_BRIEF_PROTOCOL.md`, `docs/AGENT_LOGGING_STANDARD.md` | A004 Ops Watcher, A010 Meeting Synthesizer, activity feed, GitHub docs | daily_brief, memory_note | GitHub docs, Obsidian / Graphify daily memory | No for local summary; yes for external publishing | Revenue action, content action, and system improvement logged | Forces daily execution across money, authority, and system compounding |

## Workflow Rules

- Every workflow must map to an economic purpose.
- Every workflow must leave a durable handoff in GitHub or an approved memory target.
- Review workflows can prepare artifacts locally, but Mission Control owns approval.
- External subsystems produce artifacts; they do not replace Mission Control authority.
- Live writes, publishing, rendering, or external sync require explicit future approval.
