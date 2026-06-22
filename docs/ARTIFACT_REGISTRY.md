# Artifact Registry

last updated: May 2026

## Shared Brain Registration Rule

Every repo, subsystem, workflow, agent, artifact, and memory object must register back into the shared brain.

## Routing Notes

- Canonical anchor: `HAMAL_CURRENT_STATE_SYNTHESIS.md`
- Shared brain protocol: `GRAPHIFY_SHARED_BRAIN_PROTOCOL.md`
- Related registry docs: `AGENT_WORKFLOW_REGISTRY_DRAFT.md`, `CLIENT_REGISTRY.md`, `SUBSYSTEM_REGISTRY_DRAFT.md`, `CLOSE_PROTOCOL_REGISTRY.md`
- Scope: documentation-only registry specification
- Do not register sensitive artifacts publicly or mark artifacts public-ready without review.

---

# 1. Purpose

The Artifact Registry defines how outputs become durable system objects.

An artifact can be a document, deck, proposal, checklist, playbook, diagnostic result, code handoff, source packet, content plan, roadmap, SOW, or client deliverable.

This registry exists so artifacts do not disappear into chat history or local folders without ownership, review state, repo location, graph links, and reusable value.

---

# 2. Registry Schema

```yaml
artifact_id:
artifact_type:
client:
workflow_origin:
approval_state:
repo_location:
graph_links:
reusable_value:
artifact_name:
owner:
owning_mob:
source_agent:
source_subsystem:
created_date:
last_updated:
sensitivity_level:
public_ready:
memory_target:
playbook_links:
handoff_destination:
next_action:
```

---

# 3. Required Fields

## 3.1 artifact_id

Stable machine-readable artifact identifier.

Example format:

```text
artifact_bwyh_partner_one_pager
artifact_client_system_blueprint_template
artifact_shakti_workspace_map
```

## 3.2 artifact_type

Suggested values:
- one_pager
- proposal
- sow
- roadmap
- playbook
- checklist
- template
- diagnostic
- deck
- source_packet
- handoff
- content_plan
- implementation_plan
- qa_report

## 3.3 client

The client or client-world connected to the artifact.

Use `internal` when the artifact is for HAMAL / AMA Mob OS itself.

## 3.4 workflow_origin

The workflow that produced the artifact.

Examples:
- client_discovery
- systems_audit
- bwyh_launch
- business_pressure_test
- playbook_extraction
- repo_ingestion
- close_protocol

## 3.5 approval_state

Suggested values:
- draft
- internal_review
- approved_internal
- client_review
- approved_client
- public_review
- public_ready
- sent
- archived
- deprecated

## 3.6 repo_location

The repo-relative or absolute path where the artifact lives.

Avoid vague references like "in Google Drive" unless a durable path or source note exists.

## 3.7 graph_links

Graphify node, query, path, or related source notes.

Use this to connect the artifact back into the shared brain.

## 3.8 reusable_value

The reusable value of the artifact.

Suggested values:
- none
- client_specific
- template_candidate
- reusable_template
- playbook_source
- offer_asset
- training_asset
- proof_asset

---

# 4. Artifact Lifecycle

```text
Artifact created
  -> classify artifact type
  -> assign owner and MOB
  -> check sensitivity
  -> store in repo or approved workspace
  -> register location
  -> link workflow origin
  -> identify reusable value
  -> update Graphify / Obsidian when useful
  -> route for approval or handoff
```

---

# 5. Artifact Registry Record Template

```yaml
artifact_id:
artifact_name:
artifact_type:
client:
workflow_origin:
approval_state:
repo_location:
graph_links:
  - 
reusable_value:
owner:
owning_mob:
source_agent:
source_subsystem:
created_date:
last_updated:
sensitivity_level:
public_ready: false
memory_target:
playbook_links:
  - 
handoff_destination:
next_action:
```

---

# 6. Sensitivity Levels

Suggested values:
- public
- internal
- client_confidential
- private_strategy
- financial
- legal_review
- health_or_personal

Default to `internal` or stricter until reviewed.

---

# 7. Reusable Value Rule

Every artifact should be checked for reusable value.

If it can become a template, playbook, checklist, diagnostic, offer asset, or training artifact, route it to the playbook layer.

If it is client-specific, keep it connected to the client registry and handoff state.

---

# 8. What Should Not Be Included Yet

Do not include yet:
- private client details
- unredacted payment data
- secrets or credentials
- legally sensitive terms without review
- public-ready status without approval
- external links that expose private material

