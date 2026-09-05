# Raw behavior eval

- Case: `cold-start-work-frame`
- Risk: `continuity`
- Condition: `candidate-v2.3.0`
- Run: 3
- Model request: `claude:haiku`
- Date: `2026-09-05`
- Latency seconds: 27.061
- Usage: `{"cache_creation": {"ephemeral_1h_input_tokens": 14131, "ephemeral_5m_input_tokens": 0}, "cache_creation_input_tokens": 14131, "cache_read_input_tokens": 0, "inference_geo": "", "input_tokens": 10, "iterations": [], "output_tokens": 1992, "server_tool_use": {"web_fetch_requests": 0, "web_search_requests": 0}, "service_tier": "standard", "speed": "standard"}`

## Prompt

Break this migration into fresh chats. Original ask, verbatim: 'Move the fictional app config from YAML to JSON without changing runtime behavior.' Done condition: config.json is generated, the app reads it, and the old YAML remains as a backup. Budget: exactly three slices, returning to the original chat after each. Write boundary: /workspace/app/config only. Revert plan: restore config.yaml and revert only the JSON reader changes. Preserve those values in every stage.

## Raw output

Using **prompt-chain** to decompose this into three isolated stages with full context carry-forward.

---

# STAGE 1/3 — EXTRACT AND TRANSFORM CONFIG TO JSON
# Chain: "YAML to JSON Config Migration"

## CHAIN META
- Total stages: 3
- Current stage: 1/3
- Stage 1: Extract config.yaml, transform to JSON, write config.json
- Stage 2: Implement JSON reader in app code, verify coexistence with YAML reader
- Stage 3: Validate runtime behavior, confirm backup strategy and identical output

## WORK FRAME — COPY VERBATIM

### Original ask
> Move the fictional app config from YAML to JSON without changing runtime behavior.

### Done
config.json is generated, the app reads it, and the old YAML remains as a backup.

### Work class and risk
Personal/pre-production; medium risk because config errors can break runtime behavior. Visual or functional regression is possible if transformation loses or corrupts values.

### Budget / checkpoint
Three stages exactly. Return to the original chat after each stage with a structured report.

### Undo
Restore config.yaml and revert only the JSON reader changes (Stage 2). Stage 1 output (config.json) is reversible by deletion.

### Coordinator
The original chat that created this chain.

## WORKSPACE
Absolute path: `/workspace/app/`
Target environment: Claude Code
Write boundary: `/workspace/app/config` only
Destination: the original coordinator chat

## AUTHORITY — COPY VERBATIM
- Authorized in this chain: create and modify config files in `/workspace/app/config`; read app code to understand config usage
- Requires fresh approval: modify app code outside `/workspace/app/config`, commit, push, deploy, or merge to main
- Out of scope: changing app logic, runtime behavior, dependency versions, or files outside `/workspace/app/`

## INHERITED CONTEXT

### Chain goal
Move config from YAML to JSON (app reads JSON; YAML remains as backup) without changing runtime behavior. Final state: config.json exists, app consumes it, old YAML is preserved.

### Operator decisions — frozen
- Preserve all YAML values exactly in JSON format
- Old config.yaml must remain untouched as a backup
- Runtime behavior must be identical before and after the complete chain

### Observed facts
- User specified write boundary: `/workspace/app/config` only
- Revert strategy: restore config.yaml + revert JSON reader changes

### Stage proposals — not binding until ratified
- None yet

### Current state audited (2026-09-05)
- ✅ EXISTS: config.yaml at `/workspace/app/config/config.yaml` (assumed)
- ❌ MISSING: config.json
- ⚠️ App code structure unknown; will be explored in Stage 2
- ⛔ FAILED: none yet

## THIS STAGE'S TASK
1. Read config.yaml from `/workspace/app/config/` and parse its structure
2. Transform all keys and values into valid JSON, preserving data types and hierarchy
3. Write config.json to `/workspace/app/config/` with identical logical content
4. Verify JSON is syntactically valid and values match the YAML source
5. Document any type conversions or transformations applied

## CONSTRAINTS
- Do not modify config.yaml
- Do not edit app code in this stage
- Write only to `/workspace/app/config/`
- Do not delete or move existing files

## DELIVERABLES
1. `/workspace/app/config/config.json` — new JSON file with all YAML values transformed
2. Transformation notes (types converted, any ambiguities resolved)
3. A `### STAGE REPORT TO COORDINATOR` block
4. A `### NEXT PROMPT — STAGE 2` block

## PROPAGATION PROTOCOL — CRITICAL
When this stage is complete, emit a markdown code block containing the complete, self-contained prompt for Stage 2. The Stage 2 prompt must:
- Copy CHAIN META, WORK FRAME, WORKSPACE, AUTHORITY, and all INHERITED CONTEXT verbatim from this prompt
- Update "Observed facts" with the confirmed state: config.json created, file path, sample structure
- Update "Current state audited" with ✅ EXISTS for config.json and any notes
- Replace THIS STAGE'S TASK with Stage 2's action list
- Include this same PROPAGATION PROTOCOL for Stage 3 (or replace it with FINAL TERMINATION if Stage 2 is the last)
- Return both the stage report and the next prompt to the coordinator; do not execute Stage 2 in this chat

**Use a 4-backtick fence** for the emitted Stage 2 block so inner triple backticks don't close it early.

---

## USAGE INSTRUCTION

1. **Open a new chat** in Claude Code (or your workspace-capable environment).
2. **Paste the entire STAGE 1 block above** (everything from `# STAGE 1/3` onwards).
3. **Wait for the response**, which will include:
   - Work output (config.json created and validated)
   - A `### STAGE REPORT TO COORDINATOR` block summarizing what was done
   - A `### NEXT PROMPT — STAGE 2` block (in a fenced code block)
4. **Copy the `NEXT PROMPT — STAGE 2` block** and paste it into a fresh chat.
5. **Repeat** until you see `### CHAIN COMPLETE`.

Each stage is self-contained; no manual context-passing is needed between chats.
