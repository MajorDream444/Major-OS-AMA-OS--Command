# Agent Workflow Registry Draft

last updated: May 2026

## Shared Brain Registration Rule

Every repo, subsystem, workflow, agent, artifact, and memory object must register back into the shared brain.

## Routing Notes

- Canonical anchor: `/Users/majordreamwilliams/Documents/HAMAL_MOB_OS_CANON/HAMAL_MOB_OS_CURRENT_STATE.md`
- Local command sources: `../REPO_MAP.md`, `../SYSTEM_CORE.md`, `docs/GRAPHIFY_CONTEXT_LAYER.md`
- Requested but not found locally: `The_Sovereign_AI_Organism.pdf`
- Scope: documentation-only registry draft
- Do not use this file to spawn live agents, run integrations, modify live systems, or push operational data.

---

# 1. Purpose

This file defines draft registry fields for agents, workflows, artifacts, and memory updates inside HAMAL / AMA Mob OS.

It exists to prevent isolated agent drift and make every agent action trace back to doctrine, execution, memory, and economic purpose.

Formal companion registries extend this draft:
- `CLIENT_REGISTRY.md` for client worlds, phases, archetypes, economic value, build status, playbooks, artifacts, and handoffs
- `ARTIFACT_REGISTRY.md` for durable outputs, approval state, repo location, graph links, and reusable value
- `CLOSE_PROTOCOL_REGISTRY.md` for offers, payment structures, support terms, handovers, revisions, risk, and approvals

---

# 2. Agent Registry Fields

```yaml
agent_id:
agent_name:
assigned_mob:
role:
mission:
owner:
primary_workspace:
source_of_truth:
linked_subsystem:
linked_workflows:
linked_playbooks:
tool_access:
memory_scope:
allowed_actions:
restricted_actions:
approval_required_for:
input_format:
output_format:
artifact_outputs:
handoff_rules:
kpis:
economic_purpose:
status:
last_reviewed:
```

Every agent must declare:
- assigned MOB
- workflow
- playbook
- memory surface
- artifact output
- KPI
- economic purpose
- approval boundary

No agent should operate as an isolated chatbot.

---

# 3. Workflow Registry Fields

```yaml
workflow_id:
workflow_name:
purpose:
owner:
owning_mob:
supporting_mobs:
subsystem:
trigger:
inputs:
steps:
tools_required:
approval_gates:
outputs:
artifact_registration_required:
memory_update_required:
handoff_destination:
success_metric:
economic_purpose:
status:
last_updated:
```

Every workflow must answer:
1. What starts it?
2. What source context does it need?
3. Which MOB owns it?
4. Which tools does it use?
5. What does it produce?
6. Where does the artifact go?
7. What memory gets updated?
8. What requires review?
9. What economic purpose does it serve?

---

# 4. Artifact Registration Fields

```yaml
artifact_id:
artifact_name:
artifact_type:
created_by:
source_workflow:
source_agent:
owning_mob:
workspace:
file_path:
canonical_status:
review_status:
intended_audience:
contains_sensitive_info: true/false
public_ready: true/false
memory_target:
related_subsystem:
related_playbook:
economic_purpose:
next_action:
last_updated:
```

Every durable artifact must declare:
- where it lives
- what created it
- who owns it
- whether it is canonical, draft, or deprecated
- whether it contains sensitive information
- whether it is public-ready
- where memory should be updated

---

# 5. Memory Object Registration Fields

```yaml
memory_id:
memory_type:
summary:
source:
source_date:
owner:
owning_mob:
workspace:
related_artifacts:
related_agents:
related_workflows:
canonical_destination:
graphify_destination:
obsidian_destination:
notebooklm_destination:
review_status:
economic_purpose:
expires_or_needs_review:
last_updated:
```

---

# 6. Memory Update Lifecycle

```text
Agent or workflow creates output
  -> classify artifact
  -> check sensitivity
  -> assign owner and MOB
  -> register artifact
  -> update canonical docs if doctrine changed
  -> update workflow or playbook if process changed
  -> update Graphify if relationships changed
  -> update Obsidian if durable meaning changed
  -> add to NotebookLM source set if synthesis is needed
  -> notify Command Center if review or action is needed
```

---

# 7. No Isolated Agent Drift Rule

An agent is drifting if it:
- creates outputs without a destination
- invents a workflow without registering it
- changes doctrine without updating canon
- uses tools without a playbook
- stores important context only in chat
- cannot name its economic purpose
- cannot name what requires review

Drift response:

```text
Pause
  -> classify
  -> register
  -> route
  -> update memory
  -> resume only when ownership is clear
```

---

# 8. Economic Purpose Requirement

Every agent, workflow, artifact, and memory object should support at least one of:
- reduce manual work
- improve client delivery
- create reusable IP
- improve revenue operations
- speed launch
- increase trust
- improve retention
- improve accountability
- protect memory
- turn repeated work into a repeatable offer

If economic purpose is unclear, mark the item as draft and route it for review.

---

# 9. Initial Workflow Categories

Doctrine workflows own canonical maps, playbook extraction, SOP creation, agent schema design, and quality rubrics.

Execution workflows own repo ingestion, task decomposition, delegation, tool registration, and handoffs.

Memory workflows own Graphify updates, Obsidian sync, NotebookLM source sets, decision logs, and artifact registration.

Client workspace workflows own client summaries, pain point maps, proposals, SOWs, onboarding checklists, and delivery artifacts.

Revenue product workflows own BWYH, Business Pressure Test V2, offer ladders, diagnostics, and conversion paths.

---

# 10. What Should Not Be Included Yet

Do not include yet:
- live credentials
- private client details
- unreviewed public copy
- final pricing
- production automation
- live integration actions
- agent swarm execution before registry rules are approved
