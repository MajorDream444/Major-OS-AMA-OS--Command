const data = {
  leads: [
    {
      name: "Systems audit inquiry",
      source: "Systems World CTA",
      fit: "High fit",
      note: "Needs ops dashboard and lead follow-up workflow"
    },
    {
      name: "Creator product lead",
      source: "Substack pipeline",
      fit: "Warm",
      note: "Interested in article-to-media packaging"
    },
    {
      name: "Local service operator",
      source: "Fix Up Score",
      fit: "New",
      note: "Needs diagnostic summary and next action"
    }
  ],
  actions: [
    {
      title: "Keep Command Center boot layer clean",
      note: "Use mock data until Airtable and Notion sync are intentionally wired."
    },
    {
      title: "Turn the first money workflow into a repeatable lane",
      note: "Content to product to sale is the first operating path."
    },
    {
      title: "Map every new app idea to GitHub, Airtable, or Notion",
      note: "No important system state should live only in chat."
    }
  ],
  pipelines: {
    bwyh: [
      ["Lead capture", 70],
      ["Offer framing", 45],
      ["Follow-up assets", 25]
    ],
    contour: [
      ["Intake", 40],
      ["Diagnostic", 30],
      ["Client dashboard", 15]
    ],
    saf: [
      ["Audience segment", 55],
      ["Score review", 35],
      ["Campaign handoff", 20]
    ]
  },
  apps: [
    {
      name: "Command Center",
      status: "Active",
      priority: "P1",
      repo: "Major-OS-AMA-OS--Command",
      next: "UI scaffold"
    },
    {
      name: "Major AI OS",
      status: "Planned",
      priority: "P1",
      repo: "Major-AI-OS",
      next: "Reference reusable skills"
    },
    {
      name: "52in52 Tracker",
      status: "Planned",
      priority: "P2",
      repo: "52in52",
      next: "Registry alignment"
    }
  ],
  agents: [
    ["Codex", "Ready", "Repo build worker"],
    ["OpenClaw", "Placeholder", "Agent runtime"],
    ["ChatGPT", "Ready", "Planning layer"],
    ["Hanzo", "Placeholder", "Ecosystem intelligence"]
  ],
  activity: [
    ["Now", "Command Center UI scaffold loaded with mock data."],
    ["Next", "Add real sync plan before connecting live services."],
    ["Later", "Build dashboard features after entrypoints stabilize."]
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

const renderLeads = () => {
  const target = document.querySelector("#todays-leads");
  target.innerHTML = data.leads.map((lead) => `
    <div class="lead-row">
      <strong>${escapeHtml(lead.name)}</strong>
      <div class="tag-row">
        <span class="tag">${escapeHtml(lead.source)}</span>
        <span class="tag">${escapeHtml(lead.fit)}</span>
      </div>
      <span class="meta">${escapeHtml(lead.note)}</span>
    </div>
  `).join("");
};

const renderActions = () => {
  const target = document.querySelector("#top-actions");
  target.innerHTML = data.actions.map((action) => `
    <li>
      ${escapeHtml(action.title)}
      <p>${escapeHtml(action.note)}</p>
    </li>
  `).join("");
};

const renderPipeline = (id, stages) => {
  const target = document.querySelector(id);
  target.innerHTML = `
    <div class="pipeline-track">
      ${stages.map(([name, progress]) => `
        <div class="pipeline-stage">
          <header>
            <strong>${escapeHtml(name)}</strong>
            <span>${progress}%</span>
          </header>
          <div class="progress" aria-hidden="true">
            <div class="progress-bar" style="width: ${progress}%"></div>
          </div>
        </div>
      `).join("")}
    </div>
  `;
};

const statusClass = (status) => `status-${status.toLowerCase()}`;

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
          <th>Next Action</th>
        </tr>
      </thead>
      <tbody>
        ${data.apps.map((app) => `
          <tr>
            <td><strong>${escapeHtml(app.name)}</strong></td>
            <td><span class="status ${statusClass(app.status)}">${escapeHtml(app.status)}</span></td>
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
  target.innerHTML = data.agents.map(([name, status, role]) => `
    <div class="agent-row">
      <strong>${escapeHtml(name)}</strong>
      <span class="meta">${escapeHtml(status)} - ${escapeHtml(role)}</span>
    </div>
  `).join("");
};

const renderActivity = () => {
  const target = document.querySelector("#activity-feed");
  target.innerHTML = data.activity.map(([time, item]) => `
    <div class="activity-row">
      <span class="activity-time">${escapeHtml(time)}</span>
      <strong>${escapeHtml(item)}</strong>
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
