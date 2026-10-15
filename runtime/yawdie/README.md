# Yawdie: first local execution worker

Yawdie (Yawds, Yadi, Yads) is HAMAL chief of staff. This additive worker implements one real local draft-generation workflow and a private execution spool. It does not activate twelve autonomous agents or modify the existing simulated browser dashboard. Existing OpenClaw remains the intended broader runtime; this adapter can be invoked by it.

## What works

- Durable SQLite source/job/event spool with deduplicated dispatch, atomic claims, expiring leases and three bounded attempts.
- Explicit local Ollama model; no automatic model download, cloud model, API key or paid fallback.
- Original source preservation, source hash/reference, draft JSON, vertical script, thumbnail prompt, note and YouTube community draft.
- Twelve planned channel placements. These are not twelve finished assets or twelve publications. Several formats still need channel adaptation and rendering.
- Local daily dispatch after 08:00 and morning/evening status snapshots after 08:00/19:00 Asia/Makassar. The loop must be running; a schedule in code is not a deployed service.
- Queue history, honest failures, private artifact permissions and zero publication claims.

## Start on the machine that serves Ollama

Python 3.9+ and a working Ollama installation are required. `ollama list` identifies installed models; choose an actual installed model rather than a guessed model name. Python urllib uses the documented Ollama `/api/generate` interface. No package installation is required.

```bash
python3 -m unittest discover -s runtime/yawdie/tests -v
python3 runtime/yawdie/worker.py --state /tmp/yawdie-check report
# Put owned MAIM source notes in a private inbox, then:
python3 runtime/yawdie/worker.py enqueue --source /absolute/path/to/maim-note.md --reference local-maim-note
python3 runtime/yawdie/worker.py once --model YOUR_INSTALLED_MODEL
python3 runtime/yawdie/worker.py loop --model YOUR_INSTALLED_MODEL --inbox /absolute/path/to/maim-inbox
```

Default state location is `~/.local/share/hamal-yawdie`. Do not commit its database, original sources, drafts or operational events. Airtable remains the intended business record system; this spool has no Airtable adapter yet.

For restart persistence, configure the existing host's process supervisor to run the `loop` command with an absolute Python/script path, private state directory, installed model and MAIM inbox. Installing/enabling that supervisor is not performed by this change. If the machine sleeps, jobs cannot run; due briefs catch up when the loop resumes. Use one loop per spool for daily dispatch; concurrent job consumers are supported, concurrent dispatch schedulers are not yet supported.

## Immediate MAIM mission

The Business Pressure Test leads the owned funnel. Ready products belong in MAIM's shop/library; Stripe handles payment and Resend transactional delivery. Gumroad is excluded. Shakti and other client sources are excluded from this inbox. Do not direct users to a checkout until its product-specific delivery has been verified.

## Evidence and limitations

Deterministic tests mock inference; they prove queue and artifact behavior, not local model quality. This coding session could not reach localhost:11434 because its network sandbox denied access. No live model generation or overnight execution is claimed. No scheduler installation, automatic social posting, rendered video, NotebookLM integration, Stripe/Resend fulfillment, Kai integration, external account connector, Graphify rebuild, or production deployment is included.

All twelve seats are returned by `roster`, with only H06's local content workflow executable here. Drafts require factual/voice review. The worker cannot execute model-generated commands. Paid providers and external publishing need separate tested adapters and scoped credentials; chat connectors are not inherited by this process.
