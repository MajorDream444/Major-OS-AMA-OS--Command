# Commerce Gate Evidence — 2026-10-16

Produced for the three-hour launch sprint (Issue #35 / #37 scope). All findings
read directly from the Stripe API. **No transaction was created.**

## Requested action not performed

A controlled **test-mode** transaction was requested. It was not run, because
**no test-mode context exists in this session**:

```
acct_1TLgn2BaiziDnHMm   "M.A.I.M."   livemode: true    ← only account available
```

The single Stripe context is live. Creating a checkout session or payment intent
here would charge a real card and produce a real payout record. That is not a
controlled test, so the write was refused and read-only verification was done
instead.

To run the requested test, a **test-mode / sandbox key** must be added to the
session, or the test executed from an environment that holds one.

## Evidence

### 1. No webhook endpoints — fulfillment cannot fire

```
GET /v1/webhook_endpoints  →  { "data": [], "has_more": false }
```

**Zero endpoints configured.** Even on a successful payment, Stripe has no way to
notify the application. No order record, no entitlement grant, no delivery email
can be triggered automatically. This alone blocks an owned checkout-and-delivery
path.

### 2. The MAIM products are flagged not-ready by their own metadata

| Product | ID | Metadata |
|---|---|---|
| MAIM \| The Pillar Scroll | `prod_VOxzpbJcWB5Psj` | `launch_status: checkout_hold` · `fulfillment: pending_verification` · `existing_checkout: gumroad` |
| MAIM \| Business Pressure Test + Blueprint | `prod_VQ3PnQKlO2DtQu` | `launch_status: integration_pending` · `fulfillment: human_review` |

The Pillar Scroll description states outright: *"Fulfillment and included
resources are being reconciled before Stripe checkout is activated."*

No Emerald Awakening ($97) or Pillar Code Vault ($297) product exists in Stripe
at all.

### 3. No MAIM sale has ever occurred, and no session came from the site

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

**NO-GO on the owned commerce path.** Not a judgement call — three independent
blockers, each sufficient on its own:

1. No webhook endpoint → fulfillment cannot be automated or verified.
2. Products carry `checkout_hold` / `integration_pending` and point at Gumroad.
3. No application-originated session has ever existed; success URLs point at
   `stripe.com`.

The site being deployed and READY does not change this. Deployment and commerce
are separate milestones, and commerce is at *documented*, not *built*.

## To unblock, in order

1. Add a **test-mode key** to whatever environment runs the verification.
2. Create the webhook endpoint pointing at the deployed app's handler, subscribed
   to `checkout.session.completed` at minimum.
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
