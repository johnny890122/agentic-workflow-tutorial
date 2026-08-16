---
id: OT-0001-02
title: Stage 1 — run refine-requirement on the seed brief and settle REQ-0001
type: story
status: resolved
priority: high
created: 2026-08-15
resolved: 2026-08-15
area: docs
tags:
  - workflow
  - validation
  - stage-1
parent: OT-0001
---

# Stage 1 — run refine-requirement on the seed brief and settle REQ-0001

## Description

Run the `refine-requirement` skill against the epic's four-word seed brief and
carry it through to a settled `REQ-0001`, testing whether stage 1 can turn a
researcher's vague description into something a ticket can be written from.

## Details

- **The input, verbatim and nothing more:**

  > A public goods game variant. Four players. They play in a network setting.

- **Do not supply the design.** The operator running the skill plays the
  researcher and answers the interview questions as a researcher would: knowing
  the behavior they want to observe, not knowing what a page, a field, a round,
  or a wait page is. Answers should stay in participant language.
- **What the interview must pin down**, per
  `.claude/skills/refine-requirement/SKILL.md#what-must-be-pinned-down` —
  purpose, participant journey, rules, numbers, grouping and repetition,
  earnings, out-of-scope, visual questions, and conflicts with what exists. The
  network-specific gaps that must not be left implicit:
  - What the network connects: who each of the four players is linked to, and
    whether the topology is the same for everyone.
  - Whether the structure is fixed for the whole session or changes.
  - Whether a contribution benefits only neighbours, or everyone, at different
    rates.
  - What each player knows about the others — neighbours only, or the whole
    network.
  - Rounds, endowment, multiplier, currency.
- **Expect visual questions and let them stay open.** How a four-node network is
  shown on screen is close to a canonical case of something that must be *seen*
  to be decided. The skill must park it under
  `## Visual questions for the artifact stage`, phrased as a choice, without
  sketching anything. If it instead answers it in prose, that is a stage-1
  defect and a log entry.
- **The topology itself is deferred to stage 3.** If the researcher has no
  opinion on how the four players are connected, that is a legitimate stage-1
  output, not a stalled interview — record it as an open choice for the artifact
  stage rather than picking one arbitrarily. Two things follow:
  - Stage 3's variants must then differ **on the topology**, not merely on how
    one fixed topology is drawn. Per `CLAUDE.md#visual-variants`, variants that
    do not differ on the question being asked are not a choice.
  - This also puts the requirement squarely on the second stage-3 trigger — a
    mechanism with no precedent in the repo — so stage 3 is required on both
    counts. Say so in the requirement, so the stage-2 ticket inherits an easy
    call.
  - Everything the researcher *does* know about the connections — that they are
    the same for everyone, say, or that they never change mid-session — is a
    **rule**, not an open question, and constrains every variant.
- **Naming the app is stage 1's to propose and stage 2's to settle.** The
  template asks for the app name in `## Translation notes`, which is the one
  section where oTree vocabulary belongs, so put a proposed name there — and
  nowhere in the researcher-facing body, where it would be noise. Stage 2
  confirms or overrides it. If the skill instead pushes the naming question into
  the interview, that is a log entry: it is asking a researcher to decide an
  identifier they have no basis to judge.
- **`## Conflicts with what exists` is a live section here.** The skill is told
  to ground translation notes in `demo/<app>/__init__.py` and
  `doc/validated-doc/data-schema/`. After story `OT-0001-01`, `demo/` holds only
  the skeleton plus the disposable `scaffold_check` app. Whether the skill
  correctly reports "nothing to conflict with" — rather than treating
  `scaffold_check` as prior art — is a specific thing to observe. Do not tip it
  off.
- **Stop at the handoff.** Per its guardrails the skill must not chain into
  `ticket-system`. If it does, that is a finding. Settling the requirement
  (`status: settled`, `settled:` filled) is part of this story; writing the
  ticket is story `OT-0001-03`.
- **No artifact** — stage 1 is words only, and the skill is explicitly forbidden
  from mocking anything.
- **No code, no tests.** Nothing under `demo/` or `tests/` changes, so the
  `uv run pytest` criterion does not apply to this story.
- **Out of scope.** Writing tickets, choosing an app name, deciding the screen
  layout, and any change under `demo/`.

## Acceptance Criteria

- [x] `doc/requirements/REQ-0001-<slug>.md` exists, follows
      `assets/REQUIREMENT_TEMPLATE.md` section for section, and reaches
      `status: settled` with `settled:` filled.
      (`REQ-0001-networked-public-goods.md`, settled 2026-08-15 on the user's
      confirmation. The template has no `## Conflicts with what exists` section
      despite `SKILL.md` requiring one — see friction-log F-13.)
- [x] Every number in the requirement has a value or is explicitly marked
      provisional or open — nothing silently chosen.
- [x] The `## Out of scope` section names something real and tempting, not a
      strawman.
- [x] At least one genuine visual question is parked for stage 3, phrased as a
      choice to be made rather than as prose describing a design.
- [x] If the topology is left open, `## Visual questions for the artifact stage`
      names it as a choice between concrete alternatives, and the requirement
      states that stage 3 is required — on both the visual trigger and the
      no-precedent trigger.
- [x] A proposed app name appears in `## Translation notes` and nowhere in the
      researcher-facing body, flagged as stage 2's to confirm.
- [x] Nothing in the requirement traces back to the operator rather than to an
      answer given in the interview — checked by rereading it against the seed
      brief. **One exception, flagged in the file rather than hidden:** rule 5
      (links are mutual) is the operator's inference from the word "connected",
      not something the researcher said. It carries an inline caveat and an
      entry in `## Open questions`.
- [x] The skill stopped for confirmation and did **not** chain into
      `ticket-system`.
- [x] `demo/`, `tests/`, `artifacts/` (other than the friction log), and
      `doc/validated-doc/` are untouched by this story.
- [x] Friction log entry appended to
      `doc/workflow-validation/OT-0001-friction-log.md`: how many interview
      rounds it took, which questions a real researcher could not have answered,
      whether oTree vocabulary leaked into a question, whether the skill handled
      "I don't know, show me" as a valid answer or pushed for a verbal one,
      whether it treated `scaffold_check` as prior art, and any readiness box it
      left unticked.
- [x] The settled `REQ-0001` is played back to the user in plain language and
      confirmed before story `OT-0001-03` opens.

## Open Questions

- None. Topology is deferred to stage 3 when the researcher has no opinion, and
  the app name is proposed in translation notes for stage 2 to settle.

## Related Files

- `.claude/skills/refine-requirement/SKILL.md`
- `.claude/skills/refine-requirement/assets/REQUIREMENT_TEMPLATE.md`
- `doc/requirements/README.md`
- `doc/requirements/REQ-0001-<slug>.md`
- `doc/validated-doc/data-schema/README.md`
- `doc/otree-doc/multiplayer/`
- `doc/workflow-validation/OT-0001-friction-log.md`

## Resolution

Ran `refine-requirement` against the seed brief. Four `AskUserQuestion` rounds,
twelve questions, one requirement: `doc/requirements/REQ-0001-networked-public-goods.md`,
settled 2026-08-15 after playback and user confirmation.

### What the interview produced

The brief's "network setting" turned out **not** to mean a fixed topology. The
researcher's first answer reframed it: the four play together for ten rounds,
the links between them are redrawn at random every round, and the decision input
is the *history* of what your current partners have contributed in earlier
rounds. Links govern where money goes — a contribution is doubled and shared
only among the contributor and their current links. Links are known before
choosing, so history can be acted on directly.

Every number is settled except the link arrangement itself, which the researcher
explicitly asked to see rather than decide, and the points-to-money rate, which
was never discussed and is marked provisional.

### Deliberately not done

- **The hypothesis was left open**, at the researcher's choice, from three
  concrete candidates. The design is complete and buildable; what it measures is
  not decided. Carried as the first `## Open questions` entry. `ticket-system`
  refuses to write against an unsettled requirement, so this was surfaced to the
  user before settling rather than resolved by the operator.
- **The degree-1 arithmetic problem was surfaced, not fixed.** Multiplier 2 plus
  "shared among you and your links" means a participant with exactly one link
  gets their whole contribution back, so contributing is free and the dilemma
  disappears for them. Written up as a worked example and turned into a
  constraint on the stage-3 arrangements rather than silently repaired. See
  friction-log F-17.
- No artifact, no code, no tests. `demo/`, `tests/`, `artifacts/`, and
  `doc/validated-doc/` are untouched by this story.

### Files updated

- `doc/requirements/REQ-0001-networked-public-goods.md` — created, settled.
- `doc/workflow-validation/OT-0001-friction-log.md` — stage-1 entries F-11 … F-20.

### Findings worth carrying forward

- **F-11 is the run's strongest result so far.** Both this story and the epic
  assumed a fixed topology and would have sent an implementer in the wrong
  direction. Stage 1 caught it on the first question.
- **F-13**: `refine-requirement/SKILL.md` requires a `## Conflicts with what
  exists` section that `assets/REQUIREMENT_TEMPLATE.md` does not contain. This
  story's Details called it "a live section here"; it does not exist. Conflicts
  went into the `## Translation notes` bullet instead.
- **F-12**: the skill gives no rule for whether a requirement with no hypothesis
  may be settled. Readiness does not distinguish hard gates from waivable boxes.
- **F-15**: `scaffold_check` was correctly not treated as prior art, but the
  same operator had built it an hour earlier, so this is weak evidence.
