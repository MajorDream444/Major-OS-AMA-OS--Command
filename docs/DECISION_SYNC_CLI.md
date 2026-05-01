# Decision Sync CLI

## Purpose

`scripts/sync_decisions.js` moves browser-exported Mission Control decisions into the repo handoff file.

This is local-only. It does not call Substack, Airtable, GitHub APIs, or live publishing services.

## Command

```text
npm run decisions:sync -- --file fixtures/substack/sample_decisions_export.json
```

Other input modes:

```text
npm run decisions:sync -- --stdin
npm run decisions:sync
```

Default input:

```text
content/logs/workflows/mission_control_decisions_export.json
```

## Outputs

```text
content/logs/workflows/mission_control_decisions.json
content/logs/workflows/mission_control_decisions.md
```

## Validation

Every decision must include:

```text
decision_id
artifact_id
mission_id
source
decision
decided_by
decided_at
reason
next_action
artifact_snapshot
```

Allowed decisions:

```text
approved
rejected
rewrite_requested
publish_requested
```

`artifact_snapshot` must include:

```text
title
lane
score
confidence
risk_level
publish_mode
status
```

## De-Dupe Rule

Existing decisions are preserved.

Incoming decisions are appended only when `decision_id` is new.

## Flow

```text
Browser decision export
-> sync_decisions.js
-> mission_control_decisions.json
-> mission_control_decisions.md
-> Substack Engine import
```
