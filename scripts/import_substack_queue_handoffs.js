#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const ROOT = process.cwd();
const SOURCE = "SUBSTACK_ENGINE";
const RENDER_ENV = "SUBSTACK_RENDER_QUEUE_HANDOFF_PATH";
const PUBLISH_ENV = "SUBSTACK_PUBLISH_QUEUE_HANDOFF_PATH";
const DEFAULT_RENDER = "content/logs/workflows/render_queue_handoff.json";
const DEFAULT_PUBLISH = "content/logs/workflows/publish_queue_handoff.json";
const RENDER_COPY = "content/logs/workflows/substack_render_queue_handoff.json";
const PUBLISH_COPY = "content/logs/workflows/substack_publish_queue_handoff.json";
const REPORT_PATH = "content/logs/workflows/substack_queue_handoffs.md";
const SUMMARY_PATH = "content/logs/workflows/substack_queue_handoffs_summary.json";

const resolvePath = (filePath) =>
  path.isAbsolute(filePath) ? filePath : path.join(ROOT, filePath);

const readJsonIfPresent = (filePath, label) => {
  const absolutePath = resolvePath(filePath);
  if (!fs.existsSync(absolutePath)) {
    return { present: false, path: filePath, payload: null };
  }

  const raw = fs.readFileSync(absolutePath, "utf8");
  if (!raw.trim()) {
    throw new Error(`${label} handoff is empty: ${filePath}`);
  }

  try {
    return { present: true, path: filePath, payload: JSON.parse(raw) };
  } catch (error) {
    throw new Error(`${label} handoff is not valid JSON: ${error.message}`);
  }
};

const validateHandoff = (payload, label) => {
  if (!payload || typeof payload !== "object" || Array.isArray(payload)) {
    throw new Error(`${label} handoff must be a JSON object.`);
  }
  if (!Array.isArray(payload.queue_items)) {
    throw new Error(`${label} handoff must include queue_items[].`);
  }
  if (payload.live_publish_attempted === true) {
    throw new Error(`Refusing ${label} intake: live_publish_attempted=true.`);
  }
  if (payload.render_attempted === true) {
    throw new Error(`Refusing ${label} intake: render_attempted=true.`);
  }
  if (payload.external_api_calls === true) {
    throw new Error(`Refusing ${label} intake: external_api_calls=true.`);
  }
};

const normalizeItem = (item, queueType) => {
  if (!item || typeof item !== "object" || Array.isArray(item)) {
    throw new Error(`${queueType} queue item must be an object.`);
  }

  return {
    queue_type: queueType,
    artifact_id: item.artifact_id || "",
    mission_id: item.mission_id || "",
    title: item.title || "Untitled queue item",
    lane: item.lane || "Operations",
    recommended_renderer: item.recommended_renderer || "",
    recommended_platforms: Array.isArray(item.recommended_platforms) ? item.recommended_platforms : [],
    source_asset_folder: item.source_asset_folder || "",
    execution_mode: "local_only",
    next_action: queueType === "render" ? "review_render_candidate" : "review_publish_candidate",
    status: item.render_status || item.publish_status || item.status || "queued",
    queue_id: item.render_queue_id || item.publish_queue_id || "",
    raw_item: item
  };
};

const skippedCount = (handoff) =>
  Array.isArray(handoff?.skipped_candidates) ? handoff.skipped_candidates.length : 0;

const writeJson = (filePath, payload) => {
  const absolutePath = resolvePath(filePath);
  fs.mkdirSync(path.dirname(absolutePath), { recursive: true });
  fs.writeFileSync(absolutePath, `${JSON.stringify(payload, null, 2)}\n`);
};

const writeReport = ({ render, publish, summary }) => {
  const lines = [
    "# Substack Queue Handoffs",
    "",
    `- Source: ${SOURCE}`,
    `- Render handoff present: ${render.present ? "yes" : "no"}`,
    `- Publish handoff present: ${publish.present ? "yes" : "no"}`,
    `- Render queue count: ${summary.render_queue_count}`,
    `- Publish queue count: ${summary.publish_queue_count}`,
    `- Blocked / skipped count: ${summary.blocked_skipped_count}`,
    "- Live publishing: no",
    "- Rendering: no",
    "- External API calls: no",
    "",
    "## Queue Items",
    ...summary.items.map((item) => [
      `### ${item.title}`,
      "",
      `- Queue type: ${item.queue_type}`,
      `- Artifact ID: ${item.artifact_id}`,
      `- Mission ID: ${item.mission_id}`,
      `- Lane: ${item.lane}`,
      `- Recommended renderer: ${item.recommended_renderer || "none"}`,
      `- Recommended platforms: ${item.recommended_platforms.length ? item.recommended_platforms.join(", ") : "none"}`,
      `- Source asset folder: ${item.source_asset_folder || "none"}`,
      `- Execution mode: ${item.execution_mode}`,
      `- Next action: ${item.next_action}`
    ].join("\n"))
  ];

  if (!summary.items.length) {
    lines.push("- No queue candidates imported.");
  }

  fs.writeFileSync(resolvePath(REPORT_PATH), `${lines.join("\n")}\n`);
};

const main = () => {
  const renderPath = process.env[RENDER_ENV] || DEFAULT_RENDER;
  const publishPath = process.env[PUBLISH_ENV] || DEFAULT_PUBLISH;
  const render = readJsonIfPresent(renderPath, "render");
  const publish = readJsonIfPresent(publishPath, "publish");

  if (!render.present && !publish.present) {
    throw new Error("No Substack render or publish queue handoff files found.");
  }

  if (render.present) validateHandoff(render.payload, "render");
  if (publish.present) validateHandoff(publish.payload, "publish");

  const renderItems = render.present
    ? render.payload.queue_items.map((item) => normalizeItem(item, "render"))
    : [];
  const publishItems = publish.present
    ? publish.payload.queue_items.map((item) => normalizeItem(item, "publish"))
    : [];

  if (render.present) writeJson(RENDER_COPY, render.payload);
  if (publish.present) writeJson(PUBLISH_COPY, publish.payload);

  const summary = {
    imported_at: new Date().toISOString(),
    source: SOURCE,
    render_source_path: render.present ? render.path : "",
    publish_source_path: publish.present ? publish.path : "",
    render_copy_path: render.present ? RENDER_COPY : "",
    publish_copy_path: publish.present ? PUBLISH_COPY : "",
    render_queue_count: renderItems.length,
    publish_queue_count: publishItems.length,
    blocked_skipped_count: skippedCount(render.payload) + skippedCount(publish.payload),
    execution_mode: "local_only",
    live_publish_attempted: false,
    render_attempted: false,
    external_api_calls: false,
    raw_handoffs: {
      render: render.payload,
      publish: publish.payload
    },
    items: [...renderItems, ...publishItems]
  };

  writeJson(SUMMARY_PATH, summary);
  writeReport({ render, publish, summary });

  console.log(`Imported Substack queue handoffs: render=${summary.render_queue_count} publish=${summary.publish_queue_count} blocked_skipped=${summary.blocked_skipped_count}`);
  console.log(`Wrote ${SUMMARY_PATH}`);
  console.log(`Wrote ${REPORT_PATH}`);
};

try {
  main();
} catch (error) {
  console.error(`Substack queue handoff import failed: ${error.message}`);
  process.exit(1);
}
