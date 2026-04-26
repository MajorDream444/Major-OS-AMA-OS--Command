const data = {
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
    ["ACTION", "Lock boot scaffold", "Mock data only"],
    ["HIGH", "Package first money workflow", "Content -> Product -> Sale"],
    ["REVIEW", "Map new app ideas", "GitHub / Airtable / Notion"]
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
      next: "Mission control restyle"
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
    ["A001", "Scout", "ACTIVE"],
    ["A002", "Audit", "READY"],
    ["A003", "Content Catcher", "QUEUED"],
    ["A004", "Ops Watcher", "ACTIVE"],
    ["A005", "Grant Hunter", "REVIEW"],
    ["A006", "Outreach", "READY"],
    ["A007", "Offer Builder", "QUEUED"],
    ["A008", "Deck Builder", "LOW"],
    ["A009", "Storefront Operator", "BLOCKED"],
    ["A010", "Meeting Synthesizer", "SYNCED"]
  ],
  activity: [
    ["08:58", "Lead classified -> Contour", "ACTIVE"],
    ["08:57", "Dossier created", "READY"],
    ["08:56", "Follow-up due", "ACTION"],
    ["08:55", "Airtable sync OK", "SYNCED"],
    ["08:54", "BWYH lane queued", "QUEUED"],
    ["08:53", "Storefront operator blocked", "BLOCKED"]
  ]
};

const escapeHtml = (value) =>
  String(value).replace(/[&<>"']/g, (char) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    "\"": "&quot;",
    "'": "&#39;"
  })[char]);

const labelClass = (label) => `signal ${String(label).toLowerCase()}`;

const renderLeads = () => {
  const target = document.querySelector("#todays-leads");
  target.innerHTML = data.leads.map((lead, index) => `
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
  target.innerHTML = data.actions.map(([label, title, note]) => `
    <li>
      <span class="${labelClass(label)}">${escapeHtml(label)}</span>
      <div>
        <strong>${escapeHtml(title)}</strong>
        <p>${escapeHtml(note)}</p>
      </div>
    </li>
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
        ${data.apps.map((app, index) => `
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
  target.innerHTML = data.agents.map(([id, name, status]) => `
    <div class="agent-row">
      <span class="agent-code">${escapeHtml(id)}</span>
      <strong>${escapeHtml(name)}</strong>
      <span class="${labelClass(status)}">${escapeHtml(status)}</span>
    </div>
  `).join("");
};

const renderActivity = () => {
  const target = document.querySelector("#activity-feed");
  target.innerHTML = data.activity.map(([time, item, label]) => `
    <div class="activity-row">
      <time>${escapeHtml(time)}</time>
      <strong>${escapeHtml(item)}</strong>
      <span class="${labelClass(label)}">${escapeHtml(label)}</span>
    </div>
  `).join("");
};

renderLeads();
renderActions();
renderPipeline("#pipeline-bwyh", data.pipelines.bwyh);
renderPipeline("#pipeline-contour", data.pipelines.contour);
renderPipeline("#pipeline-saf", data.pipelines.saf);
renderApps();
renderAgents();
renderActivity();
