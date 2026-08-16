---
id: OT-0001-05
title: Stage 4 — build the app, get tests green, and watch schema-writer fire
type: story
status: resolved
priority: high
created: 2026-08-15
resolved: 2026-08-15
area: docs
tags:
  - workflow
  - validation
  - stage-4
parent: OT-0001
---

# Stage 4 — build the app, get tests green, and watch schema-writer fire

## Description

Run stage 4 by implementing `OT-0002` in `demo/`, and measure whether
`schema-writer` fires automatically as `CLAUDE.md` requires, whether
`demo/modules/` ends up useful to a fresh agent, and whether the removal of
`scaffold_check` gets pruned from the data-schema docs unprompted.

## Details

- **Input.** `OT-0002` and its stories, against `REQ-0001`.
- **The clean pruning test.** Stage 0 could not provide one: the operator named
  the deleted app when invoking `schema-writer`. This story deletes
  `scaffold_check` and must invoke the skill **without mentioning the removal**.
- **The promotion gate.** `CLAUDE.md` requires behaviour "seen working, not
  merely tested". With no browser tooling, record what was actually done in its
  place and whether it satisfies the gate.
- **No artifact.** Stage 3 already ran, and was blocked — `OT-0001-04`.
- **Out of scope.** Promotion to `doc/validated-doc/guide/`, which is
  `OT-0001-06`.

## Acceptance Criteria

- [x] `demo/network_public_goods/` implements `REQ-0001`: ten rounds, four
      players, links redrawn each round, itemised partner history before the
      contribution is entered.
- [x] `uv run pytest` green — both layers.
- [x] `schema-writer` fired without being asked, per `CLAUDE.md`, and
      `doc/validated-doc/data-schema/` was not hand-edited.
- [x] Whether `schema-writer` prunes an orphaned doc unprompted is recorded,
      from a neutral invocation.
- [x] `scaffold_check` is deleted and no longer referenced anywhere.
- [x] `demo/modules/README.md` and `page-flow.md` record the implementation
      detail a later agent needs.
- [x] The app was observed running, and what "observed" meant is stated exactly.
- [x] Friction log entry appended covering the automatic trigger, the pruning
      test, the doc split, and anything the requirement could not have foreseen.

## Open Questions

- None. The rounding question raised during implementation belongs to `REQ-0001`
  and `OT-0002`, not here.

## Related Files

- `demo/network_public_goods/`
- `tests/test_network_public_goods_payoffs.py`
- `demo/modules/README.md`
- `demo/modules/page-flow.md`
- `doc/validated-doc/data-schema/network_public_goods.md`
- `doc/workflow-validation/OT-0001-friction-log.md`

## Resolution

Stage 4 ran cleanly and needed the least interpretation of any stage so far.

### What was built

`demo/network_public_goods/` — five constants, `Player.contribution`,
`Player.links`, a ring drawn per round in `creating_session()`, a neighbourhood
payoff rule, and three pages. `scaffold_check` deleted, `SESSION_CONFIGS`
repointed, `demo/modules/` rewritten, `schema-writer` run.

`uv run pytest` collects 8 and passes: seven payoff cases plus the parametrized
bot run over all ten rounds.

### What "observed working" meant

No browser exists here, so: a session was created through the running server's
REST API, four participant sessions were driven through all thirty page loads
over HTTP, and the rendered HTML was inspected at rounds 1 and 10. Links were
confirmed to change between rounds. The payoff on the page (187) matched hand
arithmetic. Rule 10 held in observation — the participant examined saw two of
the other three players and never the third.

Stronger evidence of *correctness* than a screenshot; weaker evidence of whether
the screen is good to look at, which is what the gate is probably about. Logged
as F-37.

### The pruning test, run clean

`schema-writer` was invoked as *"demo/ has changed — refresh the data-schema
docs"*, with no hint that an app had been deleted. **It does not prune.** The
procedure enumerates apps and updates the index, but never addresses a doc whose
app has disappeared; removing `scaffold_check.md` was inferred from "one doc per
package in `demo/`". F-05 confirmed, cleanly this time.

### Two things the requirement could not have foreseen

- **Rounding (F-35).** Rule 8's "shared evenly" is impossible with whole points.
  Pinned by a test, documented, and — for consistency with how the stage-2
  divergence was handled — corrected at stage 1, with the real question left open
  for the researcher.
- **The devserver's in-memory database (F-38).** A session created externally is
  invisible to the running server. Cost real time; documented nowhere.

### Deviation worth recording

**The code was written before four of its tickets existed** (F-36). `OT-0002`
correctly deferred stories 03–06 until the arrangement was settled; once it was,
the app was built in one pass and those stories were written afterwards as
records rather than specifications. The tickets are accurate, and the
whole-scope-in-one-pass decision made a single build reasonable — but nothing in
the workflow noticed, and a reader of the ticket store cannot tell which stories
drove work and which described it.
