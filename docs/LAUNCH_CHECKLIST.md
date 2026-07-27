# MAIM Launch Checklist

Target: `majoraimindset.com` public, someone can discover → understand → watch →
join → buy.

**Owners:** Codex = deployment, DNS, production · Claude Code = HTML, docs,
engineering · Major = brand assets, accounts, decisions.

**Rule for today:** the content is done, the plumbing isn't. Nothing that improves
content ships today.

---

## Build

The page sources in `maim/` are Artifact fragments — no `<head>`. **Never deploy
them directly.** `maim/build.py` wraps them into real documents.

```
python3 maim/apply-logo.py     # once md-medallion.png exists
python3 maim/build.py          # emits maim/dist/
```

`vercel.json` runs the build and serves `maim/dist` with `cleanUrls`.

| Route | File |
|---|---|
| `/` | front door |
| `/pillars` | 10 Pillars funnel |
| `/return` | post-purchase return |

---

## PRE-LAUNCH

### Infrastructure — Codex
- [ ] Vercel project created and linked to the repo
- [ ] Build command verified (`python3 maim/build.py`, output `maim/dist`)
- [ ] Preview deploy green
- [ ] `majoraimindset.com` DNS pointed at Vercel
- [ ] `www` redirects to apex (or apex to `www` — pick one)
- [ ] SSL certificate issued and valid
- [ ] Production deploy green

### Brand assets — Major
- [ ] `maim/assets/md-medallion.png` committed
- [ ] `python3 maim/apply-logo.py` run, all 3 pages carry the real seal
- [ ] Favicon renders (build uses the medallion once present; drawn fallback until then)
- [ ] `social-preview.png` — currently falls back to the medallion. A proper 1200×630 card is better but not blocking.

### Rendering
- [ ] Mobile — 375px: no horizontal scroll, hero legible, nav usable
- [ ] Mobile — 390px / 414px
- [ ] Tablet — 768px
- [ ] Desktop — 1440px
- [ ] Welcome film plays inline on iOS Safari and Android Chrome
- [ ] Dark and light system themes both legible

### Conversion paths — the money
- [ ] Front door registration submits to Kit; **test with a real address and confirm it arrives**
- [ ] Pillars guide opt-in submits to Kit; confirm delivery
- [ ] Return page access form submits to Kit; confirm delivery
- [ ] Gumroad `$27` redirect → `/return?product=pillar_scroll`
- [ ] Gumroad `$97` redirect → `/return?product=emerald_awakening`
- [ ] Gumroad `$297` redirect → `/return?product=pillar_code_vault`
- [ ] `/return` with no `?product=` still renders correctly
- [ ] **End-to-end: buy the $27 yourself.** Card → Gumroad → return page → access form → email. This is the one test that matters most; nothing else proves the loop closes.

### Links
- [ ] Every nav and footer link resolves — no 404s
- [ ] Front door ↔ Pillars cross-links work on the live domain
- [ ] Welcome film link opens the right video
- [ ] Gumroad links open the right products

### SEO + discovery
- [x] `<title>` unique per page
- [x] `<meta name="description">` per page
- [x] Canonical URLs
- [x] Open Graph + Twitter card tags
- [x] `robots.txt`
- [x] `sitemap.xml`
- [ ] Paste each URL into WhatsApp / iMessage / Instagram DM — confirm the preview card looks right
- [ ] Submit sitemap to Google Search Console

### Analytics
- [ ] Analytics installed (Vercel Analytics is one toggle — lowest friction today)
- [ ] Confirm pageviews recording on all three routes

### Accessibility — spot check
- [x] Every page has one `<h1>`
- [x] Form inputs have associated `<label>`s
- [x] Focus states visible on buttons and links
- [x] `prefers-reduced-motion` respected
- [ ] Keyboard-only pass through the registration form
- [ ] Contrast check on muted body text against `#111`

---

## LAUNCH

- [ ] Final production deploy
- [ ] Load the live site on a phone you have never used for testing
- [ ] Walk the full journey once as a stranger would
- [ ] Announce

---

## POST-LAUNCH

### Week 1
- [ ] Watch first real Kit submissions land
- [ ] Watch first real purchase complete the return loop
- [ ] Heatmaps installed
- [ ] Analytics review — where do people drop?
- [ ] Email automation: welcome sequence after guide opt-in
- [ ] Community onboarding path defined

### Known debt — deliberately shipped
- [ ] **Repo consolidation.** The site lives in `Major-OS-AMA-OS--Command`; `Major-AI-OS` is meant to be canonical. Move to `apps/maim-site/` after launch — not during.
- [ ] **Diagnostic engine unbuilt.** Pressure Test and Pillar quiz are static mocks that collect nothing. Spec in `docs/MAIM_DIAGNOSTIC_ENGINE.md`. First post-launch build.
- [ ] **Canonical member record unbuilt.** Kit is holding identity by default today. Spec in `docs/MAIM_MEMBER_RECORD.md`.
- [ ] **Studio does not exist.** `/return` promises Studio access; the access form is the bridge standing in for it.
- [ ] **Brand hexes unverified.** Palette was sampled from the brand graphic, not the Visual Identity Guide. Doctrine names Jamaican green and Knicks blue/orange; shipped values are `#1F8A4C`, `#2A78D6`, `#E07A2F`. Reconcile post-launch.
- [ ] Guide PDF and Pillar Scroll book still pre-brand — they are what buyers receive.
- [ ] Welcome film re-cut (color grade, B-roll, motion graphics).

---

## Rollback

Vercel keeps every deployment. If production breaks, promote the previous
deployment from the dashboard — it is instant and needs no code change.
