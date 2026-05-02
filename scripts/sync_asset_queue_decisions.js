#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const ROOT = process.cwd();
const DEFAULT_INPUT = "content/logs/workflows/asset_queue_decisions_export.json";
const TARGET_JSON = "content/logs/workflows/asset_queue_decisions.json";
const TARGET_MD = "content/logs/workflows/asset_queue_decisions.md";
const VALID_DECISIONS = new Set([
  "hold",
  "review_assets",
  "request_asset_rewrite",
  "approve_for_render_queue",
  "approve_for_publish_queue_later",
  "block_asset"
]);
const REQUIRED_FIELDS = [
  "asset_decision_id",
  "artifact_id",
  "mission_id",
  "title",
  "lane",
  "asset_state",
  "decision",
  "decided_by",
  "decided_at",
  "reason",
  "source",
  "execution_mode"
];

const resolvePath = (filePath) =>
  path.isAbsolute(filePath) ? filePath : path.join(ROOT, filePath);

const parseArgs = (argv) => {
  const args = { file: DEFAULT_INPUT, stdin: false };
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === "--stdin") {
      args.stdin = true;
      args.file = "";
    } else if (arg === "--file") {
      args.file = argv[index + 1];
      index += 1;
    } else if (arg.startsWith("--file=")) {
      args.file = arg.slice("--file=".length);
    }
  }
  return args;
};

const readStdin = () =>
  new Promise((resolve, reject) => {
    let input = "";
    process.stdin.setEncoding("utf8");
    process.stdin.on("data", (chunk) => { input += chunk; });
    process.stdin.on("end", () => resolve(input));
    process.stdin.on("error", reject);
  });

const readInput = async (args) => {
  const raw = args.stdin
    ? await readStdin()
    : fs.readFileSync(resolvePath(args.file), "utf8");
  if (!raw.trim()) throw new Error("Asset queue decision input is empty.");
  return JSON.parse(raw);
};

const extractDecisions = (payload) => {
  if (Array.isArray(payload)) return payload;
  if (Array.isArray(payload.decisions)) return payload.decisions;
  throw new Error("Asset queue decision input must be an array or object with decisions[].");
};

const validateDecision = (decision, index) => {
  if (!decision || typeof decision !== "object" || Array.isArray(decision)) {
    throw new Error(`Decision ${index} must be an object.`);
  }
  for (const field of REQUIRED_FIELDS) {
    if (!(field in decision)) throw new Error(`Decision ${index} missing field: ${field}`);
  }
  if (!VALID_DECISIONS.has(decision.decision)) {
    throw new Error(`Decision ${index} has invalid value: ${decision.decision}`);
  }
  if (decision.source !== "MISSION_CONTROL") {
    throw new Error(`Decision ${index} source must be MISSION_CONTROL.`);
  }
  if (decision.execution_mode !== "local_only") {
    throw new Error(`Decision ${index} execution_mode must be local_only.`);
  }
};

const readExisting = () => {
  const target = resolvePath(TARGET_JSON);
  if (!fs.existsSync(target)) return [];
  return extractDecisions(JSON.parse(fs.readFileSync(target, "utf8")));
};

const countByDecision = (decisions) =>
  decisions.reduce((counts, decision) => {
    counts[decision.decision] = (counts[decision.decision] || 0) + 1;
    return counts;
  }, {});

const writeOutputs = (decisions, added) => {
  const generatedAt = new Date().toISOString();
  const counts = countByDecision(decisions);
  const latest = decisions[decisions.length - 1];

  fs.mkdirSync(path.dirname(resolvePath(TARGET_JSON)), { recursive: true });
  fs.writeFileSync(resolvePath(TARGET_JSON), `${JSON.stringify({
    generated_at: generatedAt,
    mode: "local_only",
    target_path: TARGET_JSON,
    decisions
  }, null, 2)}\n`);

  const lines = [
    "# Asset Queue Decisions",
    "",
    `- Total decisions: ${decisions.length}`,
    `- New decisions added: ${added.length}`,
    "- Execution mode: local_only",
    "- Live publishing: no",
    "- Rendering: no",
    "- External API calls: no",
    "",
    "## Counts",
    ...Array.from(VALID_DECISIONS).map((decision) => `- ${decision}: ${counts[decision] || 0}`),
    ""
  ];
  if (latest) {
    lines.push("## Latest Decision", "");
    lines.push(`- Asset decision ID: ${latest.asset_decision_id}`);
    lines.push(`- Artifact ID: ${latest.artifact_id}`);
    lines.push(`- Decision: ${latest.decision}`);
    lines.push(`- Decided at: ${latest.decided_at}`);
    lines.push(`- Reason: ${latest.reason || "none"}`);
    lines.push("");
  }

  fs.writeFileSync(resolvePath(TARGET_MD), `${lines.join("\n")}\n`);
};

const main = async () => {
  const args = parseArgs(process.argv.slice(2));
  const incoming = extractDecisions(await readInput(args));
  incoming.forEach(validateDecision);
  const existing = readExisting();
  existing.forEach(validateDecision);

  const seen = new Set(existing.map((decision) => decision.asset_decision_id));
  const added = incoming.filter((decision) => {
    if (seen.has(decision.asset_decision_id)) return false;
    seen.add(decision.asset_decision_id);
    return true;
  });
  const decisions = [...existing, ...added];
  writeOutputs(decisions, added);
  console.log(`Synced asset queue decisions: ${decisions.length} total, ${added.length} new`);
};

main().catch((error) => {
  console.error(`Asset queue decision sync failed: ${error.message}`);
  process.exit(1);
});
