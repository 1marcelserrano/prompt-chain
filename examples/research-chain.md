# Example — 2-stage research chain

Scenario: map the competitors of a small open-source tool and produce a positioning report. Too long for one chat: the census alone eats most of a context window. Split: gather → synthesize.

## Stage 1 — what the user pastes into a fresh chat

````markdown
# STAGE 1/2 — COMPETITOR CENSUS
# Chain: "OSS Positioning Research"

## CHAIN META
- Total stages: 2
- Current stage: 1/2
- Stage 1: find competitors + one fact sheet each
- Stage 2: synthesize into positioning report with safe/unsafe claims

## WORKSPACE
Absolute path: none (chat-only)
Target environment: claude.ai chat with web search

## INHERITED CONTEXT — REQUIRED READING

### Chain goal
A positioning report for the tool "acme-sync" (open-source file sync CLI): who the competitors are, what each does better, and 3 marketing claims that survive public fact-checking.

### Decisions already made
- Only open-source competitors count (no SaaS-only products)
- Adoption numbers must be verified, never estimated

### Current state audited (2026-06-12)
- ✅ EXISTS: nothing yet — this is the first stage
- ⛔ FAILED: nothing yet

## THIS STAGE'S TASK
1. Search GitHub and the web for open-source file sync tools — at least 8 candidates
2. For each relevant one (aim 5–8): name, link, stars (verified), mechanism in 2 lines, what it does better than acme-sync
3. Output the fact sheets as a markdown table

## CONSTRAINTS
- No invented numbers — write "not verifiable" when a metric can't be confirmed

## DELIVERABLES
1. Fact-sheet table, 5–8 competitors
2. A `### NEXT PROMPT — STAGE 2` block

## PROPAGATION PROTOCOL — CRITICAL
At the end of your response, emit a markdown code block containing the complete, self-contained prompt for Stage 2. The next chat will have ZERO memory of this one. The Stage 2 prompt must: open with `# STAGE 2/2 — [NAME]`; copy CHAIN META, WORKSPACE, and all stable INHERITED CONTEXT verbatim; update "Decisions already made", "Current state audited", and `⛔ FAILED` with what you just did; replace the TASK with Stage 2's actions; replace this protocol with FINAL TERMINATION (Stage 2 ends with `### CHAIN COMPLETE`). Include the full fact-sheet table inside the Stage 2 prompt — the next chat cannot see this one. If blocked, emit `### CHAIN PAUSED` instead.
````

## What chat 1 emitted at the end of its response

Note the updated dynamic fields — including a dead end recorded in `⛔ FAILED` so chat 2 doesn't retry it:

````markdown
### NEXT PROMPT — STAGE 2

# STAGE 2/2 — POSITIONING SYNTHESIS
# Chain: "OSS Positioning Research"

## CHAIN META
- Total stages: 2
- Current stage: 2/2
- Stage 1: find competitors + one fact sheet each ✅ done
- Stage 2: synthesize into positioning report with safe/unsafe claims

## WORKSPACE
Absolute path: none (chat-only)
Target environment: claude.ai chat with web search

## INHERITED CONTEXT — REQUIRED READING

### Chain goal
A positioning report for the tool "acme-sync" (open-source file sync CLI): who the competitors are, what each does better, and 3 marketing claims that survive public fact-checking.

### Decisions already made
- Only open-source competitors count (no SaaS-only products)
- Adoption numbers must be verified, never estimated
- NEW (Stage 1): rclone and syncthing are the two reference competitors; 4 smaller ones included for completeness

### Current state audited (2026-06-12)
- ✅ EXISTS: fact-sheet table with 6 competitors (below)
- ⛔ FAILED: searching GitHub topic "file-sync" returned mostly archived repos — topic "sync" + language filter worked instead. Do not re-search the dead topic.

### Fact sheets (Stage 1 output — full table)
| Tool | Stars | Mechanism | Better than acme-sync at |
|---|---|---|---|
| rclone | 52k (verified 2026-06-12) | CLI, 70+ cloud backends | breadth of backends |
| syncthing | 68k (verified 2026-06-12) | P2P continuous sync | no-server real-time sync |
| [...4 more rows exactly as produced...] | | | |

## THIS STAGE'S TASK
1. Group the 6 competitors into families by mechanism
2. Write the positioning report: where acme-sync wins, where it loses
3. Draft 3 claims that survive fact-checking + 2 claims to avoid, each with the competitor that would refute it

## CONSTRAINTS
- Every claim must cite a row from the fact-sheet table

## DELIVERABLES
1. Positioning report (markdown)
2. `### CHAIN COMPLETE` block

## FINAL TERMINATION
This is the last stage. End with `### CHAIN COMPLETE` listing the chain goal, final deliverables, and decisions recorded during both stages. If blocked, emit `### CHAIN PAUSED` instead.
````

## What chat 2 emitted at the end

```markdown
### CHAIN COMPLETE

**Chain goal:**
Positioning report for acme-sync: competitors, strengths, 3 fact-check-proof claims.

**Final deliverables:**
- Fact-sheet table, 6 competitors (Stage 1)
- Positioning report with 3 safe claims + 2 claims to avoid (Stage 2)

**Decisions recorded during the chain:**
- Stage 1: rclone + syncthing set as reference competitors; GitHub topic "file-sync" discarded (archived repos)
- Stage 2: positioning angle = "single-binary simplicity", the one axis where both references are weaker

**Next steps outside the chain:**
Review the 3 claims before publishing the README.
```

The user pasted two prompts total. No re-explaining between chats, and chat 2 never repeated the dead-end search from chat 1.
