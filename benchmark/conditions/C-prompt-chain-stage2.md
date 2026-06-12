# Condition C — prompt-chain Stage 2 prompt

Simulates: the work was planned as a 2-stage chain. Chat 1 (outline) ended by emitting the Stage 2 prompt below, per the PROPAGATION PROTOCOL. The fresh chat receives it.

The fresh chat receives exactly this:

```markdown
# STAGE 2/2 — FINAL ANNOUNCEMENT
# Chain: "acme-sync v2 launch announcement"

## CHAIN META
- Total stages: 2
- Current stage: 2/2
- Stage 1: research + approved outline ✅ done
- Stage 2: write the final announcement

## WORKSPACE
Absolute path: none (chat-only)
Target environment: claude.ai chat

## INHERITED CONTEXT — REQUIRED READING

### Chain goal
A ~250-word launch announcement for acme-sync v2 (open-source file sync
CLI), ready to paste into the blog editor.

### Decisions already made
- Angle: "one binary, no daemon" — the differentiator vs rclone/syncthing
- Do NOT mention pricing — a paid tier exists but is unannounced
- Audience: self-hosters, not enterprises

### Voice rules (stable — copy verbatim into every stage)
- Short sentences. Active voice.
- Banned words: seamless, game-changer, robust

### Current state audited (2026-06-12)
- ✅ EXISTS: approved outline — (1) what changed in v2, (2) one binary
  no daemon, (3) how to install
- ⛔ FAILED: opening with a rhetorical question — rejected as generic.
  Do not retry.

## THIS STAGE'S TASK
1. Write the final announcement following the 3-section outline
2. Hard limits: 230–270 words, every voice rule enforced

## CONSTRAINTS
- The outline is locked — write within it, don't restructure

## DELIVERABLES
1. Final announcement, 230–270 words
2. `### CHAIN COMPLETE` block

## FINAL TERMINATION
This is the last stage. End with `### CHAIN COMPLETE` listing the chain
goal, the deliverable, and decisions recorded during the chain. If
blocked, emit `### CHAIN PAUSED` with a direct question instead.
```
