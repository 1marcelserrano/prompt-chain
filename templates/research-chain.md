# research-chain — 3 stages

For competitive research, market scans, and literature reviews. The census always eats more context than you expect — keeping synthesis in a fresh chat protects the conclusions from a polluted window.

**Stage map:** 1. Census (find + fact sheets) → 2. Deep dive (verify + per-finding analysis) → 3. Synthesis (verdict + report).

Fill every `[FILL]`, paste into a fresh chat:

````markdown
# STAGE 1/3 — CENSUS
# Chain: "[FILL: research question, short]"

## CHAIN META
- Total stages: 3
- Current stage: 1/3
- Stage 1: census — find candidates + one fact sheet each
- Stage 2: deep dive — verify claims, analyze the top findings
- Stage 3: synthesis — verdict, comparisons, final report

## WORK FRAME — COPY VERBATIM

### Original ask
> [FILL: the operator's exact words]

### Done
[FILL: one verifiable statement]

### Work class and risk
[FILL: production / personal-pre-production / one-shot; risk; what a revert cannot undo]

### Budget / checkpoint
Three stages. Return to [FILL: coordinator] after each stage.

### Undo
[FILL: how to retract or revise the report if evidence changes]

### Coordinator
[FILL: chat, person, or role]

## WORKSPACE
Absolute path: [FILL: path, or "none (chat-only)"]
Target environment: [FILL: Claude Code / Cowork / claude.ai chat with web search]
Destination / audience: [FILL]

## AUTHORITY — COPY VERBATIM
- Authorized in this chain: [FILL: research and local report creation]
- Requires fresh approval: [FILL: publication, outreach, purchase, or other external effects]
- Out of scope: [FILL: markets, sources, or actions]

## INHERITED CONTEXT — REQUIRED READING

### Chain goal
[FILL: one verifiable sentence — e.g. "A report answering X, with every factual claim linked to a source."]

### Operator decisions — frozen
- [FILL: scope boundaries — what counts, what doesn't]
- Adoption/market numbers must be verified, never estimated — write "not verifiable" when a metric can't be confirmed

### Observed facts
- None yet — Stage 1 collects them

### Stage proposals — not binding until ratified
- None yet

### Stable context (copy verbatim into every stage)
- Output language: [FILL]
- Audience of the final report: [FILL]
- [FILL: any hard rules — banned sources, confidentiality, voice]

### Current state audited ([FILL: date])
- ✅ EXISTS: nothing yet — first stage
- ⛔ FAILED: nothing yet

## THIS STAGE'S TASK
1. Search [FILL: where — GitHub, web, marketplaces, papers] for [FILL: what]; collect at least [FILL: N] candidates
2. For each relevant one: name, link, verified adoption metric, mechanism in 2 lines
3. Output the fact sheets as a markdown table, flagging the [FILL: 2–3] most important for Stage 2

## CONSTRAINTS
- No invented numbers; no analysis yet — census only

## DELIVERABLES
1. Fact-sheet table
2. A `### STAGE REPORT TO COORDINATOR` block
3. When status is complete, a `### NEXT PROMPT — STAGE 2` block; when paused, `### CHAIN PAUSED` instead

## PROPAGATION PROTOCOL — CRITICAL
Return a `STAGE REPORT TO COORDINATOR`. When its status is complete, emit the complete prompt for Stage 2; when paused, emit `CHAIN PAUSED` and no Stage 2 prompt. The next chat has ZERO memory of this one. The Stage 2 prompt must: open with `# STAGE 2/3 — DEEP DIVE`; copy CHAIN META, WORK FRAME, WORKSPACE, AUTHORITY, and stable INHERITED CONTEXT verbatim; include the fact-sheet table as observed facts and flagged candidates as stage proposals, never operator decisions; update "Current state audited" and `⛔ FAILED`; set the task to verification and analysis and include this protocol for Stage 3. Do not execute Stage 2 here or publish/contact sources without exact authorization. Never copy credentials or unnecessary personal data.
````
