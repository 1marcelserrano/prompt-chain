# Contributing to prompt-chain

Thanks for considering a contribution.

## What to edit

Single source of truth: `skills/prompt-chain/SKILL.md`. All behavior
changes go there first. The root `README.md` is the product front door
and updates after the skill body stabilizes.

## How to test locally

1. Clone the repo.
2. Copy `skills/prompt-chain/` into your Claude skills directory:
   - macOS/Linux: `~/.claude/skills/`
3. Restart Claude or open a new chat.
4. Trigger the skill with one of the phrases from the README.

## PR guidelines

- **Conventional Commits.** `feat:`, `fix:`, `docs:`, `refactor:`.
- **One concern per PR.** A docs fix and a behavior change go separately.
- **Show before/after** for any SKILL.md body change. One sentence on why
  the new wording is better.
- **Keep the README install table accurate.** A broken install command
  costs real users.

## Issues

Bug or behavior gap? Use the issue templates in `.github/ISSUE_TEMPLATE/`.
Be specific about input, expected output, actual output.

## License

By contributing you agree your contributions are licensed under MIT.
