# Evergreen Skill Loop

## Purpose

The Evergreen Skill Loop lets local agents propose reusable skills when they notice repeated work, missing leverage, or a workflow that should become part of Major OS.

Current build: local/mock only.

Do not create live tools, external integrations, API calls, or secrets from a skill request.

## Agent Proposal Rule

Agents may propose skills.

Agents may not auto-create, install, publish, execute, or connect live tools.

Every proposed skill must include:

- proposed agent
- skill name
- why it is needed
- expected input
- expected output
- risk
- approval status

## Approval Path

```text
Agent proposes -> Mission Control logs -> Major reviews -> Codex builds -> GitHub stores -> OpenClaw may use later
```

Codex only builds a skill after approval.

GitHub stores approved skills, protocols, and handoffs.

OpenClaw may use approved skills later, but this Command Center build does not execute OpenClaw.

## Mapping Requirement

Every skill must map to at least one workflow:

- revenue action
- content action
- system improvement
- agent handoff
- distribution workflow
- app factory workflow
- internal leverage workflow

If a skill does not support revenue or internal leverage, keep it in review.

## No Live Tool Rule

Skill requests must not contain:

- API keys
- tokens
- webhook URLs
- private credentials
- raw customer data
- external publish instructions
- live write actions

## Local Command

```text
propose skill <skill name>
```

This creates a local Skill Request assigned to Ops Watcher and adds a review action for Major.

## Future Path

When approved, a future build may:

1. Convert approved requests into GitHub issues.
2. Add skill specs under the reusable Major AI OS repo.
3. Add tests or dry-run examples.
4. Let OpenClaw discover approved skill metadata.
5. Keep execution gated until credentials and permissions are explicit.
