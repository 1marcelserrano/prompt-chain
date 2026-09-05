# Illustrative example — FAN-OUT with a collector

Scenario: a typographic decision, **DEC-024**, is approved and already applied in the design-system repo. Three other repositories must adopt it. Their edits are independent, but the operator wants one set-wide verification report after all three return.

Routing: the repository edits are FAN-OUT pieces because none needs another's output. The final verification is a collector because it depends on all three result envelopes. This is a hybrid topology, not a four-stage sequential chain.

## What the user pastes — the dispatcher

`````markdown
# DISPATCHER — emit 3 independent FAN-OUT prompts + 1 collector
# Set: "DEC-024 propagation"

## YOUR JOB
Emit exactly 3 self-contained piece prompts, followed by one COLLECTOR prompt. Do not execute them.

## WORK FRAME — copied verbatim into EVERY prompt

### Original ask
> Prepare isolated prompts to apply DEC-024 in the skills, docs, and marketing repositories, then verify the set. Make local edits only; do not commit, push, open PRs, or deploy.

### Done
All three live surfaces use the DEC-024 font mapping, frozen historical assets remain untouched, and one collector report accounts for every repository.

### Work class and risk
Personal/pre-production refactor; medium risk because an incorrect edit can change rendered typography.

### Budget / checkpoint
Three independent pieces plus one collector. Every piece returns to this coordinator.

### Undo
Restore changed files from version control in the affected repository.

### Coordinator
The original chat that created this dispatcher.

## WORKSPACE
Absolute path: varies per piece
Target environment: Claude Code
Destination / audience: private result for the operator
Conventions: PT-BR

## AUTHORITY — copied verbatim into EVERY prompt
- Authorized in this set: inspect files, make local edits, and run local verification
- Requires fresh approval: commit, push, open PR, deploy, publish, or change permissions
- Out of scope: color, casing, frozen studies, and embedded historical mockups

## SHARED CONTEXT — copied verbatim into EVERY prompt

### Operator decisions — frozen
- DEC-024: headline and emphasis use Fraunces; body uses Inter Tight; labels use IBM Plex Mono
- Color and letter-casing stay unchanged
- Frozen studies and period mockups remain historical records

### Observed facts
- The design-system source already contains DEC-024

### Shared proposals — not binding until ratified
- None

### Shared stable context
Use the design-system source by reference. Do not copy credentials or repository-private content into another chat.

## PIECES
1. Skills repo — update live editorial skill references. Done when retired fonts remain only in frozen examples or historical notes.
2. Docs repo — update live format documentation while preserving embedded period mockups.
3. Marketing repo — update live typography tokens and verify the local computed font family.

## COMBINED RESULT
Yes — a collector reconciles the three result envelopes and proves the set-wide Done statement.

## PIECE TEMPLATE
````markdown
# [piece name] — piece K of 3 (independent)
# Set: "DEC-024 propagation"

## WORK FRAME / WORKSPACE / AUTHORITY
[copy the relevant blocks above verbatim; fill this piece's absolute path]

## SHARED CONTEXT — REQUIRED READING
[copy the SHARED CONTEXT above verbatim]

## THIS PIECE'S TASK
1. [piece actions and local checks, each with a done criterion]

## CONSTRAINTS
- Do not commit, push, open a PR, or deploy
- Do not touch color, casing, or historical assets

## RESULT FOR COORDINATOR — REQUIRED
- Piece: K of 3 — [name]
- Status: [complete / blocked]
- Deliverables: [paths]
- Evidence: [searches, tests, or computed-style result]
- Observed facts added: [...]
- Stage proposals awaiting ratification: [...]
- Operator decisions recorded in this piece: [none / quote the decision and its exact scope]
- Operator decision or approval needed: [none / one narrow question]

## INDEPENDENCE NOTE
Run in its own chat, in any order. Return the result envelope and stop. Do not emit or execute another piece.
````

## COLLECTOR TEMPLATE
````markdown
# COLLECTOR — DEC-024 propagation

## WORK FRAME / WORKSPACE / AUTHORITY / SHARED CONTEXT
[copy the same blocks verbatim, including non-binding shared proposals]

## REQUIRED INPUTS
- Skills repo result: [paste RESULT FOR COORDINATOR]
- Docs repo result: [paste RESULT FOR COORDINATOR]
- Marketing repo result: [paste RESULT FOR COORDINATOR]

## TASK
1. Confirm all three results are present or explicitly waived by the coordinator.
2. Reconcile contradictory evidence and identify any unverified surface.
3. Produce one set-wide report. Do not commit, push, open PRs, or deploy.

## COMPLETION
Emit `### SET COMPLETE` only when every required repository satisfies the Done statement. Otherwise emit `### SET PAUSED` with one narrow question.
````
`````

## Illustrative piece result

```markdown
## RESULT FOR COORDINATOR — REQUIRED
- Piece: 1 of 3 — Skills repo
- Status: complete
- Deliverables: three updated live skill files
- Evidence: retired-font search now returns only frozen examples and historical notes
- Observed facts added: one archived example intentionally preserves the old stack
- Stage proposals awaiting ratification: none
- Operator decisions recorded in this piece: none
- Operator decision or approval needed: none
```

The other two pieces return the same envelope shape. If one is blocked, the independent pieces still finish, but the collector emits `SET PAUSED` rather than inventing or ignoring the missing evidence. After every required result arrives, the collector may emit `SET COMPLETE`. External publication remains outside the set's authority.
