# Client Registry Draft

last updated: May 2026

## Shared Brain Registration Rule

Every repo, subsystem, workflow, agent, artifact, and memory object must register back into the shared brain.

## Routing Notes

- Canonical anchor: `HAMAL_CURRENT_STATE_SYNTHESIS.md`
- Operating environment doctrine: `CLIENT_OPERATING_ENVIRONMENTS.md`
- Shared brain protocol: `GRAPHIFY_SHARED_BRAIN_PROTOCOL.md`
- Related registries: `ARTIFACT_REGISTRY_DRAFT.md`, `CLOSE_PROTOCOL_STANDARD.md`, `SUBSYSTEM_REGISTRY_DRAFT.md`
- Scope: documentation and registry architecture only
- Do not add private client data, live CRM IDs, Airtable records, Notion records, or payment data.

---

# 1. Purpose

This draft defines the client registry structure for reusable client operating environments.

It exists to make every client relationship visible to the shared brain without exposing sensitive client information or creating live operational records before approval.

---

# 2. Client Registry Schema

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
environment_id:
owner:
lead_agent:
owning_mob:
supporting_mobs:
source_index:
repo_location:
graph_links:
notion_status:
airtable_status:
notebooklm_status:
commercial_status:
approval_requirements:
next_action:
last_updated:
```

---

# 3. Required Fields

## 3.1 client_id

Stable machine-readable identifier.

Examples:

```text
client_theo_howling_mune
client_sheetal_shakti
client_shaun_graffiti_media
```

## 3.2 client_name

Human-readable client or client-world name.

Use client-safe naming. Do not include unnecessary private details.

## 3.3 subsystem

The system or client world this client belongs to.

Examples:
- Client Clarity OS
- Howling Mune OS
- Shakti System OS
- Graffiti Media Engine OS
- Business Pressure Test
- BWYH

## 3.4 current_phase

Suggested values:
- prospect
- intake
- blueprint
- blueprint_review
- proposal
- close_protocol
- sow_review
- payment_activation
- build_active
- client_update
- handover
- support
- expansion
- paused
- archived

## 3.5 archetype

The pattern this client represents.

Examples:
- creator-healer
- wisdom brand
- media engine
- founder-operator
- retreat partner
- diagnostic buyer
- systems audit client
- strategic partnership

## 3.6 economic_value

The economic role of the relationship.

Examples:
- active_revenue
- strategic_case_study
- reusable_template_source
- pilot_proof
- partnership_pipeline
- future_retainer
- learning_asset

## 3.7 build_status

Suggested values:
- not_started
- intake_pending
- intake_complete
- blueprint_drafted
- offer_pending
- sow_pending
- awaiting_payment
- build_active
- awaiting_assets
- awaiting_review
- delivered
- support_active
- blocked
- paused

## 3.8 playbook_links

Playbooks or SOPs governing the client environment.

Examples:
- close protocol
- client clarity intake
- blueprint extraction
- build activation
- document ingestion
- NotebookLM client update
- handover and support

## 3.9 artifact_links

Durable artifacts connected to the client.

Examples:
- blueprint
- proposal
- SOW
- payment structure
- source index
- update briefing
- handoff document

## 3.10 handoff_status

Suggested values:
- no_handoff_needed
- handoff_needed
- handoff_drafted
- awaiting_internal_review
- awaiting_client_review
- sent
- accepted
- support_window_active
- blocked

---

# 4. Client Registry Lifecycle

```text
Client signal
  -> client registry draft entry
  -> subsystem assignment
  -> operating environment creation
  -> source index creation
  -> intake / blueprint / close status
  -> artifact registration
  -> build activation
  -> update rhythm
  -> handoff / support / expansion
  -> reusable pattern extraction
```

---

# 5. Draft Record Template

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
environment_id:
owner:
lead_agent:
owning_mob:
supporting_mobs:
  - 
source_index:
repo_location:
graph_links:
  - 
notion_status:
airtable_status:
notebooklm_status:
commercial_status:
approval_requirements:
  - 
next_action:
last_updated:
```

---

# 6. Initial Client Environment Types

## 6.1 Theo / Howling Mune Pattern

Archetype:

```text
creator-healer / somatic operator / client flow engine
```

Reusable lessons:
- ownership and IP boundaries must be explicit
- stage deliverables must be tangible
- revision rounds must be enumerated
- support windows must be defined
- software costs must require approval
- handover must include access, exports, platform list, SOPs, and walkthrough
- revenue alignment must be attributable and time-bound
- performance language should be review framework, not guarantee

## 6.2 Sheetal / Shakti Pattern

Archetype:

```text
wisdom brand / system foundation / client update notebook candidate
```

Reusable lessons:
- client update briefings may reduce repetitive calls
- doctrine and source documents need a clear NotebookLM source manifest
- system foundation work must separate client-facing clarity from internal OS scaffolding

## 6.3 Shaun / Graffiti Media Pattern

Archetype:

```text
media engine / white-label system / production operating layer
```

Reusable lessons:
- media systems need clean operating docs, asset routing, onboarding, and production handoffs
- client-facing artifacts should stay separated from reusable media engine doctrine

---

# 7. What Should Not Be Included Yet

Do not include:
- private contact details
- live client records
- payment records
- signed SOW details
- confidential strategy
- health or deeply personal client data
- unapproved public claims

