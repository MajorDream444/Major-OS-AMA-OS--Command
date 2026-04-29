# GitHub Logs Panel

## Purpose

The GitHub Logs panel gives the Command Center a local-first view of repo truth: commits, protocol docs, handoffs, and daily log readiness.

GitHub remains the source of truth, but this build does not call GitHub APIs yet.

## Current Behavior

The panel uses local mock data stored in `app.js` and persisted through `localStorage`.

It can show:

- latest commit
- protocol docs
- handoff files
- daily log readiness
- stale or review-needed records

## Local-First Rule

Current build:

- no GitHub API reads
- no GitHub API writes
- no external service calls
- no secrets
- no tokens

The panel is a display and simulation layer only.

## Future Live GitHub Path

When approved, implement read-only GitHub access first.

Safe first reads:

- list commits
- list `/logs/daily` files
- list recently updated docs
- show latest handoff files

Later reads:

- pull request status
- build status
- review status
- release notes

Do not implement write actions until explicitly approved.

## What Should Be Logged

Log:

- commits that change operating behavior
- protocol docs
- handoff docs
- daily brief logs
- agent logging standards
- sync maps
- build verification notes

## What Should Not Be Logged

Do not log:

- API keys
- personal access tokens
- webhook URLs
- private credentials
- raw customer data
- unredacted emails or phone numbers
- secrets copied from `.env`

## Status Labels

Use these labels:

- SYNCED
- NEEDS REVIEW
- BLOCKED
- STALE

## Command Support

These local commands should review the mock logs:

```text
show github logs
check repo logs
what changed
```

Expected local behavior:

- update Activity Feed with `GitHub logs reviewed`
- highlight the GitHub Logs panel
- add a Top 3 Action when a log is `NEEDS REVIEW` or `STALE`
