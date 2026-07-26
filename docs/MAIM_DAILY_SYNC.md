# MAIM Daily Sync

Shared operating picture across three execution environments. They cannot talk to
each other — this file is the handoff. **Read it at the start of a session, update
it at the end.**

| Environment | Owns |
|---|---|
| ChatGPT | Strategy, architecture, doctrine, brand, curriculum |
| Claude Code | Repositories, engineering, documentation, PRs |
| Codex | Application development, UI, testing, deployment |

Supporting: GitHub (source of truth) · Claude Design (visual factory) · Airtable (production tracking) · Google Drive (final assets)

Chief Architect: Major. Doctrine, product architecture, and UX decisions escalate to him.

## The five questions

Every session opens with these:

1. What repository are you working in?
2. What branch or PR is active?
3. What was completed since the last sync?
4. What is today's objective?
5. What blockers or decisions need alignment?

---

# Current sync

**Objective: public launch within 24 hours.** Everything is measured against one
question — *does this help us launch?* If not, it goes to the post-launch backlog.

**Definition of done:** someone can discover MAIM, understand it in 30 seconds,
watch the welcome film, join the community, and buy something.

## State

- Repo: `MajorDream444/Major-OS-AMA-OS--Command`
- Branch: `claude/maim-ecosystem-wireframe-xk8swp`
- Open PRs: none
- Deployed: **nothing** — no host, no domain wired

## Launch-critical board

| # | Task | Owner | State |
|---|---|---|---|
| 1 | Hosting + DNS for `majoraimindset.com` | Major / Codex | **blocked — no account access** |
| 2 | Front-door email capture → Kit endpoint | Claude Code | open |
| 3 | Embed welcome film inline (currently a link) | Claude Code | open |
| 4 | Purchase path from front door → tiers | Claude Code | open |
| 5 | Real MD medallion PNG → `maim/assets/md-medallion.png` | Major | **blocked — asset not delivered** |
| 6 | Mobile pass on both pages | Codex | open |

## Post-launch backlog — explicitly NOT in the 24h scope

- Welcome film re-cut (color grade, B-roll, motion graphics). A finished 4:34 film
  already exists at <https://youtu.be/OZ10QdrUxl8>. Embed it; re-cut later.
- Guide PDF and Pillar Scroll book rebuilt in MAIM branding
- Merging the Pressure Test and "Which Pillar Are You?" into one instrument
- Studio-owned checkout (tiers currently sell off-campus on Gumroad)

## Open decisions — need Major

1. **Canonical brand hexes.** Doctrine says *Jamaican green* and *Knicks blue/orange*.
   Implemented palette was sampled from the brand graphic: gold `#C9931A`, green
   `#1F8A4C`, blue `#2A78D6`, orange `#E07A2F`, red `#C94040`. These may not match
   the Visual Identity Guide, which has not reached the repo. **If they differ, every
   page needs a correction pass.**
2. **Tagline.** Doctrine says *"Likkle by likkle, we build the future."* Pages
   currently carry only *"likkle by likkle."* Confirm the full line.
3. **One Crown hat** is named in the doctrine but is not present in any built asset.
4. **Post-purchase landing.** A $97 buyer currently receives a Gumroad download, not
   a Studio account. Biggest structural break in the campus.

## Assets not yet in the repo

These have been referenced but never landed on disk. Attach as **file paths**, not
inline images — inline chat images cannot be read as files.

- `MD medallion` PNG (gold seal, woven palm crown)
- `MAIM Visual Identity Guide.txt`
- `MAIM Welcome Video Ideas.txt`
- `Instagram Branding Advice.txt`
- Portrait of Major (for the Meet Major panel)

---

# Sync template

Copy this block, fill it, append above the previous entry.

```
## Sync — YYYY-MM-DD · <environment>

1. Repository:
2. Branch / PR:
3. Completed since last sync:
4. Today's objective:
5. Blockers / decisions needed:
6. Recommended next commit:
7. Estimated time to launch-ready:
```
