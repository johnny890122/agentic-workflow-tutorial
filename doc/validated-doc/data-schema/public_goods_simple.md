# Data schema — `public_goods_simple`

**Source:** [demo/public_goods_simple/__init__.py](../../../demo/public_goods_simple/__init__.py)
**URL name:** `public_goods_simple`
**Rounds:** `1` · **Players per group:** `3`
**Export granularity:** one row per player per round (`num_participants × C.NUM_ROUNDS`; 3 rows for the `public_goods_simple` session config)
**Currency unit:** points (`USE_POINTS = True`, `real_world_currency_per_point = 1.00`)

## Constants (`C`)

| Constant | Value | Purpose |
| --- | --- | --- |
| `NAME_IN_URL` | `'public_goods_simple'` | URL segment for participant links; not a data column |
| `PLAYERS_PER_GROUP` | `3` | Group size; divisor when splitting the pot into `individual_share` |
| `NUM_ROUNDS` | `1` | Round count; multiplies row granularity |
| `ENDOWMENT` | `cu(100)` | Per-round budget in points; upper bound on `player.contribution` |
| `MULTIPLIER` | `1.8` | Efficiency factor applied to `group.total_contribution` before splitting |

## Player

| Field | Type | Initial | Range / choices | Source | Set by | Description |
| --- | --- | --- | --- | --- | --- | --- |
| `contribution` | `CurrencyField` | `None` | `0 – C.ENDOWMENT` (`min=0`, `max=C.ENDOWMENT`) | entered | `Contribute` (form) | Amount the player puts into the public pot |
| `payoff` | built-in `CurrencyField` | `0` | — | computed | `set_payoffs()` via `ResultsWaitPage` | `C.ENDOWMENT - contribution + group.individual_share` |

`label` for `contribution` is `"How much will you contribute?"`. It is required — no `blank=True` — so a participant cannot advance past `Contribute` without a value.

## Group

| Field | Type | Initial | Range / choices | Source | Set by | Description |
| --- | --- | --- | --- | --- | --- | --- |
| `total_contribution` | `CurrencyField` | `None` | `0 – C.PLAYERS_PER_GROUP × C.ENDOWMENT` | computed | `set_payoffs()` via `ResultsWaitPage` | Sum of all members' `contribution` |
| `individual_share` | `CurrencyField` | `None` | ≥ 0 | computed | `set_payoffs()` via `ResultsWaitPage` | `total_contribution × C.MULTIPLIER / C.PLAYERS_PER_GROUP` — each member's cut of the multiplied pot |

## Subsession

_No app-defined fields._

## Page flow → fields

| # | Page | Kind | Reads | Writes |
| --- | --- | --- | --- | --- |
| 1 | `Contribute` | Page | `C.PLAYERS_PER_GROUP`, `C.ENDOWMENT`, `C.MULTIPLIER` | `player.contribution` |
| 2 | `ResultsWaitPage` | WaitPage (`after_all_players_arrive = set_payoffs`) | all members' `contribution` | `group.total_contribution`, `group.individual_share`, every member's `player.payoff` |
| 3 | `Results` | Page | `C.ENDOWMENT`, `player.contribution`, `group.total_contribution`, `group.individual_share`, `player.payoff` | — |

`Contribute.html` renders `{{ formfields }}`, which emits exactly the page's `form_fields` list — `contribution` and nothing else.

## Notes

<!-- Hand-written caveats. Preserved across regenerations. -->

- `individual_share` is computed from a `float` `MULTIPLIER` against a `CurrencyField`, so it carries oTree's currency rounding; payoffs are not guaranteed to be whole points.
- Because `NUM_ROUNDS = 1`, there is no cross-round carryover: `participant.payoff` equals this app's single-round `player.payoff`.

## Change log

| Date | Change |
| --- | --- |
| 2026-08-15 | Initial schema doc |
