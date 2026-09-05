# Trigger scorecard

Candidate: `v2.3.0`. Model: `claude:haiku`. Three clean runs per fixture.

| Fixture | Expected | Result |
|---|---:|---:|
| `trigger-chain-pt` | trigger | 3/3 |
| `trigger-fanout-pt` | trigger | 3/3 |
| `trigger-context-limit` | trigger | 3/3 |
| `trigger-handoff-people` | trigger | 3/3 |
| `trigger-sequential-repos` | trigger | 3/3 |
| `trigger-one-prompt-per-task` | trigger | 3/3 |
| `trigger-model-switch` | trigger | 3/3 |
| `trigger-hybrid` | trigger | 3/3 |
| `no-trigger-direct-task` | do not trigger | 3/3 |
| `no-trigger-same-session-subagents` | do not trigger | 3/3 |
| `no-trigger-generic-plan` | do not trigger | 3/3 |
| `no-trigger-exploration` | do not trigger | 3/3 |
| `no-trigger-checklist` | do not trigger | 3/3 |
| `no-trigger-long-single-output` | do not trigger | 3/3 |
| `no-trigger-reminder` | do not trigger | 3/3 |
| `no-trigger-agent-workflow` | do not trigger | 3/3 |
