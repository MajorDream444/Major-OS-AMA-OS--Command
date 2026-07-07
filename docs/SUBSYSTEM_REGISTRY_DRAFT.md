# Subsystem Registry Draft

last updated: May 2026

## Shared Brain Registration Rule

Every repo, subsystem, workflow, agent, artifact, and memory object must register back into the shared brain.

## Routing Notes

- Canonical anchor: `/Users/majordreamwilliams/Documents/HAMAL_MOB_OS_CANON/HAMAL_MOB_OS_CURRENT_STATE.md`
- Local command sources: `../REPO_MAP.md`, `../SYSTEM_CORE.md`, `docs/GRAPHIFY_CONTEXT_LAYER.md`
- Requested but not found locally: `The_Sovereign_AI_Organism.pdf`
- Scope: documentation-only registry draft
- Do not use this file to create live integrations, modify databases, or trigger automation.

---

# 1. Purpose

This file defines the draft registration pattern for HAMAL / AMA Mob OS subsystems.

A subsystem is any durable operating unit that owns a distinct responsibility inside the ecosystem.

Examples:
- Command Center
- Doctrine Brain
- Execution Harness
- Shared Brain
- BWYH Launch System
- Business Pressure Test V2
- client workspaces
- repo families
- tool layers

---

# 2. Subsystem Registration Pattern

Each subsystem should register using this schema.

```yaml
subsystem_id:
subsystem_name:
plain_language_role:
system_layer:
owner:
owning_mob:
supporting_mobs:
canonical_source:
repo_owner:
repo_path:
workspace_path:
primary_docs:
related_playbooks:
related_workflows:
related_agents:
artifact_outputs:
memory_targets:
graphify_status:
obsidian_status:
notebooklm_status:
approval_required_for:
economic_purpose:
current_status:
known_risks:
next_action:
last_updated:
```

---

# 3. Registry Fields

Identity fields:
- `subsystem_id`: stable machine-readable id
- `subsystem_name`: human-readable name
- `plain_language_role`: one-sentence explanation
- `system_layer`: doctrine, execution, memory, workspace, product, client, revenue, media, or launch

Ownership fields:
- `owner`: person or authority accountable for the subsystem
- `owning_mob`: primary MOB
- `supporting_mobs`: additional MOBS involved
- `repo_owner`: GitHub or local repo owner
- `repo_path`: repository path if applicable
- `workspace_path`: local workspace path if applicable

Source fields:
- `canonical_source`: primary source of truth
- `primary_docs`: docs that explain the subsystem
- `related_playbooks`: reusable procedures
- `related_workflows`: operating workflows
- `related_agents`: agent families or named agents

Output fields:
- `artifact_outputs`: what the subsystem creates
- `memory_targets`: where durable memory should land
- `approval_required_for`: what needs human review
- `economic_purpose`: why the subsystem exists in business terms

State fields:
- `graphify_status`: not initialized, initialized, stale, current, unknown
- `obsidian_status`: not mapped, mapped, needs sync, unknown
- `notebooklm_status`: not sourced, source set created, needs refresh, unknown
- `current_status`: active, paused, draft, archived, blocked
- `known_risks`: major risks or gaps
- `next_action`: next useful move
- `last_updated`: date or month

---

# 4. Initial Subsystem Map

## 4.1 HAMAL Mob OS Canon

```yaml
subsystem_id: hamal_mob_os_canon
subsystem_name: HAMAL Mob OS Canon
plain_language_role: Master orientation layer for doctrine, execution, memory, and launch priorities.
system_layer: doctrine
owner: Major
owning_mob: Visionaries
supporting_mobs:
  - Maestros
  - Strategists
  - Luminaries
canonical_source: HAMAL_MOB_OS_CURRENT_STATE.md
repo_path: /Users/majordreamwilliams/Documents/HAMAL_MOB_OS_CANON
artifact_outputs:
  - canonical maps
  - architecture docs
  - routing standards
memory_targets:
  - Graphify
  - Obsidian
  - NotebookLM
economic_purpose: Prevent system drift and turn scattered context into reusable operating IP.
current_status: active
next_action: Register docs into shared brain and update Graphify when approved.
last_updated: May 2026
```

## 4.2 Command Center

```yaml
subsystem_id: command_center
subsystem_name: Command Center
plain_language_role: Operator-facing coordination layer for apps, agents, workflows, dashboards, handoffs, and sync surfaces.
system_layer: execution_visibility
owner: Major
owning_mob: Maestros
supporting_mobs:
  - Vanguards
  - Artisans
canonical_source: SYSTEM_CORE.md
repo_owner: MajorDream444/Major-OS-AMA-OS--Command
economic_purpose: Show what is moving, blocked, awaiting review, or ready for action.
current_status: active
next_action: Keep documentation architecture separate from UI builds until approved.
last_updated: May 2026
```

## 4.3 HAMAL Mob Playbooks

```yaml
subsystem_id: hamal_mob_playbooks
subsystem_name: HAMAL Mob Playbooks
plain_language_role: Doctrine brain for SOPs, rubrics, templates, and repeatable execution.
system_layer: doctrine
owner: Major
owning_mob: Luminaries
supporting_mobs:
  - Strategists
  - Maestros
canonical_source: HAMAL_MOB_PLAYBOOKS_CANONICAL_MAP.md
repo_owner: MajorDream444/HAMAL_MOB_PLAYBOOKS
economic_purpose: Convert repeated work into scalable playbooks and client delivery IP.
current_status: active
last_updated: May 2026
```

## 4.4 MobStack Execution Harness

```yaml
subsystem_id: mobstack_execution_harness
subsystem_name: MobStack Execution Harness
plain_language_role: Runtime coordination layer for repo ingestion, delegation, approvals, tools, and memory sync.
system_layer: execution
owner: Major
owning_mob: Maestros
supporting_mobs:
  - Vanguards
  - Artisans
canonical_source: MOBSTACK_EXECUTION_HARNESS_CANONICAL_MAP.md
economic_purpose: Turn doctrine into reliable coordinated execution.
current_status: draft
last_updated: May 2026
```

## 4.5 Shared Brain

```yaml
subsystem_id: shared_brain
subsystem_name: Graphify + Obsidian Shared Brain
plain_language_role: Durable context and memory layer across repos, docs, agents, workflows, and artifacts.
system_layer: memory
owner: Major
owning_mob: Artisans
supporting_mobs:
  - Visionaries
  - Maestros
canonical_source: GRAPHIFY_SHARED_BRAIN_PROTOCOL.md
economic_purpose: Reduce repeated explanation and preserve strategic memory across the enterprise.
current_status: draft
last_updated: May 2026
```

---

# 5. Anti-Silo Rule

Every subsystem must point to:
- source of truth
- owner
- MOB
- workflow
- artifacts
- memory target
- economic purpose

If it cannot point to these, it is not ready to become a subsystem.

---

# 6. What Should Not Be Registered Yet

Do not register:
- loose ideas without ownership
- unreviewed client-sensitive details
- secret values
- private credentials
- live integration configs
- one-off experiments without economic purpose
- duplicate names for the same operating role

