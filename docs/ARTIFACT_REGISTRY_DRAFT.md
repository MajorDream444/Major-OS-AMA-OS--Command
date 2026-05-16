# Artifact Registry Draft

last updated: May 2026

## Shared Brain Registration Rule

Every repo, subsystem, workflow, agent, artifact, and memory object must register back into the shared brain.

## Routing Notes

- Canonical anchor: `HAMAL_CURRENT_STATE_SYNTHESIS.md`
- Operating environment doctrine: `CLIENT_OPERATING_ENVIRONMENTS.md`
- Shared brain protocol: `GRAPHIFY_SHARED_BRAIN_PROTOCOL.md`
- Related registries: `CLIENT_REGISTRY_DRAFT.md`, `CLOSE_PROTOCOL_STANDARD.md`, `AGENT_WORKFLOW_REGISTRY_DRAFT.md`
- Scope: documentation and registry architecture only
- Do not add private files, secret links, payment records, or public-ready flags without review.

---

# 1. Purpose

This draft defines how client and internal artifacts become durable, registered objects in the HAMAL / AMA Mob shared brain.

The rule is simple:

```text
No loose documents.
No unclassified PDFs.
No client promises without placement.
No artifact without owner, source, approval state, and reusable value check.
```

---

# 2. Artifact Registry Schema

```yaml
artifact_id:
artifact_name:
artifact_type:
client:
workflow_origin:
approval_state:
repo_location:
graph_links:
reusable_value:
source_classification:
sensitivity_level:
owner:
owning_mob:
source_index_entry:
notion_status:
airtable_status:
notebooklm_status:
handoff_destination:
next_action:
last_updated:
```

---

# 3. Source Classification Standard

Every incoming asset must be classified into one of these categories.

## 3.1 Client-Facing Documents

Examples:
- proposal PDFs
- blueprints
- one-pagers
- client decks
- SOWs sent to client
- final handoff documents
- update briefings

## 3.2 Internal Strategy Documents

Examples:
- operator notes
- strategic read
- pricing rationale
- close scripts
- build reasoning
- scope risk notes
- internal value calculations

## 3.3 Raw Source Materials

Examples:
- transcripts
- meeting notes
- email exports
- intake answers
- Loom transcripts
- client voice notes
- screenshots of chats
- reviewed websites
- source PDFs from client

## 3.4 Research And Reference Library

Examples:
- design references
- animation references
- visual inspiration
- competitor references
- market references
- system design references

## 3.5 Build Specifications

Examples:
- technical specs
- schemas
- workflow maps
- PRDs
- integration requirements
- API mappings
- data models

## 3.6 Accounting / Contract / Commercial

Examples:
- payment records
- invoices
- receipts
- signed SOWs
- cost sheets
- margin sheets
- performance share terms

Commercial artifacts should be access-controlled and reviewed before being referenced in broad docs.

---

# 4. Required Fields

## 4.1 artifact_id

Stable machine-readable identifier.

Example:

```text
artifact_theo_sow_v1
artifact_sheetal_update_briefing_001
artifact_client_clarity_intake_schema
```

## 4.2 artifact_type

Suggested values:
- blueprint
- proposal
- sow
- payment_structure
- source_index
- decision_log
- intake_schema
- intake_summary
- build_spec
- update_briefing
- podcast_prompt
- handoff_doc
- support_doc
- costing_internal
- playbook
- template

## 4.3 workflow_origin

The workflow that produced or required the artifact.

Examples:
- client_clarity_intake
- blueprint_extraction
- close_protocol
- build_activation
- document_ingestion
- notebooklm_client_update
- client_handover
- pricing_and_margin_review

## 4.4 approval_state

Suggested values:
- raw
- classified
- draft
- internal_review
- approved_internal
- client_review
- approved_client
- sent
- archived
- deprecated

## 4.5 repo_location

The repo-relative path or approved workspace location.

If the artifact lives outside GitHub, GitHub should still contain the source index entry and placement truth.

## 4.6 graph_links

Graphify node, query, scan note, or relationship reference.

## 4.7 reusable_value

Suggested values:
- client_specific
- template_candidate
- reusable_template
- playbook_source
- offer_asset
- training_asset
- proof_asset
- internal_only

---

# 5. SOURCE_INDEX.md Standard

Every client repo or project space should maintain a `SOURCE_INDEX.md` with:
- filename
- asset type
- source/date
- project relevance
- client-facing vs internal
- where stored
- Airtable record URL or note
- Notion page URL or note
- Graphify scanned? yes/no
- NotebookLM included? yes/no
- GitHub path if applicable
- action needed

---

# 6. Artifact Lifecycle

```text
Artifact appears
  -> classify source
  -> identify client/project
  -> check sensitivity
  -> assign artifact_id
  -> place in approved environment
  -> log in SOURCE_INDEX.md
  -> register approval state
  -> link Graphify / NotebookLM status
  -> assess reusable value
  -> route to client, playbook, handoff, or archive
```

---

# 7. Draft Record Template

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
source_classification:
sensitivity_level:
owner:
owning_mob:
source_index_entry:
notion_status:
airtable_status:
notebooklm_status:
handoff_destination:
next_action:
last_updated:
```

---

# 8. What Should Not Be Included Yet

Do not include:
- private client details
- raw sensitive transcripts
- unredacted payment data
- secrets or credentials
- private source links
- public-ready status without approval
- legal terms without review

