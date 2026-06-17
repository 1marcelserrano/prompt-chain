---
name: prompt-chain
version: 2.2.0
description: Use this skill whenever the user wants to break a complex multi-step task into self-contained prompts run in fresh chat sessions with full context carried forward — in two modes. CHAIN (sequential, each prompt self-propagates the next until CHAIN COMPLETE) and FAN-OUT (independent prompts, one per piece, no ordering, run in any order across isolated chats). Trigger phrases in PT-BR and EN — "executar por etapas em chats separados", "cada etapa em um novo chat", "prompt autocontido autopropagante", "prompt que gera o próximo", "quero passar esse trabalho para vários chats", "um prompt por tarefa", "um prompt por pendência", "vários prompts independentes", "prompts em paralelo para chats separados", "cold start entre chats", "monte um prompt que eu colo em outro chat", "chain of prompts", "self-propagating prompt", "fan out into independent prompts", "one prompt per task", "split this across sessions". Also trigger when the user has a long multi-phase task (P0 → P1 → P2), when they mention context limits or fresh sessions, or when they want to isolate execution between phases — whether the pieces are sequential (CHAIN) or independent (FAN-OUT). Don't wait for exact wording — if the user is distributing work across multiple isolated chat sessions with context preservation, invoke this skill.
changelog: "V2.2.0 — FAN-OUT mode (independent cold-start prompts, no propagation) + CHAIN vs FAN-OUT routing rule. V2.1.0 — secret sanitization, failed-approaches ledger (⛔ FAILED), reference-over-paste rule, context-budget pruning. V2.0.0 — English as canonical skill body; PT-BR preserved as SKILL.pt-BR.md"
---

# Prompt Chain

Turns a multi-step task into self-contained prompts, each run in a fresh chat with full context carried forward. Two modes:

- **CHAIN** — sequential. Each prompt runs one stage and ends by emitting the next stage's prompt with the accumulated context already inside it. The user copies and pastes between chats; the chain propagates itself until `CHAIN COMPLETE`. Use when the pieces have an ordering dependency.
- **FAN-OUT** — independent. One self-contained prompt per piece, all sharing the same stable context but with no propagation between them. The user opens each in its own chat, in any order (or at the same time). Use when the pieces don't depend on each other.

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
- Task whose intermediate state fits in one session with no risk of overflow → TodoWrite + direct execution is better
- Exploratory work without discrete deliverables → both modes assume pieces with a clear Definition of Done
- Same-session parallelism with no need for isolated chats → use parallel subagents instead (they run concurrently in one session). Wanting *isolated* chats for pieces that have no ordering dependency is not a reason to avoid the skill — that's FAN-OUT mode

## Mental model

A chain is a sequence of stages. Each stage:
1. Receives a self-contained prompt (pasteable cold into a new chat)
2. Executes one slice of the work
3. Emits the next stage's prompt with updated context

The key insight: **stable context vs dynamic context**.

- **Stable** — workspace path, design system, brand voice, global constraints, final goal. Copied verbatim into every stage.
- **Dynamic** — current file state, decisions made, blockers found. Updated stage by stage.

If the chain loses stable context, the next chat re-makes decisions. If it loses dynamic context, it redoes work. Either failure destroys the value.

In **FAN-OUT** mode there is no dynamic carry-forward — every prompt is stable context plus one closed task. That makes the stable context the *only* thing keeping the pieces coherent, so completing it well matters even more (see "FAN-OUT mode" below).

## How to build a chain

### Step 1 — Scope the task and extract stable context

Before decomposing, separate out:

- **Final goal** — what does "chain complete" mean? A single, verifiable statement.
- **Workspace** — absolute path + conventions (output folder, naming, language).
- **Constraints that don't change** — design system, compliance, brand voice, output format.
- **Decisions already made** — what the user has settled and won't reopen.
- **Target environment** — Claude Code / Cowork / Claude.ai Chat. Each has different tools.

This set goes into the INHERITED CONTEXT section of every stage, unchanged.

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

## WORKSPACE
Absolute path: `[absolute path]`
Target environment: [Claude Code / Cowork / Chat]
[Relevant conventions: output folder, naming, language]

## INHERITED CONTEXT — REQUIRED READING

### Chain goal
[Single statement of what "chain complete" means]

### Decisions already made
- [decision 1 — do not reopen]
- [decision 2 — do not reopen]

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
N. **REQUIRED**: a `### NEXT PROMPT — STAGE N+1` block at the end (or `### CHAIN COMPLETE` if N = TOTAL)

## PROPAGATION PROTOCOL — CRITICAL
At the end of your response, emit a markdown code block containing the complete, self-contained prompt for Stage N+1. The next chat will have ZERO memory of this one. The Stage N+1 prompt must:

- Open with `# STAGE N+1/TOTAL — [NAME]`
- Copy CHAIN META, WORKSPACE, and all stable INHERITED CONTEXT (design system / voice / compliance) from this prompt verbatim
- Update "Decisions already made" and "Current state audited" with what you just did
- Replace the TASK with Stage N+1's action list (see CHAIN META above)
- Include this same PROPAGATION PROTOCOL for Stage N+2 (or replace it with FINAL TERMINATION if Stage N+1 is the last)

If this stage cannot be completed (blocker, ambiguity, missing input), emit a `### CHAIN PAUSED` block instead of the next prompt (see protocols).
````

## Transition protocols

### PROPAGATION PROTOCOL (stage → next stage)

Every non-final stage response ends with the header:

```
### NEXT PROMPT — STAGE N+1
```

Followed by a closed markdown code block. **Watch the fence escaping**: since the next prompt's content contains triple backticks, use a **4-backtick** fence on the outer block (or `~~~~` as an alternative). This keeps the parser from closing the block early.

Principles:
- **Never abbreviate with "same as before"** — the next chat doesn't have the previous one
- **Copying stable context verbatim is the correct behavior**, not redundancy
- **Update only the dynamic fields**: Decisions already made, Current state audited, Failed approaches, THIS STAGE'S TASK
- **Keep the PROPAGATION PROTOCOL intact** inside the next stage, pointing to the stage after it
- **Adjust "Current stage"** and update Stage N+1's DoD based on what was just done
- **Sanitize before propagating** — never copy credentials, API keys, tokens, or personal data into the next prompt. Replace with a placeholder (`[API_KEY — in your env]`); the next chat asks the user only if it truly needs the value
- **Record what failed** — append to the `⛔ FAILED` list every approach this stage tried that didn't work, with the error. A fresh chat with no memory will happily retry a dead end unless the prompt forbids it
- **Reference files instead of pasting them** when the target environment reads the workspace (Claude Code): pass paths, not contents. Inline content only for chat-only environments (claude.ai, Cowork) where the next session can't open files
- **Watch the context budget** — if the inherited context grows past roughly a third of the prompt, prune: keep decisions, current state, and failed approaches; cut narration and anything the next chat can re-derive from files

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

**Refine, don't just halt:** if the environment has the AskUserQuestion tool, use it at the moment of the pause — put the blocker to the user as a direct question with 2–4 concrete options (each with its trade-off), and apply the answer to refine the approach before emitting the resume prompt. The CHAIN PAUSED block still gets emitted; AskUserQuestion runs alongside it so the decision lands now instead of in the next chat. In environments without the tool, the block's written question is the fallback.

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
- Stage 1: [...]
- Stage 2: [...]
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
- [ ] Target environment (Claude Code / Cowork / Chat) — it changes the available tools
- [ ] Design system / tokens inline in the prompt for chat-only environments; file paths are enough when the target environment reads the workspace
- [ ] Brand voice and tone (if relevant)
- [ ] Compliance / hard rules (if any)
- [ ] Conventions (naming, date format, language)
- [ ] The chain's final goal (not just this stage's)
- [ ] No secrets — credentials and tokens never travel in the chain

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

## WORKSPACE
Absolute path: `/Users/name/project/`
Target environment: Claude Code

## INHERITED CONTEXT

### Chain goal
Reduce styles.css from 1200 → < 600 lines keeping visual output identical at 320px, 768px, and 1440px.

### Decisions already made
- Use CSS custom properties (not Sass)
- Keep the BEM convention
- No preprocessors

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
2. A `### NEXT PROMPT — STAGE 2` block

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

1. **Extract stable context once** — same as Step 1 for a chain: workspace path, conventions, design system, brand voice, hard constraints, and the shared decision or spec being propagated. This block is copied verbatim into *every* prompt.
2. **List the independent pieces** — one line each, with its own Definition of Done. If two pieces turn out to share dynamic state, they aren't independent — collapse them into a 2-stage chain and treat that chain as a single piece of the fan-out.
3. **Write one self-contained prompt per piece** — each carries the full stable context plus that piece's task. No CHAIN META, no PROPAGATION PROTOCOL, no next-prompt emission.
4. **(Optional) Write a dispatcher** — a single root prompt that holds the stable context once and emits all N piece-prompts in one response. Useful when you want one chat to generate the set and then distribute the pieces.

### Canonical FAN-OUT prompt template

Copy-paste verbatim, adjusting the content. Every piece in the fan-out uses this structure.

````markdown
# [TASK NAME] — piece K of N (independent)
# Set: "[FAN-OUT NAME]"

## WORKSPACE
Absolute path: `[absolute path]`
Target environment: [Claude Code / Cowork / Chat]
[Conventions: output folder, naming, language]

## SHARED CONTEXT — REQUIRED READING
[The stable block, copied verbatim into every piece: the shared decision / spec, design system, voice, hard constraints. Identical across all N prompts.]

## THIS PIECE'S TASK
1. [concrete action with a "done" criterion]
2. ...

## CONSTRAINTS
- [what NOT to do — untouchable files, frozen decisions]

## DELIVERABLES
1. [file / output]
2. A short report of what changed + anything left for human decision

## INDEPENDENCE NOTE
This prompt is self-contained and shares no dynamic state with the other pieces of "[FAN-OUT NAME]". Run it in its own chat, in any order. There is no next prompt to emit — when the task and deliverables are done, stop. If blocked, ask the user directly (see below) rather than guessing.
````

Note what is *absent* versus a CHAIN stage: no CHAIN META, no "Current state audited" carrying forward, no PROPAGATION PROTOCOL, no `CHAIN COMPLETE`. A fan-out prompt opens, does its closed task, reports, and ends.

### Dispatcher (optional root prompt)

When you want one chat to generate the whole set, use a dispatcher: state the stable context once, list the N pieces, and instruct the agent to emit N self-contained prompts — each following the template above, one fenced block per piece, with no propagation between them. The dispatcher is a generator, not an executor: it produces the prompts; you distribute them. Use a **4-backtick** fence (or `~~~~`) on each emitted block so inner triple backticks don't close it early.

### CHAIN vs FAN-OUT at a glance

| | CHAIN | FAN-OUT |
|---|---|---|
| Ordering | Sequential, load-bearing | None — any order, even at once |
| Between prompts | Each emits the next (propagation) | Nothing — fully independent |
| Dynamic state | Carried forward stage to stage | None — stable context only |
| Completion | Last stage emits `CHAIN COMPLETE` | Each prompt just reports; no global terminator |
| Blocker | `CHAIN PAUSED` (poisons downstream if guessed) | Each prompt pauses alone; the others are unaffected |
| Build artifact | One seed prompt (Stage 1) | N prompts, or one dispatcher that emits them |

### Blockers in fan-out

Each prompt handles its own blocker in isolation. There is no downstream chain to contaminate, so a blocked piece just pauses and asks while the others proceed untouched. Same rule as a chain: if the AskUserQuestion tool is available, put the blocker as a direct question with 2–4 concrete options; otherwise state it in the deliverables and stop. **Pausing still beats guessing**, and secret sanitization still applies — no credentials, tokens, or personal data in any prompt; use placeholders.

### Signs a fan-out was applied well

- Every piece-prompt pastes cold into its own chat with no manual editing
- All pieces share *identical* stable context — fill it once, fill it well
- No piece waits on another, and none references "the previous chat"
- If you find yourself threading one piece's output into another, it wasn't independent — it should have been a CHAIN

## Signs the skill was applied well

The chain is well built when:

- Every emitted prompt pastes cold into a new chat with no manual editing
- The last stage emits `### CHAIN COMPLETE` with every deliverable listed
- The user never had to explain anything again between stages
- If a stage failed, it emitted `### CHAIN PAUSED` with a direct question — it didn't guess

The skill's value: the user goes from *"I have to explain everything again every time I open a chat"* to *"pasted it, chain ran."*
