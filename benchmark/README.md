# Qualitative benchmark — cold-start continuation

**Question:** a long task dies mid-way. A fresh chat must finish it. How much of the work survives, under three continuation protocols?

This is a small, qualitative, fully reproducible experiment — n=1 per condition, one model, one task. It illustrates failure modes; it does not prove statistics. Raw transcripts are in [runs/](./runs/).

## Setup

One fictional task with a mid-point: *phase 1 (a previous session) approved an outline for a ~250-word launch announcement, made 3 decisions (angle "one binary, no daemon"; never mention pricing; audience = self-hosters), set voice rules, and rejected one approach (rhetorical-question opening).* Phase 2 must produce the final text in a fresh session.

Three conditions — the fresh session receives a different artifact in each:

| Condition | Artifact | Simulates |
|---|---|---|
| [A — single-prompt restart](./conditions/A-single-prompt-restart.md) | The original brief only | Chat died, nothing was saved |
| [B — handoff snapshot](./conditions/B-handoff-snapshot.md) | A HANDOFF.md (status, decisions, failed approaches, style) — structure faithful to real handoff tools | Reactive session-handoff |
| [C — prompt-chain Stage 2](./conditions/C-prompt-chain-stage2.md) | The Stage 2 prompt a chain would emit (chain goal, inherited context, `⛔ FAILED`, DoD, FINAL TERMINATION) | Planned propagation |

Runner: Claude Haiku 4.5, one shot per condition, 2026-06-12. The artifact was the session's first and only message.

## Results

| Check | A | B | C |
|---|---|---|---|
| Produced the deliverable without asking the user to re-explain | ❌ stalled, asked for the outline back | ✅ | ✅ |
| Kept the decided angle ("one binary, no daemon") | — | ✅ | ✅ |
| Respected "never mention pricing" | — | ✅ | ✅ |
| Avoided the already-rejected opening | — | ✅ | ✅ |
| Enforced voice rules (banned words) | — | ✅ | ✅ |
| Word target carried and hit | — | ❌ target never traveled in the snapshot; output ~200 words vs ~250 brief | ✅ 242 words, inside the 230–270 DoD, self-audited |
| Wrote inside the approved outline | — | ❌ snapshot didn't carry the outline; invented its own structure | ⚠️ all 3 sections present, order shifted |
| Closed the task cleanly | ❌ | ❌ ended with "Want me to adjust...?" | ✅ `CHAIN COMPLETE` acta with decisions recorded |

## Honest reading

- **A is the disaster the other two exist to prevent.** The fresh session had nothing, so it stopped and asked the user to re-supply everything the dead chat knew. That's the re-explanation tax.
- **A good handoff carries decisions well.** Condition B respected the angle, the pricing embargo, the rejected opening, and the voice rules — real handoff tools that capture decisions and failed approaches earn that result. If all you need is "don't lose what we decided", a handoff does the job.
- **What the snapshot dropped was the spec, not the state.** The word target and the outline lived in the original brief — the snapshot summarized them away. The chain template forces the chain goal and deliverable spec to travel verbatim, so condition C landed inside the DoD and closed with an acta instead of an open question.
- **Neither protocol prevents invention.** Both B and C invented product details (the product is fictional and neither artifact included a feature list). Continuation protocols carry context; they don't create facts. Put the facts in the chain or expect the model to fill gaps.

## Limitations

- n=1 per condition, single model, single task — failure modes shown are real, frequencies are not measured
- All three artifacts were written by the benchmark author; condition B follows the structure of real handoff tools (status / key decisions / what we tried / next steps) but is not the output of any specific tool
- The task is small; context-window exhaustion itself is not reproduced here, only the cold-start that follows it

## Reproduce it

1. Open three fresh chats (any Claude interface; we used Haiku 4.5)
2. Paste each condition file's artifact as the first message
3. Score against the checks table — they're binary and need no judge

Different task, more runs, other models — PRs with new run folders are welcome.
