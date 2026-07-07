# 52in52 and Knowledge Center

Status: Stage A foundation

This document defines how the weekly app factory and future Knowledge Center relate to AMA Command Center.

## Core Split

```txt
52in52 = weekly app factory
Knowledge Center = learning and build archive
AMA Command Center = operator console that tracks them
```

## 52in52

52in52 owns weekly app builds.

It should hold:

- app ideas
- weekly build records
- app implementation repos or links
- build status
- app-specific notes
- demos
- shipped artifacts

AMA Command Center should not absorb 52in52 app implementations.

It should surface status, blockers, priority, links, and review needs.

## Knowledge Center

Knowledge Center is the learning and build archive.

It should eventually collect:

- lessons from weekly builds
- reusable patterns
- failed experiments
- build notes
- app retrospectives
- implementation decisions
- agent handoffs
- useful prompts
- customer or community insights

Knowledge Center is not the same as the production dashboard.

It is the memory and learning layer for the app factory.

## AMA Command Center Role

AMA Command Center coordinates:

- what is active this week
- what is blocked
- what needs Major's review
- what needs Codex
- what needs OpenClaw later
- what belongs in Airtable
- what belongs in Notion
- what should be archived into Knowledge Center

## Future View

A future AMA Command Center view may show:

```txt
Week
App Name
Status
Owner
Repo
Demo
Blocker
Next Action
Knowledge Center Link
```

Do not build this view yet.

First, keep the boundary and data ownership clear.
