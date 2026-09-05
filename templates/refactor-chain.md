# refactor-chain — 3 stages

For refactors that must not change behavior. Mapping, executing, and validating want different mindsets — and the validator should not be the chat that's attached to the changes it just made.

**Stage map:** 1. Map + plan (inventory, baseline, cut plan) → 2. Execute (apply the plan) → 3. Validate (prove behavior unchanged).

Fill every `[FILL]`, paste into a fresh chat:

````markdown
# STAGE 1/3 — MAP + PLAN
# Chain: "[FILL: refactor name, short]"

## CHAIN META
- Total stages: 3
- Current stage: 1/3
- Stage 1: inventory the target, capture a behavior baseline, write the cut plan
- Stage 2: execute the plan, smallest safe steps first
- Stage 3: validate against the baseline, fix drift, report

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
[FILL: revert path]

### Coordinator
[FILL: chat, person, or role]

## WORKSPACE
Absolute path: `[FILL: absolute repo path]`
Target environment: Claude Code
Destination / audience: [FILL]

## AUTHORITY — COPY VERBATIM
- Authorized in this chain: [FILL: files and local checks]
- Requires fresh approval: [FILL: commit, push, PR, deploy, or other external effects]
- Out of scope: [FILL: frozen APIs, data, or directories]

## INHERITED CONTEXT — REQUIRED READING

### Chain goal
[FILL: one verifiable sentence — e.g. "module X under 600 lines with identical test results and identical CLI output."]

### Operator decisions — frozen
- [FILL: techniques in / out — e.g. "no new dependencies", "keep the public API frozen"]

### Observed facts
- [FILL: baseline evidence, or "none yet"]

### Stage proposals — not binding until ratified
- None yet

### Stable context (copy verbatim into every stage)
- Test command: `[FILL]`
- Conventions: [FILL: style guide, naming, commit format]
- Frozen surfaces: [FILL: files/APIs that must not change]

### Current state audited ([FILL: date])
- ✅ EXISTS: [FILL: target files + current metrics — lines, test status]
- ⛔ FAILED: nothing yet

## THIS STAGE'S TASK
1. Inventory: map duplications, dead code, and coupling in [FILL: target] — reference file paths, don't paste file contents into the chain
2. Capture the baseline: run `[FILL: test command]` and record the exact passing state
3. Write the cut plan ordered by risk: reversible edits first, structural moves last, each step with its own "done" check

## CONSTRAINTS
- No code changes in this stage — plan only

## DELIVERABLES
1. Inventory + baseline + ordered cut plan
2. A `### STAGE REPORT TO COORDINATOR` block
3. When status is complete, a `### NEXT PROMPT — STAGE 2` block; when paused, `### CHAIN PAUSED` instead

## PROPAGATION PROTOCOL — CRITICAL
Return a `STAGE REPORT TO COORDINATOR`. When its status is complete, emit the complete prompt for Stage 2; when paused, emit `CHAIN PAUSED` and no Stage 2 prompt. The next chat has ZERO memory of this one. The Stage 2 prompt must: open with `# STAGE 2/3 — EXECUTE`; copy CHAIN META, WORK FRAME, WORKSPACE, AUTHORITY, and stable INHERITED CONTEXT verbatim; carry the baseline as observed facts and the cut plan as a stage proposal until ratified; update "Current state audited" and `⛔ FAILED`; set the task to execute the approved plan and include this protocol for Stage 3. Do not execute Stage 2 here or commit/push unless exactly authorized. Reference files by path and never copy credentials.
````
