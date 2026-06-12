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

## WORKSPACE
Absolute path: [FILL: path, or "none (chat-only)"]
Target environment: [FILL: Claude Code / Cowork / claude.ai chat with web search]

## INHERITED CONTEXT — REQUIRED READING

### Chain goal
[FILL: one verifiable sentence — e.g. "A report answering X, with every factual claim linked to a source."]

### Decisions already made
- [FILL: scope boundaries — what counts, what doesn't]
- Adoption/market numbers must be verified, never estimated — write "not verifiable" when a metric can't be confirmed

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
2. A `### NEXT PROMPT — STAGE 2` block

## PROPAGATION PROTOCOL — CRITICAL
At the end of your response, emit a markdown code block containing the complete, self-contained prompt for Stage 2. The next chat has ZERO memory of this one. The Stage 2 prompt must: open with `# STAGE 2/3 — DEEP DIVE`; copy CHAIN META, WORKSPACE, and all stable INHERITED CONTEXT verbatim; include the full fact-sheet table (the next chat cannot see this one); update "Decisions already made", "Current state audited", and `⛔ FAILED` (record any search path that came up dry, so it isn't retried); set the task to verifying and analyzing the flagged findings; include this same protocol pointing to Stage 3 (Stage 3 replaces it with FINAL TERMINATION and ends with `### CHAIN COMPLETE`). Never copy credentials or personal data into the next prompt. If blocked, emit `### CHAIN PAUSED` with a direct question instead.
````
