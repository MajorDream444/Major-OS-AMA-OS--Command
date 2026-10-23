# Major Moves — alignment table and sync packet

**Date:** 23 October 2026
**Responding to:** `MAIM_Major_Moves_Claude_Code_Handover_2026-10-23.md`
**Owner:** Major Dream Williams · **Writing:** Claude Code · **Ecosystem:** Codex

---

## 1 · Session report

| | |
|---|---|
| Working directory | `/home/user/Major-OS-AMA-OS--Command` (cloud container) |
| Repository | `MajorDream444/Major-OS-AMA-OS--Command` |
| Branch | `claude/maim-ecosystem-wireframe-xk8swp` |
| HEAD | `ad2556b` |
| Uncommitted | none |
| Second checkout | `/home/user/major-ai-os` · `main` · `33e3334` · 3 untracked mirrors |
| Series repo | `major-moves-series` cloned read-only: **6 files, scaffold only, no manuscripts** |

Instructions read: `AGENTS.md` (Command), series `README.md`, `MAJOR_MOVES_OS.md`,
`docs/STYLE_GUIDE.md`, `VOLUME_01_PRODUCTION_KIT.md`,
`MAJOR-AUTHOR-VOICE-PROTOCOL.md` (via the publishing skill).

---

## 2 · Alignment table

| Field | Value |
|---|---|
| **book_id** | `MM-BOOK-001` *(proposed convention, not a Stripe SKU)* |
| **collection** | Major Moves Series |
| **working title** | Major Moves Series — *You Are the System* · Volume One |
| **audience** | Adult. Founders, solo operators and practitioners who are load-bearing in their own business. Not a youth edition; no adult material adapted downward. |
| **visual_seed_id** | **Bottleneck** — direct, not inferred. Chapter 1 is "The Hidden Bottleneck"; the epigraph defines the word literally. Adjacent seeds *Overloaded*, *Fire Fighter*, *Leak* and *Machine* are thematically present but **OPEN** — not claimed as mappings. |
| **core idea** | A bottleneck is not a flaw in your effort, it is a feature of your architecture. Busy is not the same as load-bearing. |
| **manuscript path** | `docs/publishing/VOLUME_01_MANUSCRIPT_DRAFT_v1.md` |
| **version** | v1, approved by Major 23 Oct 2026 |
| **export path** | `build/You-Are-the-System_review-proof.pdf` — 28 pp, 6×9, review proof |
| **builder** | `scripts/build_interior.py` |
| **state** | `author review` → **approved** · export built · **delivery not tested, not released** |
| **word count** | ≈ 7,900 words · 28 pages set (series spec: 25–40 ✓) |
| **pillar mapping** | **OPEN.** `MAIM_10_Pillars` is outside this session's repository scope and was not read. No pillar is claimed without its canonical definition in hand. |
| **Academy mapping** | **OPEN and deliberately unclaimed** — see §4. |
| **assets / rights** | `assets/brand/` — mark and portrait supplied by Major 23 Oct, hashed in `supplied-assets.json`, placed unaltered but for proportionate scaling. Owner-supplied re-exports, **not** the v0.4 archival originals. |
| **cover** | **BLOCKED** on `integrity-cover-update-v0.4/assets/`. Front *and* back required; no ISBN, spine or print spec invented. |
| **factual-claim review** | No income, investment, health or learning outcome is promised anywhere in the manuscript. |
| **next action** | Author decisions in §5, then the CTA block. |
| **owner** | Major (authorial truth) · Claude Code (manuscript) |
| **updated_at** | 2026-10-23 |

### Naming conflicts

**None found — the opposite.** The series `STYLE_GUIDE.md` phrase bank already contains:

> *"If everything stops when you stop, you are the system."*

The manuscript's title and core question are a direct build of that canonical line, written
before this session read the style guide. Also adjacent: *"Build systems, not pressure"*
against Chapter 4, *"Build Systems, Not Heroics."*

The series README's *"The image is the door. The book is the doctrine"* describes this
relationship exactly: **Bottleneck** is the door; `MM-BOOK-001` is the doctrine.

### Source inventory — what exists, where

| Item | Path | Status |
|---|---|---|
| Manuscript v1 | `docs/publishing/VOLUME_01_MANUSCRIPT_DRAFT_v1.md` | approved |
| Production kit | `docs/publishing/VOLUME_01_PRODUCTION_KIT.md` | scaffolding, all slots now sourced |
| Intake — Volume 1 | `docs/publishing/MAJOR_VOICE_VOLUME_01_INTAKE.md` | 23 Oct recording |
| Intake — Awareness | `knowledge/voice/MAJOR_VOICE_AWARENESS_INTAKE.md` | 14 Oct |
| Intake — Puerto Rico | `knowledge/voice/MAJOR_VOICE_PUERTO_RICO.md` | 14 Oct |
| Gap analysis | `docs/publishing/VOLUME_01_INTAKE_GAP_2026-10-23.md` | all 10 questions closed |
| Interior builder | `scripts/build_interior.py` | working |
| Brand assets | `assets/brand/` + `supplied-assets.json` | registered |

**No other Major Moves manuscripts exist**, in any checkout. `MM-BOOK-001` is the first and
currently only book in the collection. `major-moves-series` holds no manuscripts at all —
its own README still reads *"System initialized."*

---

## 3 · Sync packet

```
COLLECTION / BOOK      Major Moves Series / MM-BOOK-001
MANUSCRIPT VERSION     v1 — approved by Major, 23 Oct 2026
REPOSITORY             MajorDream444/Major-OS-AMA-OS--Command
BRANCH                 claude/maim-ecosystem-wireframe-xk8swp
COMMIT                 ad2556b

CHANGED PATHS
  docs/publishing/VOLUME_01_MANUSCRIPT_DRAFT_v1.md      manuscript, approved
  docs/publishing/MAJOR_VOICE_VOLUME_01_INTAKE.md       intake extract
  docs/publishing/VOLUME_01_INTAKE_GAP_2026-10-23.md    gap analysis
  knowledge/voice/MAJOR_VOICE_AWARENESS_INTAKE.md       intake extract
  knowledge/voice/MAJOR_VOICE_PUERTO_RICO.md            intake extract
  scripts/build_interior.py                             6x9 typesetter
  build/You-Are-the-System_review-proof.pdf             28pp export
  assets/brand/ + supplied-assets.json                  mark, portrait, hashes
  .claude/skills/{maim-integrity-publishing-design,ebook-publishing,
                  marketing-psychology,copywriting,launch,emails,pricing}

SOURCES USED
  Three Fathom intake recordings, 14 and 23 Oct 2026 — Major's own words
  Startup Qatar Founder Profile — Major's own document, used for the bio only
  Series STYLE_GUIDE.md phrase bank, MAJOR_MOVES_OS.md 1:12 ratio

MISSING SOURCES
  integrity-cover-update-v0.4/assets/      blocks covers
  MAIM_10_Pillars repo                     outside scope; blocks pillar mapping
  MAIMACADEMY FOUNDING-OFFER / COHORT      not read; see §4

CLAIM / RIGHTS ISSUES
  Brand assets are owner-supplied re-exports, hash-registered as such, not
  represented as v0.4 originals. No ISBN, spine or print spec invented. No
  outcome promised. The US$81m AUM figure in Major's founder profile was
  deliberately omitted from the book bio — reversible on his word.

MAJOR'S DECISIONS
  2026-10-23  Approved manuscript v1. Scope: the manuscript as it stands.
  2026-10-23  NOT approved: the passage about his mother, deliberately unused
              and still requiring separate explicit sign-off.
  2026-10-23  Supplied mark, crown variants and author portrait for use.

PROPOSED ECOSYSTEM MAPPINGS  (proposals, not decisions)
  visual seed Bottleneck -> MM-BOOK-001 -> Dependency Score -> First AI Employee
  Pillar mapping: OPEN
  Academy mapping: OPEN — see section 4

FINISHED      manuscript, author approval, interior export, brand placement
DRAFT         CTA block (placeholder links), back-cover copy
NOT STARTED   covers, EPUB, delivery, release

NEXT THREE ACTIONS
  1. Author decisions in section 5
  2. Write the CTA block, Academy-safe
  3. Covers on arrival of the v0.4 asset folder
```

---

## 4 · The Academy boundary — why the CTA is still blank

The handover is explicit: the 30-Day Journey's inclusions are **program** inclusions,
*"never default book bonuses,"* and *"the book price is not US$249 by association."*

The book currently ends with a placeholder CTA. It is staying blank rather than being
filled with something plausible, because the obvious move — *buy the book, join the cohort*
— is precisely the accidental promise the handover warns against. A reader who finishes
Chapter 5 and is told to "join the Academy" will reasonably believe the book bought them
something.

Nor is checkout, booking, progress tracking or replay delivery assumed operational. None
was verified here, and production commerce remains disabled.

So the CTA needs an author decision, not a writer's guess.

---

## 5 · Author questions — three, as the protocol allows

**1 · What does the back of the book actually point to?**
Three clean options, no wrong answer:
  **(a)** the free guide and the letter — no money, builds the list, safest;
  **(b)** the Academy as a clearly separate paid step, stated plainly as not included;
  **(c)** nothing but the Try This Today action, and the book simply ends.
My recommendation is **(a)**, with (b) named once as a next step for people who want it.

**2 · Is the title final, and does it carry the collection prefix?**
Cover and metadata need *Major Moves Series — You Are the System*, or just
*You Are the System*. Title shown on the proof's title page is the latter.

**3 · Is `Bottleneck` the official seed for this book?**
It is an exact thematic match and the style guide's phrase bank already carries the line.
Confirming it locks the seed→book mapping for the 1:12 asset chain. If a different seed is
intended, say which and the mapping updates rather than the manuscript.

---

## 6 · Unresolved

- Pillar mapping stays **OPEN** until `MAIM_10_Pillars` is readable from this session.
- Covers blocked on one folder from the Integrity transfer, which blocks two tracks at once.
- `major-moves-series` has no manuscripts; whether `MM-BOOK-001` moves there is a repository
  decision for Major. This session has read-only access to it.
- Pricing remains an unlabelled proposal. No Stripe object exists or should be created.
