---
id: OT-0001-06
title: Stage 5 — promote the validated experiment to the researcher-facing guide
type: story
status: resolved
priority: high
created: 2026-08-15
resolved: 2026-08-15
area: docs
tags:
  - workflow
  - validation
  - stage-5
parent: OT-0001
---

# Stage 5 — promote the validated experiment to the researcher-facing guide

## Description

Run stage 5 by promoting the validated prototype into
`doc/validated-doc/guide/`, and measure whether the promoted doc is genuinely
researcher-facing or whether implementation detail leaks through.

## Details

- **The promotion gate is met.** `REQ-0001` is settled, `uv run pytest` is
  green, and the app has been observed running end to end — the three conditions
  `CLAUDE.md` names.
- **Filename**, deferred by the epic to this story:
  `doc/validated-doc/guide/network-public-goods.md`, matching the app and the
  target `OT-0002` already carries.
- **The test to apply**, per `CLAUDE.md#two-doc-homes`: read the promoted doc as
  someone who has never opened the code. If it only makes sense with the source
  open, the wrong thing was promoted.
- **Promote the deliberate, not the incidental.** The rounding behaviour and the
  minimum-two-connections constraint are requirements the experiment must meet,
  so they belong. The `links` encoding and the payoff function's signature are
  implementation, so they do not.
- **No artifact, no code, no tests.**
- **Out of scope.** The second pass (`OT-0001-07`) and the fix ticket
  (`OT-0001-08`).

## Acceptance Criteria

- [x] `doc/validated-doc/guide/network-public-goods.md` exists and describes the
      experiment at the design level.
- [x] No class name, field name, function name, or `demo/` file path appears in
      it.
- [x] The design consequences a researcher must know — the single-connection
      problem and the rounding losses — are stated in participant terms.
- [x] The provisional status of the ring is stated plainly, including that the
      researcher did not choose it.
- [x] Every unsettled decision is listed rather than papered over.
- [x] `doc/issues/promotion-debt.md` is empty.
- [x] Friction log entry appended covering whether implementation detail leaked
      and what stage 5 inherited from the blocked artifact stage.

## Open Questions

- Does "validated" mean "ready to run"? The promoted guide meets every gate
  `CLAUDE.md` names while carrying five open decisions, two of which go to the
  heart of what the experiment is. Recorded as F-41 for the fix ticket.

## Related Files

- `doc/validated-doc/guide/network-public-goods.md`
- `doc/validated-doc/data-schema/network_public_goods.md`
- `doc/requirements/REQ-0001-networked-public-goods.md`
- `doc/workflow-validation/OT-0001-friction-log.md`

## Resolution

Promoted to `doc/validated-doc/guide/network-public-goods.md`.

### Did implementation detail leak? No

The guide names no class, field, function, or source file. The rule in
`CLAUDE.md#two-doc-homes` was easy to apply, and its own test — read it as
someone who has never opened the code — passes. What survived promotion is the
design and its consequences; what stayed in `demo/modules/` is everything that
only means something with the source open.

### What stage 5 was forced to admit

Two paragraphs exist only because earlier stages recorded their failures
honestly:

- The **ring is provisional and the researcher did not choose it**, with the
  diamond named as the live alternative and the reason it might be better. Had
  `DECISION.md` been terser, stage 5 would have promoted "the network is a ring"
  as settled design, and the fact that nobody chose it would have been lost at
  exactly the moment the document becomes authoritative.
- The **open-decisions table**, five rows including the missing hypothesis.

### The finding this story produced

`CLAUDE.md` does not distinguish **validated** from **ready to run**. Every gate
it names is met, and the honest promoted document still tells the researcher
their experiment is not ready. Promoting it anyway was a judgment call; withholding
promotion would have been equally defensible. F-41.
