# Worked examples

Each CHAIN file is an abbreviated, illustrative transcript: the Stage 1 prompt, a representative Stage 2 emission with updated dynamic context, and the final completion shape. Ellipses mark content intentionally omitted for readability; these files are examples, not raw model evidence. Raw evaluation outputs belong under `evals/runs/`. The FAN-OUT file shows the dispatcher, independent prompts, and collector shape.

| Example | Mode | Stages / pieces | Environment | Shows |
|---|---|---|---|---|
| [research-chain.md](./research-chain.md) | CHAIN | 2 | claude.ai chat | Competitive research → synthesis report. Failed-approaches ledger (`⛔ FAILED`) carrying a dead end forward. |
| [writing-chain.md](./writing-chain.md) | CHAIN | 2 | claude.ai chat | Outline + draft → edit + final. Stable voice rules copied verbatim across stages. |
| [fanout-tasks.md](./fanout-tasks.md) | FAN-OUT | 3 (independent) | Claude Code | One decision propagated into three unrelated targets. Dispatcher → 3 self-contained prompts, no propagation, identical shared context, one piece pausing without stalling the others. |

A fourth example — a 2-stage coding chain (CSS refactor → responsive validation) — lives in the skill body itself: [SKILL.md](../skills/prompt-chain/SKILL.md#minimal-example--2-stage-chain).

Have a real chain or fan-out of your own? PRs with new examples are welcome — see [CONTRIBUTING.md](../CONTRIBUTING.md).
