# Artifact System

## Purpose

The Artifact System makes Mission Control track outputs, not just activity. Every local orchestrator mission can produce visible artifacts that Major can review, approve, or archive before any future live integration is allowed to publish or sync them.

This layer is local-first and mock-only. It does not call external services.

## Artifact Object

```js
artifact = {
  id,
  mission_id,
  title,
  type,
  lane,
  status,
  created_at,
  updated_at,
  owner_agent,
  summary,
  preview,
  source_command
}
```

## Artifact Types

- `lead_list`
- `audit_report`
- `outreach_draft`
- `substack_draft`
- `video_script`
- `product_page`
- `workflow_plan`
- `daily_brief`
- `memory_note`

## Statuses

- `DRAFT`
- `READY`
- `NEEDS REVIEW`
- `APPROVED`
- `ARCHIVED`

## Mission Creation Rules

When a simulated mission completes, Mission Control creates placeholder artifacts from the mission intent:

- `lead_generation` -> `lead_list`, `outreach_draft`
- `audit` -> `audit_report`
- `content_media` -> `substack_draft`, `video_script`
- `outreach` -> `outreach_draft`
- `commerce` -> `product_page`, `workflow_plan`
- `operations` -> `daily_brief`, `workflow_plan`

Artifacts are attached to the mission by `mission_id`. Mission cards show artifact count and latest artifact title.

## Review Flow

Commands:

- `show artifacts` highlights the Artifacts panel and logs `Artifacts reviewed`.
- `approve artifact <title>` marks the matching local artifact `APPROVED`.
- `archive artifact <title>` marks the matching local artifact `ARCHIVED`.

Any artifact with `NEEDS REVIEW` can create a Top 3 Action:

```text
Review artifact: {{title}}
```

## Local-Only Behavior

Artifacts persist through `localStorage`.

The current system may create, review, approve, and archive artifacts locally only. No external write, publish, sync, or API action is allowed in this layer.

## Future Storage Path

Later live storage should be introduced in this order:

1. GitHub read/write only for approved handoff files and durable logs.
2. Airtable records for business-state tracking after schemas are confirmed.
3. Notion dashboard mirrors for human review.

No artifact may include secrets, API keys, tokens, private credentials, or raw customer-sensitive data.
