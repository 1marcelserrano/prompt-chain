# audit-chain — 3 stages

For auditing a repo, workspace, codebase, or content set. Finding and judging are different jobs: the inventory chat collects without opinion, the verification chat is paid to be skeptical, and the report chat only writes what survived.

**Stage map:** 1. Inventory (collect, no judgment) → 2. Verify findings (confirm or kill each one) → 3. Report + fix list.

Fill every `[FILL]`, paste into a fresh chat:

````markdown
# STAGE 1/3 — INVENTORY
# Chain: "[FILL: audit target, short]"

## CHAIN META
- Total stages: 3
- Current stage: 1/3
- Stage 1: inventory — sweep the target, collect raw findings without judgment
- Stage 2: verify — confirm or kill each finding against evidence
- Stage 3: report — severity-ranked report + ordered fix list

## WORKSPACE
Absolute path: `[FILL: absolute path]`
Target environment: [FILL: Claude Code / Cowork]

## INHERITED CONTEXT — REQUIRED READING

### Chain goal
[FILL: one verifiable sentence — e.g. "A severity-ranked audit of X against checklist Y, every finding verified, with an ordered fix list."]

### Decisions already made
- Checklist / standard to audit against: [FILL: name it or inline it]
- [FILL: scope — folders/areas in, folders/areas out]
- Read-only zones: [FILL: what must never be modified]

### Stable context (copy verbatim into every stage)
- Severity scale: [FILL: e.g. CRITICAL / HIGH / LOW, with one-line definitions]
- Output language and format: [FILL]
- Confidentiality: findings never include [FILL: client names, secrets, personal data]

### Current state audited ([FILL: date])
- ✅ EXISTS: nothing yet — first stage
- ⛔ FAILED: nothing yet

## THIS STAGE'S TASK
1. Sweep [FILL: target] item by item against the checklist — reference paths, don't paste file contents into the chain
2. Record every potential finding: location, what was observed, which checklist item it touches — no severity, no judgment yet
3. Output the raw findings table

## CONSTRAINTS
- Read-only stage: observe and record, change nothing
- No judgment calls — ambiguous items go in as findings with a `?` flag

## DELIVERABLES
1. Raw findings table
2. A `### NEXT PROMPT — STAGE 2` block

## PROPAGATION PROTOCOL — CRITICAL
At the end of your response, emit a markdown code block containing the complete, self-contained prompt for Stage 2. The next chat has ZERO memory of this one. The Stage 2 prompt must: open with `# STAGE 2/3 — VERIFY`; copy CHAIN META, WORKSPACE, and all stable INHERITED CONTEXT verbatim; carry the full raw findings table; update "Current state audited" and `⛔ FAILED` (areas that couldn't be swept and why); set the task to adversarial verification — for each finding, try to refute it before confirming; include this same protocol pointing to Stage 3 (Stage 3 replaces it with FINAL TERMINATION and ends with `### CHAIN COMPLETE`). Never copy secrets or client-identifying data into the next prompt. If the checklist is ambiguous on a load-bearing item, emit `### CHAIN PAUSED` with the question instead of interpreting.
````
