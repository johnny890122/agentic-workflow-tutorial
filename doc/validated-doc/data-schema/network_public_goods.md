# Data schema — `network_public_goods`

**Source:** [demo/network_public_goods/__init__.py](../../../demo/network_public_goods/__init__.py)
**URL name:** `network_public_goods`
**Rounds:** `10` · **Players per group:** `4`
**Export granularity:** one row per player per round (`num_participants × C.NUM_ROUNDS`; 40 rows for the `network_public_goods` session config)
**Currency unit:** points (`USE_POINTS = True`, `real_world_currency_per_point = 1.00`)

## Constants (`C`)

| Constant | Value | Purpose |
| --- | --- | --- |
| `NAME_IN_URL` | `'network_public_goods'` | URL segment for participant links; not a data column |
| `PLAYERS_PER_GROUP` | `4` | Group size; the group is fixed for the whole session |
| `NUM_ROUNDS` | `10` | Round count; multiplies row granularity |
| `ENDOWMENT` | `cu(100)` | Per-round budget in points; upper bound on `player.contribution` |
| `MULTIPLIER` | `2` | Factor applied to a contribution before it is split across the contributor's neighbourhood |

## Player

| Field | Type | Initial | Range / choices | Source | Set by | Description |
| --- | --- | --- | --- | --- | --- | --- |
| `contribution` | `CurrencyField` | `None` | `0 – C.ENDOWMENT` | entered | `Decide` (form) | Points this player puts in this round |
| `links` | `StringField` | `None` | comma-separated `id_in_group` values, ascending — e.g. `"2,4"` | computed | `creating_session()` | Who this player is connected to **this round**; drawn before the round is played |
| `payoff` | built-in `CurrencyField` | `0` | — | computed | `set_payoffs()`, via `ResultsWaitPage.after_all_players_arrive` | `C.ENDOWMENT - contribution` plus a share of every contribution made inside this player's neighbourhood |

## Group

_No app-defined fields._

The neighbourhood pot is deliberately not a group-level quantity: each player
has their own neighbourhood, so there is no single shared total to store.

## Subsession

_No app-defined fields._

## Page flow → fields

| # | Page | Kind | Reads | Writes |
| --- | --- | --- | --- | --- |
| 1 | `Decide` | Page | `player.links`; each linked partner's `contribution` **and `links`** in all previous rounds | `player.contribution` |
| 2 | `ResultsWaitPage` | WaitPage | all members' `contribution` and `links` | `player.payoff` |
| 3 | `RoundResults` | Page | linked partners' `contribution`, `player.payoff` | — |

## Notes

<!-- Hand-written caveats. Preserved across regenerations. -->

**`links` is per-round state, not a grouping.** All four players stay in one
oTree group for all ten rounds; what changes each round is who is connected to
whom inside it. `creating_session()` draws a fresh ring for every round when the
session is created, so the value is populated before `Decide` renders — required
because participants see their links before choosing an amount.

**Reading `links` in analysis.** The value is plain text (`"2,4"`), so a
per-round adjacency can be reconstructed from the export with no extra tooling.
Each row records that round only; the history of the network is the sequence of
rows.

The app itself relies on this: the `Decide` page reads earlier rounds' `links`
to mark which past contributions reached the viewer, so no separate record of
historical adjacency exists or is needed.

**Payoff divisor.** Each contribution is divided by the size of the
*contributor's* neighbourhood, not the receiver's. Under the current ring
arrangement every neighbourhood is size 3, so the distinction is invisible in
this data — it would become visible under any arrangement with unequal degrees.

**Rounding.** Points are whole numbers. A share that does not divide evenly is
rounded, so a contribution of 50 into a neighbourhood of 3 yields three shares of
33 rather than 33.33, and the remainder is lost. Payoff sums will therefore not
always reconcile exactly against contributions × `MULTIPLIER`.

**`contribution` is `None` until submitted.** Rows for a session that was created
but not played carry an empty `contribution` and a `payoff` of 0.

## Change log

| Date | Change |
| --- | --- |
| 2026-08-15 | Initial schema doc — app added by `OT-0002-02` |
| 2026-08-15 | `Decide` now also reads previous rounds' `links`, to mark which past contributions reached the viewer (`OT-0003`). No field added or changed. |
