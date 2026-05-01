# External Systems

## Purpose

Command Center is the authority layer. External systems may produce artifacts, logs, packets, and dry-run summaries, but they do not own final approval, publishing, routing, or operator decisions.

## Registered External Sources

### SUBSTACK_ENGINE

Source repo:

```text
MajorDream444/SUBSTACK-AUTOMATION-ENGINE
```

Role:

- produce Substack/media artifacts
- produce dry-run export files
- expose article packets, scores, confidence, risk, and next actions
- report into Command Center for approval

Boundary:

- no Command Center UI duplication
- no final approval authority
- no live publish authority from Command Center context
- no Airtable write authority from Command Center context

## Expected Import Files

```text
content/logs/workflows/mission_control_export.json
content/logs/workflows/artifacts/*.json
```

Artifact JSON fields:

```text
artifact_id
mission_id
artifact_type
source
status
lane
title
github_path
airtable_record_id
requires_major_review
score
confidence
risk_level
publish_mode
next_action
system_underneath
```

## Current Build

Current implementation uses local fixtures under:

```text
fixtures/substack/
content/logs/workflows/
```

No file watcher, API, webhook, GitHub API, Airtable API, or Substack API is active.

## Authority Rule

External systems produce artifacts.

Command Center ingests, displays, routes, approves, rejects, requests rewrite, or allows future publish handoff.
