# Example — 2-stage writing chain

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

## WORKSPACE
Absolute path: none (chat-only)
Target environment: claude.ai chat

## INHERITED CONTEXT — REQUIRED READING

### Chain goal
A 1,500-word newsletter essay titled "Why Tools Beat Willpower", ready to paste into the newsletter editor.

### Decisions already made
- Audience: solo founders, non-technical
- One core example carried through the whole essay (no example soup)

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
2. A `### NEXT PROMPT — STAGE 2` block

## PROPAGATION PROTOCOL — CRITICAL
At the end of your response, emit a markdown code block with the complete, self-contained prompt for Stage 2. The next chat has ZERO memory of this one. It must: copy CHAIN META, WORKSPACE, and the Voice rules verbatim; update "Current state audited" and `⛔ FAILED`; include the FULL draft inside the prompt (the next chat cannot see this one); set Stage 2's task to edit, not rewrite; replace this protocol with FINAL TERMINATION. If blocked, emit `### CHAIN PAUSED` instead.
````

## What chat 1 emitted at the end of its response

````markdown
### NEXT PROMPT — STAGE 2

# STAGE 2/2 — COLD-READ EDIT + FINAL
# Chain: "Essay: Why Tools Beat Willpower"

## CHAIN META
- Total stages: 2
- Current stage: 2/2
- Stage 1: outline + full first draft ✅ done
- Stage 2: cold-read edit + final version

## WORKSPACE
Absolute path: none (chat-only)
Target environment: claude.ai chat

## INHERITED CONTEXT — REQUIRED READING

### Chain goal
A 1,500-word newsletter essay titled "Why Tools Beat Willpower", ready to paste into the newsletter editor.

### Decisions already made
- Audience: solo founders, non-technical
- One core example carried through: the shared-calendar story (chosen in Stage 1 — do not swap it)

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

The Stage 2 chat has no attachment to the draft's sentences — it cuts what the Stage 1 chat would have defended. The voice rules arrived identical in both stages, so the edit enforces the same standard the draft was written under. And the `⛔ FAILED` line stopped chat 2 from "improving" the opening back into the statistic that already failed.
