---
id: OT-0002-03
title: The per-round link draw
type: story
status: resolved
priority: high
created: 2026-08-15
resolved: 2026-08-15
area: models
requirement: REQ-0001
tags:
  - models
  - network
parent: OT-0002
---

# The per-round link draw

## Description

Draw the network for every round and store it on the players, early enough that
the decision page can show it.

## Details

- **Arrangement:** ring, per `artifacts/OT-0002-01-link-arrangements/DECISION.md`.
  Provisional — chosen by the implementer because the artifact stage could not
  run.
- **Where it runs:** `creating_session(subsession)`, which fires once per round
  at session creation. `REQ-0001` rule 6 makes links visible before the
  contribution is entered, so a wait-page or `before_next_page` draw is too late.
- **How:** shuffle the four `id_in_group` values into a cycle; each player's
  neighbours are the entries either side of them, stored ascending in
  `Player.links`.
- **Rule 12** — minimum two links — holds unconditionally for a ring.
- **No artifact** — the arrangement question was `OT-0002-01`; this story only
  implements the outcome.
- **Out of scope.** Pages, templates, session config.

## Acceptance Criteria

- [x] `creating_session()` writes `Player.links` for every player in every round.
- [x] Every player holds exactly two links, satisfying `REQ-0001` rule 12.
- [x] Links are mutual (`REQ-0001` rule 5) — a cycle guarantees it.
- [x] Links are redrawn each round, independent of the previous round.
- [x] `uv run pytest` green.
- [x] Prototype docs updated when implemented: `demo/modules/README.md`.

## Open Questions

- None.

## Related Files

- `demo/network_public_goods/__init__.py`
- `artifacts/OT-0002-01-link-arrangements/DECISION.md`
- `demo/modules/README.md`

## Resolution

`creating_session()` shuffles the four players into a cycle per round and writes
each player's two neighbours to `Player.links` as an ascending comma-separated
string.

Verified in a live session: one participant was linked to players 1 and 3 in
round 1 and players 1 and 2 in round 10, so the redraw is real rather than a
fixed arrangement computed once.

Changing the arrangement later means changing this one function — the payoff
rule, the templates, and the history table all already handle a variable number
of links per player.
