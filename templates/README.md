# Domain templates

Six ready-to-fill seed prompts. Five are **CHAIN** seeds (sequential Stage 1 prompts that self-propagate); one is a **FAN-OUT** dispatcher (emits N independent prompts and, when needed, a collector). Replace every `[FILL]` and paste into a fresh chat.

| Template | Mode | Stages / pieces | For |
|---|---|---|---|
| [research-chain.md](./research-chain.md) | CHAIN | 3 | Competitive research, market scans, literature reviews |
| [refactor-chain.md](./refactor-chain.md) | CHAIN | 3 | Code refactors that must not change behavior |
| [launch-chain.md](./launch-chain.md) | CHAIN | 3 | Shipping something public: product, post, release |
| [audit-chain.md](./audit-chain.md) | CHAIN | 3 | Auditing a repo, workspace, codebase, or content set |
| [content-chain.md](./content-chain.md) | CHAIN | 3 | Long-form content: essays, guides, course modules |
| [fanout-tasks.md](./fanout-tasks.md) | FAN-OUT | N (independent) | Propagating one decision into several repos, fixing a set of unrelated findings, one prompt per pending item |

Pick the mode with one question: **do the pieces depend on each other's output or state?** Yes → a chain template. No → `fanout-tasks.md`.

Rules that apply to every template:

- The stable context block (`Stable context` / `SHARED CONTEXT`) is copied verbatim into every stage or piece — fill it once, fill it well
- The work frame and authority block travel verbatim; permissions never widen downstream
- Operator decisions, observed facts, and stage proposals remain separate
- No secrets: credentials and tokens never travel in prompt text — use placeholders
- Every stage or piece returns to the named coordinator before dependent work advances
- If a stage/piece gets blocked, it asks (`CHAIN PAUSED` for chains; a result envelope with one question for fan-out pieces) — it never guesses

Want a domain that isn't here? PRs welcome — copy the closest template and adapt the stage breakdown.
