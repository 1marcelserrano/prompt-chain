---
name: prompt-chain
description: >-
  Builds self-contained prompts for work that must move across isolated chat
  sessions without losing context or authority. Use CHAIN when each stage
  depends on the previous stage's output and must emit the next cold-start
  prompt. Use FAN-OUT when independent pieces need one prompt each, possibly
  followed by a collector. Trigger on requests such as "prompt that generates
  the next", "run each stage in a new chat", "one prompt per task", "cold-start
  handoff", "executar por etapas em chats separados", or "um prompt por
  pendência". Do not use for a single direct task, open-ended exploration, or
  same-session parallel subagents.
license: MIT
metadata:
  version: "2.3.0"
---

# Prompt Chain

Turns a multi-step task into self-contained prompts, each run in a fresh chat with full context carried forward. Two modes:

- **CHAIN** — sequential. Each prompt runs one stage and ends by emitting the next stage's prompt with the accumulated context already inside it. The user copies and pastes between chats; the chain propagates itself until `CHAIN COMPLETE`. Use when the pieces have an ordering dependency.
- **FAN-OUT** — independent. One self-contained prompt per piece, all sharing the same stable context but with no propagation between them. The user opens each in its own chat, in any order (or at the same time). Use when the pieces don't depend on each other.

**Prompts carry work, not expanded authority.** Facts, proposals, operator decisions, and permissions keep their original status as they move between chats. A later stage may not silently promote a model conclusion into an operator decision or broaden an authorization.

## Two modes — how to route

Ask one question: **do the pieces depend on each other's output or state?**

- **Yes → CHAIN.** Stage 2 needs what Stage 1 produced (refactor → validate; outline → draft; research → synthesize). Order is load-bearing, so dynamic state has to travel forward.
- **No → FAN-OUT.** Each piece is its own closed task that merely shares stable context (propagate one decision into three repos; fix five unrelated audit findings; one prompt per pending item). No order, no shared dynamic state.

Edge cases:
- **Mostly independent, one dependency** → FAN-OUT for the independent pieces + one short CHAIN for the dependent pair, treated as a single piece of the fan-out. Don't force the whole thing sequential.
- **Same session, truly parallel, no isolation needed** → not this skill. Use parallel subagents — they run concurrently inside one session. FAN-OUT is for when you specifically want *isolated chats* (cold start, hand-off, different people / models / times) without an ordering dependency.

Everything from here down to "FAN-OUT mode" describes CHAIN. The FAN-OUT section covers only what changes for independent prompts.

## When to use

- Large task with distinct phases (P0 → P1 → P2), each with its own deliverables
- User wants to isolate context between stages (new chat = clean memory, cold cache, isolated execution)
- User explicitly asks for "a prompt that generates the next one" (CHAIN) or "one prompt per task / per pending item" (FAN-OUT)
- Work that benefits from pausing between stages to review output before continuing
- Several independent pieces that share context and each deserve an isolated, hand-offable chat (FAN-OUT)
- Environments where the same agent can't run the whole thing (session limits, audit policy, model switching)

## When NOT to use

- Single-step task → solve it directly, no overhead
- Task whose intermediate state fits in one session with no risk of overflow → a task list plus direct execution is better
- Exploratory work without discrete deliverables → both modes assume pieces with a clear Definition of Done
- Same-session parallelism with no need for isolated chats → use parallel subagents instead (they run concurrently in one session). Wanting *isolated* chats for pieces that have no ordering dependency is not a reason to avoid the skill — that's FAN-OUT mode

## Mental model

A chain is a sequence of stages. Each stage:
1. Receives a self-contained prompt (pasteable cold into a new chat)
2. Executes one slice of the work
3. Emits the next stage's prompt with updated context

Separate **stable context from dynamic context**.

- **Stable** — workspace path, design system, brand voice, global constraints, final goal. Copied verbatim into every stage.
- **Dynamic** — current file state, decisions made, blockers found. Updated stage by stage.

If the chain loses stable context, the next chat re-makes decisions. If it loses dynamic context, it redoes work. Either failure destroys the value.

In **FAN-OUT** mode there is no dynamic carry-forward — every prompt is stable context plus one closed task. That makes the stable context the *only* thing keeping the pieces coherent, so completing it well matters even more (see "FAN-OUT mode" below).

## How to build a chain

### Step 1 — Frame the work and extract stable context

Before decomposing, separate out:

- **Original ask, verbatim** — the operator's words, not a plan summary.
- **Final goal** — what does "chain complete" mean? A single, verifiable statement.
- **Work class and risk** — production, personal/pre-production, or one-shot; what a revert cannot undo.
- **Budget / checkpoint** — the agreed slice or time boundary and what happens when it is reached.
- **Undo** — how to reverse the work if the stage is wrong.
- **Workspace** — absolute path + conventions (output folder, naming, language).
- **Constraints that don't change** — design system, compliance, brand voice, output format.
- **Authority** — what is authorized, what requires fresh approval, and what is out of scope.
- **Operator decisions** — only what the user has explicitly settled and won't reopen.
- **Target environment and audience** — what the next chat can access and who will receive the prompt.

The work frame and authority block go into every stage unchanged. Observed facts, stage proposals, current state, and failed approaches are dynamic; their labels travel with them.

### Step 2 — Decompose into 2 to 6 stages

**Cutting heuristics:**
- Each stage has a concrete, verifiable deliverable (file created, decision made, output validated)
- A stage never depends on the previous stage's internal state (variables, buffers) — only on files and recorded decisions
- Prioritize by dependency and risk: P0 (blockers) → P1 (high impact) → P2 (polish)

**Ideal count:**
- **2 stages** — natural split into "build" → "validate/polish"
- **3–4 stages** — sweet spot for most cases
- **5–6 stages** — only when each phase carries > 10 min of work on its own
- **> 6** — regroup. The chain is sliced too thin and the overhead outweighs the gain.

**The 10-minute test:** if a stage takes < 5 min of real work, merge it with its neighbor. If it takes > 30 min, split it. Target: 10–20 min per stage.

### Step 3 — Write Stage 1 (the seed prompt)

Use the canonical template in the next section. This is the only prompt the user pastes manually; the chain generates the rest on its own.

### Step 4 — Hand it to the user

Deliver Stage 1 as a copyable code block, with a short usage instruction above it:

> 1. Open a new chat in environment [X]
> 2. Paste the STAGE 1 block
> 3. At the end of the response, copy the `### NEXT PROMPT — STAGE 2` block and paste it into a new chat
> 4. Repeat until `CHAIN COMPLETE`

## Canonical STAGE template

Copy-paste verbatim, adjusting the content. Every stage in the chain uses this structure.

````markdown
# STAGE N/TOTAL — [SHORT_NAME]
# Chain: "[CHAIN NAME]"

## CHAIN META
- Total stages: TOTAL
- Current stage: N/TOTAL
- Stage 1 goal: [...]
- Stage 2 goal: [...]
- (every stage summarized in one line each)

## WORK FRAME — COPY VERBATIM

### Original ask
> [the operator's exact words]

### Done
[single verifiable statement of what completes the chain]

### Work class and risk
[production / personal-pre-production / one-shot; low / medium / high; what a revert cannot undo]

### Budget / checkpoint
[slice or time boundary; return to the coordinator when reached]

### Undo
[how to reverse this work]

### Coordinator
[the chat, person, or role that reviews each stage report and authorizes continuation]

## WORKSPACE
Absolute path: `[absolute path]`
Target environment: [workspace-capable agent / chat-only agent / other named client]
[Destination / audience: who receives this prompt and what they can access]
[Relevant conventions: output folder, naming, language]

## AUTHORITY — COPY VERBATIM
- Authorized in this chain: [exact actions the original ask permits]
- Requires fresh approval: [publish / send / open PR / push / deploy / merge / pay / delete / change permissions, unless exactly authorized above]
- Out of scope: [surfaces and actions this chain must not touch]

## INHERITED CONTEXT — REQUIRED READING

### Chain goal
[Single statement of what "chain complete" means]

### Operator decisions — frozen
- [only explicit operator decision 1 — do not reopen]
- [only explicit operator decision 2 — do not reopen]

### Observed facts
- [evidence-backed fact; include source or file path]

### Stage proposals — not binding until ratified
- [recommendation or judgment produced by a stage]

### Current state audited ([YYYY-MM-DD])
- ✅ EXISTS: [files created by previous stages]
- ❌ MISSING: [missing files]
- ⚠️ [nuances, warnings, gotchas]
- ⛔ FAILED: [approaches already tried that did not work, with the error — do not retry]

### [Stable context: design system / voice / compliance / etc.]
[Literal blocks, copied verbatim into every stage]

## THIS STAGE'S TASK
1. [concrete action with a "done" criterion]
2. [concrete action with a "done" criterion]
...

## CONSTRAINTS
- [what NOT to do in this stage — untouchable files, frozen decisions]

## DELIVERABLES
1. [file/output 1]
2. [file/output 2]
...
N. **REQUIRED**: a `### STAGE REPORT TO COORDINATOR` block
N+1. **REQUIRED WHEN STATUS IS COMPLETE**: a `### NEXT PROMPT — STAGE N+1` block (or `### CHAIN COMPLETE` if N = TOTAL). When status is paused, emit `### CHAIN PAUSED` instead.

## PROPAGATION PROTOCOL — CRITICAL
When this stage is complete, emit a markdown code block containing the complete, self-contained prompt for Stage N+1. When it is paused, emit `### CHAIN PAUSED` and no next-stage prompt. The next chat will have ZERO memory of this one. The Stage N+1 prompt must:

- Open with `# STAGE N+1/TOTAL — [NAME]`
- Copy CHAIN META, WORK FRAME, WORKSPACE, AUTHORITY, and all stable INHERITED CONTEXT from this prompt verbatim
- Update "Observed facts", "Stage proposals", and "Current state audited" with what you just did
- Update "Operator decisions — frozen" only with an explicit user decision recorded during this stage; never promote a stage proposal on your own
- Replace the TASK with Stage N+1's action list (see CHAIN META above)
- Include this same PROPAGATION PROTOCOL for Stage N+2 (or replace it with FINAL TERMINATION if Stage N+1 is the last)
- Return both the stage report and next prompt to the coordinator; do not start Stage N+1 in this chat

If this stage cannot be completed (blocker, ambiguity, missing input), emit a `### CHAIN PAUSED` block instead of the next prompt (see protocols).
````

## Transition protocols

### PROPAGATION PROTOCOL (stage → next stage)

Every **complete** non-final stage response ends with the header below. A paused response uses `### CHAIN PAUSED` instead and must not contain a next-stage prompt.

```
### NEXT PROMPT — STAGE N+1
```

Followed by a closed markdown code block. **Watch the fence escaping**: since the next prompt's content contains triple backticks, use a **4-backtick** fence on the outer block (or `~~~~` as an alternative). This keeps the parser from closing the block early.

Principles:
- **Never abbreviate with "same as before"** — the next chat doesn't have the previous one
- **Copying stable context verbatim is the correct behavior**, not redundancy
- **Keep authority labels intact** — update Observed facts, Stage proposals, Current state audited, Failed approaches, and THIS STAGE'S TASK; never relabel a proposal as an operator decision
- **Keep the PROPAGATION PROTOCOL intact** inside the next stage, pointing to the stage after it
- **Adjust "Current stage"** and update Stage N+1's DoD based on what was just done
- **Propagate permission exactly** — an authorization does not widen because a later stage would benefit from it. If the original ask did not authorize the exact external effect, prepare the artifact and pause for approval
- **Minimize before propagating** — never copy credentials, API keys, or tokens. Replace them with a placeholder (`[API_KEY — in your env]`). Personal or confidential data travels only when the named destination needs it and is authorized to receive it; otherwise redact or reference an accessible local file
- **Record what failed** — append to the `⛔ FAILED` list every approach this stage tried that didn't work, with the error. A fresh chat with no memory will happily retry a dead end unless the prompt forbids it
- **Reference files instead of pasting them** when the target environment reads the workspace (Claude Code): pass paths, not contents. Inline content only for chat-only environments (claude.ai, Cowork) where the next session can't open files
- **Watch the context budget** — if the inherited context grows past roughly a third of the prompt, prune: keep decisions, current state, and failed approaches; cut narration and anything the next chat can re-derive from files

### STAGE REPORT TO COORDINATOR

Every stage returns before the chain advances. Emit this block before the next prompt:

```markdown
### STAGE REPORT TO COORDINATOR

- Status: [complete / paused]
- Deliverables: [paths or outputs]
- Evidence: [checks run and observed result]
- Observed facts added: [...]
- Stage proposals awaiting ratification: [...]
- Operator decisions recorded in this stage: [none / quote the decision and its exact scope]
- Operator decision or approval needed: [none / one narrow question]
```

The coordinator reviews this report and may accept the next prompt, revise it, or stop. A report with `Status: paused` must be followed by `CHAIN PAUSED`, never a next-stage prompt. Generating Stage N+1's prompt never authorizes the current chat to execute Stage N+1.

### AUTHORIZATION PROTOCOL

External effects include publishing, sending a message, opening a PR, pushing, deploying, merging, spending money, deleting data, and changing access or permissions. Execute one only when the original ask or a later explicit operator decision authorizes that exact effect for this scope. When authorization is absent or ambiguous, prepare everything reversible, name the pending action in the stage report, and emit `CHAIN PAUSED` with one narrow approval question.

### CHAIN PAUSED (blocker)

When a stage cannot be completed without human input, replace the next-prompt block with:

```markdown
### CHAIN PAUSED

**What was done:**
- [...]

**Blocker:**
[description of what prevents progress]

**Question for the user:**
[a single, direct question, with options when possible]

**How to resume:**
Answer the question above. Then paste this same STAGE N prompt into a new chat, adding a "## USER DECISION" section at the top with the answer. The chain continues from here.
```

**Master rule:** pausing always beats guessing. A guess at stage N contaminates every following stage, and the user only finds the error at the end.

**Refine at the pause:** if the environment can ask the user interactively, use that capability at the moment of the pause. Put the blocker to the user as a direct question with 2–4 concrete options, each with its trade-off, and apply the answer before emitting the resume prompt. Emit the `CHAIN PAUSED` block as well so the state remains portable. In environments without an interactive question capability, use the block's written question.

### CHAIN COMPLETE (last stage)

The last stage replaces the next-prompt block with:

```markdown
### CHAIN COMPLETE

**Chain goal:**
[original statement from CHAIN META]

**Final deliverables:**
- [file 1 — path]
- [file 2 — path]
...

**Decisions recorded during the chain:**
- Operator decisions ratified: [...]
- Stage proposals still awaiting ratification: [...]
...

**Next steps outside the chain:**
[if any — deploy, human review, publication]
```

This block works as the chain's minutes — the user files it with the deliverables and keeps a trail of what was decided.

## Decomposition heuristics

**Separate by type of risk:**
- Irreversible decisions first (creating structure, choosing format, packaging)
- Reversible edits next (adjustments, refinements, polish)
- Validation last (QA, counts, contrast, cross-browser)

**One stage = one execution context:**
If two steps use the same set of files and the same mindset, put them in the same stage. If they need different mental modes (build vs. audit, write vs. test), separate them.

**DoD before writing:**
Before writing stage N, state it out loud: *"Stage N is done when [X] exists and [Y] is true."* If you can't state it, the stage is poorly defined — redesign it before continuing.

**The amnesia rule:**
For each stage, ask: *"If a completely different agent opened this prompt with no context at all, would it have everything it needs?"* If not, the INHERITED CONTEXT is too loose.

## Strong stable context — checklist

The user pays the chain's price when stable context is incomplete. Include whenever applicable:

- [ ] Absolute workspace path (not relative)
- [ ] Target environment and client — they determine which tools and workspace files are available
- [ ] Original ask, done point, budget/checkpoint, undo, and coordinator
- [ ] Exact authority: authorized actions, fresh-approval actions, and out-of-scope surfaces
- [ ] Design system / tokens inline in the prompt for chat-only environments; file paths are enough when the target environment reads the workspace
- [ ] Brand voice and tone (if relevant)
- [ ] Compliance / hard rules (if any)
- [ ] Conventions (naming, date format, language)
- [ ] The chain's final goal (not just this stage's)
- [ ] Decisions, facts, and proposals are labeled separately
- [ ] No secrets; personal or confidential data is minimized for the named destination

## Minimal example — 2-stage chain

Scenario: refactor `styles.css` + validate responsive behavior.

**Stage 1 — what the user pastes:**

````markdown
# STAGE 1/2 — REFACTOR CSS
# Chain: "CSS Cleanup + Responsive"

## CHAIN META
- Total stages: 2
- Current stage: 1/2
- Stage 1: extract tokens + consolidate duplicates
- Stage 2: test viewports + final adjustments

## WORK FRAME — COPY VERBATIM

### Original ask
> Refactor styles.css and validate responsive behavior in separate cold-start stages. Do not change visual output.

### Done
styles.css is under 600 lines and renders identically at 320px, 768px, and 1440px.

### Work class and risk
Personal/pre-production; medium risk because visual regressions can survive a clean build.

### Budget / checkpoint
Two stages. Return to the coordinator after each one.

### Undo
Revert the stage commit or restore styles.css from version control.

### Coordinator
The chat that created this chain.

## WORKSPACE
Absolute path: `/Users/name/project/`
Target environment: Claude Code

## AUTHORITY — COPY VERBATIM
- Authorized in this chain: edit styles.css and run local checks
- Requires fresh approval: commit, push, deploy, or modify HTML
- Out of scope: markup, JavaScript, dependencies, and public environments

## INHERITED CONTEXT

### Chain goal
Reduce styles.css from 1200 → < 600 lines keeping visual output identical at 320px, 768px, and 1440px.

### Operator decisions — frozen
- Use CSS custom properties (not Sass)
- Keep the BEM convention
- No preprocessors

### Observed facts
- styles.css has 1247 lines and repeated values

### Stage proposals — not binding until ratified
- None yet

### Current state audited (2026-04-23)
- ✅ EXISTS: styles.css (1247 lines, many duplicates)
- ❌ MISSING: tokens file

## THIS STAGE'S TASK
1. Map duplicate selectors in styles.css
2. Extract repeated values into custom properties in :root
3. Consolidate equivalent rules
4. Save the result — must be < 700 lines

## CONSTRAINTS
- Do not change visual output (same hierarchy, same final colors)
- Do not remove selectors used in the HTML

## DELIVERABLES
1. Refactored styles.css
2. A `### STAGE REPORT TO COORDINATOR` block
3. A `### NEXT PROMPT — STAGE 2` block

## PROPAGATION PROTOCOL
[...full instruction as in the template...]
````

**Stage 2 — emitted by the agent that ran Stage 1**, already carrying:
- Updated current state (styles.css now has X lines, Y tokens extracted)
- TASK swapped for responsive validation
- PROPAGATION PROTOCOL replaced by FINAL TERMINATION (the next emission will be `### CHAIN COMPLETE`)

## FAN-OUT mode

Same isolation and cold-start safety as a chain, minus the propagation. Use it when the pieces share stable context but don't depend on each other's output — see the routing rule up top.

### How to build a fan-out

1. **Frame the set once** — carry the same WORK FRAME, WORKSPACE, AUTHORITY, operator decisions, and stable context into every piece.
2. **List the independent pieces** — one line each, with its own Definition of Done. If two pieces turn out to share dynamic state, they aren't independent — collapse them into a 2-stage chain and treat that chain as a single piece of the fan-out.
3. **Write one self-contained prompt per piece** — each carries the full stable context plus that piece's task and returns a structured result to the coordinator. No CHAIN META, no PROPAGATION PROTOCOL, no next-prompt emission.
4. **Add a collector when the set has a combined result** — synthesis, conflict resolution, or a set-wide done verdict depends on all required result envelopes. The collector is a dependent step after the fan-out, not another independent piece.
5. **Optionally write a dispatcher** — a single root prompt that holds the stable context once and emits all N piece-prompts, plus the collector when needed. The dispatcher generates prompts; it does not execute them.

### Canonical FAN-OUT prompt template

Copy-paste verbatim, adjusting the content. Every piece in the fan-out uses this structure.

````markdown
# [TASK NAME] — piece K of N (independent)
# Set: "[FAN-OUT NAME]"

## WORK FRAME — COPY VERBATIM
[Original ask, Done, Work class and risk, Budget / checkpoint, Undo, Coordinator]

## WORKSPACE
Absolute path: `[absolute path]`
Target environment: [workspace-capable agent / chat-only agent / other named client]
[Destination / audience]
[Conventions: output folder, naming, language]

## AUTHORITY — COPY VERBATIM
- Authorized for this piece: [exact actions]
- Requires fresh approval: [external effects not already authorized]
- Out of scope: [untouchable actions and surfaces]

## SHARED CONTEXT — REQUIRED READING

### Operator decisions — frozen
- [explicit operator decisions only]

### Observed facts
- [evidence-backed facts shared by every piece]

### Shared proposals — not binding until ratified
- [inherited model recommendation relevant to every piece]

### Shared stable context
[The stable specification, design system, voice, and hard constraints. Identical across all N prompts.]

## THIS PIECE'S TASK
1. [concrete action with a "done" criterion]
2. ...

## CONSTRAINTS
- [what NOT to do — untouchable files, frozen decisions]

## DELIVERABLES
1. [file / output]
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
This prompt is self-contained and shares no dynamic state with the other pieces of "[FAN-OUT NAME]". Run it in its own chat, in any order. There is no next prompt to emit — when the task and deliverables are done, stop. If blocked, ask the user directly (see below) rather than guessing.
````

A fan-out piece has no CHAIN META, dynamic state shared with other pieces, PROPAGATION PROTOCOL, or per-piece `CHAIN COMPLETE`. It opens, does its closed task, returns its result envelope, and ends.

### Dispatcher (optional root prompt)

When you want one chat to generate the whole set, use a dispatcher: state the frame and stable context once, list the N pieces, and instruct the agent to emit N self-contained prompts — each following the template above, one fenced block per piece, with no propagation between them. If the set needs a combined result, the dispatcher also emits one collector prompt. It is a generator, not an executor. Use a **4-backtick** fence (or `~~~~`) on each emitted block so inner triple backticks don't close it early.

### Collector (when the set has a combined result)

Run the collector only after every required piece has returned `RESULT FOR COORDINATOR` or the coordinator has explicitly accepted a missing piece. Give it the original frame, shared context with every status label intact, and the result envelopes — not the full production chats.

```markdown
# COLLECTOR — [FAN-OUT NAME]

## WORK FRAME / WORKSPACE / AUTHORITY / SHARED CONTEXT
[copy the same blocks verbatim, including non-binding shared proposals]

## REQUIRED INPUTS
- Required piece 1 result: [paste RESULT FOR COORDINATOR]
- Required piece 2 result: [paste RESULT FOR COORDINATOR]
- ...
- Required piece N result: [paste RESULT FOR COORDINATOR]

## TASK
1. Verify that every required piece is present or explicitly waived by the coordinator.
2. Reconcile conflicts, duplicates, and gaps without inventing missing evidence.
3. Produce the combined deliverable and a set-wide completion report.

## COMPLETION
Emit `### SET COMPLETE` only when the combined Done statement is true. Otherwise emit `### SET PAUSED` with one narrow question for the coordinator.
```

### CHAIN vs FAN-OUT at a glance

| | CHAIN | FAN-OUT |
|---|---|---|
| Ordering | Sequential, load-bearing | None — any order, even at once |
| Between prompts | Each emits the next (propagation) | Nothing — fully independent |
| Dynamic state | Carried forward stage to stage | None — stable context only |
| Completion | Last stage emits `CHAIN COMPLETE` | Each piece returns a result; collector emits `SET COMPLETE` when a combined result is required |
| Blocker | `CHAIN PAUSED` (poisons downstream if guessed) | Each prompt pauses alone; the others are unaffected |
| Build artifact | One seed prompt (Stage 1) | N prompts, optionally a dispatcher and collector |

### Blockers in fan-out

Each prompt handles its own blocker in isolation. There is no downstream chain to contaminate, so a blocked piece returns its result envelope with one narrow question while the others proceed untouched. Use the environment's user-question capability when available; otherwise write the question and stop. **Pausing still beats guessing.** Credentials and tokens never travel. Personal or confidential data is minimized for the named destination.

### Signs a fan-out was applied well

- Every piece-prompt pastes cold into its own chat with no manual editing
- All pieces share *identical* stable context — fill it once, fill it well
- No piece waits on another, and none references "the previous chat"
- Every piece returns a result envelope to the named coordinator
- A combined result is declared complete only by a collector that saw every required result or an explicit waiver
- If you find yourself threading one piece's output into another, it wasn't independent — it should have been a CHAIN

## Signs the skill was applied well

The chain is well built when:

- Every emitted prompt pastes cold into a new chat with no manual editing
- The last stage emits `### CHAIN COMPLETE` with every deliverable listed
- The user never had to explain anything again between stages
- If a stage failed, it emitted `### CHAIN PAUSED` with a direct question — it didn't guess
- No stage broadened authority or promoted an unratified proposal into an operator decision

The skill's value: the user goes from *"I have to explain everything again every time I open a chat"* to *"pasted it, chain ran."*
