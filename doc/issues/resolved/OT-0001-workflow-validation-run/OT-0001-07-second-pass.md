---
id: OT-0001-07
title: Second pass — change the requirement after seeing the app, and drive it back through
type: story
status: resolved
priority: high
created: 2026-08-15
resolved: 2026-08-15
area: docs
tags:
  - workflow
  - validation
  - second-pass
parent: OT-0001
---

# Second pass — change the requirement after seeing the app, and drive it back through

## Description

Take the settled `REQ-0001`, change it the way a real study would change once
someone has watched the thing running, and drive that change back through the
chain from stage 1 — testing whether the workflow survives work moving backward.

## Details

- **The change is chosen by looking**, not from a list invented in advance. It
  came from the round-10 decision screen in a live session.
- **The correction must start at stage 1**, per `CLAUDE.md`. The measurement is
  whether it actually does, or whether the pressure to just edit the code wins.
- **Which stages the change skips is the point.** The first pass had stage 3
  required on both triggers and then blocked; it never tested the conditional in
  the *skip* direction.
- **The sync rule is under test too**: requirement, ticket, code, `demo/modules/`
  and `doc/validated-doc/` must all agree at the end, or the divergence must be
  stated plainly.
- **Out of scope.** A third pass; the fix ticket (`OT-0001-08`).

## Acceptance Criteria

- [x] The change came from observing the running app, and what was observed is
      recorded.
- [x] `REQ-0001` was amended at stage 1 before any code changed.
- [x] A stage-2 ticket carries the change, with `requirement: REQ-0001`.
- [x] The stage-3 decision was made explicitly and stated in one line with a
      reason.
- [x] `uv run pytest` green.
- [x] The behaviour was observed working, not merely tested.
- [x] Requirement, ticket, `demo/`, `demo/modules/`, and `doc/validated-doc/`
      agree at the end — or the divergence is stated plainly.
- [x] Friction log entry appended covering where the correction started, which
      stages were revisited, and any drift left behind.

## Open Questions

- None.

## Related Files

- `doc/requirements/REQ-0001-networked-public-goods.md`
- `doc/issues/resolved/OT-0003-mark-shared-history-rounds.md`
- `demo/network_public_goods/`
- `doc/validated-doc/guide/network-public-goods.md`
- `doc/workflow-validation/OT-0001-friction-log.md`

## Resolution

**The workflow survived work moving backward, and the backward path earned its
cost.**

### What was observed, and what changed

Round 10 of a live session showed a history table reading "player 1 gave 100 in
round 3" with no indication whether any of it reached the viewer. Because links
reshuffle every round, that generosity may have gone entirely to other people —
so reciprocity and general generosity were indistinguishable on screen. That is
the behaviour the design exists to observe.

The researcher, shown this, chose to mark each past round according to whether the
two of them were linked at the time.

### The stages it visited

| Stage | Verdict |
| --- | --- |
| 1 — requirement | **Required.** `REQ-0001` rule 7 amended, plus screen 1 and the numbers table |
| 2 — ticket | **Required.** `OT-0003`, a standalone improvement, not an epic |
| 3 — artifact | **Skipped**, one line with a reason: a marker on an existing table, following the pattern already there |
| 4 — prototype | **Required.** Implemented, 3 new tests, observed running |
| 5 — validated doc | **Required.** The change alters what a participant can know |

### Why starting at stage 1 mattered

The whole change is about fifteen lines of Python and one table cell. Editing the
code directly would have been faster, and nothing would have caught the shortcut.

But writing the requirement amendment surfaced a conflict the implementer would
never have hit: marking a past round raises the question of whether to show *who
else* that partner was linked to — which would leak information about players the
viewer is not currently linked to, colliding with rule 10. Asked directly, the
researcher chose to keep rule 10 intact.

A code-first change would have picked whichever version was easier to write, and
never noticed it was deciding a participant-privacy policy. That is the clearest
evidence in the run that stage 1 is not ceremony.

### Drift

None left behind. `REQ-0001`, `OT-0003`, `demo/`, `demo/modules/`,
`doc/validated-doc/data-schema/` and `doc/validated-doc/guide/` all agree.

The pass also caught a doc that had gone stale during the *first* pass:
`demo/modules/README.md` claimed historical adjacency was unnecessary. True when
written, made false by `OT-0003`. Fixed in the same change.

### One process deviation

`OT-0001-07` existed only as a roadmap bullet until the pass had run, so this
story was written afterwards from memory — the same gap as F-36. The friction
log was appended live; the ticket was not.
