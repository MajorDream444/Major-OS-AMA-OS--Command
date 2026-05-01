# Risk Governance Layer

## Purpose

The Risk Governance Layer adds local publish guardrails to Mission Control.

It does not publish, schedule, sync, send, or call external services. It only labels local artifacts and distribution rows so Major can see what can move automatically, what requires review, and what should sit behind a delay buffer.

## Modes

- `AUTO`: local internal movement is allowed without a review gate.
- `REVIEW`: Major review is required before any future publish or distribution action.
- `SCHEDULED`: item is locally queued with a delay buffer before future handoff.

## Lane-Based Rules

Current local rules:

- `BWYH`: `SCHEDULED`, 12 hour delay buffer
- `Contour`: `REVIEW`
- `SAF`: `REVIEW`
- `Major AI OS`: `SCHEDULED`, 6 hour delay buffer
- `Doctrine`: `REVIEW`
- `Reaction Doctrine`: `REVIEW`
- `Operations`: `AUTO`
- `Commerce`: `REVIEW`

## Artifact Metadata

Artifacts may include:

```js
{
  risk_mode,
  publish_rule,
  delay_until,
  governance_override,
  risk_note
}
```

The artifact panel displays the risk mode and publish rule beside the normal artifact status.

## Distribution Metadata

Distribution queue rows may include:

```js
{
  risk_mode,
  publish_rule,
  delay_until,
  governance_override
}
```

The Distribution Queue displays `AUTO`, `REVIEW`, or `SCHEDULED` before the row status.

## Delay Buffer Logic

When a lane rule is `SCHEDULED`, Mission Control calculates a local `delay_until` timestamp using the lane's delay buffer.

This timestamp is informational only. It does not schedule a real post, notification, render, sync, or external job.

## Override Controls

The Risk Governance panel provides local override buttons:

- `AUTO`
- `REVIEW`
- `SCHEDULED`

Overrides update the selected lane rule and reapply metadata to existing local artifacts and distribution rows in that lane.

## Boundary

No integrations.

No API calls.

No secrets.

No live publishing.

Future live systems must treat this layer as an approval and scheduling signal, not as permission to execute without Major's explicit integration approval.
