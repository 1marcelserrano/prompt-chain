# Raw behavior eval

- Case: `cold-start-work-frame`
- Risk: `continuity`
- Condition: `without-skill`
- Run: 2
- Model request: `claude:haiku`
- Date: `2026-09-05`
- Latency seconds: 17.531
- Usage: `{"cache_creation": {"ephemeral_1h_input_tokens": 6887, "ephemeral_5m_input_tokens": 0}, "cache_creation_input_tokens": 6887, "cache_read_input_tokens": 0, "inference_geo": "", "input_tokens": 10, "iterations": [], "output_tokens": 1203, "server_tool_use": {"web_fetch_requests": 0, "web_search_requests": 0}, "service_tier": "standard", "speed": "standard"}`

## Prompt

Break this migration into fresh chats. Original ask, verbatim: 'Move the fictional app config from YAML to JSON without changing runtime behavior.' Done condition: config.json is generated, the app reads it, and the old YAML remains as a backup. Budget: exactly three slices, returning to the original chat after each. Write boundary: /workspace/app/config only. Revert plan: restore config.yaml and revert only the JSON reader changes. Preserve those values in every stage.

## Raw output

```yaml
# Chain Artifact: YAML-to-JSON Config Migration
# Budget: 3 slices | Boundary: /workspace/app/config | Return protocol: original chat after each slice

metadata:
  task: "Move fictional app config from YAML to JSON without changing runtime behavior"
  slices: 3
  boundary: "/workspace/app/config"
  done_condition:
    - "config.json is generated"
    - "app reads config.json"
    - "config.yaml remains as backup"
  revert_plan: "restore config.yaml, revert JSON reader changes only"

slices:
  
  - id: "slice-1"
    title: "Generate config.json from config.yaml"
    scope: "/workspace/app/config"
    tasks:
      - "Read existing config.yaml"
      - "Generate config.json with identical values"
      - "Verify JSON structure matches YAML semantics"
    deliverables:
      - "config.json (new)"
      - "config.yaml (preserved)"
    verification:
      - "config.json exists in /workspace/app/config"
      - "JSON is valid and parseable"
      - "config.yaml unchanged"
    return_to: "original chat"

  - id: "slice-2"
    title: "Update app to read config.json"
    scope: "/workspace/app/config"
    dependencies: ["slice-1"]
    tasks:
      - "Locate config reader (currently reads YAML)"
      - "Add JSON reader alongside YAML reader"
      - "Switch app to read config.json instead of config.yaml"
      - "Verify runtime behavior unchanged"
    deliverables:
      - "Updated config reader (JSON primary)"
      - "config.json (from slice-1, unchanged)"
      - "config.yaml (backup, untouched)"
    verification:
      - "App starts successfully"
      - "App loads all config values from JSON"
      - "Runtime behavior identical to YAML baseline"
    return_to: "original chat"

  - id: "slice-3"
    title: "Verify migration and document"
    scope: "/workspace/app/config"
    dependencies: ["slice-1", "slice-2"]
    tasks:
      - "Functional test: app reads config.json correctly"
      - "Compare values: config.yaml vs config.json (verify parity)"
      - "Confirm backup: config.yaml present and pristine"
      - "Document: revert procedure (restore config.yaml, revert reader)"
    deliverables:
      - "Verification report (all three conditions met)"
      - "Revert instructions documented"
    verification:
      - "config.json is active and functional"
      - "config.yaml exists as backup"
      - "Revert plan is executable"
    return_to: "original chat"

preservation_rules:
  - "config.yaml values must persist in config.json (byte-for-byte semantic equivalence)"
  - "No runtime behavior changes across all slices"
  - "Write boundary: only /workspace/app/config affected"
  - "Revert affects: config.yaml restore + JSON reader removal only"

checkpoint_gates:
  - "After slice-1: JSON file exists and is valid"
  - "After slice-2: App successfully reads JSON; YAML backup present"
  - "After slice-3: All conditions met; revert instructions available"
```
