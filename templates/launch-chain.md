# launch-chain — 3 stages

For shipping something public: a product, a release, a post, an open-source repo. Evidence before distribution, distribution before noise — each stage is a gate the next one depends on.

**Stage map:** 1. Evidence (artifact ready + claims that survive scrutiny) → 2. Distribution prep (channels, copy, schedule) → 3. Publish + first-response.

Fill every `[FILL]`, paste into a fresh chat:

````markdown
# STAGE 1/3 — EVIDENCE
# Chain: "[FILL: what's launching, short]"

## CHAIN META
- Total stages: 3
- Current stage: 1/3
- Stage 1: make the artifact self-explanatory + draft claims that survive fact-checking
- Stage 2: per-channel copy, assets, and a publish schedule with gates
- Stage 3: publish checklist execution + first-response playbook

## WORKSPACE
Absolute path: [FILL: path, or "none (chat-only)"]
Target environment: [FILL: Claude Code / Cowork / claude.ai chat]

## INHERITED CONTEXT — REQUIRED READING

### Chain goal
[FILL: one verifiable sentence — e.g. "X is live on channels A and B, with launch copy approved and a response playbook ready."]

### Decisions already made
- [FILL: positioning line — the one sentence that describes the thing]
- [FILL: channels in scope / out of scope]
- No claim ships without naming who could refute it

### Stable context (copy verbatim into every stage)
- Voice rules: [FILL: short sentences? banned words? language?]
- Audience: [FILL]
- Links that appear in every piece: [FILL: repo, site, newsletter]

### Current state audited ([FILL: date])
- ✅ EXISTS: [FILL: what's already built]
- ❌ MISSING: [FILL]
- ⛔ FAILED: nothing yet

## THIS STAGE'S TASK
1. Audit the artifact as a stranger: can a cold visitor understand it in 30 seconds? List and fix the gaps
2. Draft 3 claims to use and 2 claims to avoid — for each, name who or what could refute it
3. Define the launch gate: what must be true before Stage 3 publishes anything

## CONSTRAINTS
- Nothing goes public in this stage

## DELIVERABLES
1. Gap list (fixed or flagged) + claims sheet + launch gate
2. A `### NEXT PROMPT — STAGE 2` block

## PROPAGATION PROTOCOL — CRITICAL
At the end of your response, emit a markdown code block containing the complete, self-contained prompt for Stage 2. The next chat has ZERO memory of this one. The Stage 2 prompt must: open with `# STAGE 2/3 — DISTRIBUTION PREP`; copy CHAIN META, WORKSPACE, and all stable INHERITED CONTEXT verbatim; carry the claims sheet and the launch gate in full; update "Current state audited" and `⛔ FAILED` (angles or claims that were tried and dropped go here, with the reason); set the task to per-channel copy + schedule; include this same protocol pointing to Stage 3 (Stage 3 replaces it with FINAL TERMINATION and ends with `### CHAIN COMPLETE`). Never copy credentials or API keys into the next prompt. If the launch gate can't be defined without the user, emit `### CHAIN PAUSED` with the question instead of guessing.
````
