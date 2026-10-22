# MAIM Canonical Member Record

## Governing rule

> **No MAIM journey should terminate on an external platform.**

External tools may process payments, email, video, or community activity. Every
meaningful journey loops back into MAIM.

Corollary: **Gumroad processes the transaction. MAIM owns the relationship.**
Gumroad is not the customer database and must never be treated as one.

## Identity

A member is identified by **email**, normalized: trimmed, lowercased. One email is
one person across every door, product, and system.

## Schema

| Field | Type | Notes |
|---|---|---|
| `email` | string | **primary key.** normalized lowercase |
| `full_name` | string | |
| `source` | enum | where they came from — `instagram`, `youtube`, `referral`, `direct`, … |
| `entry_door` | enum | `front_door` (trust-first) or `funnel` (direct-response) or `gumroad` (purchase-first) |
| `assessment_result` | object | output of the diagnostic engine — see `MAIM_DIAGNOSTIC_ENGINE.md` |
| `pillar` | enum | dominant Pillar `01`–`10` |
| `product` | enum | `pillar_scroll` · `emerald_awakening` · `pillar_code_vault` · null |
| `purchase_status` | enum | `none` · `pending` · `complete` · `refunded` |
| `studio_access` | enum | `none` · `waitlist` · `active` |
| `community_status` | enum | `none` · `invited` · `joined` |
| `created_at` | timestamp | |
| `updated_at` | timestamp | |

## Flow

```
Website form / account
        ↓
Canonical MAIM member record   ← source of truth
        ↓
Kit subscriber                 ← email delivery
        ↓
Gumroad purchaser data attached to that record
```

Writes go to the canonical record first, then fan out. Never the reverse — a
Gumroad or Kit record is a projection, not the truth.

## Launch-safe bridge

Full authentication is not required to launch. The interim path:

```
Gumroad receipt
        ↓
Thank-you URL on majoraimindset.com   → maim/return.html?product=<key>
        ↓
Short access form (email, name, product)
        ↓
Product delivery + Studio waitlist/access
```

This keeps the buyer inside MAIM from the moment payment clears, and captures the
canonical record even before accounts exist.

### Gumroad configuration required

Set each product's post-purchase redirect to:

| Product | Redirect URL |
|---|---|
| The Pillar Scroll — $27 | `https://majoraimindset.com/return?product=pillar_scroll` |
| Emerald Awakening — $97 | `https://majoraimindset.com/return?product=emerald_awakening` |
| The Pillar Code Vault — $297 | `https://majoraimindset.com/return?product=pillar_code_vault` |

`return.html` reads `?product=` and adapts the confirmation line, the shelf, and the
pre-selected product on the access form. With no parameter it falls back to the
entry tier — it never breaks.

## Service blueprint — the full arc

```
Discover
Understand
Diagnose
Register
Purchase
Return to campus   ← maim/return.html (built)
Access product
Take first action
Join live experience
Re-engage
```

Current coverage:

| Stage | Surface | State |
|---|---|---|
| Discover | front door · funnel | built |
| Understand | welcome film (embedded) · ABC · Pillars | built |
| Diagnose | Pressure Test / Which Pillar | **spec'd, not built** |
| Register | Kit form on both pages | built (wired to Kit) |
| Purchase | Gumroad | external |
| Return to campus | `return.html` | built |
| Access product | access form → Kit | interim bridge |
| Take first action | three actions on `return.html` | built |
| Join live experience | live room CTA | built |
| Re-engage | Studio | **not built** |

## Open

- Studio account creation and authentication — the real fix behind the interim bridge
- Where the canonical record physically lives (Airtable is the stated Operations DB)
- Refund / chargeback handling against `purchase_status`
