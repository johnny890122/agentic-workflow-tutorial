---
id: OT-0001-08
title: Consolidate the friction log and draft the workflow fix ticket
type: story
status: resolved
priority: high
created: 2026-08-15
resolved: 2026-08-15
area: docs
tags:
  - workflow
  - validation
parent: OT-0001
---

# Consolidate the friction log and draft the workflow fix ticket

## Description

Consolidate the friction log from both passes and draft the ticket carrying
every workflow change the run justifies — as a normal `OT-XXXX`, not a child of
this epic, to be implemented on its own schedule after `OT-0001` closes.

## Details

- **Nothing is fixed here.** Editing `CLAUDE.md` or a skill definition during the
  run would invalidate it. This story writes a ticket and nothing else.
- **Every change must trace to a friction-log entry**, so the reasoning stays
  recoverable when someone later asks why a rule says what it says.
- **Known before the run started**: document `doc/workflow-validation/`, and
  repair the `CLAUDE.md` references to the deleted `public_goods_simple`.
- **Settle the standing question**: is `doc/workflow-validation/` the permanent
  home for workflow meta-work, or does it hold only this run?
- **Out of scope.** Applying any of it.

## Acceptance Criteria

- [x] The friction log carries entries from every stage of both passes,
      including the stages that ran cleanly.
- [x] A fix ticket is drafted and filed as pending, carrying every change the
      run justifies, each traced to a friction-log entry.
- [x] It covers, at minimum, documenting `doc/workflow-validation/` and repairing
      the stale `public_goods_simple` references.
- [x] The `doc/workflow-validation/` scope question is settled and recorded.
- [x] No `CLAUDE.md` or `.claude/skills/**` file was edited.

## Open Questions

- None. The two carried forward — whether `doc/workflow-validation/` becomes the
  standing home, and whether `OT-0002-01` should be reopened — now live on
  `OT-0004`, where they belong.

## Related Files

- `doc/workflow-validation/OT-0001-friction-log.md`
- `doc/issues/pending/OT-0004-workflow-doc-fixes.md`

## Resolution

Fix ticket drafted as **`OT-0004`**, filed pending. Forty-eight findings
consolidated into five groups, ordered by how much they actually cost the run
rather than by which file they touch.

### The log

48 entries: 19 `OK`, 17 `GAP`, 4 `STALE`, 5 `BLOCKER`, 3 arguable. Every stage of
both passes is represented, including the ones that needed no interpretation —
`OK` entries are evidence, and a verdict built only from complaints is not a
verdict.

### The standing question, settled

`doc/workflow-validation/` should be the **standing home for workflow meta-work**,
not an archive of this run. The argument is the log's own `OK` entries: they are
only useful if something later contradicts them, which requires the folder to
outlive the run. F-23 in particular — "the stage-2 → stage-3 gap is contingent on
requirement quality, not structural" — is a claim a future run could refute, and
the refutation would be worth more than the original finding.

Recommended to `OT-0004` and carried there as an open question for confirmation
rather than asserted unilaterally, since it changes what the structure tree says.

### What the fix ticket leads with

Not the largest group but the costliest: the absent browser tooling that stopped
stage 3 (F-07, F-29), the missing `blocked` status that forced `OT-0002-01` to
close as `wont_fix` (F-30), and the stale `CLAUDE.md` references — one of which
made `pytest` fail at *collection*, so a green-suite criterion was unreachable
rather than merely failing (F-04).

The single strongest recommendation is smaller and easy to miss: **`DECISION.md`
should be required to record who decided and on what evidence** (F-31, F-42).
The one place in this run where a researcher-owned choice was made by an
implementer for convenience survived into `doc/validated-doc/` as a stated caveat
only because the operator chose to write it down. A terser `DECISION.md` would
have promoted "the network is a ring" as settled design, and the fact that nobody
chose it would have been lost exactly where the document becomes authoritative.

### Deliberately not done

- Nothing was applied. `CLAUDE.md` and `.claude/skills/**` are untouched across
  the entire run.
- One finding group was left unfixed on purpose: tickets that describe work
  rather than specify it (F-36, F-47). Whether that is worth policing is a
  judgment call, not a documentation repair, so `OT-0004` records it without
  proposing a fix.
