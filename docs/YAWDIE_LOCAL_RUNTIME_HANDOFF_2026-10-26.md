# Yawdie local runtime handoff — 26 October 2026

Status: locally verified, reversible, drafting only. This document is redacted; private sources, artifact bodies and absolute private paths are not committed.

## What actually runs

One macOS user LaunchAgent runs one Python standard-library worker against the existing local Ollama service and installed `llama3.2:latest` model. The spool provides atomic content/task deduplication, explicit reruns, immutable sources, exclusive leases, bounded attempts, per-attempt evidence and graceful administrative interruption. Manual and watcher intake share the same database uniqueness key. The watcher requires `Yawdie-Actionable: true`, ignores template filenames, rejects group/world-readable inbox files and avoids rereading unchanged files.

Two draft tasks exist: `source-to-draft` and `operating-brief`. Operating briefs return only priorities, next actions, blockers and evidence needed. Unsupported external work is `blocked: adapter unavailable`.

Ollama calls use a proxy-free opener and accept loopback HTTP only. Cloud model metadata and cloud model names are rejected. No automatic download, paid fallback, publishing, messages or commerce adapter is present.

## Evidence ledger

Deterministic suite: 42 tests passed. It covers watcher/manual overlap, 16-way concurrent intake, changed content, intentional rerun, template exclusion, permission repair, repeated scanning, execution locks, cloud rejection, proxy disabling, URL grounding, MAIM validation, source-section preservation, stale leases, administrative interruption, idempotent service start, pre-stop vault validation, allowlisted vault paths, traversal/symlink/binary/size rejection, bounded context, unavailable iCloud files and atomic report export.

Accepted reviewed live operating brief: `254f8a36e00d4c4c982da2f0b95b3a3e`, an explicit intentional rerun with unchanged source. Two attempts were retained as `ValueError` coverage rejections before source-section preservation was deployed; the third attempt reached `draft_ready` with `llama3.2:latest`. It produced all four numbered priorities plus source-grounded next actions, blockers and evidence needed; placements and publications were empty.

Earlier live job `04b9c04f962e4b5598b5d1d76bd4c35f` needed two attempts after a `JSONDecodeError`. It proved successful retry, not interrupted-job recovery. The earlier restart check was idle restart only.

Three preserved pre-acceptance spools exist outside Git:

- verification archive: one job needed three attempts (`ValueError`, `JSONDecodeError`) and a second duplicate draft completed once;
- invalid-draft archive: one first-attempt draft was set aside after human grounding review;
- grounding-retry archive: one job remained retrying after `HTTPError` and `ValueError`.

The seven historical macOS privacy crash-loop messages came from the first LaunchAgent pointing into Documents. The installed runtime was moved to Application Support; those log lines remain as history.

## Separate-service disruptive tests

A separate temporary LaunchAgent and isolated spool were used. Mid-inference bootout returned job `17c69b5ab9714314b387ef30c73a041c` to `queued`, restored attempts to zero and recorded `administrative_interrupt`; restart then completed it. A competing loop exited zero and launchd's run count stayed unchanged. Proxy-isolated job `b56c15d3427446c4875e2b30a9db7320` completed while `HTTP_PROXY`, `HTTPS_PROXY` and `ALL_PROXY` pointed to a dead local proxy and both no-proxy variables were empty.

This proves controlled administrative stop/restart and proxy bypass in isolated state. Real crash recovery, Mac sleep/wake during inference and live-spool mid-job interruption remain unverified.

## Major OS bridge

The adapter is implemented on the PR branch but has not replaced or restarted the observed
LaunchAgent. Its path policy permits only four configured subfolders: context, brief inbox,
reports and templates. Context and brief bodies stay in private SQLite/vault storage; public
Git contains only code, relative folder contracts and redacted evidence.

Isolated end-to-end job `8a50202cc448480d9adfbabe07ff643a` read one non-sensitive
actionable operating brief plus one bounded context note, ran `llama3.2:latest`, and exported
one Markdown report. It completed on attempt 1 in 18.349 seconds. An unchanged rescan left
the isolated spool at one job. No publication or external action occurred.

The controlled activation is shown in `runtime/yawdie/README.md` and must run only after the
overnight baseline ends. That operation restages
the runtime and restarts the service, so it was deliberately deferred. Rollback is the same
install command with `YAWDIE_VAULT_ROOT` unset; private vault files and SQLite history remain.

The Major OS vault is stored in iCloud. Local inference does not make vault storage local-only:
approved notes and reports may sync externally under the user's existing iCloud configuration.
The adapter does not alter sync settings and handles unavailable files without deletion.

## Ollama exposure

The Ollama API currently listens only on `127.0.0.1:11434`. Local inference and Yawdie operation were verified after the loopback-only change. LAN clients can no longer reach this Ollama API.

## Operator commands

```bash
yawdie brief --source /private/source.md --reference SOURCE --task operating-brief
yawdie brief --source /private/source.md --reference SOURCE --task operating-brief --rerun
yawdie status
yawdie report --job-id JOB_ID
yawdie service start
yawdie service stop
```

Processing pauses when the Mac sleeps or shuts down. Publishing, customer messages, commerce and external distribution remain blocked.
