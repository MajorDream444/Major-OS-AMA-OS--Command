const STORAGE_KEY = "major-os-command-center-state-v1";

const mediaStages = [
  "Raw Thought",
  "Draft",
  "Edit",
  "Publish",
  "Hooks",
  "Video Script",
  "Remotion Queue",
  "HeyGen Queue",
  "Distribution",
  "Memory Update"
];

const missionLanes = ["INBOX", "RUNNING", "NEEDS MAJOR", "REVIEW", "DONE", "BLOCKED"];

const missionStatusLanes = ["PLANNED", "RUNNING", "NEEDS MAJOR", "REVIEW", "DONE", "BLOCKED"];

const missionIntentRules = [
  { intent: "lead_generation", pattern: /\b(lead|find|scout|contour leads|saf leads)\b/i },
  { intent: "audit", pattern: /\b(audit|diagnose|review business)\b/i },
  { intent: "content_media", pattern: /\b(content|substack|article|video|remotion|heygen)\b/i },
  { intent: "outreach", pattern: /\b(email|outreach|follow up|dm)\b/i },
  { intent: "commerce", pattern: /\b(shopify|gumroad|product|store)\b/i },
  { intent: "operations", pattern: /\b(daily brief|report|status)\b/i }
];

const orchestratorPlans = {
  lead_generation: [
    "Identify lead source",
    "Qualify lead fit",
    "Draft outreach angle",
    "Ask Major for review"
  ],
  audit: [
    "Review business context",
    "Diagnose operating gaps",
    "Summarize blockers",
    "Ask Major for review"
  ],
  content_media: [
    "Capture core idea",
    "Draft content angle",
    "Prepare video/script route",
    "Ask Major for review"
  ],
  outreach: [
    "Review target context",
    "Draft message",
    "Ask Major before sending"
  ],
  commerce: [
    "Identify product/offer",
    "Draft listing/action plan",
    "Ask Major for review"
  ],
  operations: [
    "Review system state",
    "Summarize status",
    "Recommend next action"
  ]
};

const orchestratorAgentMap = {
  lead_generation: ["A001", "A002", "A006"],
  audit: ["A002", "A004"],
  content_media: ["A003", "A007"],
  outreach: ["A006", "A002"],
  commerce: ["A009", "A007"],
  operations: ["A004"]
};

const seedState = {
  unread: 3,
  missionId: 0,
  heartbeatVisible: false,
  needsMajor: null,
  commands: [],
  githubLogsHighlighted: false,
  agentRegistryHighlighted: false,
  mediaEngineHighlighted: false,
  distributionHighlighted: false,
  missionBoardHighlighted: false,
  skillRequestsHighlighted: false,
  leads: [
    {
      name: "Systems audit inquiry",
      lane: "CONTOUR",
      priority: "HIGH",
      status: "ACTIVE",
      note: "Lead classified -> Contour"
    },
    {
      name: "Creator product lead",
      lane: "BWYH",
      priority: "MED",
      status: "QUEUED",
      note: "Dossier created"
    },
    {
      name: "Local service operator",
      lane: "SAF",
      priority: "LOW",
      status: "REVIEW",
      note: "Follow-up due"
    }
  ],
  actions: [
    {
      label: "ACTION",
      title: "Lock boot scaffold",
      next: "Mock data only",
      agent: "A004 Ops Watcher"
    },
    {
      label: "HIGH",
      title: "Package first money workflow",
      next: "Content -> Product -> Sale",
      agent: "A007 Offer Builder"
    },
    {
      label: "REVIEW",
      title: "Map new app ideas",
      next: "GitHub / Airtable / Notion",
      agent: "A004 Ops Watcher"
    }
  ],
  missions: [
    {
      id: "M-SEED-001",
      title: "Review Contour lead queue",
      command: "Review Contour lead queue",
      intent: "lead_generation",
      assigned_agent: "A001 Scout",
      assigned_agents: ["A001 Scout", "A002 Audit", "A006 Outreach"],
      status: "REVIEW",
      created_at: "2026-04-26T09:00:00.000Z",
      updated_at: "2026-04-26T09:03:00.000Z",
      plan: orchestratorPlans.lead_generation,
      current_step: "Ask Major for review",
      steps_completed: 3,
      next_action: "Major approves outreach angle",
      needs_major: true,
      output_summary: "Lead queue prepared for Major review",
      artifacts_count: 1,
      last_event: "Lead packet attached",
      thread: [
        {
          timestamp: "08:59",
          event: "Mission card created",
          agent: "A001 Scout",
          status: "INBOX",
          artifact: ""
        },
        {
          timestamp: "09:00",
          event: "Mission moved to Running",
          agent: "A001 Scout",
          status: "RUNNING",
          artifact: ""
        },
        {
          timestamp: "09:03",
          event: "Lead packet attached",
          agent: "A001 Scout",
          status: "REVIEW",
          artifact: "local lead packet"
        }
      ]
    },
    {
      id: "M-SEED-002",
      title: "Draft Substack authority note",
      command: "Draft Substack authority note",
      intent: "content_media",
      assigned_agent: "A003 Content Catcher",
      assigned_agents: ["A003 Content Catcher", "A007 Offer Builder"],
      status: "RUNNING",
      created_at: "2026-04-26T09:05:00.000Z",
      updated_at: "2026-04-26T09:06:00.000Z",
      plan: orchestratorPlans.content_media,
      current_step: "Draft content angle",
      steps_completed: 1,
      next_action: "Turn draft into media handoff",
      needs_major: false,
      output_summary: "Content mission in local simulation",
      artifacts_count: 0,
      last_event: "Content Catcher working...",
      thread: [
        {
          timestamp: "09:05",
          event: "Mission card created",
          agent: "A003 Content Catcher",
          status: "INBOX",
          artifact: ""
        },
        {
          timestamp: "09:06",
          event: "Mission moved to Running",
          agent: "A003 Content Catcher",
          status: "RUNNING",
          artifact: ""
        }
      ]
    }
  ],
  skillRequests: [
    {
      proposed_by: "A004 Ops Watcher",
      skill_name: "daily handoff summarizer",
      why_needed: "Reduce repeated operator context loading",
      input: "mission threads and activity feed",
      output: "daily GitHub-ready handoff",
      risk: "LOW",
      status: "REVIEW"
    }
  ],
  dailyBrief: [
    {
      label: "REVENUE ACTION",
      status: "ACTION",
      title: "Send Contour offer follow-up",
      owner: "A006 Outreach",
      next: "Move one warm lead toward call"
    },
    {
      label: "CONTENT ACTION",
      status: "READY",
      title: "Draft Substack authority note",
      owner: "A003 Content Catcher",
      next: "Publish one operating insight"
    },
    {
      label: "SYSTEM IMPROVEMENT",
      status: "DONE",
      title: "Add Daily Brief protocol",
      owner: "A004 Ops Watcher",
      next: "Log system improvement in GitHub"
    },
    {
      label: "BLOCKER",
      status: "REVIEW",
      title: "Choose first live sync target",
      owner: "Major",
      next: "Approve Airtable or Notion first"
    }
  ],
  githubLogs: [
    {
      title: "Latest commit: Persist command center local state",
      repo: "MajorDream444/Major-OS-AMA-OS--Command",
      path: "main@f700b0a",
      type: "commit",
      status: "SYNCED",
      timestamp: "2026-04-27 19:48",
      next: "Add local GitHub Logs panel"
    },
    {
      title: "Daily brief protocol",
      repo: "MajorDream444/Major-OS-AMA-OS--Command",
      path: "docs/DAILY_BRIEF_PROTOCOL.md",
      type: "doc",
      status: "SYNCED",
      timestamp: "2026-04-26 10:24",
      next: "Use as daily operating loop"
    },
    {
      title: "Agent logging standard",
      repo: "MajorDream444/Major-OS-AMA-OS--Command",
      path: "docs/AGENT_LOGGING_STANDARD.md",
      type: "doc",
      status: "SYNCED",
      timestamp: "2026-04-26 10:24",
      next: "Apply to future agent events"
    },
    {
      title: "System map",
      repo: "MajorDream444/Major-OS-AMA-OS--Command",
      path: "docs/SYSTEM_MAP.md",
      type: "doc",
      status: "NEEDS REVIEW",
      timestamp: "2026-04-26 10:24",
      next: "Add GitHub logs read path"
    },
    {
      title: "Handoff command center",
      repo: "MajorDream444/Major-OS-AMA-OS--Command",
      path: "HANDOFF_COMMAND_CENTER.md",
      type: "handoff",
      status: "STALE",
      timestamp: "2026-04-26 08:53",
      next: "Refresh after persistence and log panels"
    },
    {
      title: "Local persistence commit",
      repo: "MajorDream444/Major-OS-AMA-OS--Command",
      path: "f700b0a Persist command center local state",
      type: "commit",
      status: "SYNCED",
      timestamp: "2026-04-27 19:48",
      next: "Verify state survival after refresh"
    }
  ],
  mediaWorkflow: [
    {
      title: "AI Was Never Invented",
      lane: "Doctrine",
      stage: "Raw Thought",
      next_action: "Capture thesis as Substack draft",
      assigned_agent: "A003 Content Catcher",
      status: "READY"
    },
    {
      title: "Your Business Is the Bottleneck",
      lane: "Contour",
      stage: "Draft",
      next_action: "Editorial polish",
      assigned_agent: "A003 Content Catcher",
      status: "ACTION"
    },
    {
      title: "Build While You Heal: System Before Scale",
      lane: "BWYH",
      stage: "Hooks",
      next_action: "Turn hooks into video script",
      assigned_agent: "A003 Content Catcher",
      status: "REVIEW"
    }
  ],
  distributionQueue: [
    {
      title: "AI Was Never Invented",
      lane: "Doctrine",
      channel: "Substack",
      asset_type: "article",
      status: "READY",
      next_action: "Review local publish handoff",
      owner_agent: "A003 Content Catcher"
    },
    {
      title: "Your Business Is the Bottleneck",
      lane: "Contour",
      channel: "LinkedIn",
      asset_type: "hook",
      status: "NEEDS REVIEW",
      next_action: "Approve authority hook",
      owner_agent: "A003 Content Catcher"
    },
    {
      title: "Build While You Heal: System Before Scale",
      lane: "BWYH",
      channel: "YouTube Shorts",
      asset_type: "short script",
      status: "READY",
      next_action: "Queue local short script",
      owner_agent: "A003 Content Catcher"
    }
  ],
  pipelines: {
    bwyh: [
      ["Lead capture", "ACTIVE", 70],
      ["Offer framing", "REVIEW", 45],
      ["Follow-up assets", "QUEUED", 25]
    ],
    contour: [
      ["Intake", "ACTIVE", 40],
      ["Diagnostic", "QUEUED", 30],
      ["Client dashboard", "BLOCKED", 15]
    ],
    saf: [
      ["Audience segment", "READY", 55],
      ["Score review", "REVIEW", 35],
      ["Campaign handoff", "QUEUED", 20]
    ]
  },
  apps: [
    {
      name: "Command Center",
      status: "ACTIVE",
      priority: "P1",
      repo: "Major-OS-AMA-OS--Command",
      next: "Live runtime simulation"
    },
    {
      name: "Major AI OS",
      status: "READY",
      priority: "P1",
      repo: "Major-AI-OS",
      next: "Reference reusable skills"
    },
    {
      name: "52in52 Tracker",
      status: "QUEUED",
      priority: "P2",
      repo: "52in52",
      next: "Registry alignment"
    }
  ],
  agents: [
    {
      id: "A001",
      name: "Scout",
      role: "Lead discovery",
      status: "IDLE",
      current_task: "",
      last_event: "Standing by",
      needs_major: false,
      tools: ["local leads", "mock search"],
      workflow: "Find -> qualify -> queue"
    },
    {
      id: "A002",
      name: "Audit",
      role: "Diagnostic review",
      status: "READY",
      current_task: "",
      last_event: "Ready for diagnosis",
      needs_major: false,
      tools: ["local checklist", "mock score"],
      workflow: "Intake -> diagnose -> flag"
    },
    {
      id: "A003",
      name: "Content Catcher",
      role: "Content and media drafting",
      status: "IDLE",
      current_task: "",
      last_event: "Standing by",
      needs_major: false,
      tools: ["local brief", "mock media plan"],
      workflow: "Capture -> draft -> repurpose"
    },
    {
      id: "A004",
      name: "Ops Watcher",
      role: "Registry and system monitor",
      status: "READY",
      current_task: "",
      last_event: "Monitoring local runtime",
      needs_major: false,
      tools: ["localStorage", "mock logs"],
      workflow: "Observe -> log -> escalate"
    },
    {
      id: "A005",
      name: "Grant Hunter",
      role: "Opportunity scan",
      status: "IDLE",
      current_task: "",
      last_event: "Standing by",
      needs_major: false,
      tools: ["mock grants", "local notes"],
      workflow: "Scan -> shortlist -> review"
    },
    {
      id: "A006",
      name: "Outreach",
      role: "Follow-up and messaging",
      status: "READY",
      current_task: "",
      last_event: "Ready for follow-up",
      needs_major: false,
      tools: ["local contacts", "mock email"],
      workflow: "Draft -> review -> send later"
    },
    {
      id: "A007",
      name: "Offer Builder",
      role: "Offer packaging",
      status: "IDLE",
      current_task: "",
      last_event: "Standing by",
      needs_major: false,
      tools: ["local offers", "mock pricing"],
      workflow: "Frame -> package -> handoff"
    },
    {
      id: "A008",
      name: "Deck Builder",
      role: "Presentation planning",
      status: "IDLE",
      current_task: "",
      last_event: "Standing by",
      needs_major: false,
      tools: ["local outline", "mock slides"],
      workflow: "Outline -> structure -> review"
    },
    {
      id: "A009",
      name: "Storefront Operator",
      role: "Commerce setup",
      status: "IDLE",
      current_task: "",
      last_event: "Standing by",
      needs_major: false,
      tools: ["mock products", "local offer data"],
      workflow: "Product -> page -> review"
    },
    {
      id: "A010",
      name: "Meeting Synthesizer",
      role: "Meeting memory",
      status: "READY",
      current_task: "",
      last_event: "Ready to summarize",
      needs_major: false,
      tools: ["local notes", "mock transcript"],
      workflow: "Capture -> summarize -> log"
    }
  ],
  activity: [
    { time: "08:58", item: "Lead classified -> Contour", label: "ACTIVE", heartbeat: false },
    { time: "08:57", item: "Dossier created", label: "READY", heartbeat: false },
    { time: "08:56", item: "Follow-up due", label: "ACTION", heartbeat: false },
    { time: "08:55", item: "Airtable sync OK", label: "SYNCED", heartbeat: false },
    { time: "08:54", item: "BWYH lane queued", label: "QUEUED", heartbeat: false },
    { time: "08:53", item: "Storefront operator blocked", label: "BLOCKED", heartbeat: false }
  ]
};

let state;

const cloneState = (value) => JSON.parse(JSON.stringify(value));

const normalizeAgent = (agent, seedAgent) => ({
  ...seedAgent,
  ...agent,
  role: agent.role || seedAgent.role,
  current_task: agent.current_task || "",
  last_event: agent.last_event || seedAgent.last_event,
  needs_major: Boolean(agent.needs_major),
  tools: Array.isArray(agent.tools) ? agent.tools : seedAgent.tools,
  workflow: agent.workflow || seedAgent.workflow
});

const normalizeMission = (mission) => {
  const intent = mission.intent || "operations";
  const plan = Array.isArray(mission.plan) && mission.plan.length
    ? mission.plan
    : (orchestratorPlans[intent] || orchestratorPlans.operations);
  const assignedAgents = Array.isArray(mission.assigned_agents)
    ? mission.assigned_agents
    : (mission.assigned_agent ? [mission.assigned_agent] : ["A004 Ops Watcher"]);

  return {
    id: mission.id,
    command: mission.command || mission.title || "Untitled mission",
    title: mission.title || mission.command || "Untitled mission",
    intent,
    status: mission.status || "PLANNED",
    created_at: mission.created_at || new Date().toISOString(),
    updated_at: mission.updated_at || mission.created_at || new Date().toISOString(),
    assigned_agent: mission.assigned_agent || assignedAgents[0],
    assigned_agents: assignedAgents,
    plan,
    current_step: mission.current_step || plan[0] || "Review system state",
    steps_completed: Number.isFinite(mission.steps_completed) ? mission.steps_completed : 0,
    next_action: mission.next_action || "Run local mission simulation",
    needs_major: Boolean(mission.needs_major),
    output_summary: mission.output_summary || "Local mission state",
    artifacts_count: Number.isFinite(mission.artifacts_count) ? mission.artifacts_count : 0,
    last_event: mission.last_event || "Mission planned",
    thread: Array.isArray(mission.thread) ? mission.thread : []
  };
};

const mergeSeedState = (savedState) => {
  const merged = {
    ...cloneState(seedState),
    ...savedState
  };

  merged.commands = Array.isArray(savedState.commands) ? savedState.commands : [];
  merged.githubLogs = Array.isArray(savedState.githubLogs) ? savedState.githubLogs : cloneState(seedState.githubLogs);
  merged.githubLogsHighlighted = Boolean(savedState.githubLogsHighlighted);
  merged.agentRegistryHighlighted = Boolean(savedState.agentRegistryHighlighted);
  merged.mediaEngineHighlighted = Boolean(savedState.mediaEngineHighlighted);
  merged.mediaWorkflow = Array.isArray(savedState.mediaWorkflow) ? savedState.mediaWorkflow : cloneState(seedState.mediaWorkflow);
  merged.distributionHighlighted = Boolean(savedState.distributionHighlighted);
  merged.distributionQueue = Array.isArray(savedState.distributionQueue) ? savedState.distributionQueue : cloneState(seedState.distributionQueue);
  merged.missionBoardHighlighted = Boolean(savedState.missionBoardHighlighted);
  merged.skillRequestsHighlighted = Boolean(savedState.skillRequestsHighlighted);
  merged.missions = (Array.isArray(savedState.missions) ? savedState.missions : cloneState(seedState.missions))
    .map(normalizeMission);
  merged.skillRequests = Array.isArray(savedState.skillRequests) ? savedState.skillRequests : cloneState(seedState.skillRequests);
  merged.leads = Array.isArray(savedState.leads) ? savedState.leads : cloneState(seedState.leads);
  merged.actions = Array.isArray(savedState.actions) ? savedState.actions : cloneState(seedState.actions);
  merged.dailyBrief = Array.isArray(savedState.dailyBrief) ? savedState.dailyBrief : cloneState(seedState.dailyBrief);
  merged.pipelines = savedState.pipelines || cloneState(seedState.pipelines);
  merged.apps = Array.isArray(savedState.apps) ? savedState.apps : cloneState(seedState.apps);
  merged.agents = cloneState(seedState.agents).map((seedAgent) => {
    const savedAgent = Array.isArray(savedState.agents)
      ? savedState.agents.find((agent) => agent.id === seedAgent.id)
      : null;
    return normalizeAgent(savedAgent || {}, seedAgent);
  });
  merged.activity = Array.isArray(savedState.activity) ? savedState.activity : cloneState(seedState.activity);
  merged.unread = Number.isFinite(savedState.unread) ? savedState.unread : seedState.unread;
  merged.missionId = Number.isFinite(savedState.missionId) ? savedState.missionId : seedState.missionId;
  merged.needsMajor = savedState.needsMajor || null;

  return merged;
};

const saveState = () => {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch (error) {
    console.warn("Local state save failed", error);
  }
};

const loadState = () => {
  try {
    const savedState = localStorage.getItem(STORAGE_KEY);
    if (!savedState) {
      const seededState = cloneState(seedState);
      localStorage.setItem(STORAGE_KEY, JSON.stringify(seededState));
      return seededState;
    }

    return mergeSeedState(JSON.parse(savedState));
  } catch (error) {
    console.warn("Local state load failed; using seed state", error);
    return cloneState(seedState);
  }
};

state = loadState();

const routes = [
  { pattern: /\b(lead|find|scout)\b/i, agentId: "A001" },
  { pattern: /\b(audit|diagnose)\b/i, agentId: "A002" },
  { pattern: /\b(content|video|remotion|heygen|substack|article|essay|draft|newsletter|avatar)\b/i, agentId: "A003" },
  { pattern: /\b(email|outreach|follow up)\b/i, agentId: "A006" },
  { pattern: /\b(shopify|gumroad|store|product)\b/i, agentId: "A009" }
];

const githubLogCommandPattern = /\b(show github logs|check repo logs|what changed)\b/i;
const agentRegistryCommandPattern = /\bshow agents\b/i;
const missionBoardCommandPattern = /\bshow missions\b/i;
const mediaWorkflowCommandPattern = /\b(draft substack|make video from|queue remotion|queue heygen|publish)\b/i;
const distributionCommandPattern = /\b(distribute|send to x|send to substack|save to memory)\b/i;
const skillRequestCommandPattern = /^propose skill\s+(.+)$/i;

const escapeHtml = (value) =>
  String(value).replace(/[&<>"']/g, (char) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    "\"": "&quot;",
    "'": "&#39;"
  })[char]);

const labelClass = (label) => `signal ${String(label).toLowerCase()}`;
const agentLabel = (agent) => `${agent.id} ${agent.name}`;

const nowStamp = () =>
  new Intl.DateTimeFormat("en-US", {
    hour: "2-digit",
    minute: "2-digit",
    hour12: false
  }).format(new Date());

const findAgent = (agentId) => state.agents.find((agent) => agent.id === agentId);

const detectMissionIntent = (command) => {
  const match = missionIntentRules.find((rule) => rule.pattern.test(command));
  return match ? match.intent : "operations";
};

const agentLabelsForIntent = (intent) =>
  (orchestratorAgentMap[intent] || orchestratorAgentMap.operations)
    .map(findAgent)
    .filter(Boolean)
    .map(agentLabel);

const agentsForIntent = (intent) =>
  (orchestratorAgentMap[intent] || orchestratorAgentMap.operations)
    .map(findAgent)
    .filter(Boolean);

const createOrchestratorMission = (mission, command) => {
  const intent = detectMissionIntent(command);
  const now = new Date().toISOString();
  const plan = orchestratorPlans[intent] || orchestratorPlans.operations;
  const assignedAgents = agentLabelsForIntent(intent);

  return {
    id: mission.id,
    command,
    title: command,
    intent,
    status: "PLANNED",
    created_at: now,
    updated_at: now,
    assigned_agent: assignedAgents[0],
    assigned_agents: assignedAgents,
    plan,
    current_step: plan[0],
    steps_completed: 0,
    next_action: plan[0],
    needs_major: false,
    output_summary: "Mission planned locally",
    artifacts_count: 0,
    last_event: "Mission created",
    thread: []
  };
};

const routeCommand = (command) => {
  const match = routes.find((route) => route.pattern.test(command));
  return findAgent(match ? match.agentId : "A004");
};

const shouldRequestReview = (command, missionId) =>
  /\b(review|major|approve|diagnose|audit|contour)\b/i.test(command) || missionId % 3 === 0;

const logSubmittedCommand = (mission, command, agent) => {
  state.commands.unshift({
    id: mission.id,
    command,
    agent,
    time: nowStamp()
  });
  state.commands = state.commands.slice(0, 20);
  saveState();
};

const setAgentState = (agentId, updates) => {
  const agent = findAgent(agentId);
  if (!agent) return;
  Object.assign(agent, updates);
  saveState();
  renderAgents();
};

const setAgentStatus = (agentId, status) => {
  setAgentState(agentId, { status });
};

const pushActivity = (item, label = "ACTIVE", options = {}) => {
  if (options.heartbeat) {
    state.activity = state.activity.filter((event) => !event.heartbeat);
  } else {
    state.unread += 1;
  }

  state.activity.unshift({
    time: nowStamp(),
    item,
    label,
    heartbeat: Boolean(options.heartbeat)
  });

  state.activity = state.activity.slice(0, 30);
  saveState();
  renderActivity();
  renderUnread();
};

const pushAction = ({ label, title, next, agent }) => {
  state.actions.unshift({ label, title, next, agent });
  state.actions = state.actions.slice(0, 3);
  saveState();
  renderActions();
};

const findMission = (missionId) => state.missions.find((mission) => mission.id === missionId);

const updateMission = (missionId, updates) => {
  const mission = findMission(missionId);
  if (!mission) return null;
  Object.assign(mission, {
    ...updates,
    updated_at: new Date().toISOString()
  });
  mission.last_event = updates.last_event || mission.last_event;
  saveState();
  renderMissionBoard();
  return mission;
};

const appendMissionThread = (missionId, event, agent, status, artifact = "") => {
  const mission = findMission(missionId);
  if (!mission) return;

  mission.thread = Array.isArray(mission.thread) ? mission.thread : [];
  mission.thread.unshift({
    timestamp: nowStamp(),
    event,
    agent,
    status,
    artifact
  });
  mission.thread = mission.thread.slice(0, 12);
  mission.last_event = event;
  saveState();
  renderMissionBoard();
};

const createMissionCard = (mission, command, agent) => {
  const existing = findMission(mission.id);
  if (existing) return existing;

  const card = {
    id: mission.id,
    title: command,
    assigned_agent: agentLabel(agent),
    status: "INBOX",
    next_action: "Route to agent",
    artifacts_count: 0,
    last_event: "Mission card created",
    thread: []
  };

  state.missions.unshift(card);
  state.missionBoardHighlighted = true;
  saveState();
  appendMissionThread(mission.id, "Mission card created", agentLabel(agent), "INBOX");
  pushActivity("Mission card created", "ACTIVE");
  renderMissionBoard();
  return card;
};

const appendOrchestratorThread = (missionId, event, agent, status) => {
  appendMissionThread(missionId, event, agent, status);
};

const runOrchestratorMission = (missionSeed, command) => {
  const orchestratedMission = createOrchestratorMission(missionSeed, command);
  state.missions.unshift(orchestratedMission);
  state.missionBoardHighlighted = true;
  saveState();
  renderMissionBoard();

  logSubmittedCommand(missionSeed, command, orchestratedMission.assigned_agents.join(", "));
  updateNeedsMajor(null);
  pushActivity("Mission created", "ACTIVE");
  appendOrchestratorThread(
    orchestratedMission.id,
    "Mission created",
    "A004 Ops Watcher",
    "PLANNED"
  );

  window.setTimeout(() => {
    updateMission(orchestratedMission.id, {
      status: "RUNNING",
      next_action: orchestratedMission.plan[0],
      current_step: orchestratedMission.plan[0],
      output_summary: "Agents assigned by local orchestrator",
      last_event: "Orchestrator assigned agents"
    });
    pushActivity("Orchestrator assigned agents", "ACTION");
    appendOrchestratorThread(
      orchestratedMission.id,
      "Orchestrator assigned agents",
      orchestratedMission.assigned_agents.join(", "),
      "RUNNING"
    );

    agentsForIntent(orchestratedMission.intent).forEach((agent) => {
      setAgentState(agent.id, {
        status: "WORKING",
        current_task: command,
        last_event: `Running mission ${orchestratedMission.id}`,
        needs_major: false
      });
    });
  }, 250);

  orchestratedMission.plan.forEach((step, index) => {
    window.setTimeout(() => {
      const completed = index + 1;
      updateMission(orchestratedMission.id, {
        status: "RUNNING",
        current_step: step,
        steps_completed: completed,
        next_action: orchestratedMission.plan[completed] || "Prepare review handoff",
        output_summary: `Step ${completed}/${orchestratedMission.plan.length}: ${step}`,
        last_event: step
      });
      pushActivity(`Mission step: ${step}`, "WORKING");
      appendOrchestratorThread(
        orchestratedMission.id,
        step,
        orchestratedMission.assigned_agents[index % orchestratedMission.assigned_agents.length],
        "RUNNING"
      );
      const activeAgent = agentsForIntent(orchestratedMission.intent)[index % agentsForIntent(orchestratedMission.intent).length];
      if (activeAgent) {
        setAgentState(activeAgent.id, {
          status: "WORKING",
          current_task: command,
          last_event: step,
          needs_major: false
        });
      }
    }, 700 + (index * 650));
  });

  window.setTimeout(() => {
    const finishAsDone = /\b(auto|status|daily brief)\b/i.test(command);
    const finalStatus = finishAsDone ? "DONE" : "NEEDS MAJOR";
    const needsMajor = finalStatus === "NEEDS MAJOR";
    updateMission(orchestratedMission.id, {
      status: finalStatus,
      current_step: orchestratedMission.plan[orchestratedMission.plan.length - 1],
      steps_completed: orchestratedMission.plan.length,
      next_action: needsMajor ? "Major reviews mission plan" : "Review completed status",
      needs_major: needsMajor,
      output_summary: needsMajor
        ? "Mission plan simulated and waiting for Major review"
        : "Mission plan simulated and ready for review",
      last_event: needsMajor ? "Mission needs Major" : "Mission completed"
    });
    appendOrchestratorThread(
      orchestratedMission.id,
      needsMajor ? "Mission needs Major" : "Mission completed",
      "A004 Ops Watcher",
      finalStatus
    );

    if (needsMajor) {
      state.needsMajor = {
        mission: command,
        agent: orchestratedMission.assigned_agents.join(", ")
      };
      pushAction({
        label: "REVIEW",
        title: `Review mission: ${command}`,
        next: "Approve or redirect local plan",
        agent: orchestratedMission.assigned_agents.join(", ")
      });
      pushActivity("Mission needs Major", "WAITING");
    } else {
      pushActivity("Mission completed", "DONE");
    }

    agentsForIntent(orchestratedMission.intent).forEach((agent) => {
      setAgentState(agent.id, {
        status: needsMajor ? "WAITING" : "READY",
        current_task: needsMajor ? command : "",
        last_event: needsMajor ? "Needs Major review" : "Ready for next mission",
        needs_major: needsMajor
      });
    });
    saveState();
    renderNeedsMajor();
    renderMissionBoard();
  }, 950 + (orchestratedMission.plan.length * 650));
};

const moveMissionCard = (missionId, status, nextAction, agent, event, artifact = "") => {
  const mission = findMission(missionId);
  if (!mission) return;

  mission.status = status;
  mission.next_action = nextAction;
  mission.assigned_agent = agent;
  if (artifact) {
    mission.artifacts_count += 1;
  }
  appendMissionThread(missionId, event, agent, status, artifact);

  if (event === "Mission moved to Running") {
    pushActivity("Mission moved to Running", "WORKING");
  } else if (event === "Mission needs Major") {
    pushActivity("Mission needs Major", "WAITING");
  } else if (event === "Artifact attached") {
    pushActivity("Artifact attached", "READY");
  }

  saveState();
  renderMissionBoard();
};

const startMissionCard = (mission, command, agent) => {
  createMissionCard(mission, command, agent);
  moveMissionCard(mission.id, "RUNNING", "Agent working", agentLabel(agent), "Mission moved to Running");
};

const completeMissionCard = (missionId, agent, event = "Mission completed", nextAction = "Review local handoff") => {
  moveMissionCard(missionId, "DONE", nextAction, agent, event);
};

const attachMissionArtifact = (missionId, agent, artifact) => {
  moveMissionCard(missionId, "REVIEW", "Review attached artifact", agent, "Artifact attached", artifact);
};

const proposeSkillRequest = (mission, command) => {
  const match = command.match(skillRequestCommandPattern);
  const skillName = normalizeTitle(match ? match[1] : command.replace(/^propose skill\s+/i, ""));
  const agent = findAgent("A004");
  const proposedBy = agentLabel(agent);

  logSubmittedCommand(mission, command, proposedBy);
  updateNeedsMajor(null);
  startMissionCard(mission, command, agent);
  state.skillRequests.unshift({
    proposed_by: proposedBy,
    skill_name: skillName,
    why_needed: "Convert repeated local work into an approved reusable workflow",
    input: "operator command and mission thread",
    output: `${skillName} workflow handoff`,
    risk: "MED",
    status: "REVIEW"
  });
  state.skillRequests = state.skillRequests.slice(0, 12);
  state.skillRequestsHighlighted = true;
  saveState();
  renderSkillRequests();
  pushActivity("Skill request proposed", "REVIEW");
  moveMissionCard(mission.id, "REVIEW", "Major approves or rejects skill", proposedBy, "Skill request proposed", `skill:${skillName}`);
  pushAction({
    label: "REVIEW",
    title: `Approve skill: ${skillName}`,
    next: "Map workflow and leverage",
    agent: proposedBy
  });
  setAgentState("A004", {
    status: "READY",
    current_task: "",
    last_event: "Skill request queued",
    needs_major: false
  });
};

const inferMediaLane = (title) => {
  if (/\b(bwyh|heal|healing)\b/i.test(title)) return "BWYH";
  if (/\b(contour|sales|business|bottleneck|client)\b/i.test(title)) return "Contour";
  if (/\b(saf|research|narrative|study)\b/i.test(title)) return "SAF";
  if (/\b(ai|os|system|agent|command center)\b/i.test(title)) return "Major AI OS";
  return "Doctrine";
};

const extractMediaTopic = (command) => {
  const patterns = [
    /^draft substack\s+(.+)$/i,
    /^make video from\s+(.+)$/i,
    /^queue remotion\s+(.+)$/i,
    /^queue heygen\s+(.+)$/i,
    /^publish\s+(.+)$/i
  ];
  const match = patterns.map((pattern) => command.match(pattern)).find(Boolean);
  return match ? match[1].trim() : command.trim();
};

const normalizeTitle = (title) => title.trim().replace(/\s+/g, " ");

const findMediaItem = (title) =>
  state.mediaWorkflow.find((item) =>
    item.title.toLowerCase() === title.toLowerCase()
  );

const findDistributionItem = (title, channel) =>
  state.distributionQueue.find((item) =>
    item.title.toLowerCase() === title.toLowerCase() &&
    item.channel.toLowerCase() === channel.toLowerCase()
  );

const upsertMediaWorkflowItem = (title, updates) => {
  const cleanTitle = normalizeTitle(title);
  const existing = findMediaItem(cleanTitle);

  if (existing) {
    Object.assign(existing, updates);
    saveState();
    renderMediaEngine();
    return existing;
  }

  const item = {
    title: cleanTitle,
    lane: inferMediaLane(cleanTitle),
    stage: "Raw Thought",
    next_action: "Choose content angle",
    assigned_agent: "A003 Content Catcher",
    status: "READY",
    ...updates
  };

  state.mediaWorkflow.unshift(item);
  saveState();
  renderMediaEngine();
  return item;
};

const distributionTemplates = (title) => {
  const lane = inferMediaLane(title);
  return [
    {
      title,
      lane,
      channel: "Substack",
      asset_type: "article",
      status: "READY",
      next_action: "Review local Substack handoff",
      owner_agent: "A003 Content Catcher"
    },
    {
      title,
      lane,
      channel: "X",
      asset_type: "hook",
      status: "NEEDS REVIEW",
      next_action: "Approve hook before queue",
      owner_agent: "A003 Content Catcher"
    },
    {
      title,
      lane,
      channel: "Instagram",
      asset_type: "short script",
      status: "READY",
      next_action: "Cut into local IG short",
      owner_agent: "A003 Content Catcher"
    },
    {
      title,
      lane,
      channel: "YouTube Shorts",
      asset_type: "short script",
      status: "READY",
      next_action: "Prepare local short script",
      owner_agent: "A003 Content Catcher"
    },
    {
      title,
      lane,
      channel: "GitHub / Obsidian Memory",
      asset_type: "memory note",
      status: "READY",
      next_action: "Save local memory handoff",
      owner_agent: "A003 Content Catcher"
    }
  ];
};

const upsertDistributionItem = (item) => {
  const cleanTitle = normalizeTitle(item.title);
  const existing = findDistributionItem(cleanTitle, item.channel);

  if (existing) {
    Object.assign(existing, {
      ...item,
      title: cleanTitle
    });
    saveState();
    renderDistributionQueue();
    return existing;
  }

  const nextItem = {
    ...item,
    title: cleanTitle
  };

  state.distributionQueue.unshift(nextItem);
  saveState();
  renderDistributionQueue();
  return nextItem;
};

const upsertDistributionBatch = (title) => {
  const cleanTitle = normalizeTitle(title);
  const rows = distributionTemplates(cleanTitle).map(upsertDistributionItem);
  state.distributionQueue = state.distributionQueue.filter((item, index, list) =>
    list.findIndex((candidate) =>
      candidate.title.toLowerCase() === item.title.toLowerCase() &&
      candidate.channel.toLowerCase() === item.channel.toLowerCase()
    ) === index
  );
  saveState();
  renderDistributionQueue();
  return rows;
};

const extractDistributionTopic = (command) => {
  const patterns = [
    /^distribute\s+(.+)$/i,
    /^send to x\s+(.+)$/i,
    /^send to substack\s+(.+)$/i,
    /^save to memory\s+(.+)$/i
  ];
  const match = patterns.map((pattern) => command.match(pattern)).find(Boolean);
  return match ? match[1].trim() : command.trim();
};

const syncDistributionFromMediaStage = (title, stage) => {
  if (!["Publish", "Remotion Queue", "HeyGen Queue", "Distribution"].includes(stage)) return;

  const cleanTitle = normalizeTitle(title);
  upsertDistributionBatch(cleanTitle);
  state.distributionHighlighted = true;
  saveState();
  renderDistributionQueue();
};

const addDistributionActions = (title) => {
  const actionable = state.distributionQueue.find((item) =>
    item.title.toLowerCase() === title.toLowerCase() &&
    ["READY", "NEEDS REVIEW"].includes(item.status)
  );

  if (!actionable) return;

  pushAction({
    label: actionable.status,
    title: `Distribution: ${actionable.title}`,
    next: `${actionable.channel} / ${actionable.next_action}`,
    agent: actionable.owner_agent
  });
};

const handleDistributionCommand = (mission, command) => {
  const topic = normalizeTitle(extractDistributionTopic(command));
  const agent = findAgent("A003");
  const agentName = agentLabel(agent);
  let event = "Distribution queued";

  logSubmittedCommand(mission, command, agentName);
  updateNeedsMajor(null);
  state.distributionHighlighted = true;
  startMissionCard(mission, command, agent);

  if (/^distribute\b/i.test(command)) {
    upsertDistributionBatch(topic);
    upsertMediaWorkflowItem(topic, {
      stage: "Distribution",
      next_action: "Queue outbound channels",
      assigned_agent: agentName,
      status: "ACTION"
    });
    event = "Distribution queued";
  } else if (/^send to x\b/i.test(command)) {
    upsertDistributionItem({
      title: topic,
      lane: inferMediaLane(topic),
      channel: "X",
      asset_type: "hook",
      status: "QUEUED",
      next_action: "Local X handoff queued",
      owner_agent: agentName
    });
    event = "X handoff queued";
  } else if (/^send to substack\b/i.test(command)) {
    upsertDistributionItem({
      title: topic,
      lane: inferMediaLane(topic),
      channel: "Substack",
      asset_type: "article",
      status: "QUEUED",
      next_action: "Local Substack handoff queued",
      owner_agent: agentName
    });
    event = "Substack handoff queued";
  } else {
    upsertDistributionItem({
      title: topic,
      lane: inferMediaLane(topic),
      channel: "GitHub / Obsidian Memory",
      asset_type: "memory note",
      status: "READY",
      next_action: "Save local memory note",
      owner_agent: agentName
    });
    event = "Memory save queued";
  }

  pushActivity(event, "QUEUED");
  addDistributionActions(topic);
  attachMissionArtifact(mission.id, agentName, `distribution:${topic}`);
  simulateContentCatcher(mission, command, event);
  saveState();
  renderDistributionQueue();
  renderMediaEngine();
};

const simulateContentCatcher = (mission, command, finalEvent = "Media workflow updated") => {
  const agent = findAgent("A003");
  setAgentState("A003", {
    status: "WORKING",
    current_task: command,
    last_event: `${mission.id} media workflow`,
    needs_major: false
  });

  window.setTimeout(() => {
    pushActivity("Content Catcher accepted mission", "ACTIVE");
    setAgentState("A003", {
      status: "WORKING",
      current_task: command,
      last_event: "Building media handoff"
    });
  }, 500);

  window.setTimeout(() => {
    pushActivity(finalEvent, "DONE");
    setAgentState("A003", {
      status: "DONE",
      current_task: command,
      last_event: finalEvent,
      needs_major: false
    });
  }, 1700);

  window.setTimeout(() => {
    setAgentState("A003", {
      status: "READY",
      current_task: "",
      last_event: "Ready for next content mission"
    });
  }, 3200);

  return agent;
};

const handleMediaWorkflowCommand = (mission, command) => {
  const topic = extractMediaTopic(command);
  const agent = findAgent("A003");
  const agentName = agentLabel(agent);
  let update;
  let events;
  let action;
  let finalEvent;

  if (/^draft substack\b/i.test(command)) {
    update = {
      stage: "Draft",
      next_action: "Editorial Polish",
      assigned_agent: agentName,
      status: "ACTION"
    };
    events = [["Substack draft captured", "ACTION"]];
    action = {
      label: "CONTENT ACTION",
      title: `Draft Substack: ${topic}`,
      next: "Editorial Polish",
      agent: agentName
    };
    finalEvent = "Substack draft captured";
  } else if (/^make video from\b/i.test(command)) {
    update = {
      stage: "Video Script",
      next_action: "Queue Remotion / HeyGen",
      assigned_agent: agentName,
      status: "ACTION"
    };
    events = [["Hooks extracted", "ACTION"], ["Video script ready", "READY"]];
    action = {
      label: "ACTION",
      title: `Queue media render: ${topic}`,
      next: "Remotion / HeyGen queue",
      agent: agentName
    };
    finalEvent = "Video script ready";
  } else if (/^queue remotion\b/i.test(command)) {
    update = {
      stage: "Remotion Queue",
      next_action: "Queue HeyGen or Distribution",
      assigned_agent: agentName,
      status: "QUEUED"
    };
    events = [["Remotion render queued", "QUEUED"]];
    action = {
      label: "QUEUED",
      title: `Remotion queued: ${topic}`,
      next: "Review render output later",
      agent: agentName
    };
    finalEvent = "Remotion render queued";
  } else if (/^queue heygen\b/i.test(command)) {
    update = {
      stage: "HeyGen Queue",
      next_action: "Distribution",
      assigned_agent: agentName,
      status: "QUEUED"
    };
    events = [["HeyGen personalization queued", "QUEUED"]];
    action = {
      label: "QUEUED",
      title: `HeyGen queued: ${topic}`,
      next: "Prepare distribution",
      agent: agentName
    };
    finalEvent = "HeyGen personalization queued";
  } else {
    update = {
      stage: "Publish",
      next_action: "Memory Update",
      assigned_agent: agentName,
      status: "REVIEW"
    };
    events = [["Memory update needed", "REVIEW"]];
    action = {
      label: "REVIEW",
      title: `Publish / memory update: ${topic}`,
      next: "Log insight to memory graph",
      agent: agentName
    };
    finalEvent = "Memory update needed";
  }

  logSubmittedCommand(mission, command, agentName);
  updateNeedsMajor(null);
  state.mediaEngineHighlighted = true;
  startMissionCard(mission, command, agent);
  upsertMediaWorkflowItem(topic, update);
  syncDistributionFromMediaStage(topic, update.stage);
  addDistributionActions(topic);
  attachMissionArtifact(mission.id, agentName, `media:${topic}:${update.stage}`);
  pushAction(action);
  pushActivity(`${mission.id} media workflow -> Content Catcher`, "ACTION");
  events.forEach(([event, label], index) => {
    window.setTimeout(() => pushActivity(event, label), index * 450);
  });
  simulateContentCatcher(mission, command, finalEvent);
  saveState();
  renderMediaEngine();
};

const updateNeedsMajor = (mission, agent) => {
  state.needsMajor = mission
    ? {
        mission,
        agent: agentLabel(agent)
      }
    : null;
  saveState();
  renderNeedsMajor();
};

const dispatchMission = (command) => {
  const trimmed = command.trim();
  if (!trimmed) return;

  state.missionId += 1;
  const mission = {
    id: `M-${String(state.missionId).padStart(3, "0")}`,
    command: trimmed
  };

  if (githubLogCommandPattern.test(trimmed)) {
    reviewGithubLogs(mission, trimmed);
    return;
  }

  if (agentRegistryCommandPattern.test(trimmed)) {
    reviewAgentRegistry(mission, trimmed);
    return;
  }

  if (missionBoardCommandPattern.test(trimmed)) {
    reviewMissionBoard(mission, trimmed);
    return;
  }

  if (skillRequestCommandPattern.test(trimmed)) {
    proposeSkillRequest(mission, trimmed);
    return;
  }

  if (distributionCommandPattern.test(trimmed)) {
    handleDistributionCommand(mission, trimmed);
    return;
  }

  if (mediaWorkflowCommandPattern.test(trimmed)) {
    handleMediaWorkflowCommand(mission, trimmed);
    return;
  }

  runOrchestratorMission(mission, trimmed);
};

const reviewAgentRegistry = (mission, command) => {
  logSubmittedCommand(mission, command, "A004 Ops Watcher");
  state.agentRegistryHighlighted = true;
  saveState();
  renderAgents();
  pushActivity("Agent registry reviewed", "SYNCED");
};

const reviewMissionBoard = (mission, command) => {
  logSubmittedCommand(mission, command, "A004 Ops Watcher");
  state.missionBoardHighlighted = true;
  saveState();
  renderMissionBoard();
  pushActivity("Mission board reviewed", "SYNCED");
};

const reviewGithubLogs = (mission, command) => {
  logSubmittedCommand(mission, command, "A004 Ops Watcher");
  state.githubLogsHighlighted = true;
  saveState();
  renderGithubLogs();
  pushActivity("GitHub logs reviewed", "SYNCED");

  const attentionLog = state.githubLogs.find((log) =>
    ["NEEDS REVIEW", "STALE"].includes(log.status)
  );

  if (attentionLog) {
    pushAction({
      label: attentionLog.status,
      title: `Review GitHub log: ${attentionLog.title}`,
      next: attentionLog.next,
      agent: "A004 Ops Watcher"
    });
  }
};

const renderUnread = () => {
  document.querySelector("#unread-counter").textContent =
    `${String(state.unread).padStart(2, "0")} UNREAD`;
};

const renderNeedsMajor = () => {
  const panel = document.querySelector("#needs-major-panel");
  const text = document.querySelector("#needs-major-text");
  const signal = document.querySelector("#needs-major-signal");

  if (!state.needsMajor) {
    panel.classList.remove("waiting");
    text.textContent = "No review holds";
    signal.className = "signal ready";
    signal.textContent = "READY";
    return;
  }

  panel.classList.add("waiting");
  text.textContent = `${state.needsMajor.agent}: ${state.needsMajor.mission}`;
  signal.className = "signal waiting";
  signal.textContent = "WAITING";
};

const renderLeads = () => {
  const target = document.querySelector("#todays-leads");
  target.innerHTML = state.leads.map((lead, index) => `
    <div class="lead-row ${index === 0 ? "selected" : ""}">
      <div>
        <strong>${escapeHtml(lead.name)}</strong>
        <span class="meta">${escapeHtml(lead.note)}</span>
      </div>
      <div class="tag-row">
        <span class="signal">${escapeHtml(lead.lane)}</span>
        <span class="${labelClass(lead.priority)}">${escapeHtml(lead.priority)}</span>
        <span class="${labelClass(lead.status)}">${escapeHtml(lead.status)}</span>
      </div>
    </div>
  `).join("");
};

const renderActions = () => {
  const target = document.querySelector("#top-actions");
  target.innerHTML = state.actions.map((action) => `
    <li>
      <span class="${labelClass(action.label)}">${escapeHtml(action.label)}</span>
      <div>
        <strong>${escapeHtml(action.title)}</strong>
        <p>${escapeHtml(action.next)} / ${escapeHtml(action.agent)}</p>
      </div>
    </li>
  `).join("");
};

const renderDailyBrief = () => {
  const target = document.querySelector("#daily-brief-list");
  const latestLog = state.githubLogs[0];

  target.innerHTML = state.dailyBrief.map((item) => `
    <article class="brief-row">
      <span class="${labelClass(item.status)}">${escapeHtml(item.status)}</span>
      <div>
        <strong>${escapeHtml(item.label)}</strong>
        <p>${escapeHtml(item.title)}</p>
      </div>
      <div>
        <span class="meta">${escapeHtml(item.owner)}</span>
        <span class="meta">${escapeHtml(item.next)}</span>
      </div>
    </article>
  `).join("");

  document.querySelector("#latest-github-log").innerHTML = latestLog
    ? `<span class="meta">Latest GitHub log:</span><strong>${escapeHtml(latestLog.title)}</strong>`
    : `<span class="meta">Latest GitHub log:</span><strong>No local log loaded</strong>`;
};

const renderGithubLogs = () => {
  const panel = document.querySelector("#github-logs");
  const target = document.querySelector("#github-logs-list");

  panel.classList.toggle("review-highlight", Boolean(state.githubLogsHighlighted));
  target.innerHTML = state.githubLogs.map((log, index) => `
    <article class="github-log-row ${index === 0 ? "selected" : ""}">
      <div>
        <strong>${escapeHtml(log.title)}</strong>
        <span class="meta">${escapeHtml(log.repo)}</span>
      </div>
      <span class="meta path">${escapeHtml(log.path)}</span>
      <span class="signal">${escapeHtml(log.type)}</span>
      <span class="${labelClass(log.status)}">${escapeHtml(log.status)}</span>
      <time>${escapeHtml(log.timestamp)}</time>
      <span class="meta">${escapeHtml(log.next)}</span>
    </article>
  `).join("");
};

const renderMediaEngine = () => {
  const panel = document.querySelector("#media-engine");
  const stageTarget = document.querySelector("#media-stage-strip");
  const listTarget = document.querySelector("#media-workflow-list");

  panel.classList.toggle("review-highlight", Boolean(state.mediaEngineHighlighted));

  stageTarget.innerHTML = mediaStages.map((stage) => {
    const count = state.mediaWorkflow.filter((item) => item.stage === stage).length;
    return `
      <div class="media-stage ${count ? "has-items" : ""}">
        <span>${escapeHtml(stage.replace(" Queue", ""))}</span>
        <strong>${count}</strong>
      </div>
    `;
  }).join("");

  listTarget.innerHTML = state.mediaWorkflow.map((item, index) => `
    <article class="media-workflow-row ${index === 0 ? "selected" : ""}">
      <div>
        <strong>${escapeHtml(item.title)}</strong>
        <span class="meta">${escapeHtml(item.next_action)}</span>
      </div>
      <span class="signal">${escapeHtml(item.lane)}</span>
      <span class="${labelClass(item.stage)}">${escapeHtml(item.stage)}</span>
      <span class="${labelClass(item.status)}">${escapeHtml(item.status)}</span>
      <span class="meta">${escapeHtml(item.assigned_agent)}</span>
    </article>
  `).join("");
};

const renderDistributionQueue = () => {
  const panel = document.querySelector("#distribution-queue");
  const target = document.querySelector("#distribution-list");

  panel.classList.toggle("review-highlight", Boolean(state.distributionHighlighted));
  target.innerHTML = state.distributionQueue.map((item, index) => `
    <article class="distribution-row ${index === 0 ? "selected" : ""}">
      <div>
        <strong>${escapeHtml(item.title)}</strong>
        <span class="meta">${escapeHtml(item.next_action)}</span>
      </div>
      <span class="signal">${escapeHtml(item.lane)}</span>
      <span class="meta">${escapeHtml(item.channel)}</span>
      <span class="signal">${escapeHtml(item.asset_type)}</span>
      <span class="${labelClass(item.status)}">${escapeHtml(item.status)}</span>
      <span class="meta">${escapeHtml(item.owner_agent)}</span>
    </article>
  `).join("");
};

const renderMissionBoard = () => {
  const panel = document.querySelector("#mission-board");
  const target = document.querySelector("#mission-board-lanes");

  panel.classList.toggle("review-highlight", Boolean(state.missionBoardHighlighted));
  target.innerHTML = missionStatusLanes.map((lane) => {
    const cards = state.missions.filter((mission) => mission.status === lane);
    return `
      <section class="mission-lane">
        <header>
          <h3>${escapeHtml(lane)}</h3>
          <span class="signal">${cards.length}</span>
        </header>
        <div class="mission-card-list">
          ${cards.map((mission) => `
            <article class="mission-card">
              <div class="mission-card-head">
                <strong>${escapeHtml(mission.id)}</strong>
                <span class="${labelClass(mission.status)}">${escapeHtml(mission.status)}</span>
              </div>
              <p>${escapeHtml(mission.command || mission.title)}</p>
              <div class="mission-card-meta">
                <span>${escapeHtml(mission.intent || "operations")}</span>
                <span>${escapeHtml(mission.steps_completed || 0)}/${escapeHtml((mission.plan || []).length || 0)}</span>
              </div>
              <span class="mission-agents">${escapeHtml((mission.assigned_agents || [mission.assigned_agent]).join(" / "))}</span>
              <p>${escapeHtml(mission.current_step || "No active step")}</p>
              <span class="mission-next">${escapeHtml(mission.next_action || "Review mission")}</span>
              ${mission.needs_major ? "<span class=\"signal waiting\">NEEDS MAJOR</span>" : ""}
              <div class="mission-thread">
                ${(mission.thread || []).slice(0, 3).map((entry) => `
                  <div>
                    <time>${escapeHtml(entry.timestamp)}</time>
                    <span>${escapeHtml(entry.event)}</span>
                    ${entry.artifact ? `<em>${escapeHtml(entry.artifact)}</em>` : ""}
                  </div>
                `).join("")}
              </div>
            </article>
          `).join("") || "<p class=\"empty-lane\">No missions</p>"}
        </div>
      </section>
    `;
  }).join("");
};

const renderSkillRequests = () => {
  const panel = document.querySelector("#skill-requests");
  const target = document.querySelector("#skill-request-list");

  panel.classList.toggle("review-highlight", Boolean(state.skillRequestsHighlighted));
  target.innerHTML = state.skillRequests.map((request, index) => `
    <article class="skill-request-row ${index === 0 ? "selected" : ""}">
      <div>
        <strong>${escapeHtml(request.skill_name)}</strong>
        <span class="meta">${escapeHtml(request.why_needed)}</span>
      </div>
      <span class="meta">${escapeHtml(request.proposed_by)}</span>
      <span class="meta">${escapeHtml(request.input)}</span>
      <span class="meta">${escapeHtml(request.output)}</span>
      <span class="${labelClass(request.risk)}">${escapeHtml(request.risk)}</span>
      <span class="${labelClass(request.status)}">${escapeHtml(request.status)}</span>
    </article>
  `).join("");
};

const renderPipeline = (id, stages) => {
  const target = document.querySelector(id);
  target.innerHTML = `
    <div class="pipeline-track">
      ${stages.map(([name, label, progress]) => `
        <div class="pipeline-stage">
          <span class="stage-name">${escapeHtml(name)}</span>
          <span class="${labelClass(label)}">${escapeHtml(label)}</span>
          <div class="progress" aria-label="${escapeHtml(name)} ${progress}%">
            <div class="progress-bar" style="width: ${progress}%"></div>
          </div>
          <span class="stage-value">${progress}%</span>
        </div>
      `).join("")}
    </div>
  `;
};

const renderApps = () => {
  const target = document.querySelector("#app-registry");
  target.innerHTML = `
    <table>
      <thead>
        <tr>
          <th>App</th>
          <th>Status</th>
          <th>Priority</th>
          <th>Repo</th>
          <th>Next</th>
        </tr>
      </thead>
      <tbody>
        ${state.apps.map((app, index) => `
          <tr class="${index === 0 ? "selected-row" : ""}">
            <td><strong>${escapeHtml(app.name)}</strong></td>
            <td><span class="${labelClass(app.status)}">${escapeHtml(app.status)}</span></td>
            <td>${escapeHtml(app.priority)}</td>
            <td>${escapeHtml(app.repo)}</td>
            <td>${escapeHtml(app.next)}</td>
          </tr>
        `).join("")}
      </tbody>
    </table>
  `;
};

const renderAgents = () => {
  const target = document.querySelector("#agent-status");
  document.querySelector("#agents").classList.toggle(
    "review-highlight",
    Boolean(state.agentRegistryHighlighted)
  );
  target.innerHTML = state.agents.map((agent) => `
    <div class="agent-row ${agent.status === "WORKING" ? "is-working" : ""} ${agent.status === "WAITING" ? "is-waiting" : ""} ${agent.status === "BLOCKED" ? "is-blocked" : ""}">
      <span class="agent-code">${escapeHtml(agent.id)}</span>
      <div class="agent-main">
        <strong>${escapeHtml(agent.name)}</strong>
        <span class="meta">${escapeHtml(agent.role)}</span>
        <span class="agent-task">${escapeHtml(agent.current_task || agent.last_event)}</span>
      </div>
      <div class="agent-signals">
        ${agent.needs_major ? "<span class=\"signal waiting\">NEEDS MAJOR</span>" : ""}
        <span class="${labelClass(agent.status)}">
          ${agent.status === "WORKING" ? "<span class=\"work-dot\" aria-hidden=\"true\"></span>" : ""}
          ${escapeHtml(agent.status)}
        </span>
      </div>
    </div>
  `).join("");
};

const renderActivity = () => {
  const target = document.querySelector("#activity-feed");
  target.innerHTML = state.activity.map((event) => `
    <div class="activity-row ${event.heartbeat ? "heartbeat-row" : ""}">
      <time>${escapeHtml(event.time)}</time>
      <strong>${escapeHtml(event.item)}</strong>
      <span class="${labelClass(event.label)}">${escapeHtml(event.label)}</span>
    </div>
  `).join("");
};

const bindCommandInput = () => {
  const form = document.querySelector("#command-form");
  const input = document.querySelector("#command-input");

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    dispatchMission(input.value);
    input.value = "";
    input.focus();
  });
};

const bindResetControl = () => {
  const button = document.querySelector("#reset-local-state");

  button.addEventListener("click", () => {
    localStorage.removeItem(STORAGE_KEY);
    state = cloneState(seedState);
    saveState();
    renderAll();
  });
};

const startHeartbeat = () => {
  window.setInterval(() => {
    pushActivity("Ops Watcher heartbeat", "SYNCED", { heartbeat: true });
  }, 12000);
};

const renderAll = () => {
  renderUnread();
  renderNeedsMajor();
  renderMissionBoard();
  renderLeads();
  renderActions();
  renderDailyBrief();
  renderGithubLogs();
  renderMediaEngine();
  renderDistributionQueue();
  renderSkillRequests();
  renderPipeline("#pipeline-bwyh", state.pipelines.bwyh);
  renderPipeline("#pipeline-contour", state.pipelines.contour);
  renderPipeline("#pipeline-saf", state.pipelines.saf);
  renderApps();
  renderAgents();
  renderActivity();
};

bindCommandInput();
bindResetControl();
renderAll();
startHeartbeat();
