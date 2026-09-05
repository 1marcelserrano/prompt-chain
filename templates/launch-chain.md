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

## WORK FRAME — COPY VERBATIM

### Original ask
> [FILL: the operator's exact words, including whether publication is authorized]

### Done
[FILL: one verifiable statement]

### Work class and risk
[FILL: production / personal-pre-production / one-shot; risk; what a revert cannot undo]

### Budget / checkpoint
Three stages. Return to [FILL: coordinator] after each stage.

### Undo
[FILL: rollback or unpublish path; say when an effect cannot be fully undone]

### Coordinator
[FILL: chat, person, or role]

## WORKSPACE
Absolute path: [FILL: path, or "none (chat-only)"]
Target environment: [FILL: Claude Code / Cowork / claude.ai chat]
Destination / audience: [FILL]

## AUTHORITY — COPY VERBATIM
- Authorized in this chain: [FILL: preparation only, or exact publication action]
- Requires fresh approval: publish, send, push, deploy, or open a PR unless explicitly authorized above
- Out of scope: [FILL: channels, accounts, spend, permissions]

## INHERITED CONTEXT — REQUIRED READING

### Chain goal
[FILL: one verifiable sentence — e.g. "X is live on channels A and B, with launch copy approved and a response playbook ready."]

### Operator decisions — frozen
- [FILL: positioning line — the one sentence that describes the thing]
- [FILL: channels in scope / out of scope]
- No claim ships without naming who could refute it

### Observed facts
- [FILL: verified launch facts, or "none yet"]

### Stage proposals — not binding until ratified
- None yet

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
2. A `### STAGE REPORT TO COORDINATOR` block
3. When status is complete, a `### NEXT PROMPT — STAGE 2` block; when paused, `### CHAIN PAUSED` instead

## PROPAGATION PROTOCOL — CRITICAL
Return a `STAGE REPORT TO COORDINATOR`. When its status is complete, emit the complete prompt for Stage 2; when paused, emit `CHAIN PAUSED` and no Stage 2 prompt. The next chat has ZERO memory of this one. The Stage 2 prompt must: open with `# STAGE 2/3 — DISTRIBUTION PREP`; copy CHAIN META, WORK FRAME, WORKSPACE, AUTHORITY, and stable INHERITED CONTEXT verbatim; carry verified claims as observed facts and unapproved positioning choices as stage proposals; update "Current state audited" and `⛔ FAILED`; set the task to per-channel copy + schedule and include this protocol for Stage 3. Do not execute Stage 2 here. Stage 3 may publish only when AUTHORITY names the exact channel/action; otherwise it prepares and emits `CHAIN PAUSED` with one approval question. Never copy credentials or API keys.
````
