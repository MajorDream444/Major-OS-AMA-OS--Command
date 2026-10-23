# Cloud environment standard

Written 23 October 2026 after a scheduled run died at startup with
`Setup script failed`, unrecoverable, before Claude Code launched.

## The rule that prevents it

**A setup script should install only what that environment's work actually needs.
When in doubt, install nothing.**

The failure was a default `#!/bin/bash` + `npm install` left on an environment used by a
lead-research task. There is no `package.json` where it looked, so it failed — and a
failed setup script kills the session before any work begins. The task had nothing to do
with npm.

## Scripts by environment type

**Research, outreach, reporting — anything with no code**
```bash
#!/bin/bash
exit 0
```
A script that does nothing cannot fail. This covers most scheduled tasks.

**Repositories with no root package.json** — `Major-AI-OS` keeps its manifests under
`apps/`, so a root install always fails
```bash
#!/bin/bash
set -e
for d in apps/maim-site apps/maim-creative-studio-catalogue; do
  [ -f "$d/package.json" ] && (cd "$d" && npm install --no-audit --no-fund)
done
```

**Repositories with a root package.json** — `Major-OS-AMA-OS--Command` has one
```bash
#!/bin/bash
set -e
npm install --no-audit --no-fund
```

## Environment variables

Visible to anyone using the environment: **configuration only, never credentials.**

Use `NODE_ENV=development`, not `production` — production skips devDependencies, so
TypeScript and the test runner disappear and builds fail in confusing ways.

## Network secrets

For API keys the session must *use* without seeing. Leave empty unless a shell command
calls that API directly.

Most of this ecosystem does not need them: Stripe, Resend, Vercel, Supabase and Airtable
are reached through MCP connectors, which are brokered outside the container. The
website's keys live in Vercel, not here. Adding a secret you do not need is one more
credential to rotate.

## Connectors on scheduled tasks

A scheduled task does **not** inherit the account's connectors. It stores its own list,
fixed at creation, and fires into a clean session with only that list.

Tasks created through the API carry none — the `connectors` parameter is unavailable for
this organisation, so **scheduled tasks that need a connector must be created or edited in
the routines UI.** A task that writes to Airtable and has no Airtable connector will
research successfully and then have nowhere to put the result. That pattern has now cost
several weeks of silent failures.

## Before trusting any scheduled task

1. Fire it manually once.
2. Confirm the session reaches `WORKING` with no `last_init_error`.
3. Confirm it can reach its destination — have the first run report connectivity and stop.
4. Only then rely on the schedule.

A task reporting SUCCEEDED proves it ran, not that it did anything. One run finished in
eleven seconds and produced nothing.

## Known environments

| Environment | Purpose | Script |
|---|---|---|
| Major Prime OS | scheduled tasks, research | **`exit 0`** — currently broken, fix first |
| MAIM-ABC-Studio | ABC studio app | per-app install |
| AMA MOB OS V2 · AMASOLAGI SITE | AMA work | per-app install |
| HAMAL FOUNDRY OS — QATAR | Qatar venture | separate business |
| West African Mobility · 52in52 | dormant | `exit 0` |
| Default | general | `exit 0` |

## On tooling

There is no write API for cloud environments — setup scripts, variables and secrets are
edited in the environment settings only, and the documentation confirms it. So an agent
cannot be given a tool for this today, and a wrapper cannot be built over an endpoint that
does not exist.

That is not the real gap anyway. Nothing here failed for want of a tool; it failed because
no one had written down what each environment is for. This page is that record. Keep it
current and the trip-up does not recur.
