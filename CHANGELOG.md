# Changelog

All notable changes to this project are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning: [SemVer](https://semver.org/).

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
