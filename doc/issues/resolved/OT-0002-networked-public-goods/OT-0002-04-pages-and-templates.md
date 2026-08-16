---
id: OT-0002-04
title: Decision, wait, and results pages
type: story
status: resolved
priority: high
created: 2026-08-15
resolved: 2026-08-15
area: pages
requirement: REQ-0001
tags:
  - pages
  - templates
parent: OT-0002
---

# Decision, wait, and results pages

## Description

Build the three-screen round: see your links and their history, choose an
amount, wait, then see what your links did and what you earned.

## Details

- `page_sequence = [Decide, ResultsWaitPage, RoundResults]`, repeated 10 times.
- `Decide` renders the current links plus a table of every linked partner's
  contribution in every completed round (`REQ-0001` rule 7), then the
  contribution form.
- `ResultsWaitPage.after_all_players_arrive = set_payoffs`.
- `RoundResults` shows each linked partner's contribution this round, own kept
  points, and own earnings.
- **Rule 10 by construction.** Both pages iterate only `link_ids(player)`, so no
  code path can expose a non-neighbour's choice.
- **No artifact** — the layout questions belonged to `OT-0002-01`, which was
  blocked on tooling. These pages answer them by default rather than by choice.
- **Out of scope.** Session config, bots.

## Acceptance Criteria

- [x] Three pages exist and repeat for all 10 rounds.
- [x] `Decide` shows the current links and each partner's itemised history.
- [x] Nothing about a non-linked player appears on either page.
- [x] Payoffs are computed on the wait page, once all four have submitted.
- [x] `uv run pytest` green.
- [x] Prototype docs updated when implemented: `demo/modules/page-flow.md`.

## Open Questions

- The history table has never been reviewed at full load with three partners.
  Under the ring it is two columns; an unequal-degree arrangement would widen it
  to three. This is exactly what the blocked artifact stage would have answered.

## Related Files

- `demo/network_public_goods/Decide.html`
- `demo/network_public_goods/RoundResults.html`
- `demo/network_public_goods/__init__.py`
- `demo/modules/page-flow.md`

## Resolution

Built and walked end to end in a live session over HTTP: four participants
through all ten rounds, the history table populating each round, and payoffs
matching hand calculation — 100 kept + 0 own + 67 from a full contributor + 20
from a partial one = 187, which is what the page showed.

Rule 10 held in observation: the participant inspected saw players 1 and 2 and
never player 3.

`partner_history()` builds the table server-side as one row per completed round
and one column per current partner, keeping the round-10 worst case on one
screen.
