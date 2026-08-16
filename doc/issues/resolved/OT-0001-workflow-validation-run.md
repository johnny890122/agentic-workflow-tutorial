---
id: OT-0001
title: Workflow validation run — a new user builds a networked 4-player public goods app
type: epic
status: resolved
priority: high
created: 2026-08-15
resolved: 2026-08-15
area: docs
tags:
  - workflow
  - validation
  - meta
---

# Workflow validation run — a new user builds a networked 4-player public goods app

## Description

The five-stage workflow in `CLAUDE.md` has never been run end to end. This epic
drives one full pass — requirement, ticket, artifact, prototype, validated doc —
using a networked 4-player public goods variant as the vehicle, and records
where the workflow itself is unclear, missing, or wrong.

## Details

- **The app is the vehicle, not the deliverable.** The thing under test is the
  workflow: the five stages in `CLAUDE.md`, the three skills, the ticket
  generator, and the handoffs between them. A run that produces a working app
  while quietly skipping a stage is a **failed** run. A run that produces a
  mediocre app and a precise account of where the workflow broke is a
  **successful** one.
- **The operator plays a new user.** Someone who has read `CLAUDE.md` once and
  is following it literally. Every point where the docs had to be reinterpreted,
  guessed at, or contradicted is a finding, not an inconvenience to work around.

### The seed brief

Stage 1 receives exactly this and nothing more:

> A public goods game variant. Four players. They play in a network setting.

- **Do not pre-settle the game design.** What "network setting" means — who each
  player is connected to, whether the topology is fixed or varies, what a player
  sees about neighbours versus the whole group, how contributions spill across
  connections, how payoff is computed, how many rounds — is **stage 1's job to
  pin down**. Answering it here would let the run skip the stage being tested.
- The only fixed numbers are the two in the brief: a public goods game, four
  players. Everything else is open until `REQ-0001` settles it.
- Because stage 1 is itself under test, this epic carries **no `requirement:`
  frontmatter field**. Producing `REQ-0001` is story `OT-0001-02`; the feature
  tickets stage 2 writes will carry the link.

### Starting state

- `demo/` is **empty** — `settings.py`, `public_goods_simple/`, and
  `_static/` are deleted in the working tree. There is no oTree project on disk.
- `CLAUDE.md` and `doc/validated-doc/data-schema/public_goods_simple.md` both
  still describe that sample app as if it exists. These are handled differently:
  - **`doc/validated-doc/data-schema/public_goods_simple.md` is a legacy orphan
    and gets removed** in story `OT-0001-01`. That directory is owned by
    `schema-writer`, so the removal goes through the skill rather than by hand —
    and whether the skill prunes docs for apps that have disappeared, or has to
    be told, is a finding either way.
  - **`CLAUDE.md`'s own stale text stays put.** Whether the workflow notices its
    own broken references is part of what the run measures, and editing the
    document under test mid-run would invalidate the result. Log it; the fix
    lands via the ticket described under [Fixing the workflow](#fixing-the-workflow).
- `artifacts/`, `doc/requirements/`, and every `doc/issues/` status folder are
  empty. `doc/validated-doc/guide/` is empty.
- Consequence: the workflow assumes an oTree project exists and gives no account
  of how one comes into being. Story `OT-0001-01` covers the gap and is itself a
  finding.

### Stage roadmap

Each story runs one stage, then answers the same two questions: *did the stage
do what `CLAUDE.md` says it does*, and *what did a new user have to guess*.

| Story | Stage | What it runs | Status |
| --- | --- | --- | --- |
| `OT-0001-01` | 0 | Scaffold the empty oTree project so a stage-4 target exists | written |
| `OT-0001-02` | 1 | `refine-requirement` on the seed brief → `REQ-0001` | written |
| `OT-0001-03` | 2 | `ticket-system` against settled `REQ-0001` → feature epic + stories | roadmap |
| `OT-0001-04` | 3 | Visual variants for the network screen → `DECISION.md` | roadmap |
| `OT-0001-05` | 4 | Build the app in `demo/`, tests green, `schema-writer` fires | roadmap |
| `OT-0001-06` | 5 | Promote to `doc/validated-doc/guide/`, clear promotion debt | roadmap |
| `OT-0001-07` | 1→5 again | Second pass: change the requirement, drive the change back through the chain | roadmap |
| `OT-0001-08` | — | Consolidate the friction log, draft the `CLAUDE.md` fix ticket | roadmap |

Stories `03`–`08` stay roadmap bullets until the stage before them lands —
their scope depends on what the previous stage produced, and stubbing them now
would pre-decide the outcomes the run exists to observe.

- **Stage 2 output goes to a separate feature epic** (`OT-0002`), not under this
  one. `OT-0001` is the validation harness; the app's own tickets are ordinary
  work and should look like ordinary work. Mixing them would make the run easier
  than a real one.
- **Stage 3 must fire at least once.** Both triggers in
  `CLAUDE.md#stage-3-is-conditional` are plausibly present — how a network is
  drawn on screen is a question the user must answer by looking, and
  network-structured groups have no precedent in the repo. The **stage-2 ticket
  decides this, not the epic**; if it decides to skip stage 3, that decision and
  its reasoning are a finding, and the run must exercise the artifact stage
  through some other question instead.

### The second pass

One clean run only proves the workflow survives the happy path — a greenfield
feature that visits all five stages in order. The harder question is whether it
survives **a requirement that changes after the app already exists**, which is
what actually happens with researchers.

So after stage 5 closes, story `OT-0001-07` runs a second pass: take the settled
`REQ-0001`, change it the way a real study would change it once someone has seen
the thing running, and drive that change back through the chain.

- The change is chosen **when the app exists**, not now. It should come from
  looking at the working prototype and finding something a researcher would
  genuinely want different — not from a list invented up front.
- Per `CLAUDE.md`, a requirement that turns out to be wrong is **corrected at
  stage 1**, not silently overridden downstream. The pass tests exactly that:
  `refine-requirement` in refine mode on `REQ-0001`, then a new ticket, then
  whatever stages 3–5 the change actually warrants.
- **Which stages it skips is the point.** A changed number may go straight from
  stage 2 to stage 4; a changed screen may need stage 3 again. Whether the
  workflow makes that call cleanly is the measurement.
- It also tests the sync rule: after the change, requirement, ticket, code,
  `demo/modules/`, and `doc/validated-doc/` must all agree, or the divergence
  must be stated plainly. Any drift the pass leaves behind is a finding.

### The friction log

- Lives at `doc/workflow-validation/OT-0001-friction-log.md` — a **permanent
  home**, not `artifacts/`. A record of why the workflow says what it says
  outlives the run that produced it, and disposable storage would throw it away.
- Appended by each story as it runs — **while the confusion is fresh**, not
  reconstructed afterwards.
- One entry per friction point: which stage, what `CLAUDE.md` or the skill said,
  what the operator actually did, and what would have prevented the guess.
- Record successes too. "Stage 4 needed no interpretation" is evidence, and a
  verdict built only from complaints is not a verdict.
- `doc/workflow-validation/` does not exist and is not in the `CLAUDE.md`
  structure tree. Creating it is part of this epic; **documenting** it is one of
  the changes the fix ticket below must carry.

### Fixing the workflow

Nothing this run identifies gets fixed during the run. Editing `CLAUDE.md` or a
skill definition while they are under test would invalidate the result.

Instead, story `OT-0001-08` **drafts a ticket** — a normal `OT-XXXX`, not a
child of this epic — that carries every workflow change the run justifies, each
traced to a friction-log entry. That ticket is then implemented as ordinary
work, on its own schedule, after `OT-0001` closes.

Known already, before the run starts: it must document
`doc/workflow-validation/` and repair the `CLAUDE.md` references to the deleted
`public_goods_simple` sample. The rest is whatever the log turns up.

### Out of scope

- **Applying the workflow fixes.** This epic drafts the ticket that carries
  them; changing `CLAUDE.md` or a skill definition mid-run would invalidate the
  run.
- Restoring `public_goods_simple`, or repairing `CLAUDE.md`'s references to it.
  Removing the orphaned data-schema doc is in scope, and only that.
- A third pass. Two runs — greenfield, then a changed requirement — is the
  scope. If they disagree, say so and stop rather than running a tiebreaker.
- Making the network app good. It needs to be correct, tested, and validated —
  not polished, not generalized, not parameterized beyond what `REQ-0001` asks.
- Deployment, `Procfile`, rooms, and multi-session concerns.

## Acceptance Criteria

- [x] All child stories closed (`resolved` or `wont_fix`).
- [x] All five stages produced their artifact on disk — **with one qualified.**
      `REQ-0001` settled, `OT-0002`/`OT-0003` filed, `demo/network_public_goods/`
      working with notes in `demo/modules/`, and
      `doc/validated-doc/guide/network-public-goods.md` promoted.
      `artifacts/OT-0002-01-link-arrangements/` contains `DECISION.md` **but no
      variants and no `shots/`** — stage 3 was blocked on tooling. The folder
      records a decision the stage did not make.
- [x] No stage was skipped without the ticket that skipped it saying so in one
      line with a reason, per `CLAUDE.md#stage-3-is-conditional`.
- [x] `uv run pytest` green — logic tests in `tests/`, bots in
      `demo/<app>/tests.py`.
- [x] ~~The app has been **seen working** in a browser at 1555×885.~~ **Met in
      substance, not in form.** No browser exists here. Instead: a session
      created through the running server's REST API, four participants driven
      through all thirty page loads over HTTP, rendered HTML inspected at rounds
      1 and 10, links confirmed changing between rounds, and the page's payoff
      (187) matched against hand arithmetic. Stronger evidence of correctness
      than a screenshot; weaker evidence of whether the screen reads well. F-37.
- [x] The **second pass** ran: `REQ-0001` was revised at stage 1 and the change
      reached the code and the validated doc, with requirement, ticket,
      `demo/`, `demo/modules/`, and `doc/validated-doc/` agreeing at the end —
      or the divergence stated plainly.
- [x] `doc/validated-doc/data-schema/public_goods_simple.md` is gone, removed
      through `schema-writer` rather than by hand.
- [x] `doc/issues/promotion-debt.md` is empty at close.
- [x] `uv run python .claude/skills/ticket-system/scripts/generate_issues_index.py`
      exits zero throughout the run.
- [x] Friction log at `doc/workflow-validation/OT-0001-friction-log.md` has an
      entry from every stage and from the second pass, including the stages that
      ran cleanly.
- [x] A `CLAUDE.md` fix ticket is drafted and filed as pending, carrying every
      workflow change the run justifies, each traced to a friction-log entry —
      and at minimum documenting `doc/workflow-validation/` and repairing the
      stale `public_goods_simple` references.
- [x] No `CLAUDE.md` or `.claude/skills/**` file was edited during the run.
- [x] Epic `## Resolution` states a verdict: is the workflow usable as written
      by someone who has read it once?
- [x] Spec promoted when validated: `doc/validated-doc/guide/` — file named by
      story `OT-0001-06`.

## Open Questions

- What the second pass changes about `REQ-0001` — deliberately deferred to
  story `OT-0001-07`, which picks it after seeing the app run. Choosing now
  would mean inventing a researcher's reaction instead of having one.
- Does `doc/workflow-validation/` hold only this run, or is it the standing home
  for meta-work about the workflow? Story `OT-0001-08` should settle it when it
  drafts the fix ticket, since the answer changes what that ticket documents.
- If the two passes disagree — the greenfield run says the workflow is sound and
  the change pass says it is not — which one is the verdict?

## Related Files

- `CLAUDE.md`
- `.claude/skills/refine-requirement/SKILL.md`
- `.claude/skills/ticket-system/SKILL.md`
- `.claude/skills/schema-writer/SKILL.md`
- `.claude/skills/ticket-system/scripts/generate_issues_index.py`
- `doc/requirements/README.md`
- `doc/issues/promotion-debt.md`
- `doc/validated-doc/data-schema/public_goods_simple.md`
- `doc/workflow-validation/OT-0001-friction-log.md`
- `demo/`

## Handoff Appendix

### Settled Decisions

- The run starts from an empty `demo/`; scaffolding is in scope as story `01`.
- `CLAUDE.md`'s stale references to `public_goods_simple` are **observed, not
  repaired**. The orphaned data-schema doc is **removed**, via `schema-writer`.
- The seed brief is deliberately underspecified. Stage 1 pins down the game
  design; nothing upstream of `REQ-0001` may settle it.
- Friction is logged per stage as it happens, not retrospectively, and lives
  permanently at `doc/workflow-validation/OT-0001-friction-log.md`.
- The app's own tickets live under a separate feature epic `OT-0002`.
- Workflow fixes are **drafted as a ticket**, not applied during the run, and
  implemented under that ticket after `OT-0001` closes.
- The run is **two passes**: greenfield, then a changed requirement driven back
  through the chain from stage 1.

### What the run is measuring

Per stage, the question is whether a new user following `CLAUDE.md` literally
lands in the right place. Concretely:

- **Stage 1** — Does `refine-requirement` extract a usable game design from four
  words without inventing rules the user never asked for? Does it correctly park
  the network-display question as a visual question rather than answering it in
  prose?
- **Stage 2** — Can `ticket-system` write executable tickets from `REQ-0001`
  alone? Does the stage-3 conditional give a clear answer, or does the
  implementer arrive unsure?
- **Stage 3** — Do the variants differ on the actual question, per
  `CLAUDE.md#visual-variants`, or on three shades of one layout?
- **Stage 4** — Does `schema-writer` fire automatically, without being asked, as
  `CLAUDE.md` requires? Does `demo/modules/` end up useful to a fresh agent?
- **Stage 5** — Is the promoted doc researcher-facing, or did implementation
  detail leak through? Does the promotion-debt page catch anything?
- **Second pass** — When the requirement changes, does the correction actually
  start at stage 1, or does the pressure to just edit the code win? Does the
  workflow give a clear answer on which stages the change has to revisit?

### Known workflow gaps to watch

These are suspected before the run starts. Confirm or refute each in the log;
do not fix them mid-run.

- No stage covers project scaffolding — the workflow presumes `demo/` exists.
- `CLAUDE.md` and `doc/validated-doc/data-schema/` describe a deleted app.
- `doc/workflow-validation/` is absent from the `CLAUDE.md` structure tree; the
  workflow has no documented place for meta-work about itself.
- The stage-2 → stage-3 handoff depends on the ticket making a call the ticket
  author may not have enough information to make.
- Whether `schema-writer` prunes docs for apps that have disappeared is
  untested — the run exercises it twice, on the legacy
  `public_goods_simple.md` orphan and again when stage 0's placeholder app is
  removed.
- The workflow describes work moving forward through five stages and says little
  about work moving **backward** — what happens when a settled requirement turns
  out to be wrong. The second pass is aimed squarely at this.

### Deferred Decisions

- The `doc/validated-doc/guide/` filename — story `OT-0001-06` names it once the
  app exists.
- What the second pass changes about `REQ-0001` — story `OT-0001-07`, decided by
  looking at the running app.
- Whether `doc/workflow-validation/` becomes the standing home for workflow
  meta-work or holds only this run — story `OT-0001-08`.

## Resolution

### Verdict: yes, with one hole

**The workflow is usable as written by someone who has read it once.** Both
passes reached the end. Every stage that could run, ran, and produced what
`CLAUDE.md` says it produces. `uv run pytest` is green, promotion debt is empty,
and `CLAUDE.md` and `.claude/skills/**` were never touched.

The qualification is not small: **stage 3 never ran.** Of the five stages, the
one whose value is hardest to argue on paper is the one this run cannot speak to.

### What the run proved

**Stage 1 is not ceremony, and that is the strongest result.** It fired twice and
changed the outcome both times.

- On the first pass, the seed brief's "network setting" was read by both the epic
  and its story as a **fixed topology**. The researcher's first answer said it is
  not a topology at all — the four play together for ten rounds and the links are
  redrawn every round, with the accumulated history driving the decision. Anyone
  who had skipped stage 1 and built from the ticket's own framing would have
  built the wrong experiment (F-11).
- On the second pass, the change was fifteen lines of Python. Editing the code
  directly would have been faster and nothing would have caught the shortcut. But
  writing the requirement amendment surfaced a collision the implementer would
  never have hit — marking a partner's past round raises whether to show *who
  else* they were linked to, which would leak information about non-neighbours
  and break rule 10. Asked, the researcher kept rule 10 intact. A code-first
  change would have picked whichever was easier to write and never noticed it was
  deciding a privacy policy (F-43).

**The backward path works, but only because someone chose to walk it** (F-25,
F-28). A stage-2 decision invalidated part of settled `REQ-0001`; the correction
was made at stage 1 as `CLAUDE.md` requires. Nothing would have complained
otherwise. The ticket store has no concept of a requirement needing correction,
`promotion-debt.md` tracks only closure hygiene, and the generator cannot see
requirements at all. The instruction is clear and correct; the *mechanism* does
not exist.

**The stage-3 conditional gave clean answers in both directions** — required on
both triggers in pass one, skipped with a one-line reason in pass two (F-23,
F-44). The epic suspected the stage-2 → stage-3 handoff would be the weak joint.
It was a non-event, but for a contingent reason worth stating: stage 2 had an
easy call because stage 1 made it easy. A vaguer requirement would reproduce the
gap exactly.

**Honest failure records propagate.** The one place a researcher-owned choice was
made by an implementer for convenience survived into `doc/validated-doc/` as a
stated caveat — but only because `DECISION.md` was written that way by choice,
not by rule. A terser file would have promoted "the network is a ring" as settled
design, losing the fact that nobody chose it at exactly the point the document
becomes authoritative (F-31, F-42).

### What broke

Five blockers, of which one actually stopped a stage:

- **No browser tooling** (F-07, F-29). `CLAUDE.md#visual-variants` makes the
  1555×885 screenshot the deliverable. There is no browser here. Offered the
  alternatives, the user chose to skip and log. The arrangement — ring over
  diamond — was then picked by the implementer on implementation grounds, and the
  two other visual questions were answered by default. The diamond is the only
  surviving arrangement where position is measurable, which is close to what the
  researcher originally asked about.
- **No `blocked` status** (F-30). `OT-0002-01` had to close `wont_fix`, which
  overstates finality for work still worth doing.
- **A stale reference made a criterion unreachable** (F-04).
  `tests/test_public_goods_payoffs.py` imports a deleted app at module scope, so
  `pytest` failed at *collection* — not a failing test, a suite that could not be
  built. `CLAUDE.md#tests` still lists it.
- **`ticket-system/SKILL.md` forbids what it requires** (F-21) — never edit
  `doc/requirements/`, then add the ticket id to the requirement's `tickets:`
  list.
- **"Settled but incomplete" has no rule** (F-12, F-22), and it is the state
  `REQ-0001` was actually in: settled, with four open questions and no hypothesis.

### Won't-fix scope

`OT-0002-01` is `wont_fix` rather than resolved — blocked on tooling, not
abandoned. It should be reopened if a browser becomes available; the arrangement
decision deserves to be made properly.

### Where this verdict is weak

- **The operator was not a new user.** They wrote the epic's stories, and twice
  knew things a fresh reader would not (F-15).
- **Stage 3 never ran**, so the run says nothing about the stage most in need of
  evidence.
- **Six stories were ticketed after their work was done** (F-36, F-47), so the
  ticket store overstates how much tickets drove the work.
- **One operator, one app, one afternoon.** Nothing here speaks to a workflow used
  by several people over months.

### Follow-on

`OT-0004` — filed pending, carrying all 48 findings' worth of changes, each
traced to a log entry. It is ordinary work on its own schedule now that this epic
is closed.
