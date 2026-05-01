# Approval Intelligence Layer

## Purpose

The Approval Intelligence Layer helps Mission Control decide what needs Major review before any future publish, distribution, or system action.

It is local-only.

## External Artifact Review

Imported artifacts can include:

- score
- confidence
- risk level
- publish mode
- requires Major review
- next action
- source path

The Artifacts panel displays this intelligence so Command Center can make the final call.

## Commands

```text
approve artifact <artifact_id>
reject artifact <artifact_id>
rewrite artifact <artifact_id>
publish artifact <artifact_id>
```

Behavior:

- `approve artifact` marks the local artifact approved and clears `requires_major_review`.
- `reject artifact` marks the local artifact rejected.
- `rewrite artifact` routes the local artifact back for rewrite.
- `publish artifact` only approves a future publish handoff if governance rules allow it.

No command publishes externally in the current build.

## Next Move Routing

Mission Control uses hybrid priority order:

1. Blocked
2. Needs Review
3. High-score Ready
4. Scheduled / Delay Buffer
5. Recent Published

If an imported artifact is blocked, Next Move should show:

```text
Rewrite artifact: <title>
rewrite artifact <artifact_id>
```

If an imported artifact has:

```text
requires_major_review = true
```

Then Next Move should show:

```text
Review artifact: <title>
approve artifact <artifact_id>
```

If an imported artifact has `publish_mode = AUTO`, `risk_level = LOW`, and `status = READY`, Next Move should show:

```text
Ready to publish: <title>
publish artifact <artifact_id>
```

## Blocking Rules

- High risk artifacts cannot auto-publish.
- Reaction Doctrine artifacts without strong `system_underneath` are blocked.
- Command Center owns final approval.
- Substack Engine only produces artifacts.

## Current Boundary

No integrations.

No APIs.

No secrets.

No live publishing.
