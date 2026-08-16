---
id: OT-0002-01
title: Link-arrangement variants — decide what the network looks like and how it is drawn
type: story
status: wont_fix
priority: high
created: 2026-08-15
resolved: 2026-08-15
area: templates
requirement: REQ-0001
tags:
  - artifact
  - network
parent: OT-0002
---

# Link-arrangement variants — decide what the network looks like and how it is drawn

## Description

The researcher asked to *see* the possible link arrangements rather than pick one
from a description. Build standalone variants of the decision screen that differ
on the arrangement, screenshot them, and record the choice — nothing downstream
can start until this closes.

## Details

- **Two open questions, one screen.** The variants answer the arrangement
  question, and the winner also settles how the network and the partner history
  are laid out. They are inseparable: the arrangement changes how many partners
  a history panel has to hold.
- **Build under `artifacts/OT-0002-01-link-arrangements/`** — two or three
  self-contained `.html` files, one per variant. No build step, no devserver, no
  oTree, no external assets. Hardcode stand-in data where player values go.
- **Screenshot each at 1555×885 into `shots/`**, present them together, and ask
  the user to choose. Say what each trades away.
- **Record the outcome in `DECISION.md`**: which variant won, why, what was
  rejected, and what the real implementation must keep.

### The variants must differ on the arrangement

Per `CLAUDE.md#visual-variants`, three shades of one layout is not a choice.
Each variant is a different answer to "what shape are the links":

- **Ring.** A 4-cycle. Everyone has exactly two links; every neighbourhood is
  size 3. Perfectly symmetric, so nobody is structurally advantaged and any
  behavioural difference cannot be blamed on position. Redrawing means picking
  which of the three distinct cycles. Trades away: position effects are
  unmeasurable, because there are none.
- **Diamond.** `K4` minus one edge — two players with three links, two with two.
  Position becomes something you can measure. Redrawing means picking which of
  the six edges is missing. Trades away: symmetry, and with it the clean claim
  that everyone faced the same structure.
- **Mixed draw.** Each round draws uniformly from every arrangement with minimum
  degree two — ring, diamond, and complete. Degrees vary round to round, so
  history accumulates across structurally different situations. Trades away:
  interpretability; a round's outcome confounds behaviour with structure.

### Constraints every variant must respect

These are settled and not reopened here:

- **Minimum degree two.** Nobody may ever hold exactly one link — with
  `C.MULTIPLIER = 2` a degree-1 player gets their whole contribution back and the
  dilemma disappears for them. This rules out hub-and-spokes.
- **Links are mutual** (`REQ-0001` rule 5).
- **Links are visible before the contribution is entered** (rule 6), so the
  network is part of the decision screen, not a results screen.
- **Each linked partner's contribution in every completed round is available,
  itemised, not summarised** (rule 7). At round 10 that is up to three partners
  with nine rounds each — the layout has to survive the worst case, so the
  variants must show it at full load, not at round 2.
- **Nothing about non-linked players may appear** (rule 10). A variant that
  draws all four players must make unmistakably clear who is out of reach.
- Four players, 100-point budget, contribution entry from 0 to 100.

### Note on the complete graph

If everyone is linked to everyone, the network does nothing and the design
collapses to an ordinary four-player public goods game. It is a legitimate
member of the mixed draw and a useful sanity check, but it is not a standalone
variant — offering it as one would be offering "no network" as a network design.

- **Nothing here is promoted verbatim.** The winner is rewritten as a real oTree
  page against real fields in `OT-0002-04`. The artifact folder stays as the
  record of why the screen looks the way it does.
- **No code under `demo/`, no tests.** This story writes only under
  `artifacts/`. The `uv run pytest` criterion does not apply.
- **Out of scope.** Implementing the chosen arrangement, the draw function, the
  results screen, and any oTree page work.

## Acceptance Criteria

Every box below is rewritten rather than ticked: the stage was blocked on
tooling, not completed. See `## Resolution`.

- [x] ~~Variants screenshot at 1555×885 and reviewed with the user; choice
      recorded in `DECISION.md`.~~ **Not done — no browser tooling exists in the
      agent environment.** `DECISION.md` was written recording that no variants
      were built and the arrangement was picked by the operator.
- [x] ~~Each variant is a different arrangement.~~ **Not applicable — no
      variants were built.**
- [x] ~~No variant can produce a participant with fewer than two links.~~
      **Carried forward** as `REQ-0001` rule 12, which the chosen ring satisfies
      unconditionally.
- [x] ~~Every variant shows the worst-case history load.~~ **Not applicable.**
      The worst case — three partners, nine rounds — is now an untested
      assumption that stage 4 must handle blind.
- [x] ~~No variant displays anything about a player the viewer is not linked
      to.~~ **Carried forward** as `REQ-0001` rule 10, enforced in `OT-0002-04`.
- [x] `DECISION.md` records the winner, the reasoning, what was rejected, and
      what the real implementation must keep — **including that nobody chose by
      looking**.
- [x] Nothing under `demo/`, `tests/`, or `doc/validated-doc/` changed.

## Open Questions

- If the user picks the mixed draw, does the history display need to show what
  *arrangement* each past round had, or only what each partner contributed?
  `REQ-0001` rule 7 requires only the contributions, but a mixed draw makes past
  contributions harder to interpret without the structure they happened in.

## Related Files

- `artifacts/OT-0002-01-link-arrangements/`
- `artifacts/OT-0002-01-link-arrangements/DECISION.md`
- `artifacts/OT-0002-01-link-arrangements/shots/`
- `doc/requirements/REQ-0001-networked-public-goods.md`

## Resolution

**Closed `wont_fix`: blocked on tooling, not completed.** The work this story
describes remains worth doing.

`CLAUDE.md#visual-variants` requires each variant screenshotted at 1555×885 and
reviewed with the user. No browser tooling exists in this agent environment.
Offered the options — build the variants for local viewing, choose from written
descriptions, or skip and log — the user chose to skip and log it.

The arrangement was therefore picked by the operator on implementation grounds:
the **ring**, because it satisfies rule 12 unconditionally, keeps every
neighbourhood the same size, and matches the test scenarios `OT-0002-02` already
carries. The **diamond** — the only surviving arrangement where position is
measurable, and arguably the closest match to the researcher's original interest
in whether some participants are better connected — was rejected for no reason
connected to the experiment.

Recorded in `artifacts/OT-0002-01-link-arrangements/DECISION.md`, which states
plainly that the decision is provisional and should be revisited if browser
tooling becomes available.

**Two further questions `REQ-0001` parked here were never answered**: how the
network is drawn on the decision screen, and how nine rounds of itemised history
for three partners sit alongside it. `OT-0002-04` now answers both by default
rather than by choice.

**Why `wont_fix` rather than a blocked status:** the generator recognises only
`pending`, `in_progress`, `resolved`, and `wont_fix`. There is no way to express
"needs doing, cannot be done here". `wont_fix` overstates the finality and
`pending` would have blocked the epic indefinitely. Logged as part of F-29.
