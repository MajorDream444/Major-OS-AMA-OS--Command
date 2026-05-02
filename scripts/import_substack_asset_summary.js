#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const ROOT = process.cwd();
const SOURCE = "SUBSTACK_ENGINE";
const DEFAULT_INPUT = "content/logs/workflows/asset_generation_summary.json";
const SUMMARY_PATH = "content/logs/workflows/substack_asset_generation_summary.json";
const REPORT_PATH = "content/logs/workflows/substack_asset_generation_summary.md";
const HANDOFF_PATH = "content/logs/workflows/substack_asset_summary_handoff.json";

const resolvePath = (filePath) =>
  path.isAbsolute(filePath) ? filePath : path.join(ROOT, filePath);

const configuredInputPath = () =>
  process.env.SUBSTACK_ASSET_SUMMARY_PATH || DEFAULT_INPUT;

const readSummary = (sourcePath) => {
  const absolutePath = resolvePath(sourcePath);
  if (!fs.existsSync(absolutePath)) {
    throw new Error(`SUBSTACK_ASSET_SUMMARY_PATH not found: ${sourcePath}`);
  }

  const raw = fs.readFileSync(absolutePath, "utf8");
  if (!raw.trim()) {
    throw new Error(`Asset summary is empty: ${sourcePath}`);
  }

  try {
    return JSON.parse(raw);
  } catch (error) {
    throw new Error(`Asset summary is not valid JSON: ${error.message}`);
  }
};

const validateResult = (result, index) => {
  if (!result || typeof result !== "object" || Array.isArray(result)) {
    throw new Error(`results[${index}] must be an object.`);
  }

  for (const field of ["artifact_id", "mission_id", "title", "lane", "status"]) {
    if (!(field in result)) {
      throw new Error(`results[${index}] missing required field: ${field}`);
    }
  }

  if ("generated_files" in result && !Array.isArray(result.generated_files)) {
    throw new Error(`results[${index}].generated_files must be an array when present.`);
  }
};

const validateSummary = (summary) => {
  if (!summary || typeof summary !== "object" || Array.isArray(summary)) {
    throw new Error("Asset generation summary must be a JSON object.");
  }

  if (!Array.isArray(summary.results)) {
    throw new Error("Asset generation summary must include results[].");
  }

  summary.results.forEach(validateResult);

  if (summary.live_publish_attempted === true) {
    throw new Error("Refusing intake: source summary reports live_publish_attempted=true.");
  }

  if (summary.external_api_calls === true) {
    throw new Error("Refusing intake: source summary reports external_api_calls=true.");
  }
};

const routeForAsset = (asset) => {
  if (asset.skipped || asset.blocked_reason || asset.asset_state === "blocked") {
    return {
      next_action: "inspect_blocked_reason",
      queue: "blocked_asset_review",
      priority: 1
    };
  }

  if (asset.asset_state === "ready_for_distribution") {
    return {
      next_action: "approve_render_or_publish_queue_later",
      queue: "distribution_candidate_review",
      priority: 2
    };
  }

  if (asset.asset_state === "prepared") {
    return {
      next_action: "review_assets",
      queue: "prepared_assets_review",
      priority: 3
    };
  }

  return {
    next_action: "inspect_blocked_reason",
    queue: "blocked_asset_review",
    priority: 4
  };
};

const routeAssets = (summary) =>
  summary.results
    .map((asset) => {
      const route = routeForAsset(asset);
      return {
        artifact_id: asset.artifact_id,
        mission_id: asset.mission_id,
        title: asset.title,
        lane: asset.lane,
        status: asset.status,
        asset_state: asset.asset_state || (asset.skipped ? "skipped" : "unknown"),
        skipped: Boolean(asset.skipped),
        blocked_reason: asset.blocked_reason || "",
        generated_files: Array.isArray(asset.generated_files) ? asset.generated_files : [],
        next_action: route.next_action,
        queue: route.queue,
        route_priority: route.priority
      };
    })
    .sort((a, b) => {
      if (a.route_priority !== b.route_priority) return a.route_priority - b.route_priority;
      return a.title.localeCompare(b.title);
    });

const countBy = (items, key) =>
  items.reduce((counts, item) => {
    const value = item[key] || "unknown";
    counts[value] = (counts[value] || 0) + 1;
    return counts;
  }, {});

const writeJson = (filePath, payload) => {
  const absolutePath = resolvePath(filePath);
  fs.mkdirSync(path.dirname(absolutePath), { recursive: true });
  fs.writeFileSync(absolutePath, `${JSON.stringify(payload, null, 2)}\n`);
};

const writeReport = ({ sourcePath, summary, routedAssets }) => {
  const byQueue = countBy(routedAssets, "queue");
  const lines = [
    "# Substack Asset Generation Summary",
    "",
    `- Source: ${SOURCE}`,
    `- Source path: ${sourcePath}`,
    `- Total assets: ${routedAssets.length}`,
    `- Prepared: ${routedAssets.filter((asset) => asset.asset_state === "prepared").length}`,
    `- Ready for distribution: ${routedAssets.filter((asset) => asset.asset_state === "ready_for_distribution").length}`,
    `- Skipped / blocked: ${routedAssets.filter((asset) => asset.skipped || asset.blocked_reason).length}`,
    "- Live publishing: no",
    "- Rendering/audio/video generation in Mission Control: no",
    "- External API calls: no",
    "",
    "## Decision Queues",
    `- prepared_assets_review: ${byQueue.prepared_assets_review || 0}`,
    `- distribution_candidate_review: ${byQueue.distribution_candidate_review || 0}`,
    `- blocked_asset_review: ${byQueue.blocked_asset_review || 0}`,
    "",
    "## Routed Assets",
    ...routedAssets.map((asset) => [
      `### ${asset.title}`,
      "",
      `- Artifact ID: ${asset.artifact_id}`,
      `- Mission ID: ${asset.mission_id}`,
      `- Lane: ${asset.lane}`,
      `- Status: ${asset.status}`,
      `- Asset state: ${asset.asset_state}`,
      `- Queue: ${asset.queue}`,
      `- Next action: ${asset.next_action}`,
      `- Blocked reason: ${asset.blocked_reason || "none"}`,
      `- Asset files: ${asset.generated_files.length}`
    ].join("\n"))
  ];

  fs.writeFileSync(resolvePath(REPORT_PATH), `${lines.join("\n")}\n`);
};

const main = () => {
  const sourcePath = configuredInputPath();
  const summary = readSummary(sourcePath);
  validateSummary(summary);

  const routedAssets = routeAssets(summary);
  const handoff = {
    imported_at: new Date().toISOString(),
    source: SOURCE,
    source_path: sourcePath,
    summary_copy_path: SUMMARY_PATH,
    report_path: REPORT_PATH,
    raw_summary: summary,
    routing_summary: {
      total_assets: routedAssets.length,
      by_asset_state: countBy(routedAssets, "asset_state"),
      by_queue: countBy(routedAssets, "queue"),
      prepared_assets_review: routedAssets.filter((asset) => asset.queue === "prepared_assets_review").length,
      distribution_candidate_review: routedAssets.filter((asset) => asset.queue === "distribution_candidate_review").length,
      blocked_asset_review: routedAssets.filter((asset) => asset.queue === "blocked_asset_review").length
    },
    routed_assets: routedAssets,
    guardrails: {
      live_publish_attempted: false,
      rendering_attempted: false,
      audio_or_video_generated: false,
      external_api_calls: false,
      content_modified: false
    }
  };

  writeJson(SUMMARY_PATH, summary);
  writeJson(HANDOFF_PATH, handoff);
  writeReport({ sourcePath, summary, routedAssets });

  console.log(`Imported ${routedAssets.length} Substack asset records`);
  console.log(`prepared_assets_review=${handoff.routing_summary.prepared_assets_review}`);
  console.log(`distribution_candidate_review=${handoff.routing_summary.distribution_candidate_review}`);
  console.log(`blocked_asset_review=${handoff.routing_summary.blocked_asset_review}`);
  console.log(`Wrote ${SUMMARY_PATH}`);
  console.log(`Wrote ${REPORT_PATH}`);
  console.log(`Wrote ${HANDOFF_PATH}`);
};

try {
  main();
} catch (error) {
  console.error(`Substack asset summary import failed: ${error.message}`);
  process.exit(1);
}
