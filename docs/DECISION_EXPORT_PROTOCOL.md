# Decision Export Protocol

## Purpose

Mission Control owns approval decisions for external artifacts. Substack Automation Engine produces artifacts; Command Center approves, rejects, requests rewrites, or requests a future publish handoff.

## Target File

```text
content/logs/workflows/mission_control_decisions.json
```

The current static UI cannot write to disk directly. Runtime decisions are stored in local state and shown as exportable JSON in the ARTIFACTS panel. The repo file is the handoff target for future CLI or automation sync.

## Decision Schema

```json
{
  "decision_id": "D-YYYYMMDD-HHMMSS-XXXX",
  "artifact_id": "",
  "mission_id": "",
  "source": "SUBSTACK_ENGINE",
  "decision": "approved | rejected | rewrite_requested | publish_requested",
  "decided_by": "Major",
  "decided_at": "",
  "reason": "",
  "next_action": "",
  "artifact_snapshot": {
    "title": "",
    "lane": "",
    "score": 0,
    "confidence": 0,
    "risk_level": "",
    "publish_mode": "",
    "status": ""
  }
}
```

## Commands

```text
approve artifact <artifact_id>
reject artifact <artifact_id>
rewrite artifact <artifact_id>
publish artifact <artifact_id>
```

## Local Behavior

- `approve artifact` sets the artifact to `APPROVED` and exports `approved`.
- `reject artifact` sets the artifact to `REJECTED` and exports `rejected`.
- `rewrite artifact` sets the artifact to `REWRITE_REQUESTED` and exports `rewrite_requested`.
- `publish artifact` exports `publish_requested` only when the artifact is not high risk, not blocked, and not waiting on review.

## Publish Guardrails

- High-risk artifacts cannot publish from Mission Control.
- Blocked artifacts cannot publish.
- Mission Control never calls Substack or live publishing APIs.
- Publish means local handoff request only.
