# MAIM Diagnostic Engine

**One instrument. Two skins.**

The Pressure Test and "Which Pillar Are You?" are not two assessments. They are one
engine with two presentations, chosen by the door the visitor came through. Building
two would mean maintaining two question banks that produce overlapping answers and
two member records for the same person.

## Signals collected

Identical regardless of skin:

| Signal | Type | Purpose |
|---|---|---|
| `pressure` | enum | current bottleneck — what is actually in the way |
| `identity` | enum | role: athlete, creator, entrepreneur, educator, healer, professional, parent, other |
| `ai_confidence` | 1–5 | comfort operating with AI today |
| `goal` | enum | the immediate outcome they want |
| `readiness` | 1–5 | willingness to act this week |
| `pillar` | enum `01`–`10` | derived — dominant Pillar |
| `next_step` | enum | derived — recommended action |

`pillar` and `next_step` are computed, never asked directly.

## Two skins

Same engine, same data model, different framing to respect visitor intent.

### Trust-first — served on `majoraimindset.com`

Someone here is not yet in buying posture. Lead with the human problem.

- **Prompt:** *What is creating pressure in your life or work?*
- **Result headline:** *Your next MAIM starting point*
- **Result body:** the A·B·C letter to begin with, and the next live room session
- **CTA:** reserve a free seat

### Direct-response — served on the Pillars funnel

Someone here arrived through a problem/offer frame. Lead with the framework.

- **Prompt:** *Which Pillar needs your attention first?*
- **Result headline:** *Your primary Pillar and recommended offer*
- **Result body:** dominant Pillar, why it surfaced, which tier addresses it
- **CTA:** the matching product

## Result → member record

The engine writes straight into the canonical record (see `MAIM_MEMBER_RECORD.md`):

```
assessment_result = {
  pressure, identity, ai_confidence, goal, readiness
}
pillar     = <derived>
entry_door = front_door | funnel
```

Because both skins write the same shape, a visitor who takes it at one door and
returns through the other is recognized — not re-diagnosed.

## Mapping

`pillar` derives primarily from `pressure`, adjusted by `identity`:

| Pressure | Pillar |
|---|---|
| isolated / no network | 01 Diaspora Empowerment |
| self-doubt, feeling behind | 02 Mindset Shift & Resilience |
| don't know where to start learning | 03 Gamified Education |
| no ownership of what I build | 04 Blockchain & Decentralization |
| building alone | 05 Community & Collaboration |
| tools don't fit my context | 06 Localized AI & Personalization |
| burnout while scaling | 07 Holistic Wellness & Balance |
| exposed / unprotected | 08 Security & Compliance |
| can't tell what's working | 09 Data-Driven Performance |
| building without a long horizon | 10 Legacy & Long-Term Impact |

`next_step` follows from `readiness`: low readiness routes to the free live room;
high readiness routes to the tier that addresses the derived Pillar.

## Archetype names — direct-response skin only

| Archetype | Pillar |
|---|---|
| The Community Architect | 05 |
| The Sovereign Builder | 04 |
| The Knowledge Warrior | 03 |
| The Legacy Visionary | 10 |

Ten Pillars, four named archetypes — the remaining six need names, or the quiz
should collapse to the four dominant doors. **Open decision for Major.**

## State

Not built. Both surfaces currently ship a static mock: the Pressure Test card on the
front door and the archetype grid on the funnel. They demonstrate the interaction
but collect nothing.

Not launch-blocking — the site can go live with the mocks. It is the first
post-launch build, because it is what makes the member record meaningful.
