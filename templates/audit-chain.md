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
[FILL: how to reverse any authorized changes; "not applicable — read-only" when true]

### Coordinator
[FILL: chat, person, or role]

## WORKSPACE
Absolute path: `[FILL: absolute path]`
Target environment: [FILL: Claude Code / Cowork]
Destination / audience: [FILL]

## AUTHORITY — COPY VERBATIM
- Authorized in this chain: [FILL: exact actions]
- Requires fresh approval: [FILL: external effects not already authorized]
- Out of scope: [FILL: actions and surfaces]

## INHERITED CONTEXT — REQUIRED READING

### Chain goal
[FILL: one verifiable sentence — e.g. "A severity-ranked audit of X against checklist Y, every finding verified, with an ordered fix list."]

### Operator decisions — frozen
- Checklist / standard to audit against: [FILL: name it or inline it]
- [FILL: scope — folders/areas in, folders/areas out]
- Read-only zones: [FILL: what must never be modified]

### Observed facts
- None yet — Stage 1 collects them

### Stage proposals — not binding until ratified
- None yet

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
2. A `### STAGE REPORT TO COORDINATOR` block
3. When status is complete, a `### NEXT PROMPT — STAGE 2` block; when paused, `### CHAIN PAUSED` instead

## PROPAGATION PROTOCOL — CRITICAL
Return a `STAGE REPORT TO COORDINATOR`. When its status is complete, emit the complete prompt for Stage 2; when paused, emit `CHAIN PAUSED` and no Stage 2 prompt. The next chat has ZERO memory of this one. The Stage 2 prompt must: open with `# STAGE 2/3 — VERIFY`; copy CHAIN META, WORK FRAME, WORKSPACE, AUTHORITY, and stable INHERITED CONTEXT verbatim; carry the raw findings as observed facts, never operator decisions; update "Current state audited" and `⛔ FAILED`; set the task to adversarial verification; include this protocol for Stage 3. Do not execute Stage 2 here. Never widen authorization or copy secrets or client-identifying data.
````
