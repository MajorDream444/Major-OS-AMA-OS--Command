# Codex Handoff — Deploy MAIM

**Mission:** connect the verified implementation candidate to Vercel and point
`majoraimindset.com` at it.

Your blocker was identifying the deployable source of truth. This document is that
identification. **The deployment files are not in `Major-AI-OS`.** They were never
pushed there — the build session only had write access to the Command repo.

---

## The candidate

```
Repository   https://github.com/MajorDream444/Major-OS-AMA-OS--Command
Branch       claude/maim-ecosystem-wireframe-xk8swp
Commit       83e3f9aeaba539cad1c47a8ec3fb564a69ab0843
App root     repository root (vercel.json lives there)
Build        python3 maim/build.py
Output       maim/dist
```

Local HEAD equals `origin/<branch>` — nothing is sitting unpushed. The branch is
9 commits ahead of `origin/main` in that repo and has **no open PR**.

### Files that must be present

| Path | Purpose |
|---|---|
| `vercel.json` | build command, output dir, `cleanUrls`, headers, redirects |
| `maim/build.py` | wraps page fragments into real documents |
| `maim/apply-logo.py` | inlines the medallion across all pages |
| `maim/assets/md-medallion.svg` | drawn stand-in until the real PNG lands |
| `maim/majoraimindset_front_door.html` | `/` |
| `maim/MAIM_Funnel_Landing_Page.html` | `/pillars` |
| `maim/return.html` | `/return` |

If any are missing, you are on the wrong branch or the wrong repository.

---

## Verification already performed

A clean shallow clone of the pushed branch was built from scratch. Result:

```
$ git clone --branch claude/maim-ecosystem-wireframe-xk8swp --depth 1 <repo>
$ python3 maim/build.py
  majoraimindset_front_door.html -> dist/index.html   (/)
  MAIM_Funnel_Landing_Page.html  -> dist/pillars.html (/pillars)
  return.html                    -> dist/return.html  (/return)
Built 3 pages + robots.txt + sitemap.xml into maim/dist/
```

`maim/dist/` contained: `index.html` `pillars.html` `return.html` `favicon.svg`
`robots.txt` `sitemap.xml`. No build dependencies beyond Python 3 — no npm install,
no lockfile, no node_modules.

Reproduce it before linking. If your build differs from the above, stop.

---

## Which repository to deploy from

**Deploy from the Command repo now. Consolidate into `Major-AI-OS` after launch.**
(Decision D-09.)

Moving a verified build hours before launch trades a real launch for a tidy tree.
Vercel's git source can be repointed later with no downtime — the domain stays put
while the backing repo changes.

If Major overrides and wants the port done first, it is a file copy, not a rewrite:

```bash
# in a checkout of Major-AI-OS, on a fresh branch off origin/main
mkdir -p apps/maim-site
cp -r <command-repo>/maim apps/maim-site/
cp    <command-repo>/vercel.json apps/maim-site/
# then edit apps/maim-site/vercel.json:
#   buildCommand    -> "python3 maim/build.py"   (unchanged; run with Root Directory set)
# and set Vercel's Root Directory to apps/maim-site
python3 apps/maim-site/maim/build.py   # verify before pushing
```

Note the local checkout at `/Users/majordreamwilliams/Desktop/Major-AI-OS` is on
`docs/hamal-ecosystem-boundary` and behind. Fetch and branch from `origin/main`
(`5804d19`) before doing anything there.

---

## Steps

1. **Link.** Vercel project → import `Major-OS-AMA-OS--Command`, production branch
   `claude/maim-ecosystem-wireframe-xk8swp`.
   - Framework preset: **Other**
   - Build command: `python3 maim/build.py`
   - Output directory: `maim/dist`
   - Install command: leave empty
   - `vercel.json` already declares all of this; confirm the dashboard agrees.
2. **Preview deploy.** Must be green before touching DNS.
3. **Verify the three routes** on the preview URL: `/`, `/pillars`, `/return`.
   Also `/return?product=emerald_awakening` — the confirmation line, shelf, and form
   selection should change.
4. **Mobile check at 375px.** This is the specific thing that would have broken
   before `build.py` existed; confirm no horizontal scroll and a legible hero.
5. **Domain.** Point `majoraimindset.com` at the project. Pick apex or `www` and
   redirect the other. Confirm SSL issues.
6. **Production deploy.**
7. **Hand back to Major** for the Gumroad redirects and the live purchase test.

---

## Not your blockers, but they gate "launch complete"

| Item | Owner |
|---|---|
| `maim/assets/md-medallion.png` — real seal. Until it lands, favicon and all three pages use a drawn stand-in. Once committed: `python3 maim/apply-logo.py && python3 maim/build.py` | Major |
| Gumroad post-purchase redirects to `/return?product=…` (three URL fields, no code) | Major |
| End-to-end purchase test — card through to email delivery | Major |

Full list: `LAUNCH_CHECKLIST.md`. Settled decisions: `DECISION_REGISTER.md`.

---

## Rollback

Vercel retains every deployment. If production breaks, promote the previous
deployment from the dashboard — instant, no code change.
