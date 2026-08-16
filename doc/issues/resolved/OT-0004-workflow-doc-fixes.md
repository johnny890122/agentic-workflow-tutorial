---
id: OT-0004
title: Repair CLAUDE.md and the skill definitions against the OT-0001 findings
type: improvement
status: resolved
priority: high
created: 2026-08-15
resolved: 2026-08-15
area: docs
tags:
  - workflow
  - meta
---

# Repair CLAUDE.md and the skill definitions against the OT-0001 findings

## Description

`OT-0001` ran the five-stage workflow end to end twice and logged 47 findings.
This ticket carries every change those findings justify. Nothing was fixed during
the run, because editing the documents under test would have invalidated it.

## Details

Every item below traces to an entry in
`doc/workflow-validation/OT-0001-friction-log.md`. Items are grouped by the file
they change. **The first two groups are the ones that actually broke the run**;
the rest are real but survivable.

### Blockers — these stopped work

- **Say what browser tooling stage 3 needs, and what to do without it** (F-07,
  F-29). `CLAUDE.md#visual-qa` says "use the browser tooling available in the
  current agent environment". There was none, and
  `CLAUDE.md#visual-variants` makes the 1555×885 screenshot the *deliverable*,
  not an accessory. Stage 3 could not run at all, and the arrangement decision
  fell to an implementer for convenience. Name the expected tool and give a
  documented fallback — build the variants for the user to open locally is the
  obvious one.
- **Add a `blocked` status, or say what to do without one** (F-30). A ticket that
  cannot proceed has no honest home: `pending` stalls its epic forever,
  `resolved` is false, and `wont_fix` — which `OT-0002-01` had to use —
  overstates finality for work that is still worth doing. Needs a decision in
  `ticket-system/SKILL.md` and the generator.
- **Repair the stale `public_goods_simple` references** (F-02, F-04).
  `CLAUDE.md#structure` still shows the deleted sample app, and
  `CLAUDE.md#tests` still names `tests/test_public_goods_payoffs.py`. The second
  one is worse: that file's module-scope import made `pytest` fail at
  *collection*, so a green-suite criterion was unreachable rather than merely
  failing. Both sections need rewriting against the current tree.

### Missing rules — the run had to invent an answer

- **Document `doc/workflow-validation/`** (epic, F-01). It is absent from the
  `CLAUDE.md` structure tree. Decide whether it is the standing home for
  workflow meta-work or holds only this run — `OT-0001-08` recommends the former.
- **Give project scaffolding a home** (F-01). No stage covers it; the workflow
  presumes `demo/` exists. Either add a stage 0 or state that scaffolding is
  ordinary stage-4 work preceding the first feature.
- **`schema-writer` must prune** (F-05, F-34). Confirmed twice, the second time
  from a deliberately neutral prompt: the skill never says what to do with a doc
  whose app has disappeared. Add one procedure step — delete any `<app_label>.md`
  with no matching package, drop its index row, note it in the change log.
- **Rule the "settled but incomplete" case** (F-12, F-22).
  `ticket-system/SKILL.md` handles `settled` and `draft` and nothing between, but
  `REQ-0001` was settled *and* carried four open questions including no
  hypothesis at all. Key the rule on open questions, not on the status field, and
  say which kinds block a ticket. `refine-requirement`'s Readiness list should
  likewise distinguish hard gates from waivable boxes.
- **Say what happens when a requirement is unimplementable as written** (F-35).
  `CLAUDE.md` covers a requirement that "turns out to be wrong". Rule 8's "shared
  evenly" was not wrong, it was arithmetically impossible with whole points — a
  different thing, arriving from a different direction, and it happened twice.
- **Distinguish "validated" from "ready to run"** (F-41). Every promotion gate
  was met while the honest guide doc still told the researcher their experiment
  was not ready. Nothing says whether that should have blocked promotion.

### Self-contradictions

- **`ticket-system/SKILL.md` forbids what it requires** (F-21). Its guardrail
  says never edit `doc/requirements/`; four paragraphs later it requires adding
  the ticket id to the requirement's `tickets:` list. Carry the exception in the
  guardrail.
- **`refine-requirement` requires a template section that does not exist**
  (F-13). `SKILL.md` lists `## Conflicts with what exists` among the things that
  "map to a section of the template". `REQUIREMENT_TEMPLATE.md` has no such
  section — conflicts live inside `## Translation notes`. Fix one or the other.

### Smaller repairs

- **`localhost:8000` is a default, not a requirement** (F-06). Port 8000 was
  occupied by an unrelated application; `otree devserver <port>` works and is
  undocumented.
- **Warn that the devserver holds its database in memory** (F-38).
  `CLAUDE.md#tests` explains `OTREE_IN_MEMORY` as a pytest concern. It is also
  true of `otree devserver`: a session created by an external script is invisible
  to the running server, which 404s the start link. Also document
  `otree test <app> --export <dir>`, the working export path.
- **Explain `demo/__init__.py`** (F-03), or establish it is unnecessary and drop
  it. It is in no structure tree and nothing says what it is for.
- **Require `DECISION.md` to record who decided and on what evidence** (F-31,
  F-42). The strongest single recommendation from the run. `OT-0002-01`'s
  `DECISION.md` said plainly that an implementer picked the ring for convenience
  and the researcher never saw the alternatives — and *only* because the operator
  chose to write it that way. A terser file would have promoted "the network is a
  ring" into `doc/validated-doc/` as settled design, losing that fact permanently
  at the moment the document becomes authoritative.
- **Say that requirement rule numbers are load-bearing** (F-28). Tickets cite
  rules by number, so the list is effectively append-only; renumbering is a
  silent breaking change with no tooling to catch it.
- **Give the requirement template somewhere to record a change** (F-28).
  `refine-requirement/SKILL.md` says to "note what changed and why" without
  saying where; the template has no change section.
- **Rule on borderline vocabulary** (F-19). "Round" is standard
  experimental-economics language rather than oTree jargon and was used freely.
  The same argument could stretch to *treatment*, *endowment*, *matching*.

### Not fixed here — needs a decision first

- **Tickets that describe work instead of specifying it** (F-36, F-47). Four
  `OT-0002` stories and two `OT-0001` stories were written after their work was
  done. The workflow neither noticed nor could. Whether that is worth policing,
  and how, is a judgment call rather than a documentation fix.

- **No artifact** — this is a documentation change to files that are themselves
  the specification. No visual question, no unproven mechanism.
- **Out of scope.** Reopening `OT-0002-01` to actually run the artifact stage;
  answering `REQ-0001`'s open questions; any change to `demo/`.

## Acceptance Criteria

- [x] Every item above is either applied or explicitly declined with a reason
      recorded in this ticket.
- [x] `CLAUDE.md`'s structure tree and `#tests` section match the actual repo —
      no reference to `public_goods_simple` or
      `tests/test_public_goods_payoffs.py` survives.
- [x] `doc/workflow-validation/` appears in the `CLAUDE.md` structure tree, with
      its scope stated.
- [x] `schema-writer/SKILL.md` tells the skill to prune docs for apps that no
      longer exist.
- [x] `ticket-system/SKILL.md`'s `doc/requirements/` guardrail carries its own
      `tickets:` exception.
- [x] `refine-requirement`'s `SKILL.md` and `REQUIREMENT_TEMPLATE.md` agree about
      `## Conflicts with what exists`.
- [x] `CLAUDE.md#visual-qa` names the browser tooling stage 3 needs and the
      documented fallback when it is absent.
- [x] The `blocked` question is decided one way or the other, in
      `ticket-system/SKILL.md`.
- [x] `CLAUDE.md#visual-variants` requires `DECISION.md` to record who decided
      and on what evidence.
- [x] Each applied change cites its friction-log entry, so the reasoning stays
      recoverable.

## Open Questions

- None. Both were settled with the user before implementation:
  `doc/workflow-validation/` is the **standing home** for workflow meta-work, and
  blocked work closes as **`wont_fix`** under a documented convention rather than
  getting a new status.
- Carried forward, not open here: `OT-0002-01` should be reopened if browser
  tooling becomes available. That is a decision about the experiment, and it now
  lives in `artifacts/OT-0002-01-link-arrangements/DECISION.md` and the promoted
  guide, both of which name it as provisional.

## Related Files

- `CLAUDE.md`
- `.claude/skills/refine-requirement/SKILL.md`
- `.claude/skills/refine-requirement/assets/REQUIREMENT_TEMPLATE.md`
- `.claude/skills/ticket-system/SKILL.md`
- `.claude/skills/ticket-system/scripts/generate_issues_index.py`
- `.claude/skills/schema-writer/SKILL.md`
- `doc/workflow-validation/OT-0001-friction-log.md`

## Resolution

All 48 findings applied or explicitly declined. `uv run pytest` is green (11),
the generator exits zero, and the devserver boots.

### Two decisions taken with the user first

- **`doc/workflow-validation/` is the standing home** for workflow meta-work, not
  an archive of `OT-0001`. Now in the `CLAUDE.md` structure tree with its scope
  stated, and explicitly marked as not a stage and never a gate.
- **No `blocked` status.** Blocked work closes `wont_fix` under a documented
  convention: the Resolution must open by saying blocked-not-abandoned, name the
  blocker, state the reopening condition, and rewrite acceptance criteria with
  notes rather than ticking them. A `blocked` tag makes them findable. The
  generator is unchanged. The cost — `wont_fix` overstating finality — is written
  down rather than hidden.

### `CLAUDE.md`

| Change | Finding |
| --- | --- |
| Structure tree rebuilt; rows marked **required** so oTree's demands are separable from whatever apps exist | F-02 |
| `demo/__init__.py` established as unnecessary and **deleted** — verified against pytest, `otree test`, and the devserver | F-03 |
| Scaffolding named as ordinary stage-4 work, with the empty-`SESSION_CONFIGS` trap spelled out | F-01 |
| `doc/workflow-validation/` added to the doc tree, scope stated | epic, F-48 |
| `#tests` no longer names the deleted test file; module-scope app imports flagged as a collection-breaker | F-04 |
| Devserver's in-memory database documented, with the `POST /api/sessions` route for driving participants | F-38 |
| Port 8000 documented as a default; `otree test --export` added | F-06 |
| `#visual-qa` now says to check for browser tooling first, and gives a ranked fallback | F-07, F-29 |
| `DECISION.md` must record **who decided and on what evidence**, and mark convenience picks provisional | F-31, F-42 |
| Workflow rules gained: work moves backward and nothing will remind you; rule numbers are append-only; validated ≠ ready to run | F-25, F-28, F-35, F-41 |

### `.claude/skills/`

| Change | Finding |
| --- | --- |
| `ticket-system`: the `doc/requirements/` guardrail carries its own `tickets:` frontmatter exception | F-21 |
| `ticket-system`: "settled but still carrying open questions" ruled on — judge by what a question blocks, not by the status field | F-12, F-22 |
| `ticket-system`: Blocked work section added | F-30 |
| `schema-writer`: enumerate-then-**prune**, plus a verification step for orphaned docs and index rows | F-05, F-34 |
| `refine-requirement`: conflicts belong in the last Translation-notes bullet — the template has no section — and scaffolding apps are not prior art | F-13, F-15 |
| `refine-requirement`: Readiness split into hard gates and waivable boxes; a design-complete, purpose-open requirement may be settled | F-12 |
| `refine-requirement`: refining is expected, changes noted inline with a date, and **rules are never renumbered** | F-25, F-28 |
| `refine-requirement`: the line is oTree vocabulary, not technical vocabulary — *round*, *endowment*, *treatment* are the researcher's | F-19 |
| `refine-requirement`: "go back and ask" split from consequences of what the user already said, which route to the artifact stage or an open question instead | F-17, F-24, F-35 |

### Declined

**Policing tickets written after their work** (F-36, F-47). Six stories in the run
described completed work rather than specifying it. No rule was added: the honest
fix is a reviewer noticing, and a rule saying "write the ticket first" would have
been satisfied by writing it first and ignoring it. Recorded in the friction log
so a future run can judge whether it caused real harm.

### Note

This ticket edited the documents `OT-0001` was testing — which is why it could
only run after that epic closed. The friction log is unchanged: it is the record
of what the workflow looked like when it was measured, and rewriting it to match
the repairs would destroy the evidence for them.
