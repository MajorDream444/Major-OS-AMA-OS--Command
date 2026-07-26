# MAIM — Major AI Mindset

Product asset registry for `majoraimindset.com`. Reference layer for all MAIM builds in this repo.

## Brand Canon

- Ground: `#111111` (near-black). Text: `#F0EDE5` warm off-white.
- ABC colors: A = gold `#C9931A` · B = green `#1F8A4C` · C = blue `#2A78D6` · D = orange `#E07A2F` · E = red `#C94040`.
- Motifs: camera viewfinder bracket corners, MD gold medallion with woven palm crown, three-color ABC stripe.
- Type: condensed black display (uppercase), Georgia italic serif for Major's voice/quotes, monospace for labels.
- Taglines: "ONE LETTER. ONE LESSON. ONE ACTION." · "Understand your mind. Activate your intelligence. Build your legacy."
- Handle: `@major_ai_mindset` · Domain: `majoraimindset.com`
- Style rule: it is always **The Bronx** / **The South Bronx** — never "Bronx" bare.

## Welcome Film

- YouTube: https://youtu.be/OZ10QdrUxl8 · Runtime 4:34
- Opening question (the thesis): "What becomes possible when you finally understand your own mind and you learn how to use artificial intelligence without surrendering your own intelligence?"
- Key creative decision: **Major is the hero; AI is the amplifier.**
- Origin path: The South Bronx → Mount Vernon → basketball → finance → wellness → technology → blockchain → business → travel.
- ABC foundations (Major's words): Awareness "helps you recognize what's happening" · Belief "allows you to see what is possible" · Context "helps you ask better questions, understand your environment, and make better decisions." Then: information → direction → execution.
- Closer: "The future does not belong to only the people with the most technology. It belongs to the people who understand what to do with it."

## Branding Policy — single system

**Anything touching education, mindset, AI literacy, or legacy ships under MAIM branding.** No exceptions unless a piece is explicitly scoped otherwise in writing.

Older material predates the brand lock and gets migrated on contact — do not extend a legacy visual system, port it. When you rebrand something:

- Keep the substance. The Caribbean/diaspora content is Major's actual story and the spine of the 10 Pillars ("brain drain becomes brain circulation," ancestors as council / descendants as responsibility). Migrate the visual identity and framing, not the ideas.
- Drop webfont CDN links — artifacts block them. Use the system stack: `Arial Narrow` (display), `Georgia` (body + Major's voice), `Courier New` (labels/data).
- Archive the pre-brand version under `archive/` rather than deleting it.

### How the two frameworks relate

The **A–Z / ABC** is the on-ramp — one letter, one lesson, one action. The **10 Pillars** are the architecture underneath it. Same brand, two depths. Pages should state that relationship rather than presenting them as separate products.

Color carries tier access on Pillar layouts: Foundation (01–03, in Tier 1) uses live ABC colors gold/green/blue; the full architecture (04–10) renders muted until Tier 2 unlocks it.

## The 10 Pillars

| # | Pillar | Principle |
|---|---|---|
| 01 | Diaspora Empowerment | Build sovereign communities of creators, not consumers |
| 02 | Mindset Shift & Resilience | Turn adversity into strategic greatness |
| 03 | Gamified Education | Make learning irresistible and addictive |
| 04 | Blockchain & Decentralization | Restore ownership, remove middlemen |
| 05 | Community & Collaboration | Move as crews, tribes, DAOs — not individuals |
| 06 | Localized AI & Personalization | Tech that speaks the people's language and rhythms |
| 07 | Holistic Wellness & Balance | Protect mind, body, spirit while scaling |
| 08 | Security & Compliance | Guard sovereignty digitally and legally |
| 09 | Data-Driven Performance | Track what matters, grow what matters |
| 10 | Legacy & Long-Term Impact | Build 100-year dynasties, not 1-year hype |

Tier ladder: **$27** The Pillar Scroll (Pillars 01–03 deep dive) → **$97** Emerald Awakening (all 10) → **$297** The Pillar Code Vault (lifetime, Dynasty). Sold via `majordream.gumroad.com`; guide opt-in posts to `maim-the-10-pillars.kit.com`.

## Files

| File | What it is |
|---|---|
| `majoraimindset_front_door.html` | Public front-door screen built from the welcome-film transcript |
| `MAIM_Funnel_Landing_Page.html` | The 10 Pillars funnel in MAIM branding: guide opt-in → 5 Moves → Pillar architecture → quiz → tiers |
| `assets/MAIM_Free_Guide_5_AI_Moves.pdf` | Lead magnet: the 5 Moves (still pre-brand — needs redesign) |
| `assets/MAIM_Pillar_Scroll_Book.pdf` | Tier 1 product: the 10 Pillars book (still pre-brand — needs redesign) |
| `archive/` | Pre-brand versions, kept for reference only. Do not extend. |

Related in repo root: `MAIM Ecosystem Wireframe.dc.html` (Claude Design wireframe) + `support.js` (dc runtime).

## Migration backlog

- [x] Funnel landing page → MAIM branding
- [ ] `MAIM_Free_Guide_5_AI_Moves.pdf` → rebuild in MAIM system
- [ ] `MAIM_Pillar_Scroll_Book.pdf` → rebuild in MAIM system
- [ ] Swap SVG medallion for the real gold/palm-crown PNG once the asset lands in `assets/`
- [ ] Gumroad product pages + quiz to match
