const STORAGE_KEY = "major-os-command-center-state-v1";

const seedState = {
  unread: 3,
  missionId: 0,
  heartbeatVisible: false,
  needsMajor: null,
  commands: [],
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
    { id: "A001", name: "Scout", status: "IDLE" },
    { id: "A002", name: "Audit", status: "READY" },
    { id: "A003", name: "Content Catcher", status: "IDLE" },
    { id: "A004", name: "Ops Watcher", status: "READY" },
    { id: "A005", name: "Grant Hunter", status: "IDLE" },
    { id: "A006", name: "Outreach", status: "READY" },
    { id: "A007", name: "Offer Builder", status: "IDLE" },
    { id: "A008", name: "Deck Builder", status: "IDLE" },
    { id: "A009", name: "Storefront Operator", status: "IDLE" },
    { id: "A010", name: "Meeting Synthesizer", status: "READY" }
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

const mergeSeedState = (savedState) => {
  const merged = {
    ...cloneState(seedState),
    ...savedState
  };

  merged.commands = Array.isArray(savedState.commands) ? savedState.commands : [];
  merged.leads = Array.isArray(savedState.leads) ? savedState.leads : cloneState(seedState.leads);
  merged.actions = Array.isArray(savedState.actions) ? savedState.actions : cloneState(seedState.actions);
  merged.dailyBrief = Array.isArray(savedState.dailyBrief) ? savedState.dailyBrief : cloneState(seedState.dailyBrief);
  merged.pipelines = savedState.pipelines || cloneState(seedState.pipelines);
  merged.apps = Array.isArray(savedState.apps) ? savedState.apps : cloneState(seedState.apps);
  merged.agents = Array.isArray(savedState.agents) ? savedState.agents : cloneState(seedState.agents);
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
  { pattern: /\b(content|video|remotion|heygen)\b/i, agentId: "A003" },
  { pattern: /\b(email|outreach|follow up)\b/i, agentId: "A006" },
  { pattern: /\b(shopify|gumroad|store|product)\b/i, agentId: "A009" }
];

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

const routeCommand = (command) => {
  const match = routes.find((route) => route.pattern.test(command));
  return findAgent(match ? match.agentId : "A004");
};

const shouldRequestReview = (command, missionId) =>
  /\b(review|major|approve|diagnose|audit|contour)\b/i.test(command) || missionId % 3 === 0;

const setAgentStatus = (agentId, status) => {
  const agent = findAgent(agentId);
  if (!agent) return;
  agent.status = status;
  saveState();
  renderAgents();
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

  state.activity = state.activity.slice(0, 9);
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
  const agent = routeCommand(trimmed);
  const reviewRequired = shouldRequestReview(trimmed, state.missionId);

  state.commands.unshift({
    id: mission.id,
    command: trimmed,
    agent: agentLabel(agent),
    time: nowStamp()
  });
  state.commands = state.commands.slice(0, 20);
  saveState();
  updateNeedsMajor(null);
  pushAction({
    label: "ACTION",
    title: trimmed,
    next: "Mission dispatched",
    agent: agentLabel(agent)
  });
  pushActivity(`${mission.id} dispatched -> ${agent.name}`, "ACTION");
  setAgentStatus(agent.id, "WORKING");

  window.setTimeout(() => {
    pushActivity(`${agent.name} accepted mission`, "ACTIVE");
  }, 650);

  window.setTimeout(() => {
    pushActivity(`${agent.name} working...`, "WORKING");
    setAgentStatus(agent.id, "WORKING");
  }, 1500);

  window.setTimeout(() => {
    if (reviewRequired) {
      setAgentStatus(agent.id, "WAITING");
      updateNeedsMajor(trimmed, agent);
      pushAction({
        label: "REVIEW",
        title: trimmed,
        next: "Needs Major review",
        agent: agentLabel(agent)
      });
      pushActivity(`${agent.name} needs Major review`, "WAITING");
      return;
    }

    setAgentStatus(agent.id, "DONE");
    pushAction({
      label: "READY",
      title: trimmed,
      next: "Completed draft",
      agent: agentLabel(agent)
    });
    pushActivity(`${agent.name} completed draft`, "DONE");

    window.setTimeout(() => {
      setAgentStatus(agent.id, "READY");
    }, 1800);
  }, 2900);
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
  target.innerHTML = state.agents.map((agent) => `
    <div class="agent-row ${agent.status === "WORKING" ? "is-working" : ""}">
      <span class="agent-code">${escapeHtml(agent.id)}</span>
      <strong>${escapeHtml(agent.name)}</strong>
      <span class="${labelClass(agent.status)}">
        ${agent.status === "WORKING" ? "<span class=\"work-dot\" aria-hidden=\"true\"></span>" : ""}
        ${escapeHtml(agent.status)}
      </span>
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
  renderLeads();
  renderActions();
  renderDailyBrief();
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
