# Domain templates

Five ready-to-fill Stage 1 seed prompts. Each one carries a domain-tuned stage breakdown — replace every `[FILL]`, paste into a fresh chat, and the chain propagates itself.

| Template | Stages | For |
|---|---|---|
| [research-chain.md](./research-chain.md) | 3 | Competitive research, market scans, literature reviews |
| [refactor-chain.md](./refactor-chain.md) | 3 | Code refactors that must not change behavior |
| [launch-chain.md](./launch-chain.md) | 3 | Shipping something public: product, post, release |
| [audit-chain.md](./audit-chain.md) | 3 | Auditing a repo, workspace, codebase, or content set |
| [content-chain.md](./content-chain.md) | 3 | Long-form content: essays, guides, course modules |

Rules that apply to every template:

- The `Stable context` block is copied verbatim into every stage — fill it once, fill it well
- No secrets in the chain: credentials and tokens never travel in prompt text
- If a stage gets blocked, it emits `CHAIN PAUSED` and asks — it never guesses

Want a domain that isn't here? PRs welcome — copy the closest template and adapt the stage breakdown.
