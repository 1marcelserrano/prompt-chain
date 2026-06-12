# Worked examples

Each file shows a complete chain in action: the Stage 1 prompt the user pastes, the **actual Stage 2 prompt emitted by the agent** at the end of chat 1 (note the updated dynamic context), and the final `CHAIN COMPLETE` block.

| Example | Stages | Environment | Shows |
|---|---|---|---|
| [research-chain.md](./research-chain.md) | 2 | claude.ai chat | Competitive research → synthesis report. Failed-approaches ledger (`⛔ FAILED`) carrying a dead end forward. |
| [writing-chain.md](./writing-chain.md) | 2 | claude.ai chat | Outline + draft → edit + final. Stable voice rules copied verbatim across stages. |

A third example — a 2-stage coding chain (CSS refactor → responsive validation) — lives in the skill body itself: [SKILL.md](../skills/prompt-chain/SKILL.md#minimal-example--2-stage-chain).

Have a real chain of your own? PRs with new examples are welcome — see [CONTRIBUTING.md](../CONTRIBUTING.md).
