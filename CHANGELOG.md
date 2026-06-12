# Changelog

All notable changes to this project are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning: [SemVer](https://semver.org/).

## [2.1.1] — 2026-06-12

Repo content only — the skill body is unchanged.

### Added
- `templates/` — five ready-to-fill Stage 1 seeds: research, refactor, launch, audit, content chains.
- `benchmark/` — qualitative cold-start benchmark: the same dead task continued under three protocols (no carry · handoff snapshot · prompt-chain Stage 2), with conditions, raw run transcripts, results table, and honest limitations.

## [2.1.0] — 2026-06-12

### Added
- **Secret sanitization rule** in the PROPAGATION PROTOCOL: credentials, API keys, and personal data never travel in the chain — placeholders instead.
- **Failed-approaches ledger**: a `⛔ FAILED` line in the inherited-context template. A fresh chat will happily retry a dead end unless the prompt forbids it.
- **Reference-over-paste rule**: when the target environment reads the workspace (Claude Code), pass file paths instead of file contents; inline only for chat-only environments.
- **Context-budget pruning heuristic**: when inherited context grows past ~1/3 of the prompt, keep decisions/state/failures, cut narration.
- `examples/` — two complete worked chains (research, writing) showing Stage 1, the emitted Stage 2, and `CHAIN COMPLETE`.
- README: three-way comparison (session-handoff tools · workflow engines · prompt-chain), with a note on Amp Handoff.

All changes applied to both EN and PT-BR skill bodies. Informed by a competitive audit of 10+ neighboring tools (2026-06-12).

## [2.0.0] — 2026-06-12

### Changed
- **English is now the canonical skill body** (`skills/prompt-chain/SKILL.md`). Method, templates, and examples fully translated — same structure, same protocols.
- Root README: added language switcher, flow diagram, hardened install (backup + verify steps), FAQ, and author block.

### Added
- `skills/prompt-chain/SKILL.pt-BR.md` — the original Portuguese version, preserved in full (renamed, history intact).
- CHAIN PAUSED protocol: when the environment has the AskUserQuestion tool, the pause now puts the blocker to the user as a direct question with 2–4 options and refines the approach on the spot — the written block stays as fallback. (EN + PT-BR bodies.)
- Credits clause appended to the MIT LICENSE: fork, modify, rebrand — keep the credits intact.
- `prompt-chain.skill` package at root for no-terminal install.
- This CHANGELOG.

## [1.0.0] — 2026-05-22

### Added
- Initial release. Self-propagating chain skill with PROPAGATION PROTOCOL / CHAIN PAUSED / CHAIN COMPLETE protocols, canonical STAGE template, decomposition heuristics, and 2-stage minimal example. Body in PT-BR.
