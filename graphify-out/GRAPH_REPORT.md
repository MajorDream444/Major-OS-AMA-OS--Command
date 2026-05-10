# Graph Report - command-center-graphify-target  (2026-05-11)

## Corpus Check
- 5 files · ~15,538 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 252 nodes · 638 edges · 20 communities
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `943bc572`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]

## God Nodes (most connected - your core abstractions)
1. `saveState()` - 41 edges
2. `pushActivity()` - 31 edges
3. `renderAll()` - 23 edges
4. `handleDistributionCommand()` - 20 edges
5. `refreshSystemGuidance()` - 18 edges
6. `logSubmittedCommand()` - 17 edges
7. `handleMediaWorkflowCommand()` - 17 edges
8. `renderArtifacts()` - 16 edges
9. `nowStamp()` - 14 edges
10. `proposeSkillRequest()` - 14 edges

## Surprising Connections (you probably didn't know these)
- `createArtifact()` --calls--> `laneForIntent()`  [EXTRACTED]
  app.js → app.js  _Bridges community 15 → community 12_
- `renderRuntimeState()` --calls--> `saveState()`  [EXTRACTED]
  app.js → app.js  _Bridges community 1 → community 4_
- `setAgentState()` --calls--> `saveState()`  [EXTRACTED]
  app.js → app.js  _Bridges community 1 → community 2_
- `applyAssetDecisionQueueHandoff()` --calls--> `saveState()`  [EXTRACTED]
  app.js → app.js  _Bridges community 1 → community 3_
- `renderLiveMission()` --calls--> `escapeHtml()`  [EXTRACTED]
  app.js → app.js  _Bridges community 3 → community 11_

## Communities (20 total, 0 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.04
Nodes (26): agAgentsByLane, agArtifactTypesByLane, agEventTypes, agPlansByLane, allowedAssetQueueDecisions, artifactPriorityLabel(), artifactPriorityRank(), artifactTypesByIntent (+18 more)

### Community 1 - "Community 1"
Cohesion: 0.19
Nodes (32): appendArtifactDecision(), appendAssetQueueDecision(), applyAssetGenerationSummary(), applyExternalArtifactExport(), assetDecisionId(), createArtifactsForMission(), decisionId(), dispatchMission() (+24 more)

### Community 2 - "Community 2"
Cohesion: 0.15
Nodes (25): addDistributionActions(), attachMissionArtifact(), distributionTemplates(), extractDistributionTopic(), extractMediaTopic(), findAgent(), findDistributionItem(), findMediaItem() (+17 more)

### Community 3 - "Community 3"
Cohesion: 0.1
Nodes (23): applyAssetDecisionQueueHandoff(), applySubstackQueueHandoffs(), assetQueueDecisionExportJson(), decisionQueueCounts(), escapeHtml(), queueHandoffCounts(), refreshAssetDecisionQueue(), refreshSubstackQueueHandoffs() (+15 more)

### Community 4 - "Community 4"
Cohesion: 0.18
Nodes (22): agAgentsForLane(), agentLabel(), agEventLabel(), appendMissionThread(), appendOrchestratorThread(), artifactById(), completeMissionCard(), createMissionCard() (+14 more)

### Community 5 - "Community 5"
Cohesion: 0.25
Nodes (11): blockedExternalSubsystem(), buildNextMove(), buildStatusLines(), buildSystemGuidance(), commandTitle(), externalSubsystems(), getLatestMission(), getPriorityAssetIntake() (+3 more)

### Community 6 - "Community 6"
Cohesion: 0.24
Nodes (10): activeRiskRuleForLane(), agArtifactBody(), calculateDelayUntil(), canonicalRiskLane(), createAgArtifact(), governanceMetadataForLane(), normalizeArtifact(), normalizeGovernedItem() (+2 more)

### Community 7 - "Community 7"
Cohesion: 0.2
Nodes (9): code:text (Command Center = Major-OS-AMA-OS--Command), code:bash (make start), Commands, Current Scope, Grafitti Bridge, Major OS / AMA OS Command Center, Operating Stack, Repo Role (+1 more)

### Community 8 - "Community 8"
Cohesion: 0.2
Nodes (9): code:text (Plan -> Build -> Run -> Log -> Improve), Codex, Current Boundary, Daily Rule, Execution Loop, First Reads, Handoff Rule, Operating Mode (+1 more)

### Community 9 - "Community 9"
Cohesion: 0.22
Nodes (8): Build Rule, code:text (Command Center = Major-OS-AMA-OS--Command), Identity, Operating Sentence, Responsibilities, Security Rule, Source Of Truth Map, System Core

### Community 10 - "Community 10"
Cohesion: 0.22
Nodes (8): Active Mock Agent Roster, Agent Rule, Agents, code:text (Plan -> Build -> Run -> Log -> Improve), Daily Outputs, graphify, Logging, Runtime

### Community 11 - "Community 11"
Cohesion: 0.29
Nodes (7): getLiveMission(), getPriorityArtifact(), labelClass(), latestLocalArtifactForMission(), missionEventsFor(), renderLiveMission(), sortedArtifacts()

### Community 12 - "Community 12"
Cohesion: 0.29
Nodes (7): applyRiskGovernanceToItem(), artifactOwner(), artifactTitle(), createArtifact(), nextActionForRiskMode(), nowStampFromIso(), statusForRiskMode()

### Community 13 - "Community 13"
Cohesion: 0.53
Nodes (6): bindNavigationState(), currentVisibleSectionId(), navLinks(), navSections(), setActiveNav(), updateActiveNavFromScroll()

### Community 14 - "Community 14"
Cohesion: 0.33
Nodes (6): assetFileSet(), assetRoutingNote(), hasRequiredAssetFiles(), nextDecisionForAsset(), normalizeAssetGenerationResult(), rankForAsset()

### Community 15 - "Community 15"
Cohesion: 0.5
Nodes (5): agAgentLabelsForLane(), createAgMission(), detectAgLane(), laneForIntent(), normalizeMission()

### Community 16 - "Community 16"
Cohesion: 0.4
Nodes (5): fetchJsonFile(), loadAssetDecisionQueueHandoff(), loadAssetGenerationSummary(), loadExternalArtifactExport(), loadSubstackQueueHandoffs()

### Community 17 - "Community 17"
Cohesion: 0.67
Nodes (3): hardArtifactBlocker(), hasStrongSystemUnderneath(), shouldBlockArtifactPublish()

### Community 18 - "Community 18"
Cohesion: 0.67
Nodes (3): agentLabelsForIntent(), createOrchestratorMission(), detectMissionIntent()

### Community 19 - "Community 19"
Cohesion: 1.0
Nodes (3): cloneState(), loadState(), mergeSeedState()

## Knowledge Gaps
- **47 isolated node(s):** `mediaStages`, `missionLanes`, `missionStatusLanes`, `agEventTypes`, `agArtifactTypesByLane` (+42 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `saveState()` connect `Community 1` to `Community 0`, `Community 2`, `Community 3`, `Community 4`?**
  _High betweenness centrality (0.008) - this node is a cross-community bridge._
- **Why does `pushActivity()` connect `Community 1` to `Community 0`, `Community 2`, `Community 3`, `Community 4`?**
  _High betweenness centrality (0.004) - this node is a cross-community bridge._
- **Why does `renderAll()` connect `Community 3` to `Community 0`, `Community 1`, `Community 2`, `Community 4`, `Community 5`, `Community 11`?**
  _High betweenness centrality (0.003) - this node is a cross-community bridge._
- **What connects `mediaStages`, `missionLanes`, `missionStatusLanes` to the rest of the system?**
  _47 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.04 - nodes in this community are weakly interconnected._
- **Should `Community 3` be split into smaller, more focused modules?**
  _Cohesion score 0.1 - nodes in this community are weakly interconnected._