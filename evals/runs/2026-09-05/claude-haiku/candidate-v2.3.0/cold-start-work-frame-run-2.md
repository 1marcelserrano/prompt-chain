# Raw behavior eval

- Case: `cold-start-work-frame`
- Risk: `continuity`
- Condition: `candidate-v2.3.0`
- Run: 2
- Model request: `claude:haiku`
- Date: `2026-09-05`
- Latency seconds: 34.294
- Usage: `{"cache_creation": {"ephemeral_1h_input_tokens": 14129, "ephemeral_5m_input_tokens": 0}, "cache_creation_input_tokens": 14129, "cache_read_input_tokens": 0, "inference_geo": "", "input_tokens": 10, "iterations": [], "output_tokens": 3154, "server_tool_use": {"web_fetch_requests": 0, "web_search_requests": 0}, "service_tier": "standard", "speed": "standard"}`

## Prompt

Break this migration into fresh chats. Original ask, verbatim: 'Move the fictional app config from YAML to JSON without changing runtime behavior.' Done condition: config.json is generated, the app reads it, and the old YAML remains as a backup. Budget: exactly three slices, returning to the original chat after each. Write boundary: /workspace/app/config only. Revert plan: restore config.yaml and revert only the JSON reader changes. Preserve those values in every stage.

## Raw output

Using **prompt-chain** to decompose this migration into three isolated stages with context propagation.

This is a textbook CHAIN scenario: Stage 2 depends on Stage 1's JSON file, Stage 3 validates Stage 2's app changes. The user has locked the boundary, revert plan, and stage count — those values travel unchanged through every stage.

---

## Usage

1. Open a new chat in Claude Code with workspace access to `/workspace/app/config`
2. Paste the **STAGE 1** block below
3. After the run completes, copy the `### NEXT PROMPT — STAGE 2` block and paste it into a fresh chat
4. Repeat until `CHAIN COMPLETE`

---

## STAGE 1/3 — EXTRACT & GENERATE CONFIG

````markdown
# STAGE 1/3 — EXTRACT & GENERATE CONFIG
# Chain: "YAML to JSON Migration"

## CHAIN META
- Total stages: 3
- Current stage: 1/3
- Stage 1: Read config.yaml, extract structure, generate config.json, verify backup
- Stage 2: Update app to read config.json instead of YAML
- Stage 3: Validate runtime behavior unchanged, confirm both files coexist

## WORK FRAME — COPY VERBATIM

### Original ask
> Move the fictional app config from YAML to JSON without changing runtime behavior.

### Done
config.json is generated, the app reads it, and the old YAML remains as a backup.

### Work class and risk
Personal/pre-production; medium risk (app config changes can break runtime if values are lost or malformed).

### Budget / checkpoint
Exactly three stages. Return to coordinator after each stage.

### Undo
Restore config.yaml and revert only the JSON reader changes.

### Coordinator
The original chat that created this chain.

## WORKSPACE
Absolute path: `/workspace/app/config`
Target environment: Claude Code
Write boundary: `/workspace/app/config` only — do not modify files outside this directory.

## AUTHORITY — COPY VERBATIM
- Authorized in this chain: read config.yaml, generate config.json, run local validation checks
- Requires fresh approval: commit, push, deploy
- Out of scope: modify other config areas, change app runtime behavior, modify external services

## INHERITED CONTEXT — REQUIRED READING

### Chain goal
Move config from YAML to JSON without changing runtime behavior.

### Operator decisions — frozen
- Exactly three stages
- Write boundary: `/workspace/app/config` only
- Revert plan: restore config.yaml and revert only the JSON reader changes
- Preserve values in every stage

### Observed facts
- None yet (initial stage)

### Stage proposals — not binding until ratified
- None yet

### Current state audited (2026-09-05)
- ✅ EXISTS: config.yaml (to be read in this stage)
- ❌ MISSING: config.json (to be generated in this stage)
- ⚠️ Backup assumption: config.yaml will remain untouched after this stage

## THIS STAGE'S TASK
1. Read and parse `/workspace/app/config/config.yaml`
2. Validate the structure (all keys, all values present)
3. Generate `/workspace/app/config/config.json` with identical structure and values
4. Verify that both files coexist (YAML as backup)
5. Log the extraction details for Stage 2 (which keys and value types are in the config)

## CONSTRAINTS
- Do not modify config.yaml
- Do not update app code in this stage
- Stay within `/workspace/app/config` write boundary
- Preserve all values; do not transform or reformat values

## DELIVERABLES
1. `/workspace/app/config/config.json` (generated from YAML)
2. A log of extracted keys and value types (for Stage 2 reference)
3. A `### STAGE REPORT TO COORDINATOR` block
4. A `### NEXT PROMPT — STAGE 2` block

## PROPAGATION PROTOCOL — CRITICAL
When this stage is complete, emit a markdown code block containing the complete, self-contained prompt for Stage 2. The Stage 2 prompt must:
- Copy CHAIN META, WORK FRAME, WORKSPACE, AUTHORITY, and all stable INHERITED CONTEXT from this prompt verbatim
- Update "Observed facts" and "Current state audited" with what you just did (config.json now exists, YAML backup confirmed)
- Update "Stage proposals" only if a model recommendation emerged during this stage (never promote on your own)
- Replace THIS STAGE'S TASK with Stage 2's task (update app to read config.json)
- Include this same PROPAGATION PROTOCOL for Stage 3
- Return both the stage report and next prompt to the coordinator; do not start Stage 2 in this chat

If this stage cannot be completed (missing YAML file, parse error, etc.), emit a `### CHAIN PAUSED` block with one narrow question instead of the next prompt.
````
