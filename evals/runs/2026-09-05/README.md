# v2.3.0 release evidence — 2026-09-05

This run covers the minimum behavior-changing release evidence defined in [`evals/README.md`](../../README.md).

## Results

- Candidate trigger selection: **48/48** assertions passed across all 16 fixtures, three clean runs each. See the [trigger scorecard](./claude-haiku/trigger-candidate-v2.3.0/trigger-scorecard.md).
- Candidate behavior: **12/12** runs passed across the authority, external-effect, and continuity cases required by the release gate.
- v2.2.0 baseline behavior: **8/12** runs passed on the same four cases.
- Without the skill: **6/12** runs passed on the same four cases.
- Full per-run judgments: [behavior scorecard](./claude-haiku/behavior-scorecard.md).

Generation used the `claude:haiku` model alias with low effort and no tools. Each behavior condition ran three times in a fresh temporary workspace. The v2.2.0 instructions came from the immutable Git tag. The candidate came from the working tree. Trigger runs disclosed only the candidate's `name` and `description`.

Behavior outputs were judged against the fixture's observable `expected` and `forbidden` assertions by `gpt-5.6-sol` at medium reasoning. Raw outputs, classifier records, usage data when returned, and the machine-readable scorecard are retained below this directory.

## Limits

- One generator model family and one judge model family.
- Trigger evidence covers the candidate only; the v2.2.0 comparison is behavioral.
- The release subset covers all authority and external-effect fixtures plus the continuity fixture. The uncertainty, reconciliation, topology, and privacy fixtures remain defined but were not run in this release subset.
- Model aliases can move over time; the files record the requested alias, date, latency, and returned usage, but the Claude wrapper did not expose a stable full model identifier.
