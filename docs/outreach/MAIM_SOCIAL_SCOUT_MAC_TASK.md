# MAIM Social Scout — Mac-bound scheduled task

> ## ⛔ BLOCKED — do not create this task
>
> Agent Reach 1.6.0 was installed on the Mac on 23 Oct and tested. It does not
> deliver the capability this spec assumes:
>
> | Channel | Result |
> |---|---|
> | Instagram | HTTP 429 on first contact; Agent Reach auto-paused the channel |
> | Facebook — profile | returned only the URL and username. No name, bio or posts |
> | Facebook — search | returned no data |
>
> Both channels are marked experimental upstream. The install report itself said
> `还没逐项联网测试` — no channel had been tested over the network. The capability
> table in the README is a claims table, not a results table.
>
> Creating this task would produce a weekly run that reaches nothing and writes
> nothing — the exact silent failure the rest of this pipeline was built to avoid.
>
> **Status of the idea, not the tool:** the Mac-bound split is still correct. It is
> the engine that failed, not the architecture. Candidate replacements: an Apify
> Instagram actor (the strongest category on that platform), or dropping social
> entirely if the open web keeps outperforming it — all four verified leads to date
> came from podcast directories and awards lists, and none from social.
>
> Revisit only with a tested engine behind it.

**Status:** BLOCKED — engine unproven · spec retained for the architecture
**Engine:** ~~[Agent Reach](https://github.com/Panniantong/agent-reach) (MIT, v1.6.0)~~ — tested 23 Oct, insufficient
**Runs:** Thursday 11:45 · offset from the cloud task's Monday run
**Destination:** Airtable · AMA Intelligence Engine `appzY3Dz4lfMHtcMU` · GLOBAL_LEADS `tblRCmhB7YMrdQvrZ`

---

## Why this one has to be local

The cloud task has web search, web fetch and Jina Reader. It cannot see inside Instagram,
private Facebook groups, the LinkedIn feed, or X beyond public pages. Every past run said
so, correctly.

Agent Reach closes that gap by reusing the Chrome session already signed in on the Mac.
Cookies stay local — the project has a dedicated test suite for that boundary
(`test_cookie_security.py`, `test_scrub_credentials.py`, `test_home_isolation.py`,
`test_doctor_credential_boundaries.py`) and a security hardening pass merged July 2026.

It cannot be created from a cloud session: all eight environments on the account are
`anthropic_cloud`, and `create_trigger` takes no device-binding parameter.

---

## Step 1 — install Agent Reach on the Mac

In Claude Desktop, in a normal conversation (not a scheduled task):

```
Install Agent Reach for me:
https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md
```

Then configure the two channels that matter here. Tell the agent:

```
Set up Instagram and Facebook for Agent Reach
```

Both route through OpenCLI, which reuses the existing Chrome login. You will not be asked
for passwords, and nothing is uploaded.

**Verify before going further:**

```bash
agent-reach doctor
```

Instagram and Facebook must report working. The doctor is deliberately strict — it refuses
to claim a channel works merely because it is configured, which is the behaviour we want.
If it says `off` or `warn`, the scheduled task will not work either. Fix it here, not later.

**What each channel gives you:**

| Channel | Capability |
|---|---|
| Instagram | user search, profile, recent posts, Explore |
| Facebook | search, pages, feed, group lists |
| Twitter/X | read tweet; search and timeline with config |
| LinkedIn | public pages only — **the monthly Apify task covers LinkedIn properly** |

---

## Step 2 — create the task

1. Claude Desktop → Scheduled tasks → **New task**
2. Name: `MAIM Social Scout`
3. Schedule: **Thursday 11:45**
4. Connectors: attach **Airtable** to the task itself. It stores its own connector list and
   inherits nothing from the account. This step has silently failed before — check it.
5. Paste the prompt below.
6. **Run once manually** and confirm rows land in GLOBAL_LEADS before trusting the schedule.

---

## The prompt

```text
You are the MAIM Social Scout. You run once a week on Major's Mac and use Agent Reach,
which reuses the Chrome session already signed in on this machine. You are the
social-platform half of the MAIM lead engine; a cloud task covers the open web each
Monday, and a monthly task covers LinkedIn.

This is a READ-AND-RECORD-ONLY task.

## Absolute limits — you are signed in, so these matter more than usual

Anything you do happens inside Major's own accounts, in public, under his name. Therefore:

- Do NOT send a message or DM to anyone.
- Do NOT request a connection, follow, unfollow, like, react, or comment.
- Do NOT join, leave, or request access to any group.
- Do NOT submit any form, reply to any thread, or post anything.
- Do NOT accept or decline anything.

Read and record. Nothing else. If a page needs an action to reveal more, stop and log it
as unreachable rather than taking the action.

## Your tools

Use Agent Reach for the social platforms:

    agent-reach read <url>
    agent-reach search <platform> "<query>"

Run `agent-reach doctor` first. If Instagram or Facebook reports anything other than
working, say so in your summary and do not pretend you covered that platform.

For ordinary websites, use Jina Reader — https://r.jina.ai/<full original URL> — which
returns clean text. LinkedIn blocks it with HTTP 999; do not retry LinkedIn.

## Who you are looking for

Caribbean diaspora and English-speaking solopreneurs who sell what they know: coaches,
consultants, creators, educators, practitioners. Hubs are the UK, Canada, the USA, the
Netherlands, Jamaica, Trinidad and Bali.

The signal is real expertise with no digital product yet — an empty Services section, a
bio promising a programme that does not exist, an audience with nothing to buy. The MAIM
line is "If you can text, you can use AI."

Exclude: people already building AI products or visibly advanced with AI (collaborators
or podcast guests, not buyers), enterprise tech buyers, and anyone who appears to be a
minor.

Spelling matters: MAIM, never MAME. The Bronx, never Bronx.

## Where to look — only where the cloud task cannot

- Instagram: Caribbean diaspora coaches, creators and practitioners. Check the bio link,
  Highlights, and whether there is anything to actually buy.
- Facebook groups Major already belongs to: Caribbean entrepreneur, diaspora business and
  coaching groups. Members who post expertise and have no offer are the target.
- X: Caribbean diaspora professional circles.

If a candidate is findable by plain public web search, leave them to Monday's run. Your
value is the platforms nothing else can reach.

## WRITE AS YOU GO

Write each candidate to Airtable the moment you finish scoring them. Never hold
candidates until the end. One candidate verified, one record written, next candidate. A
previous run was cut off by a usage limit and only the already-written records survived.

## What to record

- Name or handle
- Platform and profile URL
- Location
- What they sell today
- The specific gap you observed — quote or describe what you actually saw on screen
- Score out of 10 with a one-sentence rationale
- One suggested opening topic
- VERIFIED vs INFERRED, separated. You are opening real pages, so most should be
  verified; say so where it is not.

Up to 8 candidates scoring 6/10 or higher. Three real ones beat eight thin ones. Do not
pad and do not invent anyone.

## Where records go

Airtable:
  base:  AMA Intelligence Engine   appzY3Dz4lfMHtcMU
  table: GLOBAL_LEADS              tblRCmhB7YMrdQvrZ

Before writing anything, list existing records and skip anyone already present, matching
on name, handle or URL. Three tasks write to this table, so duplicates are a real risk.
If the table cannot be read, say so and write nothing — a missed week beats a polluted
table.

For each record:
- Name field: the person or handle
- Notes field: the structured detail above, beginning with "SOURCE: social scout (Mac)"
- Status: Todo. Do not use "New" — that option does not exist in this base.

Add anyone excluded as already-advanced-with-AI to the existing
"EXCLUSIONS — do not re-research" record rather than creating a new row.
Mark organisations clearly as ORGANISATION, not as a person to DM.

Do NOT save to a local folder. Do NOT save only to a project document. Do NOT write any
named person to a Git repository — both MAIM repositories are public, and a list of named
individuals scored as sales prospects must never be published.

## Also each week

One group, community or account worth a partnership approach, with its public contact
route. An organisation reaches many people at once and is warmer than a cold DM; these
have historically been the most valuable findings.

One content angle drawn from what you actually saw this run, not from a template.

## End with

CANDIDATES FOUND: X
CANDIDATES WRITTEN TO AIRTABLE: X
DUPLICATES SKIPPED: X
AGENT REACH DOCTOR: [which channels reported working]
PLATFORMS REACHED THIS RUN: [list]
PLATFORMS STILL UNREACHABLE: [list, with why]
PARTNERSHIP TARGET: [one + contact route]
CONTENT ANGLE: [one line]
MOST USEFUL NEXT HUMAN ACTION: [one sentence]

If you were cut short before this block, that is acceptable — provided every candidate you
scored was already written to Airtable as you went.
```

---

## Before trusting the schedule

1. `agent-reach doctor` — Instagram and Facebook report working
2. Fire the task manually once
3. Open GLOBAL_LEADS and confirm rows tagged `SOURCE: social scout (Mac)`
4. Only then leave it on the schedule

A task nobody has watched reach its destination is not yet a working task.

---

## Cookie hygiene

Agent Reach reads browser cookies for Instagram and Facebook. Worth a clean-out first:
Chrome → Settings → Privacy → Third-party cookies → See all site data. Keep the sites you
actually use signed in, clear the rest. Fewer cookies means a smaller surface for anything
reading them, this tool included.
