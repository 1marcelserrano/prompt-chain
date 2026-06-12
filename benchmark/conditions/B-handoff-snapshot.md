# Condition B — reactive handoff snapshot

Simulates: before the session ended, a handoff tool captured state into a HANDOFF.md (structure faithful to thepushkarp/handoff and willseltzer/claude-handoff: status, decisions, failed approaches, next steps). The fresh chat receives the snapshot.

The fresh chat receives exactly this:

```markdown
# HANDOFF — acme-sync v2 announcement

## Task status
Writing the launch announcement for acme-sync v2 (open-source file sync
CLI). Outline approved. Draft not started.

## Key decisions (with rationale)
- Angle: "one binary, no daemon" — the differentiator vs rclone/syncthing
- Do NOT mention pricing — a paid tier exists but is unannounced
- Audience: self-hosters, not enterprises

## What we tried
- Opening with a rhetorical question ("Tired of sync tools that...?") —
  rejected by the editor as generic. Don't reuse.

## Style notes
Short sentences. Active voice. Banned words: seamless, game-changer, robust.

## Next steps
Write the final announcement.
```
