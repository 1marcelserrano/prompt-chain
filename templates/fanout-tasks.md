# fanout-tasks — N independent prompts (FAN-OUT mode)

For work that splits into independent pieces sharing one stable context but with **no ordering dependency** — propagate a decision into several repos, fix a set of unrelated findings, one prompt per pending item. Each piece runs cold in its own chat, in any order. There is no propagation between pieces and no `CHAIN COMPLETE`.

Use this instead of a chain when the routing question — *do the pieces depend on each other's output or state?* — answers **no**. If two pieces share state, collapse them into a short chain and treat it as one piece here.

This seed is a **dispatcher**: paste it into one chat, it emits N self-contained piece-prompts. Distribute each to its own chat.

Fill every `[FILL]`, paste into a fresh chat. (The dispatcher block uses a 5-backtick fence; the nested PIECE TEMPLATE uses 4 — keep the levels distinct so neither closes early.)

`````markdown
# DISPATCHER — emit N independent FAN-OUT prompts
# Set: "[FILL: fan-out name, short]"

## YOUR JOB
Emit exactly N self-contained prompts, one per piece listed below. Each follows the PIECE TEMPLATE. Emit each in its own 4-backtick fenced block, in order of the list, with NO propagation between them — they are independent. Do not execute the pieces; just generate the prompts. After the N blocks, stop.

## WORKSPACE
Absolute path: `[FILL: absolute path]`
Target environment: [FILL: Claude Code / Cowork / Chat]
Conventions: [FILL: output folder, naming, language]

## SHARED CONTEXT — copied verbatim into EVERY piece
[FILL: the stable block every piece needs — the shared decision or spec being propagated, design system / tokens, brand voice, hard constraints, read-only zones. If the target environment reads the workspace (Claude Code), reference paths; inline content only for chat-only environments. No secrets — use placeholders like `[API_KEY — in your env]`.]

## PIECES (one prompt each)
1. [FILL: piece 1 — name + one-line Definition of Done]
2. [FILL: piece 2 — name + one-line Definition of Done]
3. [FILL: piece N — name + one-line Definition of Done]

## PIECE TEMPLATE (apply to each piece above)
````markdown
# [piece name] — piece K of N (independent)
# Set: "[fan-out name]"

## WORKSPACE
Absolute path: `[absolute path]`
Target environment: [env]
Conventions: [output folder, naming, language]

## SHARED CONTEXT — REQUIRED READING
[the SHARED CONTEXT block above, verbatim — identical in every piece]

## THIS PIECE'S TASK
1. [the piece's concrete actions, each with a "done" criterion]

## CONSTRAINTS
- [what NOT to do — untouchable files, frozen decisions, read-only zones]

## DELIVERABLES
1. [the piece's file/output]
2. A short report of what changed + anything left for human decision

## INDEPENDENCE NOTE
Self-contained. Shares no dynamic state with the other pieces of "[fan-out name]". Run in its own chat, any order. No next prompt to emit — when the task and deliverables are done, stop. If blocked, ask the user directly (AskUserQuestion if available; otherwise state the blocker in the deliverables and stop) — never guess.
````
`````

Rules that apply to this template:

- The `SHARED CONTEXT` block is copied verbatim into every piece — fill it once, fill it well
- No secrets in any prompt: credentials and tokens never travel in prompt text — use placeholders
- No propagation, no `CHAIN COMPLETE` — each piece reports and ends on its own
- If a piece gets blocked, it asks (AskUserQuestion or a written question) and stops — it never guesses, and the other pieces are unaffected
- One real dependency hiding in the set? Pull the dependent pair into a 2-stage chain (see [refactor-chain.md](./refactor-chain.md)) and list that chain as a single piece here

Want the sequential cousin? See the chain templates in this folder — use them when order is load-bearing.
