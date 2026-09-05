# Contributing to prompt-chain

Thanks for considering a contribution.

## What to edit

Single source of truth: `skills/prompt-chain/SKILL.md`. All behavior
changes go there first. The root `README.md` is the product front door
and updates after the skill body stabilizes.

## How to test locally

1. Clone the repo and install development requirements: `python3 -m pip install -r requirements-dev.txt`.
2. Run `python3 -m unittest discover -s tests -v` and `python3 scripts/validate_repo.py`.
3. Copy `skills/prompt-chain/` into your Claude skills directory:
   - macOS/Linux: `~/.claude/skills/`
4. Restart Claude or open a new chat.
5. Trigger the skill with representative cases from `evals/trigger-evals.json` and record behavior runs per `evals/README.md`.

When source changes, rebuild `prompt-chain.skill` with `python3 scripts/build_skill.py`. The package is derived; do not edit it directly.

## PR guidelines

- **Conventional Commits.** `feat:`, `fix:`, `docs:`, `refactor:`.
- **One concern per PR.** A docs fix and a behavior change go separately.
- **Show before/after** for any SKILL.md body change. One sentence on why
  the new wording is better.
- **Keep the README install table accurate.** A broken install command
  costs real users.
- **Attach evidence.** Behavior changes include raw candidate runs against the immutable baseline tag; deterministic checks alone are not model evidence.

## Issues

Bug or behavior gap? Use the issue templates in `.github/ISSUE_TEMPLATE/`.
Be specific about input, expected output, actual output.

## License

By contributing you agree your contributions are licensed under MIT.
