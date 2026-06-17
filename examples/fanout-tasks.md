# Example — FAN-OUT, 3 independent prompts

Scenario: a typographic decision — call it **DEC-024**: unify headline and emphasis on one variable font and retire the old editorial font stack — is approved and already applied in the design-system repo. It now has to land in three places that **don't depend on each other**:

1. the editorial skills in a sibling repo that still reference the old fonts,
2. a docs/format page in the design-system repo whose prose still describes the old stack,
3. a deploy/render verification + opening the PR for the change.

Routing question — *do the pieces depend on each other's output or state?* **No.** None needs another's result; they only share the same DEC-024 decision. So this is FAN-OUT, not a chain. One self-contained prompt per piece, run in any order, in its own isolated chat. There is no propagation between them and no `CHAIN COMPLETE`.

## What the user pastes — the dispatcher

`````markdown
# DISPATCHER — emit 3 independent FAN-OUT prompts
# Set: "DEC-024 propagation"

## YOUR JOB
Emit exactly 3 self-contained prompts, one per piece below. Each follows the PIECE TEMPLATE. Emit each in its own 4-backtick fenced block, with NO propagation between them. Do not execute the pieces; just generate the prompts. After the 3 blocks, stop.

## WORKSPACE
Absolute path: varies per piece (stated in each)
Target environment: Claude Code
Conventions: PT-BR; never commit/push without being asked

## SHARED CONTEXT — copied verbatim into EVERY piece
DEC-024 (2026-06-17): one variable font now governs headline and emphasis in both registers via its optical axis. The old editorial stack (Sans + Caslon + Mono) is retired. Remap: headline → Fraunces (opsz 24–36, wght 340–400); emphasis → Fraunces italic; body → Inter Tight; label → IBM Plex Mono. Color and letter-casing are untouched. Frozen study assets and embedded period mockups are preserved as historical record — do not migrate them.

## PIECES (one prompt each)
1. Skills repo — migrate editorial skills that reference the old fonts. Done when grep shows old fonts only in legacy comments / frozen examples.
2. Docs/format page — migrate the live prose that still describes the old stack; preserve embedded mockups. Done when the page's live copy names the new stack.
3. Verify + PR — open the PR and confirm computed render (font-family per element) on the beta deploy. Done when PR URL exists and render is confirmed by computed style.

## PIECE TEMPLATE (apply to each piece above)
````markdown
# [piece name] — piece K of 3 (independent)
# Set: "DEC-024 propagation"

## WORKSPACE
Absolute path: `[piece's repo path]`
Target environment: Claude Code
Conventions: PT-BR; never commit/push without being asked

## SHARED CONTEXT — REQUIRED READING
[the SHARED CONTEXT block above, verbatim]

## THIS PIECE'S TASK
1. [the piece's concrete actions, each with a "done" criterion]

## CONSTRAINTS
- Do not touch color or casing; do not migrate frozen studies/mockups

## DELIVERABLES
1. [the piece's output]
2. A short report of what changed + anything left for human decision

## INDEPENDENCE NOTE
Self-contained. Shares no dynamic state with the other pieces of "DEC-024 propagation". Run in its own chat, any order. No next prompt to emit — when done, stop. If blocked, ask the user directly (AskUserQuestion if available) — never guess.
````
`````

## What the dispatcher emitted

Three independent blocks. Abbreviated here — note each carries the **identical** SHARED CONTEXT, none references another, and none emits a next prompt:

````markdown
# Skills repo — piece 1 of 3 (independent)
# Set: "DEC-024 propagation"

## WORKSPACE
Absolute path: `/path/to/skills-repo`
Target environment: Claude Code
Conventions: PT-BR; never commit/push without being asked

## SHARED CONTEXT — REQUIRED READING
DEC-024 (2026-06-17): one variable font now governs headline and emphasis [...identical block, verbatim...]

## THIS PIECE'S TASK
1. `grep -rln` the three retired font names; map every occurrence
2. Migrate the live editorial skills (SKILL.md, templates, specs) to the new stack
3. Preserve frozen example assets; re-audit until old fonts remain only in legacy comments / frozen examples

## CONSTRAINTS
- Do not touch color or casing; do not migrate frozen studies/mockups

## DELIVERABLES
1. Migrated skills + final categorized audit grep
2. Report of what changed + anything left for human decision

## INDEPENDENCE NOTE
Self-contained. Shares no dynamic state with pieces 2 and 3. Run in its own chat, any order. No next prompt. If blocked, ask directly — never guess.
````

(Pieces 2 and 3 follow the same shape — same SHARED CONTEXT verbatim, their own task/path, their own INDEPENDENCE NOTE. Omitted here for length.)

## How it ran

The user opened three chats — in no particular order, two at the same time. Each did its closed task and reported back; none waited on another, and there was no terminator block to collect. Piece 2 hit an ambiguity (was the page "live" or "frozen"?) and paused with an AskUserQuestion — pieces 1 and 3 were unaffected and finished while that decision was pending.

Contrast with a chain: there was nothing to carry forward, so forcing `STAGE 1 → STAGE 2 → STAGE 3` would have serialized three unrelated jobs for no reason and let an early blocker stall the rest. FAN-OUT keeps them independent.
