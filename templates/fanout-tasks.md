# fanout-tasks — N independent prompts (FAN-OUT mode)

For work that splits into independent pieces sharing one stable context but with **no ordering dependency** — propagate a decision into several repos, fix unrelated findings, or create one prompt per pending item. Each piece runs cold in its own chat, in any order, and returns a result envelope to the coordinator. There is no propagation between pieces. Add a collector only when the set needs a combined result.

Use this instead of a chain when the routing question — *do the pieces depend on each other's output or state?* — answers **no**. If two pieces share state, collapse them into a short chain and treat it as one piece here.

This seed is a **dispatcher**: paste it into one chat, it emits N self-contained piece-prompts. Distribute each to its own chat.

Fill every `[FILL]`, paste into a fresh chat. (The dispatcher block uses a 5-backtick fence; the nested PIECE TEMPLATE uses 4 — keep the levels distinct so neither closes early.)

`````markdown
# DISPATCHER — emit N independent FAN-OUT prompts
# Set: "[FILL: fan-out name, short]"

## YOUR JOB
Emit exactly N self-contained prompts, one per piece listed below. Each follows the PIECE TEMPLATE. Emit each in its own 4-backtick fenced block, in order of the list, with NO propagation between them. When COMBINED RESULT says yes, emit one COLLECTOR prompt after the N pieces. Do not execute any prompt.

## WORK FRAME — copied verbatim into EVERY piece and the collector

### Original ask
> [FILL: the operator's exact words]

### Done
[FILL: what makes each piece complete; if there is a combined result, what makes the set complete]

### Work class and risk
[FILL: production / personal-pre-production / one-shot; risk; what a revert cannot undo]

### Budget / checkpoint
[FILL: number of pieces and when they return to the coordinator]

### Undo
[FILL: revert path per piece]

### Coordinator
[FILL: chat, person, or role collecting results]

## WORKSPACE
Absolute path: `[FILL: absolute path]`
Target environment: [FILL: workspace-capable agent / chat-only agent / other named client]
Conventions: [FILL: output folder, naming, language]
Destination / audience: [FILL]

## AUTHORITY — copied verbatim into EVERY piece and the collector
- Authorized in this set: [FILL: exact actions]
- Requires fresh approval: [FILL: external effects not already authorized]
- Out of scope: [FILL: actions and surfaces]

## SHARED CONTEXT — copied verbatim into EVERY piece

### Operator decisions — frozen
- [FILL: explicit operator decisions only]

### Observed facts
- [FILL: evidence-backed facts shared by the set]

### Shared proposals — not binding until ratified
- [FILL: inherited model recommendations relevant to every piece]

### Shared stable context
[FILL: specification, design system / tokens, brand voice, hard constraints, and read-only zones. Reference paths when the environment can read them. No secrets; minimize personal or confidential data for the named destination.]

## PIECES (one prompt each)
1. [FILL: piece 1 — name + one-line Definition of Done]
2. [FILL: piece 2 — name + one-line Definition of Done]
3. [FILL: piece N — name + one-line Definition of Done]

## COMBINED RESULT
[FILL: yes — name the synthesis / no — the piece results are the final deliverables]

## PIECE TEMPLATE (apply to each piece above)
````markdown
# [piece name] — piece K of N (independent)
# Set: "[fan-out name]"

## WORK FRAME — COPY VERBATIM
[the WORK FRAME above]

## WORKSPACE
Absolute path: `[absolute path]`
Target environment: [env]
Conventions: [output folder, naming, language]
Destination / audience: [who receives this result]

## AUTHORITY — COPY VERBATIM
[the AUTHORITY block above]

## SHARED CONTEXT — REQUIRED READING
[the SHARED CONTEXT block above, verbatim — identical in every piece]

## THIS PIECE'S TASK
1. [the piece's concrete actions, each with a "done" criterion]

## CONSTRAINTS
- [what NOT to do — untouchable files, frozen decisions, read-only zones]

## DELIVERABLES
1. [the piece's file/output]
2. The result envelope below

## RESULT FOR COORDINATOR — REQUIRED
- Piece: K of N — [name]
- Status: [complete / blocked]
- Deliverables: [paths or outputs]
- Evidence: [checks run and observed result]
- Observed facts added: [...]
- Stage proposals awaiting ratification: [...]
- Operator decisions recorded in this piece: [none / quote the decision and its exact scope]
- Operator decision or approval needed: [none / one narrow question]

## INDEPENDENCE NOTE
Self-contained. Shares no dynamic state with the other pieces of "[fan-out name]". Run in its own chat, any order. No next prompt to emit — when the task and deliverables are done, stop. If blocked, use the environment's interactive question capability when available; otherwise state the blocker in the deliverables and stop. Never guess.
````

## COLLECTOR TEMPLATE — emit only when COMBINED RESULT is yes
````markdown
# COLLECTOR — [fan-out name]

## WORK FRAME / WORKSPACE / AUTHORITY / SHARED CONTEXT
[copy the same blocks verbatim, including non-binding shared proposals]

## REQUIRED INPUTS
- Required piece 1 result: [paste RESULT FOR COORDINATOR]
- Required piece 2 result: [paste RESULT FOR COORDINATOR]
- ...
- Required piece N result: [paste RESULT FOR COORDINATOR]

## TASK
1. Verify every required piece is present or explicitly waived by the coordinator.
2. Reconcile conflicts, duplicates, and gaps without inventing missing evidence.
3. Produce the combined deliverable and set-wide completion report.

## COMPLETION
Emit `### SET COMPLETE` only when the combined Done statement is true. Otherwise emit `### SET PAUSED` with one narrow question for the coordinator.
````
`````

Rules that apply to this template:

- The `SHARED CONTEXT` block is copied verbatim into every piece — fill it once, fill it well
- No secrets in any prompt: credentials and tokens never travel in prompt text — use placeholders
- No propagation and no per-piece `CHAIN COMPLETE` — each piece returns its result envelope and ends
- When the set has a combined result, only the collector can emit `SET COMPLETE`
- Operator decisions, observed facts, and stage proposals keep their labels
- Permission never widens between dispatcher, pieces, and collector
- If a piece gets blocked, it asks interactively or in writing and stops — it never guesses, and the other pieces are unaffected
- One real dependency hiding in the set? Pull the dependent pair into a 2-stage chain (see [refactor-chain.md](./refactor-chain.md)) and list that chain as a single piece here

Want the sequential cousin? See the chain templates in this folder — use them when order is load-bearing.
