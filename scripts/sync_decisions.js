#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const ROOT = process.cwd();
const DEFAULT_INPUT = "content/logs/workflows/mission_control_decisions_export.json";
const TARGET_JSON = "content/logs/workflows/mission_control_decisions.json";
const TARGET_MD = "content/logs/workflows/mission_control_decisions.md";
const VALID_DECISIONS = new Set([
  "approved",
  "rejected",
  "rewrite_requested",
  "publish_requested"
]);

const requiredFields = [
  "decision_id",
  "artifact_id",
  "mission_id",
  "source",
  "decision",
  "decided_by",
  "decided_at",
  "reason",
  "next_action",
  "artifact_snapshot"
];

const requiredSnapshotFields = [
  "title",
  "lane",
  "score",
  "confidence",
  "risk_level",
  "publish_mode",
  "status"
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

  if (!args.stdin && !args.file) {
    throw new Error("Expected --file <path>, --stdin, or default export file.");
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
  const raw = args.stdin
    ? await readStdin()
    : fs.readFileSync(resolvePath(args.file), "utf8");

  if (!raw.trim()) {
    throw new Error("Decision export input is empty.");
  }

  return JSON.parse(raw);
};

const extractDecisions = (payload) => {
  if (Array.isArray(payload)) return payload;
  if (Array.isArray(payload.decisions)) return payload.decisions;
  throw new Error("Decision export must be an array or an object with decisions[].");
};

const validateDecision = (decision, index) => {
  if (!decision || typeof decision !== "object" || Array.isArray(decision)) {
    throw new Error(`Decision ${index} must be an object.`);
  }

  for (const field of requiredFields) {
    if (!(field in decision)) {
      throw new Error(`Decision ${index} missing required field: ${field}`);
    }
  }

  if (!VALID_DECISIONS.has(decision.decision)) {
    throw new Error(`Decision ${index} has invalid decision value: ${decision.decision}`);
  }

  if (
    !decision.artifact_snapshot ||
    typeof decision.artifact_snapshot !== "object" ||
    Array.isArray(decision.artifact_snapshot)
  ) {
    throw new Error(`Decision ${index} artifact_snapshot must be an object.`);
  }

  for (const field of requiredSnapshotFields) {
    if (!(field in decision.artifact_snapshot)) {
      throw new Error(`Decision ${index} artifact_snapshot missing required field: ${field}`);
    }
  }
};

const readExistingDecisions = () => {
  const targetPath = resolvePath(TARGET_JSON);
  if (!fs.existsSync(targetPath)) {
    return [];
  }

  const payload = JSON.parse(fs.readFileSync(targetPath, "utf8"));
  return extractDecisions(payload);
};

const countByType = (decisions) =>
  decisions.reduce((counts, decision) => {
    counts[decision.decision] = (counts[decision.decision] || 0) + 1;
    return counts;
  }, {});

const writeJson = (decisions) => {
  const targetPath = resolvePath(TARGET_JSON);
  fs.mkdirSync(path.dirname(targetPath), { recursive: true });
  fs.writeFileSync(targetPath, `${JSON.stringify({
    generated_at: new Date().toISOString(),
    mode: "local cli sync",
    target_path: TARGET_JSON,
    decisions
  }, null, 2)}\n`);
};

const writeMarkdownSummary = ({ decisions, added }) => {
  const counts = countByType(decisions);
  const latest = decisions[decisions.length - 1];
  const lines = [
    "# Mission Control Decisions",
    "",
    `- Total decisions: ${decisions.length}`,
    `- New decisions added: ${added.length}`,
    `- Approved count: ${counts.approved || 0}`,
    `- Rejected count: ${counts.rejected || 0}`,
    `- Rewrite requested count: ${counts.rewrite_requested || 0}`,
    `- Publish requested count: ${counts.publish_requested || 0}`,
    ""
  ];

  if (latest) {
    lines.push("## Latest Decision", "");
    lines.push(`- Decision ID: ${latest.decision_id}`);
    lines.push(`- Artifact ID: ${latest.artifact_id}`);
    lines.push(`- Decision: ${latest.decision}`);
    lines.push(`- Decided at: ${latest.decided_at}`);
    lines.push(`- Next action: ${latest.next_action}`);
    lines.push("");
  }

  lines.push("## By Decision Type", "");
  for (const value of VALID_DECISIONS) {
    lines.push(`- ${value}: ${counts[value] || 0}`);
  }
  lines.push("");

  const targetPath = resolvePath(TARGET_MD);
  fs.writeFileSync(targetPath, `${lines.join("\n")}\n`);
};

const main = async () => {
  const args = parseArgs(process.argv.slice(2));
  const incoming = extractDecisions(await readJsonInput(args));
  incoming.forEach(validateDecision);

  const existing = readExistingDecisions();
  existing.forEach(validateDecision);

  const seen = new Set(existing.map((decision) => decision.decision_id));
  const added = incoming.filter((decision) => {
    if (seen.has(decision.decision_id)) return false;
    seen.add(decision.decision_id);
    return true;
  });
  const decisions = [...existing, ...added];

  writeJson(decisions);
  writeMarkdownSummary({ decisions, added });

  const counts = countByType(decisions);
  console.log(`Synced decisions: ${decisions.length} total, ${added.length} new`);
  console.log(`approved=${counts.approved || 0} rejected=${counts.rejected || 0} rewrite_requested=${counts.rewrite_requested || 0} publish_requested=${counts.publish_requested || 0}`);
};

main().catch((error) => {
  console.error(`Decision sync failed: ${error.message}`);
  process.exit(1);
});
