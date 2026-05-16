# Close Protocol Registry

last updated: May 2026

## Shared Brain Registration Rule

Every repo, subsystem, workflow, agent, artifact, and memory object must register back into the shared brain.

## Routing Notes

- Canonical anchor: `HAMAL_CURRENT_STATE_SYNTHESIS.md`
- Shared brain protocol: `GRAPHIFY_SHARED_BRAIN_PROTOCOL.md`
- Related registry docs: `CLIENT_REGISTRY.md`, `ARTIFACT_REGISTRY.md`, `AGENT_WORKFLOW_REGISTRY_DRAFT.md`
- Scope: documentation-only registry specification
- Do not add live payment links, final contract language, Stripe settings, legal terms, or client-specific close details without explicit approval.

---

# 1. Purpose

The Close Protocol Registry defines how offers, payment structures, support terms, handovers, revisions, risk, and approval requirements are documented before a deal is closed or delivered.

It exists to prevent revenue conversations from becoming scattered across chat, email, DMs, invoices, and unregistered documents.

---

# 2. Registry Schema

```yaml
close_protocol_id:
offer_type:
payment_structure:
support_terms:
handover_rules:
revision_rules:
risk_level:
approval_requirements:
client:
subsystem:
workflow_origin:
artifact_links:
owner:
owning_mob:
economic_purpose:
status:
last_updated:
```

---

# 3. Required Fields

## 3.1 offer_type

The type of offer being closed.

Suggested values:
- diagnostic
- blueprint
- systems_audit
- one_page_strategy
- implementation_build
- retainer
- cohort
- workshop
- partner_pilot
- white_label
- custom_project

## 3.2 payment_structure

The payment model.

Suggested values:
- free
- paid_in_full
- deposit_plus_balance
- milestone_based
- monthly_retainer
- revenue_share
- pilot_terms
- scholarship_or_trade
- pending_review

Do not add live payment links or processor configuration here.

## 3.3 support_terms

The support scope after payment or delivery.

Capture:
- support duration
- support channel
- response expectations
- meeting count
- async review limits
- what is excluded

## 3.4 handover_rules

The rules for final handoff.

Capture:
- what gets delivered
- where it gets delivered
- who receives it
- what counts as accepted
- what remains internal
- what requires client approval

## 3.5 revision_rules

The rules for revisions.

Capture:
- number of included revisions
- revision window
- what counts as a revision
- what counts as new scope
- approval flow

## 3.6 risk_level

Suggested values:
- low
- medium
- high
- legal_review
- financial_review
- founder_review

## 3.7 approval_requirements

The approvals required before sending or executing.

Examples:
- Major approval
- client approval
- legal review
- pricing review
- payment review
- public-copy review
- delivery capacity review

---

# 4. Close Protocol Lifecycle

```text
Offer identified
  -> close protocol drafted
  -> payment structure reviewed
  -> support terms clarified
  -> handover rules defined
  -> revision rules defined
  -> risk level assigned
  -> approval requirements checked
  -> artifacts linked
  -> client registry updated
  -> artifact registry updated
```

---

# 5. Close Protocol Record Template

```yaml
close_protocol_id:
offer_type:
payment_structure:
support_terms:
  duration:
  channel:
  response_expectations:
  included_sessions:
  exclusions:
handover_rules:
  deliverables:
  delivery_location:
  recipient:
  acceptance_rule:
  internal_only_items:
revision_rules:
  included_revisions:
  revision_window:
  new_scope_definition:
  approval_flow:
risk_level:
approval_requirements:
  - 
client:
subsystem:
workflow_origin:
artifact_links:
  - 
owner:
owning_mob:
economic_purpose:
status:
last_updated:
```

---

# 6. Status Values

Suggested values:
- draft
- needs_pricing_review
- needs_scope_review
- needs_legal_review
- needs_major_approval
- approved_internal
- sent
- accepted
- declined
- paused
- archived

---

# 7. Risk Rules

Use higher risk when:
- payment terms are unclear
- support expectations are open-ended
- deliverables are not bounded
- public claims are unreviewed
- legal language is needed
- client-sensitive details are involved
- delivery capacity is uncertain

High-risk close protocols require explicit approval before sending.

---

# 8. Economic Purpose Requirement

Every close protocol must name the business reason for the offer.

Examples:
- convert diagnostic into paid blueprint
- turn strategy call into scoped build
- create recurring support
- validate pilot offer
- generate case study
- preserve delivery boundaries
- improve cash flow

If no economic purpose is clear, do not send the offer yet.

---

# 9. What Should Not Be Included Yet

Do not include yet:
- live payment links
- card or bank details
- final legal terms
- private client negotiation notes
- unapproved discounts
- public-facing claims
- Stripe, Airtable, Notion, or CRM configuration

