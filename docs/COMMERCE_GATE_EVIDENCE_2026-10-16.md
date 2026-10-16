# Commerce Gate Evidence — 2026-10-16

Produced for the three-hour launch sprint (Issue #35 / #37 scope). All findings
read directly from the Stripe API. **One test-mode checkout session was created;
no live write was ever made.**

## Controlled test transaction — RUN

Test-mode access was granted on the second pass. A controlled session was created
in **test mode only**. No live write was ever made.

```
session   cs_test_a1ibuwzAg5rDaqoNmWxOUtJVhBGQzueHAtPItNZCxJCHVRRbE14BLxfyNu
product   MAIM Client System Blueprint (prod_VRECOlalAX3Ufa)
price     price_1UQLkGBaiziDnHMmEeEDuMSU — $250.00 one-time USD
status    open / unpaid   ·   expires 2026-10-17
success   https://www.majoraimindset.com/return?product=blueprint&session_id={CHECKOUT_SESSION_ID}
cancel    https://www.majoraimindset.com/pillars
metadata  purpose=sprint_controlled_test
```

Hosted Checkout cannot be completed headlessly — card entry needs a browser. The
session URL is payable with test card `4242 4242 4242 4242`, any future expiry,
any CVC. Completing it is the remaining step, and it will exercise the webhook.

**Prediction on record before that happens: the webhook will fail.** See blocker 1.

### What the test already established

- Checkout branding **is** configured — dark `#1e1e1e` ground, gold `#a06e18`
  button, "M.A.I.M." display name, logo and icon uploaded. The payment page looks
  like the brand.
- Payment methods enabled: card, Klarna, Link, Affirm, Cash App, Amazon Pay.
- Session creation works against the price. The Stripe object graph is sound.

What it does **not** establish: this session was created directly against the
Stripe API, not by the deployed application. It therefore proves nothing about
the app's own checkout code, which this environment cannot reach (egress is
allowlisted).

## Evidence

### 1. Webhooks — live has none, test has one and it is broken

**Live mode: zero endpoints.**

```
GET /v1/webhook_endpoints (livemode=true)  →  { "data": [] }
```

A real customer paying today triggers nothing. No order record, no entitlement,
no delivery email. Production commerce cannot fulfill, full stop.

**Test mode: one endpoint, with an unsubstituted placeholder in the URL.**

```
we_1UQLIIBaiziDnHMm9A0CX34a
https://business-pressure-test-9v10k7039-hamal-agi.vercel.app
  /api/stripe-webhook?x-vercel-protection-bypass=YOUR_BYPASS_SECRET
                                                  ^^^^^^^^^^^^^^^^^^
events: checkout.session.completed, checkout.session.async_payment_succeeded
```

Three defects in one URL:

1. **`YOUR_BYPASS_SECRET` is the literal template text.** The bypass token was
   never filled in, so the request carries no valid bypass.
2. **It points at a preview deployment** (`…-9v10k7039-…`), not a stable domain.
   Vercel SSO is enabled for all targets *except custom domains*, so preview URLs
   sit behind an auth wall — which is exactly what the missing bypass token was
   meant to get through. The call will be rejected before reaching the handler.
3. **Preview URLs are per-deployment.** Even with a correct secret, the next
   deploy changes the hostname and the webhook breaks again. It should target a
   custom domain or a stable production alias.

It also points at project `business-pressure-test`, not `major-ai-os` — a third
MAIM-related deployment target.

### 2. The MAIM products are flagged not-ready by their own metadata

| Product | ID | Metadata |
|---|---|---|
| MAIM \| The Pillar Scroll | `prod_VOxzpbJcWB5Psj` | `launch_status: checkout_hold` · `fulfillment: pending_verification` · `existing_checkout: gumroad` |
| MAIM \| Business Pressure Test + Blueprint | `prod_VQ3PnQKlO2DtQu` | `launch_status: integration_pending` · `fulfillment: human_review` |

The Pillar Scroll description states outright: *"Fulfillment and included
resources are being reconciled before Stripe checkout is activated."*

No Emerald Awakening ($97) or Pillar Code Vault ($297) product exists in Stripe
at all.

### 3. The implementation has never been tested

```
GET /v1/checkout/sessions (livemode=false)  →  { "data": [] }
```

**Zero test sessions existed before this one.** No end-to-end verification has
ever been performed against this integration by anyone.

Test mode also contains **only** the Blueprint product ($250). The Pillar Scroll
— the stated V1 revenue journey — has no test-mode product or price at all.

### 4. No MAIM sale has ever occurred, and no session came from the site

Seven checkout sessions exist, all live mode:

- **Every one originates from a Payment Link** (`plink_…`), not from an
  application integration.
- **Every one has `success_url` and `cancel_url` set to `https://stripe.com`** —
  not `majoraimindset.com`. None was ever wired to the site or to `/return`.
- Two completed: **$2,000** and **$2,500**, both the Shakti client engagement
  milestones. Both manual invoices.
- The remaining five expired unpaid.
- **Zero sessions reference any MAIM digital product.**

The deployed application has never created a Stripe checkout session.

## Gate decision

**NO-GO on the owned commerce path.** Not a judgement call — four independent
blockers, each sufficient on its own:

1. Live mode has **no webhook at all**; the test webhook carries an
   unsubstituted `YOUR_BYPASS_SECRET` and targets an ephemeral preview URL behind
   SSO. Fulfillment cannot fire in either mode.
2. Products carry `checkout_hold` / `integration_pending` and point at Gumroad.
3. The integration has **never been tested** — zero prior test sessions.
4. No application-originated session has ever existed; every live success URL
   points at `stripe.com`.

The site being deployed and READY does not change this. Deployment and commerce
are separate milestones, and commerce is at *documented*, not *built*.

## To unblock, in order

1. ~~Add a test-mode key~~ — done, granted 2026-10-16.
2. **Fix the test webhook and create a live one.** Replace `YOUR_BYPASS_SECRET`
   with the real token, and repoint both at a stable custom domain rather than a
   per-deployment preview URL. Live mode currently has no endpoint at all.
3. Decide Gumroad vs Stripe for the Pillar Scroll — currently both are referenced
   and neither is wired. Running two checkouts for one product will produce two
   customer records for the same person.
4. Create the missing $97 and $297 products, or confirm they stay on Gumroad.
5. Set real `success_url` → `/return?product=…` and `cancel_url`.
6. Only then run the end-to-end test, in test mode, and record the session ID,
   webhook delivery, and email receipt as evidence.

## Scope note

This session is scoped to `Major-OS-AMA-OS--Command` and cannot read
`MajorDream444/Major-AI-OS`, where the deployed code and Issues #34–37 live. The
findings above are from the Stripe account, which is shared across both.
