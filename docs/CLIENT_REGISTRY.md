# Client Registry

last updated: May 2026

## Shared Brain Registration Rule

Every repo, subsystem, workflow, agent, artifact, and memory object must register back into the shared brain.

## Routing Notes

- Canonical anchor: `HAMAL_CURRENT_STATE_SYNTHESIS.md`
- Shared brain protocol: `GRAPHIFY_SHARED_BRAIN_PROTOCOL.md`
- Related registry docs: `SUBSYSTEM_REGISTRY_DRAFT.md`, `AGENT_WORKFLOW_REGISTRY_DRAFT.md`, `ARTIFACT_REGISTRY.md`, `CLOSE_PROTOCOL_REGISTRY.md`
- Scope: documentation-only registry specification
- Do not add private client details, live CRM records, payment data, or confidential strategy notes until explicitly approved.

---

# 1. Purpose

The Client Registry defines how client worlds register into HAMAL / AMA Mob OS.

It exists to prevent client work from becoming isolated delivery fragments. Every client should connect to a subsystem, phase, archetype, economic value, playbook set, artifact set, and handoff state.

---

# 2. Registry Schema

```yaml
client_id:
client_name:
subsystem:
current_phase:
archetype:
economic_value:
build_status:
playbook_links:
artifact_links:
handoff_status:
owner:
owning_mob:
supporting_mobs:
workspace_path:
repo_location:
memory_target:
graph_links:
approval_requirements:
next_action:
last_updated:
```

---

# 3. Required Fields

## 3.1 client_id

Stable machine-readable client identifier.

Example format:

```text
client_sheetal_shakti
client_graffiti_media
client_theo_healing_os
```

## 3.2 client_name

Human-readable client or client-world name.

Do not include private personal details unless approved.

## 3.3 subsystem

The operating subsystem the client belongs to.

Examples:
- Shakti Universe
- Graffiti Media OS
- Healing OS
- Business Pressure Test
- BWYH
- Command Center

## 3.4 current_phase

The current delivery or relationship phase.

Suggested values:
- discovery
- audit
- strategy
- proposal
- build
- review
- handoff
- support
- paused
- archived

## 3.5 archetype

The client pattern or delivery archetype.

Examples:
- wisdom brand
- media engine
- healing-centered operator
- creator-founder
- retreat partner
- diagnostic lead
- systems audit client

## 3.6 economic_value

The economic role of the client relationship.

Examples:
- active revenue
- pilot proof
- case study
- reusable template source
- strategic partnership
- future pipeline
- learning asset

## 3.7 build_status

The current build state.

Suggested values:
- not_started
- intake_complete
- mapped
- in_build
- awaiting_review
- awaiting_client
- delivered
- iterating
- blocked
- paused

## 3.8 playbook_links

Links to playbooks, SOPs, or templates used for this client.

Use repo-relative paths when possible.

## 3.9 artifact_links

Links to artifacts created for this client.

Artifacts should also be registered in `ARTIFACT_REGISTRY.md` when they become durable.

## 3.10 handoff_status

The state of the client handoff.

Suggested values:
- no_handoff_needed
- handoff_needed
- handoff_drafted
- awaiting_review
- sent
- accepted
- blocked

---

# 4. Client Lifecycle

```text
Client signal
  -> client registry entry
  -> subsystem assignment
  -> archetype classification
  -> playbook mapping
  -> artifact creation
  -> handoff tracking
  -> memory update
  -> reusable pattern extraction
```

---

# 5. Client Registry Record Template

```yaml
client_id:
client_name:
subsystem:
current_phase:
archetype:
economic_value:
build_status:
playbook_links:
  - 
artifact_links:
  - 
handoff_status:
owner:
owning_mob:
supporting_mobs:
  - 
workspace_path:
repo_location:
memory_target:
graph_links:
  - 
approval_requirements:
  - 
next_action:
last_updated:
```

---

# 6. Anti-Silo Rule

No client should remain only in:
- a chat thread
- a private note
- a disconnected folder
- a one-off deliverable
- a payment conversation
- an unregistered repo

If client work creates a reusable pattern, route that pattern into the playbook layer.

---

# 7. What Should Not Be Included Yet

Do not include yet:
- private client contact details
- confidential client strategy
- live payment data
- signed contract terms
- private health or personal history
- unreviewed claims
- external CRM IDs unless approved

