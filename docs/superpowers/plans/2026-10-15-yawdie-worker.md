# Yawdie local worker implementation plan

Goal: turn the existing Command Center's simulation into a first verifiable local execution path, preserving the wider OpenClaw integration boundary.

Architecture: an additive Python standard-library worker uses SQLite as a private durable execution spool, not a replacement for Airtable operational records. Ollama is the only inference adapter in this increment. No paid fallback or arbitrary shell execution. The existing browser dashboard remains unchanged and simulated until an adapter connects it.

Founder mandate: Yawdie/Yawds is chief of staff; 12 core seats; MAIM Business Pressure Test leads the funnel; owned storefront with Stripe/Resend; no Gumroad; client isolation; target twelve daily placements across available channels. Twelve is a distribution target, never a fabricated publication count.

1. Test durable enqueue/deduplication, exclusive claims, expired lease recovery, retry exhaustion, workspace validation and safe artifact paths.
2. Implement SQLite jobs/events/source records, local source hashing, run leases and evidence-backed reporting.
3. Test local inference failure, invalid model output and twelve distinct placement contracts. Implement Ollama draft generation with explicit model selection, bounded context/output, no external actions and no cloud fallback.
4. Implement idempotent daily source enqueue and a daily report. Worker polling can be scheduled by an existing host supervisor; this session cannot install a persistent service or reach localhost.
5. Execute deterministic tests, run a real local dependency check, commit source to existing Command Center main, and report tested versus activated status separately.

Acceptance: source survives restart; duplicate dispatch creates one job; interrupted jobs recover; drafts retain source provenance; inference failure never becomes completed work; reports show zero published until receipt-backed publication adapters exist.

Not included in this increment: automatic social posting, live payment changes, arbitrary CLI execution, global context ingestion, voice/avatar rendering, private client reads, model installation, Graphify rebuild, and holographic UI. These are integration work, not implied capabilities of the worker.
