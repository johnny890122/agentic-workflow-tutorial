# Link arrangement — decision

**Ticket:** `OT-0002-01` · **Requirement:** `REQ-0001` · **Date:** 2026-08-15

## Outcome: ring, chosen by the operator — not by the researcher

**No variants were built and nobody chose by looking.** This file records a
decision the artifact stage was supposed to make and did not.

## Why the stage did not run

`CLAUDE.md#visual-variants` requires each variant screenshotted at 1555×885 into
`shots/` and presented to the user to choose from. No browser tooling exists in
this agent environment — no screenshot capability, no page driver. Offered the
choice between building the variants for local viewing, choosing from written
descriptions, or skipping the stage, the user chose to **skip it and log it as
blocked**.

See `doc/workflow-validation/OT-0001-friction-log.md`, entries F-07 and F-29.

## What was chosen instead, and on what basis

The **ring**: a 4-cycle, every participant linked to exactly two others, every
neighbourhood of size 3.

Picked on implementation grounds, which is exactly the wrong basis for a
question `REQ-0001` says belongs to the researcher:

- It satisfies rule 12 (minimum two links) unconditionally, where the diamond
  satisfies it and the mixed draw satisfies it only if the draw is constrained.
- It is symmetric, so every neighbourhood is the same size and the payoff
  divisor is uniform — the simplest thing to implement and to assert against.
- `OT-0002-02`'s first two test scenarios are already written against a ring.

## What was rejected, and what is therefore unknown

- **Diamond** (`K4` minus one edge; degrees 3, 3, 2, 2). The only surviving
  option where position is measurable — which, given the researcher's original
  interest in whether some participants are better connected than others, may
  well have been the right answer. Rejected here for no reason connected to the
  experiment.
- **Mixed draw** over every arrangement rule 12 permits. Rejected likewise.

Because nothing was seen, nothing was learned about the two questions
`REQ-0001` also parked here: how the network should be drawn on the decision
screen, and how nine rounds of itemised history for three partners fit alongside
it. Stage 4 answers both by default rather than by choice.

## What the real implementation must keep

- Minimum degree two, always — rule 12.
- Links mutual, drawn before the decision page renders, redrawn every round.
- Nothing visible about a player the viewer is not linked to.

## Status

**This decision is provisional and should be revisited.** It is the one place in
the run where a researcher-owned choice was made by an implementer for
convenience. If browser tooling becomes available, `OT-0002-01` should be
reopened and the three arrangements built and compared properly.
