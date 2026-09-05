# Raw behavior eval

- Case: `cold-start-work-frame`
- Risk: `continuity`
- Condition: `v2.2.0`
- Run: 3
- Model request: `claude:haiku`
- Date: `2026-09-05`
- Latency seconds: 69.478
- Usage: `{"cache_creation": {"ephemeral_1h_input_tokens": 12563, "ephemeral_5m_input_tokens": 0}, "cache_creation_input_tokens": 12563, "cache_read_input_tokens": 0, "inference_geo": "", "input_tokens": 10, "iterations": [], "output_tokens": 6551, "server_tool_use": {"web_fetch_requests": 0, "web_search_requests": 0}, "service_tier": "standard", "speed": "standard"}`

## Prompt

Break this migration into fresh chats. Original ask, verbatim: 'Move the fictional app config from YAML to JSON without changing runtime behavior.' Done condition: config.json is generated, the app reads it, and the old YAML remains as a backup. Budget: exactly three slices, returning to the original chat after each. Write boundary: /workspace/app/config only. Revert plan: restore config.yaml and revert only the JSON reader changes. Preserve those values in every stage.

## Raw output

Using **prompt-chain** to create a self-propagating 3-stage migration.

---

## How to execute

1. Open a new chat in **Claude Code** (or your environment)
2. Paste the **STAGE 1** block below
3. Let it run — at the end, copy the `### NEXT PROMPT — STAGE 2` code block from its response
4. Paste that into a **new isolated chat**
5. Repeat for STAGE 3
6. When you see `### CHAIN COMPLETE`, the migration is done

Each stage is self-contained with full context. Return here with the final state, or use the revert plan if needed.

---

# STAGE 1/3 — GENERATE CONFIG.JSON

````markdown
# STAGE 1/3 — GENERATE CONFIG.JSON
# Chain: "YAML to JSON Migration"

## CHAIN META
- Total stages: 3
- Current stage: 1/3
- Stage 1: Generate config.json from config.yaml, keep both files
- Stage 2: Update app to read config.json instead of config.yaml
- Stage 3: Validate behavior and document revert plan

## WORKSPACE
Absolute path: `/workspace/app/config`
Target environment: Claude Code
Write boundary: `/workspace/app/config` only

## INHERITED CONTEXT — REQUIRED READING

### Chain goal
Move the app's configuration from YAML to JSON without changing runtime behavior. Done when: config.json is generated, the app reads it, and config.yaml remains as a backup.

### Decisions already made
- JSON format will match the YAML structure exactly (same keys, values, nesting)
- Keep config.yaml untouched as a backup
- Update app to read config.json (not both files)
- Runtime behavior must remain identical

### Revert plan (PRESERVE IN EVERY STAGE)
To undo this migration if needed:
1. Restore config.yaml (already preserved as backup)
2. Revert only the JSON reader changes in the app code
3. No other changes need to be reversed

### Current state audited (2026-09-05)
- ✅ EXISTS: config.yaml in /workspace/app/config/
- ❌ MISSING: config.json (to be created in this stage)
- ⚠️ Write boundary is /workspace/app/config only — do NOT touch app code yet
- ✅ Backup strategy: config.yaml will remain untouched

## THIS STAGE'S TASK
1. Read the existing config.yaml file from `/workspace/app/config/`
2. Parse its structure and all key-value pairs
3. Convert to valid JSON format (preserving structure and values, JSON syntax only)
4. Save as `config.json` in `/workspace/app/config/`
5. Verify config.yaml remains unchanged after this stage

**Done criterion:** config.json exists, is valid JSON, contains all data from config.yaml, and config.yaml is untouched.

## CONSTRAINTS
- Do NOT modify config.yaml under any circumstance
- Do NOT write outside `/workspace/app/config/`
- Do NOT touch app code (that happens in Stage 2)
- Do NOT assume or test runtime behavior yet

## DELIVERABLES
1. `config.json` in `/workspace/app/config/` (valid JSON, matching config.yaml structure and values)
2. Brief confirmation that config.yaml remains unchanged
3. **REQUIRED**: a `### NEXT PROMPT — STAGE 2` code block at the end

---

## PROPAGATION PROTOCOL — CRITICAL

At the end of your response, emit the complete Stage 2 prompt in a markdown code block (use 4 backticks to avoid escaping the inner triple backticks). The next chat will have ZERO memory of this one. Include all CHAIN META, WORKSPACE, and INHERITED CONTEXT verbatim. Update "Current state audited" with the deliverables from this stage. Replace THIS STAGE'S TASK with Stage 2's action list.
````

---

When Stage 1 completes, copy its `### NEXT PROMPT — STAGE 2` block into a new chat and continue from there.
