# Graphify Shared Brain Protocol

last updated: May 2026

## Shared Brain Registration Rule

Every repo, subsystem, workflow, agent, artifact, and memory object must register back into the shared brain.

## Routing Notes

- Canonical anchor: `/Users/majordreamwilliams/Documents/HAMAL_MOB_OS_CANON/HAMAL_MOB_OS_CURRENT_STATE.md`
- Local command sources: `../REPO_MAP.md`, `../SYSTEM_CORE.md`, `docs/GRAPHIFY_CONTEXT_LAYER.md`
- Requested but not found locally: `The_Sovereign_AI_Organism.pdf`
- Scope: documentation-only shared brain protocol
- Do not run live Graphify updates, integrations, deploys, or external syncs without approval.

---

# 1. Purpose

This protocol defines how Graphify, Obsidian, canonical markdown, and future memory systems work together as the shared brain for HAMAL / AMA Mob OS.

It exists to stop context drift and make every future agent operate from registered memory architecture.

---

# 2. Shared Brain Model

```text
Canonical Markdown
  -> defines doctrine and operating truth
Graphify
  -> maps relationships and dependencies
Obsidian
  -> preserves human-readable memory and synthesis
NotebookLM
  -> supports source-grounded explanation, review, audio, and summaries
Command Center
  -> surfaces what is active, blocked, or needs review
```

No single layer is the whole brain. The shared brain is the relationship between them.

---

# 3. Graphify Role

Graphify is the persistent context graph.

It should track:
- repos
- docs
- playbooks
- workflows
- agents
- artifacts
- memory objects
- subsystem relationships
- routing paths
- source-of-truth boundaries

Graphify is not a replacement for reading current files. It is a navigation and relationship layer.

---

# 4. Obsidian Role

Obsidian is the durable human memory vault.

It should preserve:
- decisions
- synthesis notes
- operating principles
- workspace maps
- client-safe summaries
- historical context
- cross-system explanations

Obsidian should be readable by humans who need continuity without reopening every chat.

---

# 5. NotebookLM Role

NotebookLM should be used for source-grounded synthesis and operator-friendly review.

Useful NotebookLM outputs:
- briefings
- explainers
- study guides
- podcast-style summaries
- source-backed comparisons
- doctrine review packets

NotebookLM should not become the only source of truth.

---

# 6. Registration Pattern

Every new object should register with the shared brain.

```yaml
registration:
  object_id:
  object_type: repo/subsystem/workflow/agent/artifact/memory
  name:
  owner:
  owning_mob:
  workspace:
  source_path:
  canonical_path:
  related_docs:
  graphify_node:
  obsidian_note:
  notebooklm_source_set:
  current_status:
  economic_purpose:
  approval_required:
  last_updated:
```

---

# 7. Formal Registry Layer

The shared brain protocol now expects formal registry surfaces for the objects that drive delivery and revenue.

Initial formal registries:
- `CLIENT_REGISTRY.md` — client worlds, phases, archetypes, economic value, build status, playbooks, artifacts, and handoffs
- `ARTIFACT_REGISTRY.md` — durable outputs, approval state, repo location, graph links, and reusable value
- `CLOSE_PROTOCOL_REGISTRY.md` — offer type, payment structure, support terms, handover rules, revision rules, risk, and approvals

Client operating system doctrine:
- `CLIENT_OPERATING_ENVIRONMENTS.md` — reusable doctrine for client operating environments, build activation, update rhythm, and handover boundaries
- `CLIENT_REGISTRY_DRAFT.md` — draft client registry fields for reusable client environments
- `ARTIFACT_REGISTRY_DRAFT.md` — draft artifact registry fields aligned to source classification and placement discipline
- `CLOSE_PROTOCOL_STANDARD.md` — close protocol standard for offers, payment structures, support, handover, revisions, risk, and build activation

These registries should remain documentation-first until a live database or automation path is explicitly approved.

---

# 8. Memory Update Lifecycle

```text
Input appears
  -> classify object type
  -> assign owner / MOB / workspace
  -> register artifact path
  -> update canonical markdown if doctrine changed
  -> update Graphify if relationships changed
  -> update Obsidian if durable meaning changed
  -> update NotebookLM source set if synthesis is needed
  -> notify Command Center if action or review is needed
```

---

# 9. Graphify Update Rules

Before broad repo work:
1. Check whether `graphify-out/GRAPH_REPORT.md` exists.
2. If it exists, read it before broad searches.
3. If `graphify-out/wiki/index.md` exists, use it as a navigation map.
4. Verify current code or docs directly before editing.

After meaningful documentation or architecture changes in a graphified repo, recommend:

```bash
graphify update .
```

If no graph exists, say so clearly.

---

# 10. Anti-Silo Rule

No object should remain only in one chat, one agent output, one local folder, or one person's head.

If an object matters, it needs at least one durable destination:
- canonical markdown
- registered repo path
- Obsidian note
- Graphify graph node
- Command Center event
- playbook
- artifact registry entry

---

# 11. No Isolated Agent Drift Rule

Agents must not create private side-worlds.

An agent output should always say:
- where the artifact lives
- what canon it updates
- what workflow it belongs to
- what memory should be updated
- what economic purpose it serves
- what review gate remains

---

# 12. Economic Purpose Requirement

Memory is not hoarding. Memory exists to improve execution.

Every memory update should support:
- faster onboarding
- less repeated explanation
- better client delivery
- reusable IP
- stronger offers
- fewer dropped decisions
- clearer accountability
- better revenue operations

---

# 13. Source Priority

When sources conflict, prioritize:
1. current canonical markdown
2. repo-local source files
3. current handoff docs
4. Graphify reports and wiki maps
5. Obsidian synthesis notes
6. NotebookLM summaries
7. chat memory

If a claim comes from a missing or unverified source, mark it as pending.
