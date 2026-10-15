# Retired platforms — founder directive, 15 October 2026

## Decision
Shopify, Gumroad and Kit (ConvertKit) are RETIRED / DO NOT USE for Major's owned MAIM, AMA and HAMAL operations. Do not recommend, provision, install, reactivate or route new products, subscriber intake, campaigns, checkouts or fulfillment through them. A historical account, installed skill, credential or old URL is not current authorization. This decision supersedes contradictory source documents and agent routing instructions. Existing client-owned systems are separate: identify their owner and obligations before any external account or integration change.

## Selected replacement stack
- Owned website and shop on the existing Vercel deployment.
- Stripe for payments, product-specific orders and entitlements.
- Resend for transactional email and authorized mailing workflows.
- Airtable for operational registries, intake, segmentation and delivery state where already selected.
- GitHub for source code, instructions, retirement evidence and operator handoff; controlled Drive storage for private assets.

Provider selection is approved; completion of integrations must be verified independently. Do not claim Vercel, Resend or Airtable alone supplies payment settlement or durable paid-file access.

## Deactivation versus deletion
The accounts are reported active by the founder. Account closure, billing cancellation, integration disablement and removal of production links are separate checklist items. A documentation update does not perform those actions. Preserve original products, customer/order/refund/tax records, consent and suppression lists, templates, automations and owned assets before destructive closure. Preserve consent/unsubscribe state when moving email records; do not convert a contact export into blanket newsletter consent.

The founder has directed deactivation. Permanent account/data deletion was raised as a possibility, not completed or certified here. Use the provider's actual controls and record receipts; never mark a provider disabled without authoritative evidence. Do not erase historical Git commits or third-party research references. Mark old operational instructions SUPERSEDED and preserve migration provenance.

## Execution register
| Work | State |
| --- | --- |
| Founder stack decision and agent-facing prohibition | Recorded in GitHub |
| Legacy daily-sync and commissioning instructions | Updated to selected owned stack |
| Platform account inventory, plans and subscriptions | Not verified |
| Export and integrity check of products/orders/subscriber/consent data | Pending |
| Disable old forms, sequences, automations and checkout/listing entry points | Pending source/provider-specific verification |
| Remove or replace every public legacy link, deploy and smoke-test | Pending; inspect generated as well as source pages |
| Cancel recurring provider plans | Not performed |
| Close/delete provider accounts | Not performed |
| Verify owned registration, Stripe checkout, Resend delivery and access | Pending end-to-end evidence |

## Known discovery targets
Major-AI-OS: apps/maim-site/maim/pillar-scroll.html contains a legacy Gumroad checkout; apps/maim-site/maim/shop.html contains a legacy Kit guide link. Inspect all generated routes, registration form actions, redirects, scripts and environment dependencies before declaring the public site clean. docs/kit/ contains reusable editorial material; retain copy but retire Kit-specific activation instructions. Other skills, marketing references and external accounts still require inventory.

Command repository: remove retired-provider activation instructions from commerce workflow documentation and skill handoffs. Incoming requests naming a retired provider should route to migration/retirement review, not activate that provider.

## Reporting
Every brief and worker startup must load this decision alongside current launch/context documents. Report policy, source changes, deployed behavior, provider settings and billing separately. Discovery of a remaining active dependency is a tracked migration item, not permission to reuse the retired stack. No messages to external recipients are sent by publishing this internal directive.
