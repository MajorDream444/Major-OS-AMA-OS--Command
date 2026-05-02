#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const ROOT = process.cwd();
const DEFAULT_INPUT = "content/logs/workflows/asset_generation_summary.json";
const FALLBACK_INPUT = "fixtures/substack/asset_generation_summary.json";
const TARGET_JSON = "content/logs/workflows/asset_generation_intake.json";
const TARGET_MD = "content/logs/workflows/asset_generation_intake.md";
const VALID_DECISIONS = new Set([
  "hold",
  "review assets",
  "request rewrite",
  "approve for rendering queue later",
  "approve for publishing queue later"
]);

const resolvePath = (filePath) =>
  path.isAbsolute(filePath) ? filePath : path.join(ROOT, filePath);

const parseArgs = (argv) => {
  const args = { file: DEFAULT_INPUT, stdin: false };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === "--stdin") {
      args.stdin = true;
      args.file = "";
      continue;
    }
    if (arg === "--file") {
      args.file = argv[index + 1];
      index += 1;
      continue;
    }
    if (arg.startsWith("--file=")) {
      args.file = arg.slice("--file=".length);
    }
  }

  return args;
};

const readStdin = () =>
  new Promise((resolve, reject) => {
    let input = "";
    process.stdin.setEncoding("utf8");
    process.stdin.on("data", (chunk) => {
      input += chunk;
    });
    process.stdin.on("end", () => resolve(input));
    process.stdin.on("error", reject);
  });

const readJsonInput = async (args) => {
  if (args.stdin) {
    const raw = await readStdin();
    if (!raw.trim()) {
      throw new Error("Asset generation summary input is empty.");
    }
    return { payload: JSON.parse(raw), sourcePath: "stdin" };
  }

  let sourcePath = args.file;
  if (!fs.existsSync(resolvePath(sourcePath)) && args.file === DEFAULT_INPUT) {
    sourcePath = FALLBACK_INPUT;
  }

  const raw = fs.readFileSync(resolvePath(sourcePath), "utf8");
  if (!raw.trim()) {
    throw new Error("Asset generation summary input is empty.");
  }

  return { payload: JSON.parse(raw), sourcePath };
};

const extractResults = (payload) => {
  if (Array.isArray(payload)) return payload;
  if (Array.isArray(payload.results)) return payload.results;
  throw new Error("Asset generation summary must be an array or an object with results[].");
};

const generatedFileSet = (result) => new Set(Array.isArray(result.generated_files) ? result.generated_files : []);

const hasRequiredAssetFiles = (result) => {
  const files = generatedFileSet(result);
  return [
    "video_script.md",
    "voice_script.txt",
    "hooks.json",
    "visual_prompts.json",
    "distribution_plan.json",
    "asset_manifest.json"
  ].every((name) => Array.from(files).some((file) => file.endsWith(name)));
};

const nextDecisionForAsset = (result) => {
  if (result.skipped || result.blocked_reason) return "request rewrite";
  if (!hasRequiredAssetFiles(result)) return "hold";
  if (result.asset_state === "ready_for_distribution") return "approve for publishing queue later";
  if (result.asset_state === "prepared") return "approve for rendering queue later";
  return "review assets";
};

const rankForAsset = (result, decision) => {
  if (decision === "request rewrite") return 1;
  if (result.asset_state === "ready_for_distribution") return 2;
  if (result.asset_state === "prepared") return 3;
  if (decision === "review assets") return 4;
  return 5;
};

const normalizeResult = (result) => {
  if (!result || typeof result !== "object" || Array.isArray(result)) {
    throw new Error("Each asset result must be an object.");
  }

  const nextDecision = nextDecisionForAsset(result);
  if (!VALID_DECISIONS.has(nextDecision)) {
    throw new Error(`Invalid generated decision: ${nextDecision}`);
  }

  return {
    artifact_id: result.artifact_id || "",
    mission_id: result.mission_id || "",
    title: result.title || "Untitled asset artifact",
    lane: result.lane || "Operations",
    status: result.status || "unknown",
    asset_state: result.asset_state || "none",
    skipped: Boolean(result.skipped),
    blocked_reason: result.blocked_reason || "",
    generated_files: Array.isArray(result.generated_files) ? result.generated_files : [],
    next_decision: nextDecision,
    route_rank: rankForAsset(result, nextDecision),
    routing_note: routingNote(result, nextDecision)
  };
};

const routingNote = (result, decision) => {
  if (decision === "request rewrite") {
    return result.blocked_reason || "Asset generation skipped; route back for rewrite.";
  }
  if (decision === "approve for publishing queue later") {
    return "Assets are ready for later publishing queue approval. No live action now.";
  }
  if (decision === "approve for rendering queue later") {
    return "Assets are prepared for later render queue approval. No rendering now.";
  }
  if (decision === "hold") {
    return "Required asset files are incomplete; hold until the producer refreshes output.";
  }
  return "Review asset package before downstream routing.";
};

const countBy = (items, key) =>
  items.reduce((counts, item) => {
    const value = item[key] || "unknown";
    counts[value] = (counts[value] || 0) + 1;
    return counts;
  }, {});

const writeOutputs = ({ sourcePath, payload, routed }) => {
  const summary = {
    generated_at: new Date().toISOString(),
    source: "SUBSTACK_ENGINE",
    source_path: sourcePath,
    total_assets: routed.length,
    prepared: routed.filter((item) => item.asset_state === "prepared").length,
    ready_for_distribution: routed.filter((item) => item.asset_state === "ready_for_distribution").length,
    skipped: routed.filter((item) => item.skipped).length,
    by_next_decision: countBy(routed, "next_decision"),
    by_lane: countBy(routed, "lane"),
    live_publish_attempted: false,
    render_attempted: false,
    external_api_calls: false,
    routed_assets: routed
  };

  fs.mkdirSync(path.dirname(resolvePath(TARGET_JSON)), { recursive: true });
  fs.writeFileSync(resolvePath(TARGET_JSON), `${JSON.stringify(summary, null, 2)}\n`);

  const lines = [
    "# Asset Generation Intake",
    "",
    `- Source: SUBSTACK_ENGINE`,
    `- Source path: ${sourcePath}`,
    `- Total assets: ${summary.total_assets}`,
    `- Prepared: ${summary.prepared}`,
    `- Ready for distribution: ${summary.ready_for_distribution}`,
    `- Skipped: ${summary.skipped}`,
    "- Live publish attempted: no",
    "- Render attempted: no",
    "- External API calls: no",
    "",
    "## Next Decisions",
    ...Object.entries(summary.by_next_decision).map(([decision, count]) => `- ${decision}: ${count}`),
    "",
    "## Routed Assets",
    ...routed.map((item) => [
      `### ${item.title}`,
      "",
      `- Artifact ID: ${item.artifact_id}`,
      `- Mission ID: ${item.mission_id}`,
      `- Lane: ${item.lane}`,
      `- Asset state: ${item.asset_state}`,
      `- Route rank: ${item.route_rank}`,
      `- Next decision: ${item.next_decision}`,
      `- Routing note: ${item.routing_note}`,
      `- Generated files: ${item.generated_files.length ? item.generated_files.join(", ") : "none"}`
    ].join("\n"))
  ];

  fs.writeFileSync(resolvePath(TARGET_MD), `${lines.join("\n")}\n`);
};

const main = async () => {
  const args = parseArgs(process.argv.slice(2));
  const { payload, sourcePath } = await readJsonInput(args);
  const results = extractResults(payload);
  const routed = results.map(normalizeResult).sort((a, b) => {
    if (a.route_rank !== b.route_rank) return a.route_rank - b.route_rank;
    return a.title.localeCompare(b.title);
  });

  writeOutputs({
    sourcePath,
    payload,
    routed
  });

  const counts = countBy(routed, "next_decision");
  console.log(`Imported asset summary: ${routed.length} artifacts`);
  console.log(Object.entries(counts).map(([decision, count]) => `${decision}=${count}`).join(" "));
  console.log(`Wrote ${TARGET_JSON}`);
  console.log(`Wrote ${TARGET_MD}`);
};

main().catch((error) => {
  console.error(`Asset summary intake failed: ${error.message}`);
  process.exit(1);
});
