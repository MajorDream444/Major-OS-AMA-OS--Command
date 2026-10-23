# MAIM LinkedIn Scout — monthly Apify task

**Status:** spec'd, not yet created · needs `APIFY_TOKEN` in environment secrets first
**Runs:** monthly · deliberately low frequency to live inside the $5 free credit
**Destination:** Airtable · AMA Intelligence Engine `appzY3Dz4lfMHtcMU` · GLOBAL_LEADS `tblRCmhB7YMrdQvrZ`

---

## Why Apify, and only for LinkedIn

LinkedIn is the one platform where every free route fails, and this was tested rather than
assumed:

| Route | Result |
|---|---|
| Jina Reader (`r.jina.ai`) | **HTTP 999** — LinkedIn anti-bot block, verified 23 Oct |
| Cloud web fetch | same block |
| Agent Reach LinkedIn channel | public pages only; full profiles need `linkedin-scraper-mcp` running as a local server |
| Apify LinkedIn actor | works, costs credits |

Everything else — Instagram, Facebook, X, ordinary websites, podcast directories — is
covered free by Agent Reach on the Mac or Jina Reader in the cloud. **Apify is bought for
LinkedIn alone.** Do not route other platforms through it; that spends credit on things
already solved.

This matters because LinkedIn is where the ICP actually is. Of the four leads recorded on
22 Oct, three came from LinkedIn or a LinkedIn-adjacent source, and the strongest signal
in the whole profile — an empty Services section — is a LinkedIn-specific observation.

---

## Before creating the task

### 1. Put the token in environment secrets, never in chat

Environment **Major Prime OS** (`env_0126NNocsUo6ttPrCiAaTVgd`) → Environment variables →

```
APIFY_TOKEN = <the token from the dedicated LinkedIn Apify account>
```

A token pasted into a conversation is a token that has to be rotated. This has already
happened once. Secrets go in the environment; the task reads them without them ever
passing through a message.

### 2. Choose the actor

Pick one LinkedIn actor in the Apify console and note its actor ID. Two things to check
before committing to it:

- **Does it use its own proxies, or your LinkedIn session?** Prefer its own. An actor that
  wants your cookies puts your personal LinkedIn account at risk of restriction. The whole
  point of paying is to keep that risk off your account.
- **What does one run cost?** Note the per-run or per-1000-results price. The budget below
  depends on it.

### 3. Budget

$5 of free credit, one run a month. Set `maxItems` on the actor input so a single run
cannot drain the balance — a cap of 50–100 profiles is plenty at eight qualified leads a
month. Check the console's usage page after the first run and adjust.

---

## Creating the task

Cloud scheduled task, environment **Major Prime OS**, monthly — first Monday, 11:45
Makassar, so it does not collide with the weekly runs.

Connectors: **Airtable** attached to the task itself.

### The prompt

```text
You are the MAIM LinkedIn Scout. You run once a month. You are the LinkedIn half of the
MAIM lead engine — a weekly cloud task covers the open web, and a weekly Mac task covers
Instagram and Facebook. LinkedIn is yours alone.

This is a READ-AND-RECORD-ONLY task. Do not send outreach, do not message anyone, do not
request a connection, do not submit any form, do not post anything.

## Budget discipline — read this first

This task spends real money from a small balance. One run per month, and the balance is
about $5. Therefore:

- Run the actor ONCE. If the first run returns usable data, do not run it again this month.
- Set a result cap on the actor input (50-100 profiles). Never run uncapped.
- If a run fails, report the failure and STOP. Do not retry in a loop — a retry loop on a
  paid API is how a month's budget disappears in ten minutes.
- Before finishing, report what the run cost if the API tells you.

## How to call Apify

The token is in the environment as APIFY_TOKEN. Never print it, never write it to a file,
never include it in your summary.

    curl -sS -X POST \
      "https://api.apify.com/v2/acts/<ACTOR_ID>/run-sync-get-dataset-items?token=$APIFY_TOKEN" \
      -H 'Content-Type: application/json' \
      -d '{ ...actor input, including a result cap... }'

## Who you are looking for

Caribbean diaspora and English-speaking solopreneurs who sell what they know: coaches,
consultants, creators, educators, practitioners. Hubs are the UK, Canada, the USA, the
Netherlands, Jamaica, Trinidad and Bali.

The signal is real expertise with no digital product yet. On LinkedIn this is unusually
legible: an EMPTY SERVICES SECTION on someone who describes themselves as a coach or
consultant is the single strongest indicator in the whole profile. Look for it directly.

Also strong: a published book with nothing else to buy; a headline promising a programme
that does not exist anywhere on their profile; a large following and no offer.

Exclude: people already building AI products or visibly advanced with AI (collaborators
or podcast guests, not buyers), enterprise tech buyers, anyone who appears to be a minor.

Spelling matters: MAIM, never MAME. The Bronx, never Bronx.

## Scraped data is raw material, not leads

The actor returns rows. Rows are not qualified leads. Your job is the judgement the
scraper cannot do:

1. Pull the batch.
2. Read each row and score it 1-10 against the profile above.
3. Write ONLY those scoring 6/10 or higher — up to 8 — into GLOBAL_LEADS.
4. Discard the rest. Do not write unscored rows "to review later". A table of 100
   unqualified rows is worse than a table of 4 good ones, because nobody will read it.

Never record a person you have not actually assessed.

## WRITE AS YOU GO

Write each qualified candidate the moment you finish scoring them, not in a batch at the
end. A previous run was cut off by a usage limit and only the already-written records
survived.

## Where records go

Airtable:
  base:  AMA Intelligence Engine   appzY3Dz4lfMHtcMU
  table: GLOBAL_LEADS              tblRCmhB7YMrdQvrZ

Before writing anything, list existing records and skip anyone already present, matching
on name or URL. Three tasks write to this table. If it cannot be read, say so and write
nothing.

For each record:
- Name field: the person
- Notes field: platform, profile URL, location, what they sell, the specific gap, score +
  one-sentence rationale, suggested opening topic, and VERIFIED vs INFERRED — beginning
  with "SOURCE: LinkedIn scout (Apify)"
- Status: Todo. Do not use "New" — that option does not exist in this base.

Mark organisations clearly as ORGANISATION, not as a person to DM. Add anyone excluded as
already-advanced-with-AI to the existing "EXCLUSIONS — do not re-research" record.

Do NOT save to a local folder. Do NOT save only to a project document. Do NOT write any
named person to a Git repository — both MAIM repositories are public.

## End with

ACTOR RUN: [succeeded / failed + why]
ROWS RETURNED: X
ROWS SCORED: X
CANDIDATES WRITTEN TO AIRTABLE: X
DUPLICATES SKIPPED: X
APPROXIMATE COST OF THIS RUN: [if the API reports it]
MOST USEFUL NEXT HUMAN ACTION: [one sentence]
```

---

## Verification, first run only

1. Fire manually. Watch it reach WORKING with no init error.
2. Confirm it did **one** actor run, not several.
3. Check the Apify console usage page — know the real per-run cost before trusting a schedule.
4. Confirm rows in GLOBAL_LEADS tagged `SOURCE: LinkedIn scout (Apify)`.
5. Only then leave it monthly.

---

## Data protection

The ICP includes the UK, Canada and the Netherlands. Scraping personal data on people
there into a database engages UK GDPR and GDPR. B2B prospecting can generally run on
legitimate interest, but that basis carries obligations — being able to tell people where
their data came from, and honouring objections.

Practical version: keep the `SOURCE:` tag on every record so provenance is always
answerable, keep volume low and relevance high, and delete anyone who asks. The current
design — 8 qualified people a month, each individually assessed — sits comfortably inside
that. A 10,000-row scrape would not.

---

## The three-task picture

| Task | Cadence | Sees | Cost |
|---|---|---|---|
| Lead Engine (cloud) | Mon weekly | open web, directories, awards lists, via Jina Reader | free |
| Social Scout (Mac) | Thu weekly | Instagram, Facebook groups, X — Chrome session | free |
| **LinkedIn Scout (cloud)** | **monthly** | **LinkedIn profiles + Services sections** | **~$5/mo** |

All three dedup against GLOBAL_LEADS. All three tag their rows. Spread across Mon / Thu /
first-Monday so no two read the table at the same time.
