# CLAUDE.md — prompt-chain

## What this repo is

A single Claude skill distributed as a public GitHub repo. The single source
of truth is `skills/prompt-chain/SKILL.md`. Every behavioral change starts there.

## What to edit

| File | What it controls |
|------|------------------|
| `skills/prompt-chain/SKILL.md` | Skill behavior — triggers, workflow, output format. The body the agent loads. |
| `skills/prompt-chain/README.md` | Per-skill human-facing summary. |
| `README.md` (root) | Product front door. Optimize for non-technical readers. Before/After table is the pitch. |
| `CONTRIBUTING.md` | How to contribute. |

## What NOT to edit

Nothing is auto-generated in this repo. Every file is hand-maintained.
Keep the SKILL.md frontmatter (`name`, `description`) intact — `npx skills`
and the Claude plugin loader both parse it.

## Voice

README and SKILL.md stay terse and direct. No marketing fluff.
Before/After examples ship the value in 5 seconds of scan.

## License

MIT. Contributions welcome. See CONTRIBUTING.md.
