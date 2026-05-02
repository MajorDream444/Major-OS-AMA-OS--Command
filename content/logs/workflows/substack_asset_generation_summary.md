# Substack Asset Generation Summary

- Source: SUBSTACK_ENGINE
- Source path: /Users/majordreamwilliams/Documents/SUBSTACK-AUTOMATION-ENGINE/content/logs/workflows/asset_generation_summary.json
- Total assets: 3
- Prepared: 1
- Ready for distribution: 1
- Skipped / blocked: 1
- Live publishing: no
- Rendering/audio/video generation in Mission Control: no
- External API calls: no

## Decision Queues
- prepared_assets_review: 1
- distribution_candidate_review: 1
- blocked_asset_review: 1

## Routed Assets
### Sample Reaction Doctrine

- Artifact ID: e79f8de5-b553-4b4b-8e4f-0ebaf161ba4b
- Mission ID: M-0501
- Lane: Reaction Doctrine
- Status: needs_rewrite
- Asset state: skipped
- Queue: blocked_asset_review
- Next action: inspect_blocked_reason
- Blocked reason: Status needs_rewrite is not eligible for asset generation.
- Asset files: 0
### Fixture Reaction Doctrine Clip

- Artifact ID: 3dd5955e-d00d-45bf-af2c-5740f1046b0d
- Mission ID: M-0501
- Lane: Reaction Doctrine
- Status: scheduled_dry_run
- Asset state: ready_for_distribution
- Queue: distribution_candidate_review
- Next action: approve_render_or_publish_queue_later
- Blocked reason: none
- Asset files: 6
### Sample Major Thought Approved

- Artifact ID: f626c438-7485-444b-98a7-520471e12651
- Mission ID: M-0501
- Lane: Major AI OS
- Status: ready
- Asset state: prepared
- Queue: prepared_assets_review
- Next action: review_assets
- Blocked reason: none
- Asset files: 6
