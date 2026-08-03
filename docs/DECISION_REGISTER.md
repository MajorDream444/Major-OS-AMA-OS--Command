# MAIM Decision Register

Settled decisions. **Do not re-debate an entry marked `SETTLED`** — if you believe
one is wrong, raise it with Major and change the entry. Silent divergence from this
register is the failure mode it exists to prevent.

Three environments read this: ChatGPT (strategy), Claude Code (engineering), Codex
(deployment). Chief Architect: Major.

| ID | Decision | Status |
|---|---|---|
| [D-01](#d-01) | Everything in MAIM's scope ships under MAIM branding | SETTLED |
| [D-02](#d-02) | It is always *The Bronx* | SETTLED |
| [D-03](#d-03) | Launch with the existing welcome film; re-cut later | SETTLED |
| [D-04](#d-04) | No archetypes in v1 | SETTLED |
| [D-05](#d-05) | One diagnostic engine, two skins | SETTLED |
| [D-06](#d-06) | Email is the canonical identity | SETTLED |
| [D-07](#d-07) | No MAIM journey terminates on an external platform | SETTLED |
| [D-08](#d-08) | Vercel is the production host | SETTLED |
| [D-09](#d-09) | `Major-AI-OS` is canonical; consolidate after launch | SETTLED |
| [D-10](#d-10) | One logo asset, applied by script | SETTLED |
| [D-11](#d-11) | Page sources are fragments; never deploy them directly | SETTLED |
| [D-12](#d-12) | Launch, then improve | SETTLED |
| [D-13](#d-13) | Ownership split across the three environments | SETTLED |
| [D-14](#d-14) | Palette approved as shipped; hexes reconciled later | PROVISIONAL |

---

### D-01
**Everything touching education, mindset, AI literacy, or legacy ships under MAIM
branding.** Older material predates the brand lock and is migrated on contact, not
extended. Pre-brand versions are archived under `maim/archive/`, never deleted.

*Applied:* the 10 Pillars funnel was rebuilt from Syne/navy into the MAIM system.
The Caribbean/diaspora substance was kept — it is Major's story and the spine of the
Pillars. Only the visual identity and framing changed.

### D-02
**It is always "The Bronx" / "The South Bronx".** Never the bare noun. Applies to
every surface, forever.

### D-03
**Launch with the existing 4:34 film** at <https://youtu.be/OZ10QdrUxl8>, embedded
inline. The re-cut (color grade, B-roll, motion graphics) is post-launch. A re-cut
produces zero new visitors and delays the only thing that does.

### D-04
**Ship no archetypes in v1.** Ten Pillars against four named archetypes left six
Pillars with no result. The quiz returns the plain shape instead: *your strongest
Pillar · your next lesson · recommended action*. Naming all ten is post-launch, if
ever.

### D-05
**One diagnostic instrument, two presentation skins** — never two assessments.
Trust-first door asks *"What is creating pressure in your life or work?"*;
direct-response door asks *"Which Pillar needs your attention first?"* Same signals,
same data model, same member record. Spec: `MAIM_DIAGNOSTIC_ENGINE.md`.

### D-06
**Email is the primary key**, normalized lowercase. One email is one person across
every door, product, and system. Gumroad processes transactions; **Gumroad is not
the customer database.** MAIM owns the relationship. Schema:
`MAIM_MEMBER_RECORD.md`.

### D-07
**No MAIM journey should terminate on an external platform.** External tools may
process payments, email, video, or community activity — every meaningful journey
loops back into MAIM. This is why `/return` exists.

### D-08
**Vercel.** CLI already authenticated as `majorprimeos`. Config committed at
`vercel.json`.

### D-09
**`MajorDream444/Major-AI-OS` is the long-term canonical repository**, with the site
living at `apps/maim-site/`. The implementation currently lives in
`MajorDream444/Major-OS-AMA-OS--Command` because that is where the build session had
write access. **Consolidation happens after launch, not during.** Moving a working
build hours before going live trades a real launch for a tidy tree.

### D-10
**One logo asset, applied by script.** `maim/assets/md-medallion.png` is the real
seal and always wins; `md-medallion.svg` is a drawn stand-in used only until the PNG
lands. `apply-logo.py` inlines it as a data URI everywhere. Never hand-edit a
medallion into a page — that is what caused six divergent copies.

### D-11
**The page sources in `maim/` are Claude Artifact fragments** — they open with
`<title>` and carry no `<head>`. That is correct for Artifacts, which inject a
document skeleton. **Serving them raw has no charset and no viewport meta, so mobile
renders at desktop width.** `maim/build.py` wraps them into real documents.
Deploy `maim/dist/`, never `maim/`.

### D-12
**Launch, then improve.** One excellent home page, one welcome film, one lead
magnet, one product, one community CTA. Known debt is shipped knowingly and tracked
in `LAUNCH_CHECKLIST.md`, not silently.

### D-13
| Environment | Owns |
|---|---|
| ChatGPT | Strategy, architecture, doctrine, brand, curriculum |
| Claude Code | HTML, docs, engineering, repositories, PRs |
| Codex | Vercel, domain, DNS, environment, deployment, production QA |
| Major | Brand assets, accounts, and every decision in this register |

Deployment, DNS, payment verification, and production QA are still engineering —
a different layer, the same seriousness.

### D-14 — PROVISIONAL
**Palette approved as shipped:** gold `#C9931A`, green `#1F8A4C`, blue `#2A78D6`,
orange `#E07A2F`, red `#C94040`, ground `#111111`, text `#F0EDE5`.

Provisional because these were sampled from the brand graphic, not read from the
Visual Identity Guide, which has never reached the repo. Doctrine names *Jamaican
green* and *Knicks blue/orange*, which may differ. Major has approved the shipped
values on sight; reconciliation is post-launch and non-blocking.

---

## Open — not yet decided

| Question | Needs |
|---|---|
| Does the Studio eventually own checkout, replacing Gumroad? | Major |
| Where does the canonical member record physically live? Airtable is the stated Operations DB. | Major |
| Full tagline — *"Likkle by likkle, we build the future"* appears on `/return` only; other pages carry the short form. | Major |
| Refund / chargeback handling against `purchase_status` | post-launch |
