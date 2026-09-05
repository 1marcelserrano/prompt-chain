# Mirror contract

`skills/prompt-chain/` in this repository is the source of truth. The copies in `mscs-skills` and `ms-skills` are distribution mirrors. Behavioral edits start here and flow outward after this repository passes its tests.

The renderer gives each destination the shape it needs:

- `mscs-skills` receives the canonical `SKILL.md` byte for byte.
- `ms-skills` receives the complete skill directory. Its `SKILL.md` adds the legacy top-level `version` field required by that catalog while keeping the body byte-identical. Its short README points back to the canon.
- Both mirrors receive `MIRROR.json`, which records the source version, source hash, target profile, and hashes of the generated files.

Render into a new empty directory:

```bash
python3 scripts/render_mirrors.py --output /tmp/prompt-chain-mirrors
```

Review the generated diff in each destination repository, run that repository's validation, and merge through its normal pull-request flow. A mirror is never edited to change behavior. If a destination needs a new compatibility transform, change the renderer and its tests here first.

Runtime installations are another downstream copy. Publish from the canonical skill directory, keep backups outside runtime discovery folders, and verify availability in a fresh session. Filesystem equality proves installation; it does not prove spontaneous selection or invocation.
