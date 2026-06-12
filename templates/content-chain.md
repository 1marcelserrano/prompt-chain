# content-chain — 3 stages

For long-form content: essays, guides, course modules, documentation. A fresh chat edits more honestly than the one that wrote the draft — it has no attachment to sentences it didn't write.

**Stage map:** 1. Research + outline → 2. Draft → 3. Cold-read edit + package.

Fill every `[FILL]`, paste into a fresh chat:

````markdown
# STAGE 1/3 — RESEARCH + OUTLINE
# Chain: "[FILL: piece title or working title]"

## CHAIN META
- Total stages: 3
- Current stage: 1/3
- Stage 1: gather material + locked outline
- Stage 2: full draft following the outline, weaknesses flagged
- Stage 3: cold-read edit + final packaged version

## WORKSPACE
Absolute path: [FILL: path, or "none (chat-only)"]
Target environment: [FILL: Claude Code / Cowork / claude.ai chat]

## INHERITED CONTEXT — REQUIRED READING

### Chain goal
[FILL: one verifiable sentence — e.g. "A [N]-word [format] on [topic], ready to paste into [destination]."]

### Decisions already made
- Audience: [FILL]
- Core argument: [FILL: the one thing the piece claims]
- [FILL: structural choices already locked — format, sections, example policy]

### Voice rules (stable — copy verbatim into every stage)
- [FILL: sentence style, person, register]
- Banned words: [FILL]
- [FILL: any house rules — how claims land, how examples work]

### Current state audited ([FILL: date])
- ✅ EXISTS: nothing yet — first stage
- ⛔ FAILED: nothing yet

## THIS STAGE'S TASK
1. Gather the material the piece needs: [FILL: sources, examples, data] — every factual claim gets a source
2. Write the outline: hook, sections with one-line summaries, close — and lock it
3. Choose the core example that carries the piece (one, not three)

## CONSTRAINTS
- No drafting yet — outline quality decides the chain, spend the stage on it

## DELIVERABLES
1. Material list with sources + locked outline + chosen core example
2. A `### NEXT PROMPT — STAGE 2` block

## PROPAGATION PROTOCOL — CRITICAL
At the end of your response, emit a markdown code block containing the complete, self-contained prompt for Stage 2. The next chat has ZERO memory of this one. The Stage 2 prompt must: open with `# STAGE 2/3 — DRAFT`; copy CHAIN META, WORKSPACE, and the Voice rules verbatim; carry the locked outline, the material list, and the core example in full; update "Current state audited" and `⛔ FAILED` (angles or hooks tried and rejected go here, so the draft doesn't resurrect them); set the task to writing the full draft following the outline, flagging the 2 weakest passages with `[WEAK: reason]`; include this same protocol pointing to Stage 3 (Stage 3 replaces it with FINAL TERMINATION — edit, don't rewrite — and ends with `### CHAIN COMPLETE`). If the outline can't be locked without a decision from the user, emit `### CHAIN PAUSED` with the options instead of choosing silently.
````
