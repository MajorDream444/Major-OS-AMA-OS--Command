# Yawdie: first local execution worker

Yawdie (Yawds, Yadi, Yads) is Major Dream Williams's chief of staff. MAIM means Major Artificial Intelligence Mindset. This additive worker implements one real local draft-generation workflow and a private execution spool. It does not activate twelve autonomous agents or modify the existing simulated browser dashboard. Existing OpenClaw remains the intended broader runtime; this adapter can be invoked by it.

## What works

- Durable SQLite source/job/event/attempt spool with atomic content/task deduplication, explicit reruns, atomic claims, expiring leases and three bounded attempts.
- Explicit local Ollama model; no automatic model download, cloud model, API key or paid fallback.
- Original source preservation and two bounded tasks: creative content packets and operating briefs.
- Watcher intake requires `Yawdie-Actionable: true`; files containing `template` in the filename are never automatically submitted.
- Twelve planned channel placements. These are not twelve finished assets or twelve publications. Several formats still need channel adaptation and rendering.
- Local daily dispatch after 08:00 and morning/evening status snapshots after 08:00/19:00 Asia/Makassar. The loop must be running; a schedule in code is not a deployed service.
- Queue history, honest failures, private artifact permissions and zero publication claims.
- Optional Major OS Markdown bridge with four fixed folders, bounded context, hashed provenance,
  atomic report exports and the same SQLite job/deduplication authority.

## Install and operate on the Mac that serves Ollama

Python 3.9+ and a working Ollama installation are required. `ollama list` identifies installed models; choose an actual installed model rather than a guessed model name. Python urllib uses the documented Ollama `/api/generate` interface. No package installation is required.

```bash
python3 -m unittest discover -s runtime/yawdie/tests -v
python3 runtime/yawdie/service.py install

# Put owned MAIM source notes in the private inbox, then:
yawdie brief --source "$HOME/.local/share/hamal-yawdie/inbox/brief.md" --reference founder-brief --task operating-brief
yawdie brief --source "$HOME/.local/share/hamal-yawdie/inbox/brief.md" --reference founder-brief --task operating-brief --rerun
yawdie status
yawdie report --job-id JOB_ID
```

## Major OS bridge

The bridge never reads the whole vault and never inherits Obsidian plugin settings. Set the
vault path only in the local shell; do not commit it:

```bash
export MAJOR_OS_VAULT="/private/path/to/Major OS"

# Safe before service activation: create/verify the four approved folders.
python3 runtime/yawdie/yawdie.py vault --root "$MAJOR_OS_VAULT" init

# Explicit manual submission and optional intentional rerun.
python3 runtime/yawdie/yawdie.py vault --root "$MAJOR_OS_VAULT" submit \
  --source "Yawdie/Briefs/Inbox/brief.md"
python3 runtime/yawdie/yawdie.py vault --root "$MAJOR_OS_VAULT" submit \
  --source "Yawdie/Briefs/Inbox/brief.md" --rerun
```

An actionable note requires `Yawdie-Actionable: true` and a supported `Yawdie-Task`.
Files with `template` in their name are never submitted. Context is read only from
`Yawdie/Context`; inbox is `Yawdie/Briefs/Inbox`; reports are written only to
`Yawdie/Reports`; `Yawdie/Templates` is never intake. SQLite remains the only execution
queue and report state is derived from it.

The controlled service activation is intentionally disruptive because it restages code and
restarts the LaunchAgent. Perform it only after the observation baseline is complete:

```bash
YAWDIE_VAULT_ROOT="$MAJOR_OS_VAULT" python3 runtime/yawdie/service.py install
```

Rollback disables vault scanning without deleting the vault folders, reports or SQLite history:

```bash
unset YAWDIE_VAULT_ROOT
python3 runtime/yawdie/service.py install
```

Inference remains on loopback Ollama. The vault is in iCloud, so approved brief, context and
report files may sync through the user's existing iCloud settings. The adapter does not change
those settings. Temporarily unavailable iCloud files are skipped and retried on a later scan;
they are never deleted or overwritten.

The installer stages only runtime code in private Application Support, creates an absolute-path user LaunchAgent, and selects the already-installed `llama3.2:latest` model. It never downloads a model. Run only after `ollama list` confirms the model exists.

One-command lifecycle:

```bash
yawdie service start
yawdie service stop
yawdie status
yawdie service uninstall
```

Uninstall removes the LaunchAgent, installed runtime copy and command, but deliberately retains private state for recovery. The source checkout remains the install authority. Processing pauses when the Mac sleeps or shuts down and resumes after login/wake.

Default state location is `~/.local/share/hamal-yawdie`. Do not commit its database, original sources, drafts or operational events. Airtable remains the intended business record system; this spool has no Airtable adapter yet.

Restart persistence uses `~/Library/LaunchAgents/com.major.hamal.yawdie.plist`. Runtime code is staged under `~/Library/Application Support/HAMAL/Yawdie/runtime`, state under `~/.local/share/hamal-yawdie`, and logs under `~/Library/Logs/HAMAL/Yawdie`. A per-spool lock prevents duplicate worker loops. If the machine sleeps or shuts down, jobs cannot run; due briefs catch up when the loop resumes.

## Immediate MAIM mission

The Business Pressure Test leads the owned funnel. Ready products belong in MAIM's shop/library; Stripe handles payment and Resend transactional delivery. Gumroad is excluded. Shakti and other client sources are excluded from this inbox. Do not direct users to a checkout until its product-specific delivery has been verified.

## Evidence and limitations

Deterministic tests mock inference; isolated integration checks additionally prove local inference, proxy bypass, graceful administrative interruption, duplicate-loop behavior and one Major OS note-to-report flow. The live service has produced local drafts, but the Major OS service integration remains deliberately unactivated during the overnight baseline. Overnight execution, real crash recovery, sleep/wake recovery, automatic social posting, rendered video, NotebookLM, Stripe/Resend, Kai, external accounts and production deployment remain unverified or unavailable.

All twelve seats are returned by `roster`, with only the local source-to-draft content workflow executable here. Drafts require factual/voice review. Unsupported work is reported as `blocked: adapter unavailable`. The worker cannot execute model-generated commands. Paid providers and external publishing need separate tested adapters and scoped credentials; chat connectors are not inherited by this process.
