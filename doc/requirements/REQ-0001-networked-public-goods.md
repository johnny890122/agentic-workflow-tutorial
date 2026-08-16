---
id: REQ-0001
title: Public goods with reshuffled links and visible partner history
status: settled
created: 2026-08-15
settled: 2026-08-15
tickets:
  - OT-0002
  - OT-0003
---

# Public goods with reshuffled links and visible partner history

## What we are trying to learn

Four people play a public goods game together ten times. Every round they are
re-linked at random, so who your contribution reaches keeps changing — and
before deciding, you can look up exactly what each of your current partners has
put in during every earlier round. The interest is in what people do with that
history when the relationship itself is temporary.

The specific behaviour to be measured is **not yet decided** — see
[Open questions](#open-questions). The design is settled; the hypothesis it
serves is not.

## What the participant does

- **Screen 1 — the links for this round.** They are shown who they are linked to
  this round, and for each of those partners, what that partner contributed in
  every completed round so far — with each past round marked according to
  whether the two of them were linked at the time. They choose how much of their
  100 points to put in, and submit.
- **Screen 2 — waiting.** They wait until all four have chosen.
- **Screen 3 — what happened.** They see what each of their linked partners put
  in this round, and what they themselves earned. They see nothing about the
  choices of players they were not linked to. They continue to the next round.

Rounds 2 through 10 repeat the same three screens, with the links redrawn.

## Rules the experiment must follow

1. All four participants take part in all ten rounds. Nobody sits out a round.
2. Every participant starts every round with 100 points, regardless of what they
   earned previously.
3. A contribution is at least 0 and at most 100 points.
4. Links are redrawn at random at the start of every round. The previous round's
   links place no constraint on the new ones.
5. Links are mutual: if A is linked to B this round, B is linked to A. *(Assumed
   from "connected", not stated in the interview — see
   [Open questions](#open-questions).)*
6. A participant sees this round's links **before** choosing an amount.
7. For each partner they are linked to this round, a participant can see that
   partner's contribution in every completed round — itemised round by round,
   not summarised, and including rounds in which that partner was linked to
   somebody else. Each of those past rounds is marked according to whether the
   viewer was linked to that partner at the time. *(Amended 2026-08-15. The
   marking was added after watching the experiment run: the history said "player
   1 gave 100 in round 3" without saying whether any of it reached you, so
   reciprocity and general generosity were indistinguishable — the thing the
   design exists to observe. Rule 10 still holds: the marking says only whether
   it was **you**, never who else was linked.)*
8. A contribution is doubled, then shared as evenly as whole points allow among
   the contributor and the people they are linked to that round. *(Amended
   2026-08-15: this originally said "shared evenly". Points are whole numbers,
   so an amount that does not divide by the neighbourhood size is rounded down
   per recipient and the remainder is lost — 50 into a neighbourhood of three
   pays three shares of 33, not 33.33. Discovered when the rule was built. See
   [Open questions](#open-questions).)*
9. Points not contributed stay with the contributor.
10. After the round resolves, a participant sees each of their current partners'
    contributions for that round and their own earnings for that round — and
    nothing about the choices of players they were not linked to.
11. Participants are told before round 1 that there are ten rounds.
12. No participant ever holds fewer than two links. *(Decided 2026-08-15, once
    the arithmetic below showed that a single link makes contributing free. This
    was previously left open for the artifact stage to resolve — see
    [Visual questions](#visual-questions-for-the-artifact-stage).)*

### How earnings work — worked example

Say this round A is linked to B and C, and B is also linked to D.

- A contributes 30, keeping 70. That 30 is doubled to 60 and split evenly across
  A, B and C — 20 each.
- B contributes 60, keeping 40. That 120 is split across B, A and D — 40 each.
- A therefore earns 70 kept + 20 from their own contribution + 40 from B, plus
  whatever share C sends them.

Note what rule 8 implies: the share you get back from your **own** contribution
is `contribution × 2 ÷ (1 + number of links you have)`. With two or more links
you lose money by contributing and the usual public-goods tension holds. With
exactly **one** link, you get your entire contribution back and giving becomes
free — the dilemma disappears for that person. **Rule 12 rules this out**: no
arrangement may ever leave anyone with a single link.

## Numbers and defaults

| Thing | Value | Settled? |
| --- | --- | --- |
| Participants per group | 4 | yes |
| Rounds | 10, announced in advance | yes |
| Budget per round | 100 points, refreshed each round | yes |
| Contribution range | 0–100 points | yes |
| Multiplier on a contribution | 2 | yes |
| Who shares a contribution | the contributor plus their current links | yes |
| History shown per partner | every completed round, itemised, each marked linked-to-you or not | yes |
| Minimum links per person | 2 — never fewer, per rule 12 | yes |
| How many links each person has | **open** above that floor — depends on the arrangement chosen at the artifact stage | no |
| Which link arrangements are drawn from | **open** — artifact stage decides | no |
| Points-to-money conversion rate | not discussed; repo default is 1 point = 1.00 | provisional — confirm before build |

## What we are not building

- **Punishment.** No mechanism for paying to reduce a stingy partner's earnings.
  Explicitly excluded by the researcher: it is the obvious follow-up study and a
  large amount of additional work, and it would confound the reputation signal
  this design is built to expose.

Three other nearby features were offered for exclusion and **not** excluded:
letting participants choose their own links, chat between participants, and a
fixed-partner control treatment to compare the reshuffling against. None was
asked for either, so none is being built — but they were not ruled out. See
[Open questions](#open-questions).

## Visual questions for the artifact stage

- **Which link arrangements should the random draw come from?** The researcher
  explicitly asked to see the options rather than decide from a description.
  Concrete alternatives to build and compare: a **ring**, where everyone has
  exactly two links and nobody is structurally advantaged; a **diamond** —
  everyone connected to everyone except for one missing connection — where two
  people have three links and two have two, so position becomes measurable; and
  a **mixed draw** over every arrangement rule 12 permits, so how connected you
  are varies from round to round. The variants must differ on **the arrangement
  itself**, not on how one arrangement is drawn.

  *Revised 2026-08-15.* This question originally offered **hub-and-spokes** as
  its third alternative, and left the single-link problem for the artifact stage
  to "avoid or deliberately accept". Asked to decide, the researcher ruled it
  out outright — now rule 12. Hub-and-spokes cannot satisfy that rule, since it
  leaves three of the four people with exactly one link, so the diamond replaces
  it as the unequal-positions option. The question itself is unchanged: which
  arrangement, chosen by looking.
- **How is the network shown on the decision screen**, so a participant can tell
  at a glance who they are linked to this round?
- **How does a partner's itemised history sit alongside it?** By round 10 a
  participant may be looking at three partners with nine rounds of history each.
  Whether that reads as a table, per-partner strips, or something revealed on
  demand is a question that has to be looked at.

**Stage 3 is required on both of `CLAUDE.md`'s triggers**: the arrangement is a
choice the researcher must make by looking, and a per-round link structure
within a fixed group has no precedent anywhere in this repo.

## Open questions

- **What behaviour is this measuring?** Deliberately left open by the
  researcher. Three candidates were on the table: whether visible reputation
  sustains cooperation despite temporary partners; whether constant reshuffling
  prevents cooperation forming at all; and whether people target generosity at
  partners with good histories. The design supports all three, but the answer
  decides what the analysis and any later treatment structure look like.
- **Are links mutual?** Rule 5 assumes so. It follows naturally from the word
  "connected" but was never stated. If links were one-directional, "who your
  contribution reaches" and "whose history you can read" would come apart.
- **Choosing your own links, chat, and a fixed-partner control** were offered as
  exclusions and not taken. Are these future work, or intentionally still on the
  table for this build?
- **The points-to-money conversion rate** was never discussed.
- **Is losing the rounding remainder acceptable?** Rule 8 cannot split whole
  points evenly when the amount does not divide. As built, each recipient's
  share rounds down and the difference simply disappears — with everyone
  contributing 50 into neighbourhoods of three, the group loses 4 points a
  round, 40 over the session. The alternatives are to allow fractional points,
  to choose numbers that always divide, or to accept the loss. Nobody has been
  asked.

## Translation notes

Written in oTree terms for stage 2. Nothing here adds behaviour the researcher
did not agree to.

- **App:** new. Proposed name `network_public_goods` — **stage 2 confirms or
  overrides this**; the researcher was never asked to name an identifier.
- **Round structure:** `C.NUM_ROUNDS = 10`, `C.PLAYERS_PER_GROUP = 4`,
  `C.ENDOWMENT = cu(100)`, `C.MULTIPLIER = 2`.
- **Grouping is not oTree matching.** All four are one oTree group for the whole
  session, unchanged across rounds. The "network" is per-round state *inside*
  that group, so this is not a `group_by_arrival_time` or shuffling problem —
  `Subsession.group_randomly()` would re-matter the wrong thing. The per-round
  adjacency has to be drawn and stored by the app itself, in a new field, and it
  must persist per round because rule 7 requires reading it back historically.
- **Screens → pages:** Screen 1 → a `Decide` page carrying the contribution
  form; Screen 2 → a `WaitPage` whose `after_all_players_arrive` computes the
  round's payoffs; Screen 3 → a `RoundResults` page. `page_sequence` is
  `[Decide, ResultsWaitPage, RoundResults]`, repeated by `C.NUM_ROUNDS`.
- **Data the participant enters:** `Player.contribution`, `CurrencyField`,
  `min=0`, `max=C.ENDOWMENT`, one per player per round — the only `form_fields`
  entry.
- **Data the experiment computes:** the round's adjacency (drawn at the start of
  the round, before `Decide` renders, since rule 6 requires it to be visible);
  and `Player.payoff` = kept points + the contributor's own share + the sum of
  shares received from each linked partner, per rule 8. Written by a
  `set_payoffs`-style function called from `after_all_players_arrive`.
- **History across rounds** is read with `player.in_previous_rounds()` /
  `in_all_rounds()`, filtered to the partners linked *this* round. Rule 7 means
  the historical adjacency is not needed to render history — only the partner's
  own past `contribution` values are — which keeps the storage requirement to
  "this round's links", per round.
- **Existing behaviour this touches or conflicts with:** **none.** `demo/` holds
  only `demo/scaffold_check/`, which is disposable scaffolding with no fields, no
  form, and no payoff rule (see
  `doc/validated-doc/data-schema/scaffold_check.md`). It is not prior art and
  supplies no pattern. There is no promoted spec in `doc/validated-doc/guide/`
  to conflict with, and no other requirement exists.
