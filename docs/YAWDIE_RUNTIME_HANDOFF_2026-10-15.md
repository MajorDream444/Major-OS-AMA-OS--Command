# Yawdie runtime handoff — 15 October 2026

## Founder-approved direction
Move existing HAMAL systems from design to execution. Yawdie/Yawds is chief of staff, one of twelve core seats. Preserve existing wider Mob identities. Use existing tools and local open-source inference; no automatic paid token fallback. MAIM is first: Business Pressure Test lead funnel, owned shop/library, Stripe and Resend. Organic distribution target is at least twelve daily placements across relevant accounts. Client systems remain separate.

## Implemented in runtime/yawdie
A Python standard-library worker with private SQLite spool, immutable sources, deduplicated jobs, exclusive claim leases, interrupted-job recovery, bounded retries, evidence records, local Ollama draft generation, twelve planned distribution slots, daily source dispatch and morning/evening local brief files. No paid API credential is needed. Cloud Ollama proxy models are rejected. Generation records available model token counts and duration.

Ten deterministic tests cover persistence, duplicate dispatch, concurrent job claims, stale-worker completion rejection, retry exhaustion, workspace validation, invalid content, cloud endpoint rejection, daily dispatch and no-source behavior. Inference is mocked in those tests. Live inference, rendering and publication are not proven by them.

## Actual environment observations
Ollama, Node, Claude Code and Codex executables are installed. `ollama list` was denied connection to localhost by the coding session sandbox. That is an access limit, not evidence the local service is off. No worker process inspection, installed-model list, persistent host service, overnight run or local model output was verified. Git shell network cannot resolve github.com; authenticated GitHub tools remain usable.

## Existing systems found
Local SUBSTACK-AUTOMATION-ENGINE has source scripts, installed dependencies and article/asset/queue handoff commands. Its own rules keep publishing and asset generation dry-run. It remains an external artifact producer; this new worker does not duplicate its publishing controller. Local HAMAL_MOB_OS_CANON confirms doctrine/playbooks, MobStack execution harness, Command Center visibility and memory as separate layers. Existing Command Center browser app remains simulated.

## Next integration sequence
1. Run the worker with an actually installed local model on the host; verify one source-to-draft job and token/duration evidence. Register the loop under the existing host supervisor and confirm restart recovery and morning/evening files.
2. Connect Substack engine intake/exports and Airtable using current schemas and stable IDs. Add a source acceptance check and finished asset production before publication adapters. Preserve raw source; prevent client leakage.
3. Repair sandbox Stripe webhook protection configuration. Existing endpoint uses a placeholder bypass value. Verify Blueprint purchase/order/email path. Build separate book fulfillment and access before exposing book checkout.
4. Wire owned MAIM storefront and actual ready products; retire Gumroad/Kit calls to action only with functional owned replacements. Do not activate undeliverable offers.
5. Attach account-specific publishing adapters and confirmation receipts, with dedupe, retries, failed-post visibility and verified destination CTAs. Twelve planned slots do not equal twelve posts.
6. Connect Command Center visualization to this actual job/event state. Holographic/3D presentation follows accurate telemetry.

No secrets, private source notes, databases, client files or account credentials are committed. This is a tested first execution adapter, not completion of the wider launch or activation of all twelve agents.
