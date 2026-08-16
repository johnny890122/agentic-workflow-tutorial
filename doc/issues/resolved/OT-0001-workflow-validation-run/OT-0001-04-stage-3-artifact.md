---
id: OT-0001-04
title: Stage 3 — run the artifact stage on the link-arrangement question
type: story
status: resolved
priority: high
created: 2026-08-15
resolved: 2026-08-15
area: docs
tags:
  - workflow
  - validation
  - stage-3
parent: OT-0001
---

# Stage 3 — run the artifact stage on the link-arrangement question

## Description

Run stage 3 against the visual question `REQ-0001` parked and `OT-0002-01`
carried: which link arrangement the random draw should come from. Measure
whether the variants differ on the actual question, per
`CLAUDE.md#visual-variants`, or on three shades of one layout.

## Details

- **Input.** `OT-0002-01`, which names three arrangements to build — ring,
  diamond, and a mixed draw — and the constraints every variant must respect.
- **What stage 3 is supposed to produce.** Two or three self-contained `.html`
  files under `artifacts/OT-0002-01-link-arrangements/`, screenshots at
  1555×885 in `shots/`, and `DECISION.md` recording the choice.
- **The epic requires stage 3 to fire at least once.** It is the only stage
  whose triggers were both plausibly present from the start, and `REQ-0001`
  confirmed both.

### What actually happened

The stage was **blocked on tooling and skipped by the user's decision**. No
browser exists in this agent environment, so the screenshot step — which is the
deliverable, not an accessory to it — could not be performed. See the Resolution.

- **No code, no tests.** Nothing under `demo/` or `tests/` changes.
- **Out of scope.** Implementing the chosen arrangement; that is `OT-0002-03`
  and `OT-0002-04`.

## Acceptance Criteria

- [x] ~~Variants exist under `artifacts/OT-0002-01-link-arrangements/`, differ on
      the arrangement, and are screenshot at 1555×885.~~ **Not done — blocked on
      the absence of browser tooling.**
- [x] ~~The user chose by looking.~~ **Not done.** The operator chose on
      implementation grounds, which `REQ-0001` explicitly assigns to the
      researcher.
- [x] `artifacts/OT-0002-01-link-arrangements/DECISION.md` exists and records the
      outcome, the reasoning, what was rejected, and that nobody chose by
      looking.
- [x] `OT-0002-01` is closed with its acceptance criteria rewritten rather than
      silently ticked, and its Resolution states the blockage.
- [x] The epic's acceptance criterion "no stage was skipped without the ticket
      that skipped it saying so in one line with a reason" is satisfied — both
      `OT-0002-01` and `DECISION.md` say so at length.
- [x] Friction log entry appended covering why the stage could not run, what was
      chosen instead, and what is now unknown as a result.

## Open Questions

- Should `OT-0002-01` be reopened if browser tooling becomes available? The
  arrangement is the one researcher-owned decision in this run that an
  implementer made for convenience, and the diamond may well have been the right
  answer.
- Does the ticket store need a `blocked` status? `wont_fix` overstates
  finality and `pending` would stall the epic. Story `OT-0001-08` should decide
  whether this belongs in the fix ticket.

## Related Files

- `artifacts/OT-0002-01-link-arrangements/DECISION.md`
- `doc/issues/wont_fix/OT-0002-networked-public-goods/OT-0002-01-link-arrangement-variants.md`
- `doc/requirements/REQ-0001-networked-public-goods.md`
- `doc/workflow-validation/OT-0001-friction-log.md`

## Resolution

Stage 3 **did not run**. It is the only stage in this validation pass that
produced no artifact of the kind `CLAUDE.md` describes, and the run's verdict
must say so.

### Why

`CLAUDE.md#visual-variants` makes the screenshot the deliverable: variants are
"screenshot each at the standard viewport into `shots/`" and "presented together"
for the user to choose from. The environment has no browser — no screenshot
capability and no page driver. `CLAUDE.md#visual-qa` says only "use the browser
tooling available in the current agent environment", which assumes some exists.

The user was offered three routes: build the variants for local viewing, choose
from written descriptions, or skip and log. They chose to skip and log.

### What was decided instead

The **ring**, chosen by the operator on implementation grounds — it satisfies
`REQ-0001` rule 12 unconditionally, keeps every neighbourhood the same size, and
matches the test scenarios `OT-0002-02` already carries. Recorded in
`artifacts/OT-0002-01-link-arrangements/DECISION.md`, flagged as provisional.

### What is now unknown

- Whether the **diamond** was the better design. It is the only surviving
  arrangement where position is measurable — which is close to what the
  researcher asked about when they said some participants might be better
  connected than others.
- How the network should be **drawn** on the decision screen.
- How nine rounds of itemised history for three partners **fit** on one screen.
  Stage 4 will answer this blind, at full load, having never seen it.

The last is the most likely to cause trouble: it is a real layout problem that
the artifact stage existed to catch early.

### Deliberately not done

- No variants were built. Building them without being able to screenshot or
  present them would have produced artifacts nobody looked at, which is worse
  than an honest gap.
- `CLAUDE.md` was not edited, per the epic.
