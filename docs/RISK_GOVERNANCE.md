# Risk Governance

## Authority

Command Center owns final approval.

External systems may recommend a publish mode, risk level, score, and next action. Command Center may accept or reject those recommendations locally.

## Publish Modes

- `AUTO`: local artifact can move without a review gate only if risk allows.
- `REVIEW`: Major review is required.
- `SCHEDULED`: local delay buffer is required before future handoff.

## Hard Rules

- High risk artifacts cannot auto-publish.
- High risk artifacts cannot receive publish requests from Mission Control.
- Reaction Doctrine artifacts without strong `system_underneath` must be blocked.
- Imported artifacts requiring Major review must appear in Next Move before publish handoff.
- Substack Engine only produces artifacts.
- Command Center owns final approval.

## Artifact-Level Metadata

```text
source
score
confidence
risk_level
publish_mode
requires_major_review
system_underneath
github_path
airtable_record_id
```

## Current Implementation

The current build:

- loads sample `SUBSTACK_ENGINE` artifacts as local seed data
- mirrors a sample export at `content/logs/workflows/mission_control_export.json`
- displays source, score, confidence, risk level, and publish mode
- filters artifacts by `ALL`, `LOCAL`, or `SUBSTACK_ENGINE`
- ranks artifacts using the hybrid priority order
- routes imported review-needed artifacts into Next Move
- supports local approval, rejection, rewrite, and publish-handoff commands
- appends local decision records for approved, rejected, rewrite requested, and publish requested outcomes

Decision export target:

```text
content/logs/workflows/mission_control_decisions.json
```

No live publish or external write exists.
