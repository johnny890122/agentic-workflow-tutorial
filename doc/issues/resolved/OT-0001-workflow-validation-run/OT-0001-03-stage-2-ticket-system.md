---
id: OT-0001-03
title: Stage 2 — run ticket-system against settled REQ-0001 and produce the OT-0002 feature epic
type: story
status: resolved
priority: high
created: 2026-08-15
resolved: 2026-08-15
area: docs
tags:
  - workflow
  - validation
  - stage-2
parent: OT-0001
---

# Stage 2 — run ticket-system against settled REQ-0001 and produce the OT-0002 feature epic

## Description

Run the `ticket-system` skill against the now-settled `REQ-0001` and see whether
stage 2 can write executable tickets from a requirement alone — and whether the
stage-3 conditional gives the implementer a clear answer or leaves them
guessing.

## Details

- **Input.** `doc/requirements/REQ-0001-networked-public-goods.md`,
  `status: settled` as of 2026-08-15. Read it in full; it is the only source of
  intent. Nothing in `OT-0001` may add design the requirement does not carry.
- **Output goes to a separate feature epic `OT-0002`**, not under `OT-0001`, per
  the epic's Settled Decisions. `OT-0001` is the validation harness; the app's
  own tickets are ordinary work and must look like ordinary work. `OT-0002`
  carries `requirement: REQ-0001` in frontmatter, and `REQ-0001`'s `tickets:`
  list gains the id.

### What stage 2 has to get right

- **The stage-3 call.** `REQ-0001` states plainly that stage 3 is required on
  both `CLAUDE.md` triggers — the link arrangement is a choice the researcher
  asked to make by looking, and per-round link structure has no precedent in the
  repo. If `ticket-system` restates that cleanly, the handoff works. If it
  hedges, waffles, or silently drops it, that is the stage-2 → stage-3 gap the
  epic suspected, and a log entry.
- **A settled requirement that still carries open questions.** This is the
  interesting case and it was not anticipated. `REQ-0001` is `settled`, but its
  `## Open questions` still holds four items — most importantly **no
  hypothesis**: the researcher declined to say what the experiment measures.
  `ticket-system/SKILL.md` has rules for "settled" and for "draft", and none for
  "settled but incomplete". Observe which way it goes and do not tip it off.
  The three lesser open questions (mutual links, the not-taken exclusions, the
  conversion rate) are all things a ticket could reasonably carry forward as its
  own Open Questions.
- **The degree-1 arithmetic constraint** must survive into `OT-0002`. With
  `C.MULTIPLIER = 2`, a player holding exactly one link gets their whole
  contribution back and the dilemma vanishes for them. `REQ-0001` records this
  as a constraint on the stage-3 variants. A ticket that loses it hands the
  artifact stage an under-specified brief.
- **The app name.** `REQ-0001` proposes `network_public_goods` in its
  translation notes and flags it as stage 2's to confirm. Stage 2 settles it —
  either way, deliberately.
- **Do not let the epic's own vocabulary leak.** `OT-0002` is written for
  someone building an oTree app, with no knowledge that a workflow validation
  run is happening. It must not reference `OT-0001`, the friction log, or this
  story.

### Story split

The `ticket-system` skill's Epic Handoff Workflow prescribes splitting by
implementation workstream. Which stories `OT-0002` actually gets is stage 2's
call, not this story's — but per that skill, models before pages, and the
artifact story before anything that depends on the arrangement.

Only write child stories whose scope is settled. The arrangement is *not*
settled until stage 3 runs, so any story whose shape depends on it stays a
roadmap bullet.

- **No artifact for this story.** Stage 2 is ticket-writing; there is no open
  visual question about a ticket and no unproven mechanism. (The artifact
  `OT-0002` *requires* is stage 3's work, story `OT-0001-04`.)
- **No code, no tests.** Nothing under `demo/` or `tests/` changes, so the
  `uv run pytest` criterion does not apply.
- **Out of scope.** Implementing anything, building the variants, choosing the
  arrangement, and editing `REQ-0001` — if the requirement turns out to be
  wrong, `ticket-system` is required to say so and send the work back to stage 1
  rather than patch it in the ticket. Whether it actually does that is worth
  watching.

## Acceptance Criteria

- [x] A feature epic `OT-0002` exists, carries `requirement: REQ-0001` in
      frontmatter, and follows `assets/TICKET_TEMPLATE.md` section for section.
- [x] `REQ-0001`'s `tickets:` frontmatter list names `OT-0002`.
- [x] `OT-0002` requires an artifact and says what the spike must demonstrate,
      with the acceptance-criteria checkbox `CLAUDE.md#stage-3-is-conditional`
      calls for — or explicitly skips stage 3 in one line with a reason, which
      would itself be a finding.
- [x] The degree-1 arithmetic constraint appears in `OT-0002`, not only in
      `REQ-0001`.
- [x] The app name is settled in `OT-0002`, either confirming
      `network_public_goods` or naming a replacement.
- [x] Every child story `OT-0002` creates has settled scope; anything depending
      on the unchosen arrangement is a roadmap bullet, not a stub file.
- [x] `OT-0002` reads as ordinary feature work — no reference to `OT-0001`, the
      friction log, or the validation run.
- [x] `uv run python .claude/skills/ticket-system/scripts/generate_issues_index.py`
      exits zero and files `OT-0002` and its stories correctly.
- [x] `demo/`, `tests/`, `artifacts/`, and `doc/validated-doc/` are untouched by
      this story.
- [x] Friction log entry appended to
      `doc/workflow-validation/OT-0001-friction-log.md` covering: whether the
      requirement alone was enough to write executable tickets, how
      `ticket-system` handled a settled requirement with open questions and a
      missing hypothesis, whether the stage-3 call was unambiguous, whether
      oTree design decisions had to be invented that `REQ-0001` did not supply,
      and how the story split was chosen.

## Open Questions

- Does a settled-but-hypothesis-less requirement justify a ticket at all? If
  `ticket-system` stops and sends the work back to stage 1, that is a legitimate
  outcome of this story, not a failure — record it and decide with the user
  whether to answer the hypothesis or proceed regardless.

## Related Files

- `.claude/skills/ticket-system/SKILL.md`
- `.claude/skills/ticket-system/assets/TICKET_TEMPLATE.md`
- `.claude/skills/ticket-system/scripts/generate_issues_index.py`
- `doc/requirements/REQ-0001-networked-public-goods.md`
- `doc/issues/pending/OT-0002-*.md`
- `doc/workflow-validation/OT-0001-friction-log.md`

## Resolution

Ran `ticket-system` against settled `REQ-0001`. One `AskUserQuestion` round of
three questions, then epic `OT-0002` plus two child stories.

### What stage 2 produced

- `doc/issues/pending/OT-0002-networked-public-goods.md` — epic,
  `requirement: REQ-0001`, seven-row child-story roadmap, dependency plan, and a
  handoff appendix carrying the payoff formula and six test scenarios.
- `OT-0002-01` — the stage-3 artifact story: three arrangement variants (ring,
  diamond, mixed draw), each differing on the arrangement itself.
- `OT-0002-02` — constants, fields, and the payoff rule. Written now because the
  payoff function takes an adjacency as *input*, so its tests can set one by hand
  and run before the arrangement is chosen.
- Five further stories stayed roadmap bullets: they depend on the unchosen
  arrangement or the unchosen screen design.
- `REQ-0001`'s `tickets:` list now names `OT-0002`.

### Decisions stage 2 settled

- **App name** `network_public_goods`, confirming `REQ-0001`'s proposal.
- **Scope** is the whole requirement in one pass, not a staged cut.
- **Promotion target** `doc/validated-doc/guide/network-public-goods.md`.
- **Degree-1 is a hard constraint** — every arrangement must give each
  participant at least two links. See the divergence below.

### The answer to this story's Open Question

*Does a settled-but-hypothesis-less requirement justify a ticket at all?*
Yes, and the epic was written — but the skill gave no rule for it. `REQ-0001` is
`settled` while carrying four open questions, and `ticket-system/SKILL.md` has
rules only for `settled` and for `draft`. The judgment applied: the design is
complete and every number has a value, so the build is unblocked; the missing
hypothesis decides what the *promoted guide doc* says the experiment is for, so
it blocks `OT-0002-07` and nothing earlier. Recorded as friction-log F-22.

### Divergence left behind — needs a stage-1 correction

**`REQ-0001` and `OT-0002` now disagree, and this story does not fix it.**

The degree-1 answer rules out hub-and-spokes. `REQ-0001` names hub-and-spokes as
one of three concrete alternatives for stage 3 to build; `OT-0002` says it will
not be built. `REQ-0001` did delegate the choice ("must either avoid or
deliberately accept"), so this resolves a delegated question rather than
reversing a settled one — but the requirement's prose still misleads a reader
who only opens that file.

Both documents say the same thing about what to do: `CLAUDE.md` — *"A
requirement that turns out to be wrong gets corrected at stage 1, not silently
overridden downstream"* — and `ticket-system/SKILL.md` — *"say so and send the
user back to that skill rather than patching the gap inside the ticket."* So
`REQ-0001` was **not** edited from inside this skill beyond its `tickets:` list.
The correction is the next action, through `refine-requirement` in refine mode.

Recorded as friction-log F-25, the most consequential stage-2 finding: the
workflow's instruction is clear and correct, but no stage *owns* the case where a
downstream decision invalidates part of an upstream doc, and nothing in the
ticket store records the debt while it is outstanding.

### Deliberately not done

- No implementation, no variants built, no arrangement chosen.
- `demo/`, `tests/`, `artifacts/`, and `doc/validated-doc/` untouched.
- `REQ-0001` prose unedited — only the `tickets:` frontmatter key, which
  `SKILL.md` requires and its own guardrail forbids (F-21).

### Files updated

- `doc/issues/pending/OT-0002-networked-public-goods.md` — created.
- `doc/issues/pending/OT-0002-networked-public-goods/OT-0002-01-link-arrangement-variants.md` — created.
- `doc/issues/pending/OT-0002-networked-public-goods/OT-0002-02-constants-fields-and-payoff.md` — created.
- `doc/requirements/REQ-0001-networked-public-goods.md` — `tickets:` list only.
- `doc/workflow-validation/OT-0001-friction-log.md` — F-21 … F-27.
