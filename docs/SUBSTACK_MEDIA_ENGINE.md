# Substack Media Engine

## Purpose

The Substack Media Engine turns Major's ideas, voice notes, briefs, and operating insights into authority-building content.

This engine supports the 30-day aggressive execution cycle by producing the daily Content Action.

## Current Boundary

Local/mock only.

Do not connect Substack, Gmail, HeyGen, Remotion, Telegram, Airtable, Notion, GitHub APIs, or n8n yet.

No secrets. No API keys.

## Role In The Stack

```text
Substack = expression and content engine
GitHub = truth
Airtable = business state
Notion = human dashboard
Obsidian / Graphify = memory graph
n8n = automation engine
OpenClaw = agent runtime
```

## Daily Output

Every day should produce one content action.

Acceptable content actions:

- Substack post draft
- article outline
- voice-note-to-post transformation
- video script
- podcast outline
- tweet thread
- short-form caption set
- campaign angle
- authority note

## Engine Flow

```text
Input -> Angle -> Draft -> Repurpose -> Log -> Improve
```

### 1. Input

Sources may include:

- daily brief
- operator command
- voice note transcript
- meeting note
- system insight
- client lesson
- offer idea
- blocker

### 2. Angle

Choose one clear angle:

- authority
- proof
- teaching
- offer
- behind the build
- systems insight
- client transformation

### 3. Draft

Create the core written asset first.

Do not generate media before the message is clear.

### 4. Repurpose

Turn the core asset into smaller assets:

- video script
- social post
- email seed
- podcast segment
- carousel outline
- sales page section

### 5. Log

Record the content action in the Daily Brief handoff.

Minimum log:

```text
Date:
Source:
Angle:
Core Asset:
Repurposed Assets:
Owner Agent:
Status:
Next Action:
Evidence:
```

### 6. Improve

Capture the blocker or improvement:

- unclear offer
- weak hook
- missing proof
- no CTA
- needs publish decision
- needs media generation

## Agent Ownership

Primary owner:

- A003 Content Catcher

Supporting agents:

- A004 Ops Watcher
- A006 Outreach
- A007 Offer Builder
- A008 Deck Builder

## Status Labels

Use these labels:

- READY
- ACTION
- REVIEW
- WAITING
- BLOCKED
- DONE

## Command Examples

```text
draft today's Substack authority note
turn this daily brief into a post
make a video script from the BWYH insight
create a tweet thread from the blocker
repurpose this into a podcast outline
```

## Next Implementation Step

Add a local command route for Substack/media commands that assigns work to A003 Content Catcher and creates a mock Content Action in the Daily Brief panel.
