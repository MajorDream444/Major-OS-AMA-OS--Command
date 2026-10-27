# Yawdie activation and cohort handoff — 26 October 2026

> Sequencing and countdown are superseded by the
> [28 October launch baseline](../handoffs/YAWDIE_LAUNCH_BASELINE_2026-10-28.md). Evidence below is
> retained as historical verification.

## Outcome

The Major OS bridge is activated against the existing SQLite queue and local Ollama worker. One
worker is supervised by the existing user LaunchAgent. No cloud fallback, publishing, external
message, payment, database mutation or production promotion was enabled.

The pre-activation observation ended early and is labelled `COMPLETE_WITH_GAPS_OR_FAILURES`: one
snapshot covered roughly one hour and no sleep/wake event was observed. It is not an overnight
verification. The Codex heartbeat was paused and a separately labelled deterministic local
post-activation observer was started. Private JSONL and summary paths remain under the runtime's
existing `operations` state folder and are not committed.

## Live bridge evidence

- First job `79dc2f7ffa0941a6ba8adae8ecec19b8`: rejected after three `ValueError` attempts and retained as
  `blocked`. This is first-pass failure evidence, not completed drafting.
- Intentional rerun `88373010d812441e936e35a4230dff3d`: `draft_ready` on attempt 1 with
  `llama3.2:latest`; inference duration 12.669 seconds; report exported atomically. An unchanged
  source rescan submitted zero jobs.
- Repository-grounded cohort brief `ff8de6ea319b40f58a1439001f372ead`: `draft_ready` on attempt 1;
  report exported with bounded context provenance.
- Queue history was preserved. Unsupported external actions remain `blocked: adapter unavailable`.

Private vault contents, absolute vault/checkouts, artifacts, SQLite data and logs are deliberately
omitted from Git.

## Repository adapter

The adapter uses the shared path policy plus a private manifest of exact approved roots and include
paths. It records checkout commit/dirty state, file hashes and snapshot provenance while rejecting
traversal, hidden paths, symlinks, binaries and oversized files. The activated snapshot covered:

| Repository | Snapshot commit | Dirty at snapshot | Scope |
| --- | --- | --- | --- |
| Command | `1b31118f1bcdaf7bdad05906195b07d39ea4a306` | yes — focused changes were uncommitted | runtime instructions and reconciliation evidence |
| Major-AI-OS | `ef60719d8302aa1b285b11bc2dd0d4dd075b79fd` | no | root/cohort instructions and blocker record |
| MAIMACADEMY | `c90ce2779c4dcc606d09c3181cb7b0e5d3c25cc8` | no | root instructions and blocker record |

The larger generated snapshot was retained as rejected context evidence because it exceeded the
per-file prompt limit. A separate 3,420-byte summary was accepted. This proves bounded reading and
provenance, not general repository execution.

## Cohort readiness PRs

- Major-AI-OS draft PR #69: missing immutable terms route, readiness-gated November 11 wording,
  truthful reservation/capacity copy, legacy duplicate intake removal and blocker record. Local
  typecheck, 22/22 tests, 16-page build and diff check passed. The Vercel preview is SSO-protected,
  so hosted route behavior remains unverified.
- MAIMACADEMY draft PR #25: payment/replay/member-access claims made readiness-gated and truthful,
  checkout fail-closed evidence corrected, regression coverage and blocker record. HTML validation,
  33/33 tests, build checks and dependency audit passed; Vercel checks passed. Fresh browser QA was
  not run because Playwright is not an installed project dependency.

Both preserve November 11 only after approval, November 18, US$249 once and the 20-seat cap. Pillar
Scroll remains separate. Neither PR changes Stripe, sends a message, submits a form, touches
production data, deploys or merges.

## Remaining release gates

1. Read-only Stripe inventory must prove no active Academy payment link before release approval.
2. Controlled hosted evidence is still required for authenticated checkout, atomic 20-seat
   capacity, entitlement, signed webhook/deduplication, refunds and reservation receipts/consent.
3. Replay/meeting delivery and continuation dates need owner confirmation.
4. Rights-cleared curriculum/capacity evidence and fresh browser/mobile review remain open.
5. The local post-activation observation must actually elapse before it can be called overnight or
   sleep/wake evidence.

## Rollback

Reinstall the same runtime without `YAWDIE_VAULT_ROOT` to stop vault scanning while preserving the
vault, reports and SQLite history. Stop the observer with `observer_service.py uninstall`; its
evidence is retained. Reverting either draft PR is independent and does not affect the installed
Yawdie queue.
