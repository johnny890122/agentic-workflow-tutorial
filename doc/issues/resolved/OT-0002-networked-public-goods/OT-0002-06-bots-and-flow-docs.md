---
id: OT-0002-06
title: Bot coverage and the page-flow table
type: story
status: resolved
priority: medium
created: 2026-08-15
resolved: 2026-08-15
area: bots
requirement: REQ-0001
tags:
  - bots
  - tests
  - docs
parent: OT-0002
---

# Bot coverage and the page-flow table

## Description

Cover the page flow with a `PlayerBot` and record the flow in
`demo/modules/page-flow.md`.

## Details

- The bot asserts the contribution bounds with `SubmissionMustFail` on both an
  over-endowment and a negative amount, then plays a fixed strategy that varies
  by `id_in_group` so the history table has content to render.
- `tests/test_bots.py` picks it up automatically for the session config.
- The page-flow table lists all three pages with what is shown, submitted,
  validated, hooked, and written.
- **No artifact** — bot and docs work.

## Acceptance Criteria

- [x] `demo/network_public_goods/tests.py` defines a `PlayerBot` covering all 10
      rounds.
- [x] Out-of-range contributions are rejected, asserted with `SubmissionMustFail`
      at both ends.
- [x] `uv run pytest` green — logic tests in
      `tests/test_network_public_goods_payoffs.py`, bot flow in
      `demo/network_public_goods/tests.py`.
- [x] Prototype docs updated when implemented: `demo/modules/page-flow.md`.

## Open Questions

- None.

## Related Files

- `demo/network_public_goods/tests.py`
- `tests/test_bots.py`
- `demo/modules/page-flow.md`

## Resolution

The bot plays all ten rounds with bounds assertions on both ends.
`uv run pytest` collects 8 tests — seven payoff cases plus the parametrized bot
run — and all pass.

Page-flow table written, including the note that the history table's
three-partner worst case has never been reviewed, because the artifact stage
that would have shown it was blocked.
