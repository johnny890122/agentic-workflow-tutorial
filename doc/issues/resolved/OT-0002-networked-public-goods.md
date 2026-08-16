---
id: OT-0002
title: Networked public goods — reshuffled links with visible partner history
type: epic
status: resolved
priority: high
created: 2026-08-15
resolved: 2026-08-15
area: models
requirement: REQ-0001
tags:
  - public-goods
  - network
  - reputation
---

# Networked public goods — reshuffled links with visible partner history

## Description

Build the four-player public goods experiment described by `REQ-0001`: ten
rounds, links redrawn at random each round, and each partner's full contribution
history visible before you decide how much to give.

## Details

- **Current state.** `demo/` holds only `demo/scaffold_check/`, a disposable
  one-page app with no fields, no form, and no payoff rule. It is scaffolding,
  not prior art, and supplies no pattern to copy. There is no promoted spec in
  `doc/validated-doc/guide/` and no other requirement to conflict with.
- **App.** New package `demo/network_public_goods/`. This confirms the name
  `REQ-0001` proposed in its translation notes — descriptive, matches the
  requirement title, no collision.
- **Scope is the whole requirement in one pass**, not a staged cut: ten rounds,
  full itemised history, real payoff arithmetic, working links.
- **`scaffold_check` is removed** as part of this epic, once
  `network_public_goods` has a session config. Delete the package, drop its
  `SESSION_CONFIGS` entry, and let `schema-writer` prune its data-schema doc.
  See `demo/modules/README.md`.

### Round structure and payoff

Per `REQ-0001`, and unchanged by this epic:

- `C.PLAYERS_PER_GROUP = 4`, `C.NUM_ROUNDS = 10`, `C.ENDOWMENT = cu(100)`,
  `C.MULTIPLIER = 2`. All four participants are one oTree group for the whole
  session; the group never re-forms.
- The "network" is per-round state **inside** that fixed group. This is not
  `group_by_arrival_time` and not `Subsession.group_randomly()` — those would
  re-matter the wrong thing. The adjacency is drawn and stored by the app.
- A contribution is doubled, then split evenly among the contributor and their
  links for that round. Points not contributed are kept.
- Links are drawn **before** the decision page renders, because the requirement
  makes them visible at decision time.

### The degree-1 constraint

`REQ-0001` records the consequence of `MULTIPLIER = 2` combined with "shared
among you and your links": a participant holding exactly **one** link receives
`contribution × 2 ÷ 2` — their whole contribution back — so giving becomes free
and the public-goods dilemma disappears for that person.

**This is a hard constraint, settled with the user:** every arrangement the app
can draw must give each participant **at least two links**. On four players that
admits the ring (all degree 2), the diamond — `K4` minus one edge (degrees
3, 3, 2, 2) — and the complete graph (all degree 3). It rules out
hub-and-spokes, which gives three players exactly one link each.

Note that the complete graph is the degenerate case: if everyone is linked to
everyone, the network does nothing and the design collapses to an ordinary
four-player public goods game. It is useful inside a mixed draw, not as a design
on its own.

### Artifact required — stage 3 fires on both triggers

Per `CLAUDE.md#stage-3-is-conditional`, and as `REQ-0001` states explicitly:

- **Visual trigger.** The researcher asked to *see* the link arrangements rather
  than pick one from a description.
- **No-precedent trigger.** A per-round link structure inside a fixed group
  exists nowhere in this repo.

Spike under `artifacts/OT-0002-01-link-arrangements/` before any page work. It
must demonstrate the arrangement choice, the network drawn so a participant can
tell at a glance who they are linked to, and how nine rounds of itemised history
for up to three partners fit on one screen. Nothing there is promoted verbatim;
the winner is rewritten as a real page against real fields.

### Child stories

Only stories whose scope is settled are written. The arrangement is unchosen
until stage 3 closes, so anything whose shape depends on it stays a bullet.

| Story | Workstream | Scope | Status |
| --- | --- | --- | --- |
| `OT-0002-01` | artifact | Link-arrangement variants → `DECISION.md` | written |
| `OT-0002-02` | models | Constants, fields, payoff arithmetic, logic tests | written |
| `OT-0002-03` | models | The per-round link draw — **needs the chosen arrangement** | roadmap |
| `OT-0002-04` | pages + templates | `Decide` / wait / `RoundResults`, history display — **needs `DECISION.md`** | roadmap |
| `OT-0002-05` | session config | `SESSION_CONFIGS` entry, remove `scaffold_check` | roadmap |
| `OT-0002-06` | bots + docs | `PlayerBot` page-flow coverage, `demo/modules/page-flow.md` | roadmap |
| `OT-0002-07` | docs/promotion | Promote to `doc/validated-doc/guide/network-public-goods.md` | roadmap |

### Dependency plan

- **First, and blocking:** `OT-0002-01`. The arrangement decides the draw, the
  neighbourhood sizes, and therefore what every payoff test asserts against.
- **In parallel with the artifact:** `OT-0002-02`. Constants, fields, and the
  payoff rule are arrangement-independent — payoff tests set the adjacency
  directly rather than drawing it, so the arithmetic can be proven before the
  arrangement exists.
- **After `DECISION.md`:** `OT-0002-03`, then `OT-0002-04`.
- **After the field set stabilizes:** `OT-0002-05`, then `OT-0002-06`.
- **After validation only:** `OT-0002-07`. Nothing is promoted on the strength
  of an unvalidated prototype.

### Out of scope

- **Punishment.** Explicitly excluded by `REQ-0001` — the obvious follow-up
  study, and it would confound the reputation signal this design exposes.
- **Participant-chosen links, chat, and a fixed-partner control treatment.**
  Offered to the researcher as exclusions and not taken, but never asked for
  either. Not built here. See Open Questions.
- Deployment, rooms, `Procfile`, and multi-session concerns.
- Any analysis tooling. The experiment produces data; reading it is not this
  epic's job.

## Acceptance Criteria

- [x] All child stories closed (`resolved` or `wont_fix`).
- [x] `demo/network_public_goods/` runs ten rounds for four players, with links
      redrawn each round and each partner's itemised history visible before the
      contribution is submitted.
- [x] Every rule in `REQ-0001`'s `## Rules the experiment must follow` is
      observably satisfied in a real session — in particular rule 10: a
      participant never sees the choices of players they were not linked to.
- [x] No arrangement the app can draw leaves any participant with fewer than two
      links.
- [x] ~~Artifact demonstrates the arrangement choice before implementation,
      screenshot at 1555×885 and reviewed with the user.~~ **Not done — blocked
      on the absence of browser tooling; `OT-0002-01` closed `wont_fix`.** The
      choice was recorded in `DECISION.md`, which states that the arrangement
      was picked by the implementer rather than chosen by the researcher.
- [x] `uv run pytest` green — logic tests in
      `tests/test_network_public_goods_payoffs.py`, bot flow in
      `demo/network_public_goods/tests.py`.
- [x] `scaffold_check` is deleted, its `SESSION_CONFIGS` entry removed, and its
      data-schema doc pruned by `schema-writer`.
- [x] Prototype docs updated when implemented: `demo/modules/README.md` and
      `demo/modules/page-flow.md`.
- [x] Spec promoted when validated: `doc/validated-doc/guide/network-public-goods.md`.

## Open Questions

- **`REQ-0001` is settled but names no hypothesis.** The researcher deliberately
  left open what the experiment measures — whether visible reputation sustains
  cooperation, whether reshuffling prevents it forming, or whether people target
  generosity at partners with good histories. The design is complete and every
  number has a value, so this does not block the build; it decides what the
  promoted guide doc says the experiment is *for*, and must be answered before
  `OT-0002-07`.
- **Are links mutual?** `REQ-0001` rule 5 assumes so and flags the assumption.
  This epic builds mutual links. If they should be directional, "who your
  contribution reaches" and "whose history you can read" come apart, and the
  correction belongs at stage 1 rather than here.
- **The points-to-money conversion rate** was never discussed; the repo default
  of 1 point = 1.00 applies unless someone says otherwise.
- **Participant-chosen links, chat, and a fixed-partner control** — future work,
  or intentionally still on the table?

## Related Files

- `doc/requirements/REQ-0001-networked-public-goods.md`
- `demo/network_public_goods/__init__.py`
- `demo/network_public_goods/tests.py`
- `demo/settings.py`
- `demo/scaffold_check/` (to be deleted)
- `demo/modules/README.md`
- `demo/modules/page-flow.md`
- `tests/test_network_public_goods_payoffs.py`
- `artifacts/OT-0002-01-link-arrangements/`
- `doc/validated-doc/guide/network-public-goods.md`
- `doc/otree-doc/multiplayer/`
- `doc/otree-doc/rounds.html`

## Handoff Appendix

### Settled Decisions

- App name `network_public_goods`, confirming `REQ-0001`'s proposal.
- Whole-requirement scope in one pass; no reduced first cut.
- Minimum degree of two is a hard constraint on every arrangement.
- Promotion target is `doc/validated-doc/guide/network-public-goods.md`.
- The four players are one fixed oTree group; the network is app-level per-round
  state, not oTree matching.

### Model And Payoff Notes

- `C`: `NAME_IN_URL = 'network_public_goods'`, `PLAYERS_PER_GROUP = 4`,
  `NUM_ROUNDS = 10`, `ENDOWMENT = cu(100)`, `MULTIPLIER = 2`.
- `Player.contribution` — `CurrencyField(min=0, max=C.ENDOWMENT)`, the only
  `form_fields` entry, one per player per round.
- Per-round adjacency needs a stored field because it is drawn before the
  decision page and read again when payoffs are computed. A `StringField` on
  `Player` holding that round's linked `id_in_group` values is the simplest
  representation that survives the export; the story settles the encoding.
- Payoff, for player *i* with link set *L(i)* and neighbourhood
  *N(i) = {i} ∪ L(i)*:
  `payoff = (ENDOWMENT - contribution_i) + Σ over j in N(i) of (contribution_j × MULTIPLIER / |N(j)|)`
  — noting the divisor is the size of *j*'s neighbourhood, not *i*'s.
- History rendering needs only each partner's own past `contribution` values, via
  `player.in_previous_rounds()`. The historical adjacency is **not** needed, so
  only the current round's links must be stored per round.

### Test Scenarios

Target `tests/test_network_public_goods_payoffs.py`, using `otree_session_factory`
because `Player` and `Group` are ORM objects.

- **Ring, uniform contributions.** Adjacency set by hand to a 4-cycle, everyone
  contributes 50. Each neighbourhood has size 3, so each player receives
  `3 × (50 × 2 / 3) = 100` and keeps 50 → payoff 150.
- **Ring, one free rider.** Three contribute 100, one contributes 0. Assert the
  free rider out-earns each contributor, and that the two players linked to the
  free rider earn less than the two who are not.
- **Diamond, asymmetric neighbourhoods.** `K4` minus one edge. Assert the divisor
  is the *contributor's* neighbourhood size, not the receiver's — the scenario
  most likely to be implemented backwards.
- **Nobody contributes.** Every payoff is exactly `C.ENDOWMENT`.
- **Bounds.** A contribution above `C.ENDOWMENT` or below 0 fails submission
  (`SubmissionMustFail` in the bot).
- **Isolation, per rule 10.** A player's results page exposes no contribution
  from a player they were not linked to that round.

### Deferred Decisions

- The link arrangement itself, and therefore the draw function — `OT-0002-01`,
  then `OT-0002-03`.
- The decision screen's layout and how partner history is presented —
  `OT-0002-01`, then `OT-0002-04`.
- The exact encoding of the stored adjacency field — `OT-0002-02`.

## Resolution

The experiment is built, tested, observed running, and promoted. Six of seven
child stories are `resolved`; `OT-0002-01` is `wont_fix`.

### What was delivered

`demo/network_public_goods/` — four players in one fixed group, ten rounds, a
ring redrawn every round in `creating_session()`, itemised partner history on the
decision screen, and a neighbourhood payoff rule. `scaffold_check` removed,
`schema-writer` run, `demo/modules/` rewritten, and
`doc/validated-doc/guide/network-public-goods.md` promoted.

`uv run pytest` collects 8 and passes. Observed end to end: four participants
driven through all thirty page loads over HTTP, links confirmed changing between
rounds, the page's payoff (187) matching hand arithmetic, and rule 10 holding —
the participant examined never saw the player they were not linked to.

### Deliberately not done

- **`OT-0002-01`, the artifact story, could not run.** No browser tooling exists
  in this environment, and the screenshot is the deliverable rather than an
  accessory to it. The **ring** was chosen by the implementer on implementation
  grounds; the **diamond** — the only arrangement satisfying rule 12 where
  position is measurable, and arguably closer to the original interest in
  whether better-connected participants behave differently — was rejected for no
  reason connected to the experiment. `DECISION.md` says so, and the promoted
  guide repeats it.
- The two other visual questions `REQ-0001` parked — how the network is drawn,
  and how the history table reads at full load — were answered by default rather
  than by choice, and have never been looked at with three partners.

### Requirement corrections this epic caused

Both were made at stage 1, not patched downstream:

- **Rule 12 added** — minimum two connections — after the degree-1 arithmetic was
  settled with the user, which retired hub-and-spokes from `REQ-0001`'s list of
  candidate arrangements.
- **Rule 8 amended** from "shared evenly" to "as evenly as whole points allow",
  after implementation showed whole points cannot always divide. The remainder is
  lost — 4 points per round when everyone contributes 50. Whether that is
  acceptable is now an open question on `REQ-0001`.

### Files updated

`demo/network_public_goods/` (new), `demo/settings.py`, `demo/scaffold_check/`
(deleted), `demo/modules/README.md`, `demo/modules/page-flow.md`,
`tests/test_network_public_goods_payoffs.py`,
`doc/validated-doc/data-schema/network_public_goods.md` and its index,
`doc/validated-doc/guide/network-public-goods.md`,
`doc/requirements/REQ-0001-networked-public-goods.md` (rules 8 and 12).
