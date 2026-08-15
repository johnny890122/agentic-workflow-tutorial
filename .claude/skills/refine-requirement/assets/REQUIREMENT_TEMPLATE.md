---
id: REQ-XXXX
title: Short requirement title
status: draft
created: YYYY-MM-DD
settled:
tickets:
---

# Short requirement title

## What we are trying to learn

Two or three sentences, in the user's own terms: the behavior this experiment is
meant to observe, and why it matters. No oTree vocabulary here.

## What the participant does

Screen by screen, in plain language. One bullet per screen, in order.

- Screen 1 — what they are shown, what they do, what happens when they submit.
- Screen 2 — ...

## Rules the experiment must follow

Numbered, checkable statements. Someone watching a single run must be able to
say whether each rule held.

1. Every participant starts each round with the same budget.
2. A participant can never send more than they hold.

## Numbers and defaults

| Thing | Value | Settled? |
| --- | --- | --- |
| Participants per group | 3 | yes |
| Rounds | 10 | yes |
| Starting budget | 100 points | provisional — confirm before build |

## What we are not building

- The tempting nearby feature that is explicitly out of scope, and why.

## Visual questions for the artifact stage

Things the user cannot decide from a description and needs to see first. Each
becomes a set of variants under `artifacts/`; none is decided here. When there
are none, say so — that is what lets the ticket skip the artifact stage.

- How the deduction control should look — one row per player, or a single total?

<!-- or: _None — nothing here is decided by looking._ -->

## Open questions

- What still needs a human answer before a ticket can be written?

## Translation notes

The bridge to stage 2. Written by the agent, in oTree terms, from everything
above — never introducing behavior the user did not agree to.

- **App:** new / existing `demo/<app>/`
- **Round structure:** `C.NUM_ROUNDS`, `C.PLAYERS_PER_GROUP`
- **Screens → pages:** which page each screen becomes, and the wait pages between
- **Data the participant enters:** the fields, their types and bounds
- **Data the experiment computes:** payoff arithmetic and who writes it
- **Existing behavior this touches or conflicts with**
