# Illustrative example — 2-stage research chain

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

## WORK FRAME — COPY VERBATIM

### Original ask
> Map the open-source competitors of acme-sync in one fresh chat, then synthesize a positioning report in another. Do not publish or contact anyone.

### Done
A sourced competitor table and a positioning report with three claims that survive public fact-checking.

### Work class and risk
One-shot research; low risk; a mistaken conclusion is reversed by correcting the report.

### Budget / checkpoint
Two stages. Return to the original chat after each stage.

### Undo
Replace unsupported claims and preserve the source table as evidence.

### Coordinator
The original chat that created this chain.

## WORKSPACE
Absolute path: none (chat-only)
Target environment: claude.ai chat with web search
Destination / audience: private draft for the operator

## AUTHORITY — COPY VERBATIM
- Authorized in this chain: public web research and draft creation
- Requires fresh approval: publication, outreach, or account actions
- Out of scope: SaaS-only competitors and private data

## INHERITED CONTEXT — REQUIRED READING

### Chain goal
A positioning report for the tool "acme-sync" (open-source file sync CLI): who the competitors are, what each does better, and 3 marketing claims that survive public fact-checking.

### Operator decisions — frozen
- Only open-source competitors count (no SaaS-only products)
- Adoption numbers must be verified, never estimated

### Observed facts
- None yet — Stage 1 collects them

### Stage proposals — not binding until ratified
- None yet

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
2. A `### STAGE REPORT TO COORDINATOR` block
3. A `### NEXT PROMPT — STAGE 2` block

## PROPAGATION PROTOCOL — CRITICAL
Return a `STAGE REPORT TO COORDINATOR`, then emit the complete prompt for Stage 2. Copy CHAIN META, WORK FRAME, WORKSPACE, AUTHORITY, and stable context verbatim. Carry verified findings as Observed facts and research judgments as Stage proposals; never promote either to Operator decisions. Include the fact-sheet table, replace the task, and use FINAL TERMINATION. Do not execute Stage 2 here or perform an external effect. If blocked, emit `### CHAIN PAUSED`.
````

## Illustrative emission from chat 1

Note the updated dynamic fields — including a dead end recorded in `⛔ FAILED` so chat 2 doesn't retry it:

````markdown
### STAGE REPORT TO COORDINATOR

- Status: complete
- Deliverables: fact-sheet table with 6 competitors
- Evidence: source links and metrics recorded in the table
- Observed facts added: 6 verified competitor records
- Stage proposals awaiting ratification: use rclone and syncthing as reference comparisons
- Operator decision or approval needed: none for synthesis; publication remains unauthorized

### NEXT PROMPT — STAGE 2

# STAGE 2/2 — POSITIONING SYNTHESIS
# Chain: "OSS Positioning Research"

## CHAIN META
- Total stages: 2
- Current stage: 2/2
- Stage 1: find competitors + one fact sheet each ✅ done
- Stage 2: synthesize into positioning report with safe/unsafe claims

## WORK FRAME — COPY VERBATIM

### Original ask
> Map the open-source competitors of acme-sync in one fresh chat, then synthesize a positioning report in another. Do not publish or contact anyone.

### Done
A sourced competitor table and a positioning report with three claims that survive public fact-checking.

### Work class and risk
One-shot research; low risk; a mistaken conclusion is reversed by correcting the report.

### Budget / checkpoint
Two stages. Return to the original chat after each stage.

### Undo
Replace unsupported claims and preserve the source table as evidence.

### Coordinator
The original chat that created this chain.

## WORKSPACE
Absolute path: none (chat-only)
Target environment: claude.ai chat with web search
Destination / audience: private draft for the operator

## AUTHORITY — COPY VERBATIM
- Authorized in this chain: public web research and draft creation
- Requires fresh approval: publication, outreach, or account actions
- Out of scope: SaaS-only competitors and private data

## INHERITED CONTEXT — REQUIRED READING

### Chain goal
A positioning report for the tool "acme-sync" (open-source file sync CLI): who the competitors are, what each does better, and 3 marketing claims that survive public fact-checking.

### Operator decisions — frozen
- Only open-source competitors count (no SaaS-only products)
- Adoption numbers must be verified, never estimated

### Observed facts
- Six relevant open-source competitors were verified; their records are in the table below

### Stage proposals — not binding until ratified
- Use rclone and syncthing as the two reference comparisons; include 4 smaller tools for completeness

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

## Illustrative completion from chat 2

```markdown
### CHAIN COMPLETE

**Chain goal:**
Positioning report for acme-sync: competitors, strengths, 3 fact-check-proof claims.

**Final deliverables:**
- Fact-sheet table, 6 competitors (Stage 1)
- Positioning report with 3 safe claims + 2 claims to avoid (Stage 2)

**Decisions recorded during the chain:**
- Operator decisions ratified: only open-source competitors; adoption numbers verified rather than estimated
- Stage proposals still awaiting ratification: use rclone + syncthing as reference competitors; positioning angle = "single-binary simplicity"

**Next steps outside the chain:**
Review the 3 claims before publishing the README.
```

The user pasted two prompts total. No re-explaining between chats, and chat 2 never repeated the dead-end search from chat 1.
