---
id: OT-0002-02
title: Constants, fields, and the payoff rule
type: story
status: resolved
priority: high
created: 2026-08-15
resolved: 2026-08-15
area: models
requirement: REQ-0001
tags:
  - models
  - payoff
parent: OT-0002
---

# Constants, fields, and the payoff rule

## Description

Create the `network_public_goods` package with its constants, model fields, and
the neighbourhood payoff rule, proven by logic tests that set the adjacency
directly. This is the one part of the epic that does not wait on the arrangement
choice.

## Details

- **Why this can run before stage 3.** The payoff rule takes an adjacency as
  input; it does not care where the adjacency came from. Tests set it by hand,
  so the arithmetic is settled and proven before `OT-0002-01` closes. The *draw*
  is `OT-0002-03` and does wait.
- **New package `demo/network_public_goods/`.** This story creates
  `__init__.py` with constants, models, and the payoff function only. No pages,
  no templates, no `page_sequence` entries beyond what is needed to import
  cleanly, no session config — those are later stories.

### Constants

```text
NAME_IN_URL = 'network_public_goods'
PLAYERS_PER_GROUP = 4
NUM_ROUNDS = 10
ENDOWMENT = cu(100)
MULTIPLIER = 2
```

All four players are one oTree group for the whole session. The group never
re-forms: `Subsession.group_randomly()` and `group_by_arrival_time` are both
wrong here, because the thing that changes each round is the network *inside*
the group, not the group.

### Fields

- `Player.contribution` — `CurrencyField(min=0, max=C.ENDOWMENT)`, the only
  player-entered field, one per player per round. Initial value is `None`, per
  oTree's default.
- **Per-round adjacency**, stored because it is drawn before the decision page
  renders and read again when payoffs are computed. A `StringField` on `Player`
  holding that round's linked `id_in_group` values is the simplest
  representation that survives the data export. **Settle the encoding in this
  story** and write it down — a comma-separated sorted list of ids is the
  obvious choice, but whatever is picked must be readable from an exported CSV
  without a decoder ring.
- No `Group` or `Subsession` fields are required. The neighbourhood pot is not a
  group-level quantity — each player has their own neighbourhood, so there is no
  single shared total to store.

### The payoff rule

For player *i* with link set *L(i)* and neighbourhood *N(i) = {i} ∪ L(i)*:

```text
payoff_i = (ENDOWMENT - contribution_i)
         + Σ over j in N(i) of (contribution_j × MULTIPLIER / |N(j)|)
```

**The divisor is the size of the contributor's neighbourhood, not the
receiver's.** This is the single most likely thing to implement backwards, and
it is only observable when neighbourhoods differ in size — which is why the
diamond test scenario below is not optional.

Written by a `set_payoffs`-style function. It will be called from the results
wait page's `after_all_players_arrive` in `OT-0002-04`; this story only needs it
callable and correct.

### Tests

`tests/test_network_public_goods_payoffs.py`, using the `otree_session_factory`
fixture — `Player` is an ORM object, so a real session is required.

- **Ring, uniform.** 4-cycle adjacency set by hand, everyone contributes 50.
  Every neighbourhood is size 3, so each player receives `3 × (50 × 2 / 3) = 100`
  and keeps 50 → payoff 150 each.
- **Ring, one free rider.** Three contribute 100, one contributes 0. Assert the
  free rider out-earns every contributor, and that the two players linked to the
  free rider earn less than the two who are not.
- **Diamond, asymmetric.** `K4` minus one edge; neighbourhoods of size 4, 4, 3,
  3. Assert receipts are computed with the contributor's divisor. A
  same-divisor-for-everyone implementation passes both ring tests and fails only
  this one.
- **Nobody contributes.** Every payoff is exactly `C.ENDOWMENT`.
- **Everyone contributes everything, ring.** Total payoff across the group
  exceeds `4 × C.ENDOWMENT` — the multiplier grows the pie.

Bot coverage and `SubmissionMustFail` bounds checking belong to `OT-0002-06`,
once pages exist to submit to.

- **No artifact** — payoff arithmetic and model fields, settled on paper by
  `REQ-0001`, with no open visual question. Per `CLAUDE.md#stage-3-is-conditional`
  this goes straight from stage 2 to stage 4. (The epic's artifact requirement
  is `OT-0002-01` and concerns the arrangement, not this story.)
- **`schema-writer` fires automatically** on the new `__init__.py`, per
  `CLAUDE.md`. Do not hand-write anything under
  `doc/validated-doc/data-schema/`.
- **Out of scope.** The link draw, pages, templates, the session config, bots,
  and deleting `scaffold_check`.

## Acceptance Criteria

- [x] `demo/network_public_goods/__init__.py` defines the five constants above,
      `Player.contribution`, and the per-round adjacency field.
- [x] The adjacency encoding is documented in `demo/modules/` and readable from
      an exported CSV without additional tooling.
- [x] The payoff function divides each contribution by the **contributor's**
      neighbourhood size, proven by the diamond scenario.
- [x] `uv run pytest` green — logic tests in
      `tests/test_network_public_goods_payoffs.py`. Bot coverage is
      `OT-0002-06`; no empty bot test is added here.
- [x] `schema-writer` has run and `doc/validated-doc/data-schema/` documents the
      new app, without any hand edit to that directory.
- [x] Prototype docs updated when implemented: `demo/modules/README.md`.
- [x] No page, template, or `SESSION_CONFIGS` change in this story.

## Open Questions

- None. The arrangement is not needed here; the tests supply adjacency directly.

## Related Files

- `demo/network_public_goods/__init__.py`
- `tests/test_network_public_goods_payoffs.py`
- `tests/conftest.py`
- `demo/modules/README.md`
- `doc/requirements/REQ-0001-networked-public-goods.md`
- `doc/otree-doc/models.html`
- `doc/otree-doc/currency.html`

## Resolution

`demo/network_public_goods/__init__.py` created with the five constants,
`Player.contribution`, `Player.links`, and `set_payoffs()`.

**Adjacency encoding settled:** a comma-separated ascending list of
`id_in_group` values — `"2,4"`. Verified readable straight out of the CSV
export as `player.links`, with no decoding step. Documented in
`demo/modules/README.md`.

**The divisor is the contributor's neighbourhood**, asserted against a diamond
(`K4` minus one edge, degrees 3/3/2/2) in
`test_divisor_is_the_contributors_neighbourhood`. Under the ring every
neighbourhood is size 3, so a receiver's-divisor implementation would pass every
other test — that scenario is the only thing standing between the code and a
plausible, silent, wrong answer.

**A design problem surfaced during implementation.** Points are whole numbers,
so a share that does not divide evenly is rounded: 50 contributed into a
neighbourhood of 3 yields three shares of 33, not 33.33, and one point per
contributor is lost. `REQ-0001` rule 8 says "shared evenly", which whole points
cannot always deliver. Rather than absorb it silently, the behaviour is pinned
by `test_uneven_splits_round_and_the_group_loses_the_remainder`, documented in
`demo/modules/README.md` and the data-schema Notes, and raised as an open
question on `OT-0002`.

`schema-writer` ran on the new `__init__.py`; nothing under
`doc/validated-doc/data-schema/` was hand-edited.
