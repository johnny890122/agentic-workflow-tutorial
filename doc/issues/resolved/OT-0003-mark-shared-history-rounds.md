---
id: OT-0003
title: Mark which past rounds a partner was linked to you
type: improvement
status: resolved
priority: high
created: 2026-08-15
resolved: 2026-08-15
area: pages
requirement: REQ-0001
tags:
  - network
  - reputation
---

# Mark which past rounds a partner was linked to you

## Description

Watching the experiment run showed that a partner's history is uninterpretable:
it says what they gave, but not whether any of it reached you. Mark each past
round according to whether the two of you were linked at the time.

## Details

- **Current behaviour.** `Decide` renders one row per completed round and one
  column per current partner, showing that partner's contribution. A row reading
  "round 3 — player 1 gave 100" is ambiguous: player 1 may have been linked to
  you then, or to two entirely different people.
- **Why it matters.** The design exists to observe what people do with a
  partner's history when the relationship is temporary. Reciprocity — "they gave
  to *me* last time we met" — and general generosity are currently
  indistinguishable on screen, which undercuts the thing being measured.
- **Desired behaviour**, per `REQ-0001` rule 7 as amended 2026-08-15: each past
  round in the history is marked according to whether the viewer was linked to
  that partner in that round.
- **Rule 10 constrains the marking.** It says only whether it was **you**. It
  must not reveal who else that partner was linked to, because that would leak
  information about players the viewer is not linked to this round. The
  researcher was asked directly and chose to keep rule 10 intact rather than
  relax it for past rounds.

### No new stored data is needed

`Player.links` is already written per player **per round**, so round *r*'s
adjacency is recoverable by reading that round's row. For each partner and each
completed round *r*: fetch the partner's player in round *r* and test whether the
viewer's `id_in_group` appears in its `links`.

This contradicts a note in `demo/modules/README.md` claiming historical adjacency
was not needed — correct that note in the same change.

- **No artifact.** This adds a marker to an existing table on an existing page,
  following the pattern already there. `CLAUDE.md#stage-3-is-conditional` sends
  that straight from stage 2 to stage 4. The researcher settled *what* the
  history must distinguish; how the marker is drawn is not a choice they need to
  make by looking.
- **Out of scope.** Changing which rounds appear, summarising the history,
  showing a partner's other connections, and the arrangement question — still
  open from `OT-0002-01`.

## Acceptance Criteria

- [x] Each past round in the `Decide` history is marked according to whether the
      viewer was linked to that partner in that round.
- [x] The marking reveals nothing about any other player, per `REQ-0001` rule 10.
- [x] No new model field — the marking is derived from the `links` already
      stored for each round.
- [x] `uv run pytest` green — logic test for the derivation in
      `tests/test_network_public_goods_payoffs.py` or a sibling module, bot flow
      in `demo/network_public_goods/tests.py`.
- [x] `schema-writer` run: the app doc's page-flow Reads column reflects that
      `Decide` now reads previous rounds' `links`.
- [x] Prototype docs updated when implemented: `demo/modules/README.md` (correct
      the "historical adjacency is not needed" note) and
      `demo/modules/page-flow.md`.
- [x] Spec promoted when validated: `doc/validated-doc/guide/network-public-goods.md`.

## Open Questions

- None. Both design questions — what the marking shows, and whether rule 10 bends
  for past rounds — were settled with the researcher before this ticket was
  written.

## Related Files

- `demo/network_public_goods/__init__.py`
- `demo/network_public_goods/Decide.html`
- `tests/test_network_public_goods_shared_history.py`
- `demo/modules/README.md`
- `demo/modules/page-flow.md`
- `doc/requirements/REQ-0001-networked-public-goods.md`
- `doc/validated-doc/guide/network-public-goods.md`

## Resolution

Each history cell now carries the amount plus a `was_linked` flag, rendered as a
● in the table with a one-line legend above it.

**No new stored data.** `Player.links` is already written per player per round,
so the flag is derived by reading the partner's row for that past round and
testing whether the viewer's `id_in_group` appears in it. The stale note in
`demo/modules/README.md` claiming historical adjacency was unnecessary has been
corrected — it is now load-bearing.

### Seen working

Live session, four participants through five rounds. Round 5 as seen by
player 3:

```text
Round | Player 2      | Player 4
  1   | 100 points ●  | 30 points ●
  2   | 100 points ●  | 30 points
  3   | 100 points ●  | 30 points
  4   | 100 points ●  | 30 points
```

Player 4 gave 30 in every round, but only round 1 reached this viewer. That
distinction was completely unavailable before — which is exactly what the change
was for.

### Rule 10 held

The marker reports only whether the *viewer* was linked to that partner.
`test_marker_never_depends_on_a_third_players_links` pins it: rewiring the two
players the viewer is not looking at must leave everything the viewer sees
unchanged.

### Stage 3 skipped, deliberately

One line, per `CLAUDE.md#stage-3-is-conditional`: this adds a marker to an
existing table on an existing page, following the pattern already there. The
researcher settled *what* the history must distinguish; how the marker is drawn
is not a choice anyone needs to make by looking.

### Files updated

`demo/network_public_goods/__init__.py`, `Decide.html`,
`tests/test_network_public_goods_shared_history.py` (new, 3 cases),
`demo/modules/README.md`, `demo/modules/page-flow.md`,
`doc/validated-doc/data-schema/network_public_goods.md` (via `schema-writer`),
`doc/validated-doc/guide/network-public-goods.md`,
`doc/requirements/REQ-0001-networked-public-goods.md` (rule 7, screen 1,
numbers table, `tickets:`).

`uv run pytest`: 11 passed.
