# Expertise excerpt pilot — local execution evidence

Date: 2026-10-27  
Status: **eventual success; awaiting founder review; not published**

Editorial review on 28 October requested changes for this checksum. See
[`EXPERTISE_EXCERPT_REVIEW_2026-10-28.md`](EXPERTISE_EXCERPT_REVIEW_2026-10-28.md). The queue stage
remains historical evidence and is not founder acceptance.

## Scope and acknowledgment

- Operating contract: 1.1.0
- Architecture: 1.0.0
- Authority commit: `a18cac669e47e0dd489bffe8c7b3d2e74736b40c`
- Installed implementation: `ac224ce46056e24eb3083d5f4fca868add2a1b4b`
- Runtime identity: `launchagent:com.major.hamal.yawdie`
- Acknowledgment ID: `0a850e54e85209a70e8c767528e7e233c47f2df4d715e51878261c507d31501c`

The existing LaunchAgent, SQLite database, retry authority, Major OS bridge, and drafting history
were retained. No cloud inference, paid fallback, publishing, external message, commerce change,
or model-authored shell execution was enabled. The media stages are deterministic and did not call
Ollama; local `llama3.2:latest` remains the separate drafting model.

## Result

| Evidence | Value |
| --- | --- |
| Successful job | `daf1f5aae7434e65beaeeb7b97dc37d5` |
| Submitted | `2026-10-27T09:48:13.940367Z` |
| Started | `2026-10-27T09:48:19.010589Z` |
| Reached review gate | `2026-10-27T09:52:13.216718Z` |
| Final status | `awaiting_review` |
| Worker PIDs | pre-fix `71821`; corrected render/QA `78880` |
| Source SHA-256 | `840d83d08dc3ed44adca676d6313a180326195415312d8626252c7b351c84434` |
| Preview SHA-256 | `db3eff9797c70a3be0853d749205554ea50e290acc04e2df79974bf7a90c1c87` |
| Evidence SHA-256 | `7752bd40b2cf1867b629cb5d0bc414e5935c5ba778f6fa024bf200303a103a5d` |
| Preview | 98 seconds; H.264/AAC; 1920x1080; 126,722,502 bytes |
| Private preview location | `~/.local/share/hamal-yawdie/production/outputs/daf1f5aae7434e65beaeeb7b97dc37d5/expertise-content-workflow-live-v3.mp4` |
| Private evidence location | `~/.local/share/hamal-yawdie/production/outputs/daf1f5aae7434e65beaeeb7b97dc37d5/evidence.json` |

All fixed stages completed. The current stage rows have no error label. Two earlier render attempts
remain in the immutable attempt ledger as `RuntimeError`; attempt 3 completed under the corrected
compiled renderer. Resubmitting the unchanged v3 manifest returned the same job ID with
`duplicate: true`. Restarting through the idempotent installer produced one worker and retained the
completed job and evidence.

## First-pass failures retained

| Job | Outcome | Finding |
| --- | --- | --- |
| `b75a5c5fd1d74b23b8fc45c6e4934bf1` | blocked | The Downloads organizer moved the submitted source while later stages were running; interpreted Swift also proved unsuitable under the LaunchAgent. Three failed render attempts remain recorded. |
| `f67a7362d154436aaff67aeb48fdecf0` | blocked | LaunchAgent intake was denied direct Downloads access (`PermissionError`). One failed attempt remains recorded. |
| `daf1f5aae7434e65beaeeb7b97dc37d5` | eventual success | A checksum-verified private source copy and installer-compiled renderer resolved the two boundaries. Render attempts 1 and 2 failed before the corrected runtime; attempt 3 and all later stages completed. |

The final design snapshots the verified media into the private job directory at intake. The worker
therefore does not depend on a movable Downloads path during later stages and is not granted broad
filesystem access. The installer compiles a pinned renderer before stopping the service; a compile
failure leaves the currently running service untouched.

## Verification

- `python3 -m unittest discover -s runtime/yawdie/tests -v`: **65 passed**
- `xcrun swiftc -typecheck runtime/yawdie/render_excerpt.swift`: passed with only SDK deprecation warnings
- `git diff --check`: passed
- Installed toolchain: macOS 27.0.1 (arm64), LaunchAgent Python 3.9.6, FFmpeg 8.1,
  Apple Swift 6.3.3, Ollama server 0.40.11 (`llama3.2:latest` already installed)
- SQLite pre-change backup: `PRAGMA integrity_check = ok`; 15 drafting jobs retained
- Installed source hashes matched the branch; compiled renderer identified as arm64 Mach-O
- Exactly one `com.major.hamal.yawdie` worker was running after final restart
- Technical QA: video and audio present, duration exactly 98 seconds, captions present
- Visual frame review: white captions, thin black outline, gold active word; speaker, crest, and CTA remain visible

Private backup location: `~/.local/share/hamal-yawdie/operations/20261027T093901Z-pre-expertise/`.
It contains the SQLite-aware database backup, prior installed runtime, and prior LaunchAgent plist.

## Rollback

1. Stop the service with `yawdie service stop`.
2. Preserve the current state directory for investigation.
3. Restore the saved runtime and plist from the private backup.
4. Restore the backed-up SQLite database as a complete database while the service is stopped.
5. Start with `yawdie service start` and verify one worker plus `PRAGMA integrity_check`.

Rollback is not currently required. Private source media, manifests, absolute user paths, database,
logs, and rendered artifacts are excluded from Git.

## Remaining review and next adapter

Founder review is still required for word sync, legibility, excerpt boundaries, and editorial
approval. Publishing remains unavailable and was not attempted. Sleep/wake recovery was not tested
in this pilot. The Swift source uses APIs deprecated by newer SDKs but compiles and runs on the
installed Mac; modernization is maintenance work, not a pilot blocker.

The next adapter is the separately approved, bounded GitHub assignment intake bridge. It was not
implemented ahead of this pilot. Repository text must remain task data, with explicit assignment
types, deduplication, acknowledgment, and no arbitrary command authority.

Founder direction for the next media enhancement, including Remotion, title placeholders, lesson
callouts, Obsidian ownership, Claude Code visibility, and productization, is recorded in
`docs/handoffs/YAWDIE_VIDEO_WORKFLOW_FOUNDER_DIRECTION_2026-10-27.md`.
