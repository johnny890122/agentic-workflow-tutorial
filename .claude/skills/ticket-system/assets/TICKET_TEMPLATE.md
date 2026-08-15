---
id: OT-XXXX
title: Short ticket title
type: bug|feature|improvement|refactor|todo|epic|story
status: pending
priority: high|medium|low
created: YYYY-MM-DD
resolved:
area: short-area
requirement: REQ-XXXX
tags:
  - tag
# Stories only: parent epic id, and the story id extends it (OT-XXXX-01).
# parent: OT-XXXX
---

# Short ticket title

## Description

One or two sentences: who needs what, and why now.

## Details

- Current behavior, desired behavior, or key constraint.
- App and page scope: which `demo/<app>/` package, which pages in
  `page_sequence`.
- Out of scope: what this ticket should not do.

## Acceptance Criteria

- [ ] Verifiable done condition.
- [ ] `uv run pytest` green — logic tests in `tests/`, bots in
      `demo/<app>/tests.py`.
- [ ] Prototype docs updated when implemented: `demo/modules/...`.
- [ ] Spec promoted when validated: `doc/validated-doc/guide/...`.

## Open Questions

- What needs a human answer before implementation?

## Related Files

- `path/to/file`

## Handoff Appendix

Use only when the planning discussion includes implementation-critical detail
that should not be compressed away.

### Settled Decisions

- Concrete decisions from the discussion.

### Participant Flow Details

- Page, form fields shown, what the participant does, what the template shows
  next, which model fields change.

### Model And Payoff Notes

- `C` constants, `Player` / `Group` / `Subsession` fields, payoff arithmetic,
  group formation, round structure.

### Test Scenarios

- Target test modules and scenario bullets.

### Deferred Decisions

- Details intentionally left for a later ticket.
