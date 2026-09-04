# Behavioral evaluations

These fixtures test two different boundaries. `trigger-evals.json` asks whether the skill should be selected. `behavior-evals.json` asks whether a selected skill preserves authority, continuity, topology, and privacy.

The JSON files are test definitions, not model results. A schema-valid fixture does not prove model behavior.

## Comparison protocol

Run every case in a clean context under three conditions:

1. **Without the skill**: the same model and prompt, with no prompt-chain instructions loaded.
2. **v2.2.0 baseline**: load `skills/prompt-chain/SKILL.md` from the `v2.2.0` tag.
3. **Candidate**: load the working-tree skill.

Run each condition at least three times. Keep model and reasoning settings fixed within a comparison. Record the exact model, date, condition, run number, raw output, assertion verdicts, latency when available, and token usage when available.

Use the `expected` and `forbidden` statements as observable assertions. Do not grade for matching a particular heading or phrase. A run passes when its behavior satisfies every expected assertion and none of the forbidden outcomes appears.

Store raw results under:

```text
evals/runs/YYYY-MM-DD/<model>/<condition>/<case-id>-run-N.md
```

## Baseline source

The baseline is the immutable `v2.2.0` Git tag, not a copied skill file that can drift. Confirm it before a comparison:

```bash
git show v2.2.0:skills/prompt-chain/SKILL.md
```

## Minimum release evidence

A behavior-changing release needs:

- all deterministic repository checks passing;
- trigger results for every trigger fixture;
- behavior results for every authority and external-effect fixture;
- no candidate regression against v2.2.0 on the continuity cases;
- raw outputs retained so a human can audit the verdicts.
