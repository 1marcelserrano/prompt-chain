# Illustrative example — 2-stage writing chain

Scenario: a 1,500-word newsletter essay. Drafting and editing want different mindsets — and a fresh chat edits more honestly than the one that wrote the draft. Split: outline + draft → cold-read edit + final.

Note how the **voice rules travel verbatim** in both stages: that's stable context. The draft itself is what moves: that's dynamic context.

## Stage 1 — what the user pastes into a fresh chat

````markdown
# STAGE 1/2 — OUTLINE + DRAFT
# Chain: "Essay: Why Tools Beat Willpower"

## CHAIN META
- Total stages: 2
- Current stage: 1/2
- Stage 1: outline + full first draft
- Stage 2: cold-read edit + final version

## WORK FRAME — COPY VERBATIM

### Original ask
> Draft a 1,500-word newsletter essay for non-technical solo founders, using the shared-calendar story as the one core example. A fresh chat should edit it. Do not publish or send it.

### Done
A clean essay of at most 1,500 words, ready for the operator to review before publication.

### Work class and risk
Personal/pre-production writing; low risk; undo by restoring the prior draft.

### Budget / checkpoint
Two stages. Return to the original chat after each stage.

### Undo
Keep the first draft and restore it if the edit loses the argument or voice.

### Coordinator
The original chat that created this chain.

## WORKSPACE
Absolute path: none (chat-only)
Target environment: claude.ai chat
Destination / audience: private draft for the operator

## AUTHORITY — COPY VERBATIM
- Authorized in this chain: draft and edit the essay
- Requires fresh approval: publishing, sending, or changing the intended audience
- Out of scope: newsletter account actions and promotional distribution

## INHERITED CONTEXT — REQUIRED READING

### Chain goal
A 1,500-word newsletter essay titled "Why Tools Beat Willpower", ready to paste into the newsletter editor.

### Operator decisions — frozen
- Audience: solo founders, non-technical
- The shared-calendar story is the one core example carried through the essay

### Observed facts
- None yet

### Stage proposals — not binding until ratified
- None yet

### Voice rules (stable — copy verbatim into every stage)
- Short sentences. Active voice. No filler.
- Banned words: game-changer, leverage, empower, seamless
- Every abstract claim lands on a concrete example within 2 sentences

### Current state audited (2026-06-12)
- ✅ EXISTS: nothing yet
- ⛔ FAILED: nothing yet

## THIS STAGE'S TASK
1. Outline: hook, 3 sections, close — one line each
2. Write the full first draft (~1,500 words) following the outline
3. Flag the 2 weakest passages with `[WEAK: reason]` inline

## DELIVERABLES
1. Outline + full draft with weakness flags
2. A `### STAGE REPORT TO COORDINATOR` block
3. A `### NEXT PROMPT — STAGE 2` block

## PROPAGATION PROTOCOL — CRITICAL
Return a `STAGE REPORT TO COORDINATOR`, then emit the complete prompt for Stage 2. Copy CHAIN META, WORK FRAME, WORKSPACE, AUTHORITY, operator decisions, and Voice rules verbatim. Carry draft properties as Observed facts and editorial recommendations as Stage proposals. Include the full draft, set Stage 2 to edit rather than rewrite, and use FINAL TERMINATION. Do not execute Stage 2 here or publish/send the essay. If blocked, emit `### CHAIN PAUSED`.
````

## Illustrative emission from chat 1

````markdown
### STAGE REPORT TO COORDINATOR

- Status: complete
- Deliverables: outline and 1,580-word first draft
- Evidence: word count checked; two weak passages marked
- Observed facts added: the draft is 80 words over target
- Stage proposals awaiting ratification: none
- Operator decision or approval needed: none for editing; publication remains unauthorized

### NEXT PROMPT — STAGE 2

# STAGE 2/2 — COLD-READ EDIT + FINAL
# Chain: "Essay: Why Tools Beat Willpower"

## CHAIN META
- Total stages: 2
- Current stage: 2/2
- Stage 1: outline + full first draft ✅ done
- Stage 2: cold-read edit + final version

## WORK FRAME — COPY VERBATIM

### Original ask
> Draft a 1,500-word newsletter essay for non-technical solo founders, using the shared-calendar story as the one core example. A fresh chat should edit it. Do not publish or send it.

### Done
A clean essay of at most 1,500 words, ready for the operator to review before publication.

### Work class and risk
Personal/pre-production writing; low risk; undo by restoring the prior draft.

### Budget / checkpoint
Two stages. Return to the original chat after each stage.

### Undo
Keep the first draft and restore it if the edit loses the argument or voice.

### Coordinator
The original chat that created this chain.

## WORKSPACE
Absolute path: none (chat-only)
Target environment: claude.ai chat
Destination / audience: private draft for the operator

## AUTHORITY — COPY VERBATIM
- Authorized in this chain: draft and edit the essay
- Requires fresh approval: publishing, sending, or changing the intended audience
- Out of scope: newsletter account actions and promotional distribution

## INHERITED CONTEXT — REQUIRED READING

### Chain goal
A 1,500-word newsletter essay titled "Why Tools Beat Willpower", ready to paste into the newsletter editor.

### Operator decisions — frozen
- Audience: solo founders, non-technical
- The shared-calendar story is the one core example — do not swap it

### Observed facts
- The first draft is 1,580 words and has two passages marked `[WEAK]`

### Stage proposals — not binding until ratified
- None

### Voice rules (stable — copy verbatim into every stage)
- Short sentences. Active voice. No filler.
- Banned words: game-changer, leverage, empower, seamless
- Every abstract claim lands on a concrete example within 2 sentences

### Current state audited (2026-06-12)
- ✅ EXISTS: full draft, 1,580 words, 2 passages flagged `[WEAK]`
- ⛔ FAILED: opening with a statistic — felt generic, replaced with the calendar story. Don't revert to a stat hook.

### The draft (Stage 1 output — full text)
[...the complete 1,580-word draft exactly as written, including the two [WEAK] flags...]

## THIS STAGE'S TASK
1. Read the draft as a cold editor who never saw Stage 1
2. Fix the 2 `[WEAK]` passages first
3. Cut to ≤1,500 words; enforce every voice rule; remove anything a tired reader would skip
4. Output the final clean version, no flags

## CONSTRAINTS
- Edit, don't rewrite — the structure and the calendar example stay

## DELIVERABLES
1. Final essay, ≤1,500 words
2. `### CHAIN COMPLETE` block

## FINAL TERMINATION
This is the last stage. End with `### CHAIN COMPLETE` listing the chain goal, deliverables, and decisions recorded in both stages. If blocked, emit `### CHAIN PAUSED` instead.
````

## Why this split works

The Stage 2 chat has no attachment to the draft's sentences — it cuts what the Stage 1 chat would have defended. The voice rules and authority arrived identical in both stages, so the edit enforces the same standard without silently publishing the result. The `⛔ FAILED` line stopped chat 2 from "improving" the opening back into the statistic that already failed.
