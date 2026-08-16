# Page flow

One table per app: every page in `page_sequence`, what the participant sees,
which `form_fields` they submit, what validation applies, which wait-page or
`before_next_page` hook runs, and which model fields change as a result.

## `network_public_goods`

**Rounds:** 10 · **Players per group:** 4, fixed for the whole session
**Requirement:** [REQ-0001](../../doc/requirements/REQ-0001-networked-public-goods.md) · **Ticket:** `OT-0002`

`page_sequence = [Decide, ResultsWaitPage, RoundResults]`, repeated 10 times.

| # | Page | Participant sees | Form fields | Validation | Hooks | Fields written |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `Decide` | Who they are linked to this round, and a table of every linked partner's contribution in every completed round, each marked ● when the two of them were linked that round | `contribution` | `min=0`, `max=C.ENDOWMENT`; oTree rejects out-of-range on submit | — | `player.contribution` |
| 2 | `ResultsWaitPage` | Standard wait screen | — | — | `after_all_players_arrive = set_payoffs` | `player.payoff` for all four |
| 3 | `RoundResults` | Each linked partner's contribution this round, own contribution, own kept points, own earnings | — | — | — | — |

### Before round 1

`creating_session(subsession)` runs once per round when the session is created
and writes `player.links` for every player in every round. Nothing on the page
flow draws the network; by the time `Decide` renders, the links already exist.
This is required by `REQ-0001` rule 6 — links are visible before the amount is
chosen.

### What each page may show

`Decide` and `RoundResults` both iterate **only** over `link_ids(player)`.
Neither has access to a non-linked player's contribution, which is how
`REQ-0001` rule 10 is enforced — by construction rather than by a filter that
could be forgotten.

### History table shape

`Decide` renders one row per completed round and one column per current partner,
built server-side by `partner_history()`. Each cell carries the amount plus
`was_linked`, derived by reading that past round's `links` on the partner —
which is why the marker needed no new field (`OT-0003`). Under the ring that is 2 columns × up
to 9 rows in round 10. An arrangement with unequal degrees would widen it to 3
columns; the template handles that already, but nobody has looked at it — the
artifact stage that would have answered "does this still read well at full
load?" did not run. See
[artifacts/OT-0002-01-link-arrangements/DECISION.md](../../artifacts/OT-0002-01-link-arrangements/DECISION.md).

### Bot coverage

[network_public_goods/tests.py](../network_public_goods/tests.py) asserts the
bounds with `SubmissionMustFail` on both an over-endowment and a negative
contribution, then plays a fixed strategy that alternates by `id_in_group`, so
the history table has varied content to render across all ten rounds.
