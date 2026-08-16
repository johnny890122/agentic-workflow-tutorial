# Prototype notes

Stage 4 of the [workflow](../../CLAUDE.md#workflow), written for the next agent:
which piece does what, which page writes which field, and why the implementation
went the way it did. Markdown only — oTree never treats this folder as an app.

For the researcher-facing view, see [doc/validated-doc/](../../doc/validated-doc/).

## What exists

| Path | What it is |
| --- | --- |
| [settings.py](../settings.py) | One session config, `network_public_goods`, 4 demo participants |
| [network_public_goods/](../network_public_goods/) | The experiment: `REQ-0001`, ticket `OT-0002` |
| [_static/global/empty.css](../_static/global/empty.css) | Empty global stylesheet oTree expects |
| [page-flow.md](page-flow.md) | Page sequence, wait pages, form fields, rounds |

## `network_public_goods` — why it is built this way

### The network is not an oTree grouping

All four players are **one oTree group for all ten rounds**. What changes each
round is who is connected to whom *inside* that group.

This is the single most important thing to understand before changing anything
here. The obvious-looking tools are all wrong: `Subsession.group_randomly()`
re-forms groups, and `group_by_arrival_time` decides who plays together at all.
Neither expresses "same four people, different connections". So the adjacency is
app state: a `Player.links` string, drawn and stored per round.

### Links are drawn in `creating_session`, not on a wait page

`REQ-0001` rule 6 makes the links visible *before* the contribution is entered,
so they must exist before `Decide` renders. `creating_session(subsession)` runs
once per round at session creation, which is early enough for every round at
once. Drawing them in `before_next_page` or on the wait page would be too late.

### `links` encoding

A comma-separated, ascending list of `id_in_group` values — `"2,4"`. Plain text
on purpose: it lands in the CSV export readable, so an analyst can reconstruct
the per-round adjacency without a decoder. `link_ids()` parses it;
`neighbourhood_size()` is `1 + len(link_ids())` and is the payoff divisor.

**Historical adjacency is load-bearing.** An earlier version of this note said
it was not needed. That was true until `OT-0003`: `partner_history()` now reads
each *past* round's `links` to decide whether a partner's contribution that round
reached the current viewer. Because `links` is stored per player per round, that
needed no new field — but it does mean past rounds' `links` values can no longer
be treated as write-once trivia.

### The payoff divisor is the giver's, not the receiver's

```text
payoff_i = (ENDOWMENT - contribution_i)
         + Σ over j in N(i) of (contribution_j × MULTIPLIER / |N(j)|)
```

`|N(j)|` — the **contributor's** neighbourhood. Under the current ring every
neighbourhood is size 3, so an implementation that used the receiver's divisor
would pass every ring test and still be wrong. That is why
[tests/test_network_public_goods_payoffs.py](../../tests/test_network_public_goods_payoffs.py)
asserts it against a *diamond*, whose degrees are unequal. Do not delete that
test when refactoring.

### The arrangement is a ring, and that choice is provisional

See [artifacts/OT-0002-01-link-arrangements/DECISION.md](../../artifacts/OT-0002-01-link-arrangements/DECISION.md).
The artifact stage could not run — no browser tooling — so the ring was chosen by
the implementer on implementation grounds rather than by the researcher looking
at alternatives. A **diamond** (`K4` minus one edge) is the live alternative and
may be the better design, since it is the only arrangement satisfying rule 12
where position is measurable.

Changing the arrangement means changing `creating_session()` only. Everything
downstream — the payoff rule, the templates, the history table — already handles
a variable number of links per player.

### Rule 12: minimum two links

Nobody may ever hold exactly one link. With `MULTIPLIER = 2`, a single link means
`contribution × 2 ÷ 2` — the contributor gets their whole contribution back and
the dilemma disappears for them. A ring satisfies this unconditionally. Any
replacement arrangement must be checked against it.

### Rounding loses points

Points are whole numbers, so a share that does not divide is rounded. 50 into a
neighbourhood of 3 gives three shares of 33, not 33.33 — one point per
contributor evaporates. This is asserted in
`test_uneven_splits_round_and_the_group_loses_the_remainder` so it cannot change
silently, and it is flagged as an open question on `OT-0002`: `REQ-0001` rule 8
says "shared evenly", which whole points cannot always deliver.

### Rule 10 is enforced by construction

A participant must never see anything about a player they were not linked to.
Both `Decide` and `RoundResults` iterate over `link_ids(player)` and nothing
else, so there is no code path that could leak a non-neighbour's contribution.
Keep it that way — a template that iterated `group.get_players()` would break the
requirement invisibly.

The history marker added by `OT-0003` is the one place this was nearly bent. It
reports only whether the viewer *themselves* was linked to that partner in a past
round; showing who **else** the partner was linked to would reveal something
about players the viewer is not linked to now. The researcher was asked directly
and chose to keep rule 10 intact, so
`test_marker_never_depends_on_a_third_players_links` pins it: rewiring the two
players the viewer is not looking at must not change anything the viewer sees.
