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

## WORKSPACE
Absolute path: `[FILL: absolute repo path]`
Target environment: Claude Code

## INHERITED CONTEXT — REQUIRED READING

### Chain goal
[FILL: one verifiable sentence — e.g. "module X under 600 lines with identical test results and identical CLI output."]

### Decisions already made
- [FILL: techniques in / out — e.g. "no new dependencies", "keep the public API frozen"]

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
2. A `### NEXT PROMPT — STAGE 2` block

## PROPAGATION PROTOCOL — CRITICAL
At the end of your response, emit a markdown code block containing the complete, self-contained prompt for Stage 2. The next chat has ZERO memory of this one. The Stage 2 prompt must: open with `# STAGE 2/3 — EXECUTE`; copy CHAIN META, WORKSPACE, and all stable INHERITED CONTEXT verbatim; carry the baseline and the full cut plan; update "Current state audited" and `⛔ FAILED` (any approach considered and discarded goes here, with the reason); set the task to executing the plan step by step, re-running tests after each step; include this same protocol pointing to Stage 3 (Stage 3 replaces it with FINAL TERMINATION and ends with `### CHAIN COMPLETE`). Reference files by path — never paste file contents into the chain. Never copy credentials into the next prompt. If a step breaks the baseline and the fix isn't obvious, emit `### CHAIN PAUSED` instead of improvising.
````
