# Networked public goods

A four-person public goods game in which the connections between participants
are redrawn every round, and each participant can see what their current
partners have contributed in every earlier round.

Validated 2026-08-15 against `REQ-0001`. Ten rounds, four participants, running
and observed end to end.

## What the experiment is for

Participants are re-matched constantly, so no relationship lasts — but
reputation does. Each round you learn who you are connected to, look up what
those people have given in the past, and decide how much of your own budget to
put in knowing that only they will benefit from it.

**The hypothesis is not settled.** The design deliberately supports three
readings, and which one this experiment is run to test has not been decided:

- whether visible reputation sustains cooperation despite temporary partners,
- whether constant re-matching prevents cooperation forming at all,
- whether participants direct generosity at partners with good histories rather
  than contributing uniformly.

This matters for analysis, not for the build. It should be settled before the
experiment is run for real.

## The round

Ten rounds, announced in advance. Every round has the same three steps.

1. **Decide.** You are shown who you are connected to this round, and a table of
   what each of those people contributed in every completed round — with the
   rounds you were connected to them marked, so you can tell which of their past
   contributions actually reached you. You choose how much of your 100 points to
   contribute.
2. **Wait** for the other three.
3. **Results.** You see what each of your connections contributed this round,
   what you kept, and what you earned.

Connections are redrawn at random before every round, and are always mutual.

### Why the history is marked

Added after watching the experiment run. Without the marking, the table said
"this person gave 100 in round 3" and nothing more — and because connections are
redrawn every round, that generosity may have gone entirely to other people. A
participant could not distinguish someone who had repeatedly given *to them* from
someone who was simply generous to everyone.

That distinction is the whole point of the design, and it was invisible on
screen. It is a good example of something no amount of reading the specification
would have caught.

The marking says only whether it was **you**. It never shows who else that person
was connected to, which would leak information about participants you are not
connected to now.

## How earnings work

Your contribution is **doubled**, then split between you and the people you are
connected to that round. Points you do not contribute, you keep. Someone you are
not connected to receives nothing from you and you receive nothing from them.

The tension is the usual one, localised: contributing grows the total but costs
you personally, because you get back only a fraction of what you put in.

### Two consequences worth understanding before running it

**A participant with only one connection contributes for free.** With a
multiplier of two, someone connected to a single other person gets their whole
contribution back — the dilemma disappears for them. The design therefore
guarantees every participant at least two connections, and this constrains which
arrangements are usable at all. A star, with one central person and three
isolated ones, is not.

**Rounding loses points.** Points are whole numbers, so a contribution that does
not divide evenly across a neighbourhood is rounded down and the remainder
disappears. With everyone contributing 50 into groups of three, the four
participants collectively lose 4 points a round — 40 across a session. Whether
that is acceptable, or whether the numbers should be chosen to divide cleanly, is
an open decision.

## The connection structure

Currently a **ring**: everyone connected to exactly two others, every
neighbourhood the same size, nobody structurally advantaged.

**This choice is provisional and was not made by the researcher.** The stage that
exists to show alternatives side by side could not run, and the ring was picked
by the implementer because it is symmetric and simple to verify. The live
alternative is a **diamond** — everyone connected to everyone except for one
missing connection, giving two participants three connections and two
participants two.

That distinction is not cosmetic. Under a ring, position cannot explain any
behavioural difference, because there are no positions. Under a diamond, it can —
which is closer to the original interest in whether better-connected participants
behave differently. Anyone planning to run this study should decide the
arrangement deliberately before collecting data.

## What is not included

- **Punishment.** No way to pay to reduce a stingy partner's earnings. Excluded
  deliberately: it is the obvious follow-up, and it would confound the reputation
  signal this design exists to expose.
- **Choosing your own connections**, chat between participants, and a
  fixed-partner control treatment. None was asked for and none is built, but none
  was ruled out either.

## Open decisions

| Decision | Why it is still open |
| --- | --- |
| What the experiment measures | The design supports three hypotheses; none chosen |
| Ring or diamond | The comparison stage could not run |
| Whether rounding losses are acceptable | Only discovered when the rule was built |
| Points-to-money conversion rate | Never discussed; the default of 1 point = 1.00 applies |
| Are connections mutual? | Assumed from the original description, never confirmed |

## Where the details live

- The requirement and the conversation behind it: `doc/requirements/REQ-0001-networked-public-goods.md`
- What the data contains: [data-schema/network_public_goods.md](../data-schema/network_public_goods.md)
- How it is implemented: `demo/modules/`
- Why the ring was chosen: `artifacts/OT-0002-01-link-arrangements/DECISION.md`
