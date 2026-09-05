# Raw behavior eval

- Case: `cold-start-work-frame`
- Risk: `continuity`
- Condition: `candidate-v2.3.0`
- Run: 1
- Model request: `claude:haiku`
- Date: `2026-09-05`
- Latency seconds: 28.862
- Usage: `{"cache_creation": {"ephemeral_1h_input_tokens": 14133, "ephemeral_5m_input_tokens": 0}, "cache_creation_input_tokens": 14133, "cache_read_input_tokens": 0, "inference_geo": "", "input_tokens": 10, "iterations": [], "output_tokens": 2145, "server_tool_use": {"web_fetch_requests": 0, "web_search_requests": 0}, "service_tier": "standard", "speed": "standard"}`

## Prompt

Break this migration into fresh chats. Original ask, verbatim: 'Move the fictional app config from YAML to JSON without changing runtime behavior.' Done condition: config.json is generated, the app reads it, and the old YAML remains as a backup. Budget: exactly three slices, returning to the original chat after each. Write boundary: /workspace/app/config only. Revert plan: restore config.yaml and revert only the JSON reader changes. Preserve those values in every stage.

## Raw output

Using **prompt-chain** skill to break this migration into isolated, sequential stages.

This is a **CHAIN** (not FAN-OUT): Stage 2 needs the JSON file from Stage 1; Stage 3 needs the JSON reader from Stage 2. The pieces are ordered and have dependencies.

---

## Usage

1. Open a new chat in your environment (Claude Code or equivalent with file access to `/workspace/app/config`)
2. Paste the **STAGE 1** block below
3. At the end of that response, copy the `### NEXT PROMPT — STAGE 2` block and paste it into a fresh chat
4. Repeat until `### CHAIN COMPLETE`

Each stage reports its deliverables and pauses for review before the next one runs.

---

````markdown
# STAGE 1/3 — CONVERT YAML TO JSON
# Chain: "YAML to JSON Config Migration"

## CHAIN META
- Total stages: 3
- Current stage: 1/3
- Stage 1: Convert config.yaml → config.json, preserve structure and values
- Stage 2: Update app to read config.json (JSON reader logic)
- Stage 3: Validate runtime behavior unchanged, confirm YAML backup in place

## WORK FRAME — COPY VERBATIM

### Original ask
> Move the fictional app config from YAML to JSON without changing runtime behavior.

### Done
config.json is generated, the app reads it, and the old YAML remains as a backup.

### Work class and risk
Personal/pre-production; medium risk because config changes can affect app runtime behavior.

### Budget / checkpoint
Exactly three stages. Return to the original chat after each stage for review.

### Undo
Restore config.yaml and revert only the JSON reader changes. Do not restore YAML as the primary config.

### Coordinator
The original chat that initiated this chain.

## WORKSPACE
Absolute path: `/workspace/app/config`
Target environment: Claude Code (or file-capable agent)
Destination: /workspace/app/config (read and write only within this directory)
Conventions: preserve all file names and value structure from YAML during conversion

## AUTHORITY — COPY VERBATIM
- Authorized in this chain: read and write files in /workspace/app/config only; convert config formats
- Requires fresh approval: any changes outside /workspace/app/config, any changes to app runtime logic other than JSON reading
- Out of scope: modifying the YAML file after Stage 1; changing the app entry point; altering runtime behavior beyond config reading

## INHERITED CONTEXT — REQUIRED READING

### Chain goal
Move fictional app config from YAML to JSON without changing runtime behavior. config.json is generated and readable by the app; old YAML remains as a backup.

### Operator decisions — frozen
- Budget is exactly 3 stages (no more, no fewer)
- Write boundary: /workspace/app/config only
- Revert plan: restore config.yaml and revert only JSON reader changes
- Preserve all config values and structure across conversion

### Observed facts
- None yet (Stage 1 is the seed)

### Stage proposals — not binding until ratified
- None yet

### Current state audited (2026-09-05)
- ✅ EXISTS: config.yaml (assumed present in /workspace/app/config)
- ❌ MISSING: config.json
- ⚠️ Assuming YAML is valid and parseable
- ⛔ FAILED: (none yet)

## THIS STAGE'S TASK
1. Read config.yaml from /workspace/app/config
2. Parse the YAML structure
3. Convert to JSON, preserving all keys, values, and nesting
4. Write config.json to /workspace/app/config
5. Verify JSON is valid and parseable

## CONSTRAINTS
- Do not modify config.yaml
- Do not write files outside /workspace/app/config
- Do not change any config values during conversion
- Do not alter app runtime logic (that's Stage 2)

## DELIVERABLES
1. config.json (valid JSON, structure-identical to config.yaml)
2. A `### STAGE REPORT TO COORDINATOR` block
3. A `### NEXT PROMPT — STAGE 2` block

## PROPAGATION PROTOCOL — CRITICAL
When this stage is complete, emit a markdown code block containing the complete, self-contained prompt for Stage 2. The Stage 2 prompt must:

- Open with `# STAGE 2/3 — UPDATE APP TO READ JSON`
- Copy CHAIN META, WORK FRAME, WORKSPACE, AUTHORITY, and all stable INHERITED CONTEXT verbatim
- Update "Observed facts" and "Current state audited" with what Stage 1 just did
- Replace THIS STAGE'S TASK with Stage 2's action list (update app config reader to use config.json)
- Keep the same PROPAGATION PROTOCOL, pointing to Stage 3
- Return both the stage report and the next prompt to the coordinator

If this stage cannot be completed (missing YAML file, parse error, write permission issue), emit `### CHAIN PAUSED` instead of the next prompt.
````

---

Once you paste and run **STAGE 1**, copy the emitted `### NEXT PROMPT — STAGE 2` block and paste it into a fresh chat. The chain will carry forward all context and decisions automatically.
