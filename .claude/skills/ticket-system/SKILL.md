---
name: ticket-system
description: "Create, refine, or help select tracked issues (`OT-XXXX`) in `doc/issues/`. Use when the user asks to add/write/refine a ticket, choose what to work on, or discuss an experiment feature/problem before implementation. Requirement gathering only: ask clarifying questions, preserve detailed discussion in tickets when needed, write the ticket, and identify the prototype docs plus the formal `doc/validated-doc/` requirements that should change later. Never implement."
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, AskUserQuestion
---

# Ticket System

Use this skill to turn rough experiment ideas into short, actionable tickets in
the status folders under `doc/issues/`.

Project goal: this repo refines oTree experiment requirements through prototype
work. The prototype in `demo/` is a validation tool, not the specification.
Keep exploratory details in `demo/modules/`; promote deliberate requirements to
`doc/validated-doc/guide/`. This skill writes stage 2 of the promotion flow in
`CLAUDE.md` and nothing else.

## Guardrails

- Do not implement. Author ticket content only under `doc/issues/`. Never edit
  `demo/`, `tests/`, or `doc/validated-doc/` from this skill.
- Keep tickets short enough to skim. Use concrete bullets and verifiable checks.
- Read before writing: `CLAUDE.md`, `doc/issues/README.md`,
  `doc/issues/pending.md`, `doc/validated-doc/data-schema/README.md`,
  `.claude/skills/ticket-system/assets/TICKET_TEMPLATE.md`, the upstream
  `doc/requirements/REQ-XXXX-*.md` when one exists, and any referenced ticket or
  doc.
- Do not edit `doc/requirements/`. That is stage 1, owned by the
  `refine-requirement` skill. If the requirement turns out to be wrong or
  incomplete, say so and send the user back to that skill rather than patching
  the gap inside the ticket.
  **One exception:** adding this ticket's id to the requirement's `tickets:`
  frontmatter list, which Upstream Requirement below requires. Frontmatter only —
  never a word of the requirement's prose.
- `doc/otree-doc/` is read-only vendored documentation. Consult it to get the
  oTree API right in a ticket; never edit it.
- `doc/validated-doc/data-schema/` is generated and owned by the `schema-writer`
  skill. A ticket may say a field changes; it must never plan a hand edit there.
- If facts are uncertain, ask the user or leave an explicit Open Question.

## Modes

Choose the mode first. If unclear, use AskUserQuestion. It is always better to
align on the need and then write the detailed ticket.

1. Create new ticket.
2. Refine existing `OT-XXXX`.
3. Help choose the next pending ticket.

For "what should I work on", list pending tickets from `doc/issues/pending.md`
by priority/area, then ask which to inspect.

## Upstream Requirement

Check `doc/requirements/` before creating a feature ticket.

- **A settled `REQ-XXXX` exists.** Read it in full and write the ticket against
  it: the requirement supplies the intent, the rules, the numbers, the
  out-of-scope list, and the translation notes that name apps, pages, and
  fields. Put `requirement: REQ-XXXX` in the ticket frontmatter and add the
  ticket's id to the requirement's `tickets:` list. The ticket must not
  contradict the requirement or quietly widen it; a ticket that needs behavior
  the requirement does not mention is a signal to go back to stage 1.
- **A draft `REQ-XXXX` exists but is not settled.** Say so and stop. Drafts have
  open questions by design; building a ticket on one buries them.
- **A settled `REQ-XXXX` that still carries open questions.** Common, and not the
  same as a draft — settling means the design is agreed, not that every question
  is answered. Judge by **what the open questions block**, not by the status
  field:
  - Questions about *what to build* — an unpinned rule, a number nobody chose, a
    screen nobody has decided — block the ticket. Go back to stage 1.
  - Questions about *why* or *what happens afterwards* — which hypothesis the
    study tests, the payment rate, whether a known limitation is acceptable —
    do not block the build. Carry each onto the ticket's `## Open Questions`,
    and name the story or stage each one does block, so it cannot be lost.
  - If a question could be read either way, ask the user rather than deciding.
- **No requirement exists.** Fine for a bug fix, a test, a docs change, or any
  small change to established behavior. For a new experiment feature described
  in vague or participant-level terms, recommend `refine-requirement` first
  rather than inventing the missing detail inside the ticket.

## AskUserQuestion

Use AskUserQuestion for alignment questions that affect ticket shape. Batch up
to three short questions and include a defer option such as "Not sure, leave as
Open Question".

For every new feature ticket, ask enough to capture:

- Experiment behavior: which app, which page in `page_sequence`, what the
  participant does, what the desired outcome is, MVP vs out-of-scope.
- Data effect: which `C` constants, `Player` / `Group` / `Subsession` fields,
  `form_fields`, or payoff arithmetic change — and whether the change is
  observable in the data export.
- Artifact need: whether the approach must be proven in `artifacts/` before it
  is built in `demo/`, and whether any visual question needs variants for the
  user to pick from. Default to **no artifact** for changes that follow an
  established pattern in the existing app.
- Prototype scope: which `demo/` behavior validates the idea, and which
  `demo/modules/` note records the implementation detail a later agent needs.
- Page-flow documentation: whether the feature needs a child story for the
  page-flow table in `demo/modules/page-flow.md`.
- Spec target: which `doc/validated-doc/guide/` file should be updated if the
  prototype validates the requirement.

Use these prompts when applicable:

- "Which app and which page in `page_sequence` is this for?"
- "What should the prototype prove, and what is out of scope?"
- "Does this need a spike in `artifacts/` first, or is the implementation path
  already clear from the existing app?"
- "Is the layout of this screen already decided, or should we build a couple of
  variants for you to look at first?"
- "Which participant actions need a page-flow table with the model fields they
  write?"
- "Which `doc/validated-doc/guide/` doc should this update later?"

## Spec Doc Targets

For new feature tickets, ask the user which formal spec doc should change later.
If they cannot choose yet, carry that as an Open Question.

`doc/validated-doc/` is written for the researcher, at the architecture and
system-design level. Implementation detail — class names, function signatures,
template internals — belongs in `demo/modules/` and is never promoted. Common
targets:

- Experiment behavior and requirements: `doc/validated-doc/guide/<topic>.md` — what
  the experiment must do, the design rationale, and the treatment structure.
- Session configuration and participant setup: the guide doc covering
  `SESSION_CONFIGS`, group size, rounds, and payment.
- Data produced: `doc/validated-doc/data-schema/` — **generated**. A ticket that
  changes a model field should note that `schema-writer` fires automatically on
  the code change (see `CLAUDE.md`), not that a doc will be hand-written.

Do not update those docs while using this skill. Add a future-facing Acceptance
Criteria item instead.

## Artifact-Backed Tickets

Stage 3 of the promotion flow is `artifacts/` — disposable spikes that prove or
kill an approach before it is built in `demo/`. Require one only when the ticket
genuinely does not have a settled implementation path, or when a visual choice
is still open.

Require an artifact when the ticket asks for one or more of:

- **An unanswered visual question** — the upstream requirement lists one under
  `## Visual questions for the artifact stage`, or the user cannot say what a
  screen should look like without seeing it. This is the common case in this
  frontend-heavy project; see Visual Variant Tickets below.
- A mechanism with no precedent in the repo: a new grouping or matching scheme,
  live pages (`live_method`), a timeout/auto-advance behavior, a custom export,
  or third-party integration.
- A payoff or treatment design where more than one plausible structure exists
  and the choice needs to be seen working before it is committed to.
- Anything the user explicitly asks to prototype, compare, or explore first.

Do **not** require an artifact for ordinary work. This is most tickets:

- Adding, renaming, or retyping a model field; adjusting a `C` constant.
- Payoff arithmetic, grouping and matching rules, round structure.
- Adding a page that follows the existing page pattern, editing a template,
  changing copy or a label.
- Session-config, data, export, bot, test, docs-only, or bug-fix work.
- Cases where the user says not to bother with an artifact.

Stage 3 is conditional, and the ticket is what decides it — so **say which way
it went, either way**. A ticket that skips stage 3 carries one Details bullet
naming the reason: `No artifact — model and payoff change, no open visual
question.` Silence reads as an unanswered question and stalls implementation.

For artifact-backed tickets:

- In Details, add a bullet requiring a spike under
  `artifacts/<ticket-id>-<short-slug>/` before implementation, naming what the
  spike must demonstrate.
- In Acceptance Criteria, add a checkbox:
  `Artifact in artifacts/<ticket-id>-<short-slug>/ demonstrates <behavior> before implementation.`
- In Related Files, include the expected `artifacts/...` folder.
- Nothing in `artifacts/` is promoted verbatim; the ticket should say what gets
  rewritten into `demo/`.

## Visual Variant Tickets

When the open question is what a screen should look like, the artifact is a set
of variants the user picks from, per the Visual variants section of `CLAUDE.md`.
Carry each visual question from the requirement into the ticket rather than
answering it.

- In Details, name the question being decided, the two or three variants worth
  building, and what distinguishes them. Variants must differ on the question —
  say so explicitly, so the implementer does not build three versions of the
  same layout.
- Record what is **not** open: any visual decision the requirement already
  settled is a constraint every variant must respect.
- In Acceptance Criteria, add:
  `Variants in artifacts/<ticket-id>-<short-slug>/ screenshot at 1555x885 and reviewed with the user; choice recorded in DECISION.md.`
- Expect a follow-up implementation ticket or story: the picked variant is a
  decision, and turning it into a real page in `demo/` against real fields is
  separate work.
- The chosen design is promoted as a requirement, not as markup. Note which
  `doc/validated-doc/guide/` doc should record the decision after validation.

## Page-Flow Stories

For every new prototype feature, discuss the participant-facing flow. When the
flow scope is settled, create or link one child story for the flow table using
the Epics and Stories rules below (`type: story`, `parent`, and `OT-XXXX-YY`).
If the scope is not settled, record it as a roadmap bullet or Open Question on
the epic instead of stubbing a child story.

The flow story should require a table in `demo/modules/page-flow.md` showing,
for each page in `page_sequence`: what the participant sees, which
`form_fields` they submit, what validation applies, which wait page or
`before_next_page` / `after_all_players_arrive` hook runs, and which model
fields change as a result.

After the feature is implemented and validated, ask the user whether to promote
it to `doc/validated-doc/guide/`. If yes, create or link a second child story to
translate the prototype flow into settled requirements. Call out expected
differences from the prototype — hardcoded constants that should become session
config parameters, single-round shortcuts that should generalize across rounds,
placeholder copy, and skipped edge cases.

## New Ticket Workflow

1. Read the ticket inventory and template, plus the upstream `REQ-XXXX` if there
   is one (see Upstream Requirement above).
2. AskUserQuestion for whatever the requirement does not already answer:
   experiment behavior, prototype flow story or epic roadmap, and
   `doc/validated-doc/` alignment. Do not re-ask what stage 1 settled.
3. Do tight read-only grounding with `rg`, existing docs and tickets, the
   relevant `demo/<app>/__init__.py` and templates, and `doc/otree-doc/` for any
   oTree API the ticket names.
4. Pick the next `OT-XXXX` id: take the **highest id across all four status
   folders** (scan the whole tree, never just one status), and increment. The
   generator hard-fails on duplicate ids. For a story under an epic, use the
   epic id plus the next two-digit sequence (`OT-XXXX-YY`).
5. Write the ticket with exactly the template sections. New tickets default to
   `pending`: put a standalone ticket or epic file in `doc/issues/pending/`, and
   put a story in `doc/issues/pending/<epic-folder>/`.
6. Regenerate the index:

```bash
uv run python .claude/skills/ticket-system/scripts/generate_issues_index.py
```

## Index Layout and Filing by Status

The generator validates the store, files tickets by status, and rewrites the
index. Run it after every ticket edit; never move ticket files by hand.

- Validation runs first and fails the whole run on: duplicate ids, ids not
  matching `OT-XXXX` / `OT-XXXX-YY`, story ids that do not extend their
  `parent`, unknown statuses, completed epics with active stories, or a filing
  move that would overwrite a file. Filing collisions are checked before any
  file moves occur.
- The index is split across files: a slim `doc/issues/README.md` landing page
  plus one overview per status group — `in-progress.md`, `pending.md`,
  `done.md` (Resolved then Won't Fix) — and `promotion-debt.md` (see Resolving
  Tickets below). Within a status overview, stories nest under a same-status
  parent when possible; a Parent column preserves context when the epic is in
  another status.
- Every ticket lives under the folder matching its canonical status:
  `pending/`, `in_progress/`, `resolved/`, or `wont_fix/`.
- Standalone tickets and epic files live directly in their status folder.
  Stories live in `<status>/<epic-folder>/`, based on the story's own status.
- Parent epics and stories move independently. A mixed-status epic can therefore
  have story folders under several statuses while the epic file remains directly
  under its own status folder.
- Store ticket-specific images at `<ticket-parent>/img/<lowercase-ticket-id>/`.
  The generator moves that companion folder with the ticket so relative image
  links remain valid.
- Reopening any completed ticket moves it back to `pending/` or `in_progress/`
  on the next generator run.
- Legacy status values are normalized for display and filing:
  `in-progress` → `in_progress`, `done` → `resolved`. Always write the canonical
  values (`pending`, `in_progress`, `resolved`, `wont_fix`) in new and edited
  tickets.

### Blocked work

There is no `blocked` status, deliberately — four statuses are enough to keep the
generator simple. Work that cannot proceed closes as **`wont_fix`**, with the
Resolving Tickets rules below applied in full plus three extra requirements:

1. The `## Resolution` opens by saying it is **blocked, not abandoned**, and names
   the blocker concretely.
2. It states the **condition for reopening**, so a later reader knows what would
   change the answer.
3. Acceptance criteria are **rewritten with notes**, never silently ticked — say
   which were carried forward to another ticket and which are simply unmet.

`wont_fix` overstates finality here, and that is a known cost of keeping the
status set small. The Resolution is what carries the truth, so it has to be
written properly. Add a `blocked` tag so these are findable.

Do **not** leave blocked work `pending` to signal that it is unfinished: a
pending story prevents its parent epic from ever resolving, which converts one
blocked ticket into a blocked initiative.

## Epics and Stories

Use an epic when one initiative needs several tickets that share a goal and a
done condition — typically a feature that spans models, pages, bots, and spec
docs.

- Epic: `type: epic`, normal `OT-XXXX` id. Its Details must list the planned
  child stories as a roadmap; its Acceptance Criteria include "all child stories
  closed" plus the initiative-level done condition.
- Story: `type: story`, id extends the epic id with a two-digit sequence
  (`OT-0012-01`), frontmatter `parent: OT-0012`, lowercase kebab filename
  (`OT-0012-01-contribution-field-and-payoff.md`).
- Each story lives in the parent epic's designated folder under the story's own
  status: a directory named exactly after the epic file. The epic file itself
  lives directly under its own status. Example: a pending epic lives at
  `doc/issues/pending/OT-0012-punishment-round-epic.md`; its pending story lives
  in `doc/issues/pending/OT-0012-punishment-round-epic/`, while a resolved story
  lives in `doc/issues/resolved/OT-0012-punishment-round-epic/`.
- Do not stub every story upfront. Create stories when their scope is settled;
  until then they live only as roadmap bullets in the epic.
- The generated index groups stories directly under a same-status parent and
  links cross-status parents in the Parent column.
- Resolve the epic only after all its stories are closed (`resolved` or
  `wont_fix`) and its initiative-level criteria are complete. Explain any
  won't-fix scope in the epic Resolution. Reopen the epic before adding an
  active child to a completed epic.

## Epic Handoff Workflow

Use this workflow when the user wants a feature split for handoff, especially
when the idea spans constants, models, pages, templates, bots, tests, and formal
docs.

Before writing the epic:

- Align experiment defaults: number of rounds, group size, treatment
  parameters, which values are session-config parameters versus `C` constants,
  currency and payoff units, and explicit out-of-scope items.
- Do a grounding pass across existing tickets, docs, `demo/`, and tests.
- Record current status in the epic: what already exists, what is deprecated,
  and which related tickets may conflict with or depend on this work.
- Split child stories by implementation workstream, not by vague feature area.
  Useful workstreams for an oTree feature:
  - **models** — `C` constants, `Player` / `Group` / `Subsession` fields,
    payoff and grouping functions
  - **pages** — page classes, `page_sequence`, `form_fields`, wait pages,
    `is_displayed` / `vars_for_template`
  - **templates** — the `.html` files and what they render
  - **session config** — `SESSION_CONFIGS`, `PARTICIPANT_FIELDS`,
    `SESSION_FIELDS` in `demo/settings.py`
  - **tests** — logic tests in `tests/`, `PlayerBot` coverage in
    `demo/<app>/tests.py`
  - **docs/promotion** — prototype notes, then promotion to
    `doc/validated-doc/guide/`
- Add a dependency plan to the epic:
  - what must be built first (usually models before pages),
  - what can run in parallel,
  - what should integrate after the field set stabilizes,
  - what docs should wait until validation.
- For each child story, include concrete test modules and scenario logic: setup,
  participant or bot action, expected field mutation, payoff assertion, and
  regression risk.
- For each child story, name the prototype docs and the `doc/validated-doc/guide/`
  docs that should be updated after implementation and validation.
- Create child story files only when their scope is settled enough for another
  agent to execute. Otherwise keep them as roadmap bullets or Open Questions on
  the epic.

## Test Coverage

Any ticket that adds or changes participant-visible behavior or stored data must
plan test coverage in the same delivery. Both layers run under `uv run pytest`
from the repo root (see `CLAUDE.md`).

- **Logic tests** in `tests/` for payoff arithmetic, constants, and field
  values: name the target module, e.g. `tests/test_punishment_payoffs.py`.
  These need a session fixture (`otree_session_factory`) because `Player` and
  `Group` are ORM objects.
- **Bot coverage** in `demo/<app>/tests.py` for page flow: form submission,
  validation errors (`SubmissionMustFail`), wait pages, and page sequence.
  `tests/test_bots.py` picks these up automatically for every session config.
- Add an Acceptance Criteria checkbox naming both when both apply:
  `uv run pytest green — logic tests in tests/test_....py, bot flow in demo/<app>/tests.py.`
- In Details, sketch the test logic: setup, action sequence, expected field and
  payoff assertions.
- Pure-template or copy changes are exempt but must be called out as such; do
  not add empty tests.

## Ticket Content

Follow `.claude/skills/ticket-system/assets/TICKET_TEMPLATE.md` exactly.

- Frontmatter: `id`, `title`, `type`, `status: pending`, `priority`, `created`,
  blank `resolved`, `area`, optional `tags`, `requirement: REQ-XXXX` when the
  ticket has an upstream requirement (drop the line entirely when it does not),
  and `parent` (stories only).
  Use oTree-shaped area slugs: `models`, `pages`, `templates`, `session-config`,
  `bots`, `tests`, `docs`.
- `## Description`: 1-2 sentences: who needs what, and why now.
- `## Details`: concise bullets for current behavior, desired behavior, app and
  page scope, data effect, implementation constraints, and out-of-scope. Include
  an `artifacts/` spike bullet only for tickets that pass the Artifact-Backed
  Tickets threshold above.
- `## Acceptance Criteria`: checkbox lines only, focused on the most important
  verifiable checks. Include:
  `Prototype docs updated when implemented: demo/modules/...` and
  `Spec promoted when validated: doc/validated-doc/guide/...` when known. For new
  prototype features, also include the page-flow child story or epic roadmap
  bullet, the post-validation promotion decision, the artifact checkbox only
  when the ticket passes the threshold, and the `uv run pytest` checkbox when
  behavior or data changes.
- `## Open Questions`: unresolved human decisions, especially the
  `doc/validated-doc/` target if not chosen.
- `## Related Files`: likely implementation/docs paths, backticked.
- `## Handoff Appendix`: optional; use when detailed discussion would otherwise
  be lost.

## High-Detail Handoff Appendix

When the user discussion contains concrete decisions, examples, edge cases, test
cases, page behavior, model fields, or implementation constraints, preserve
those details in the ticket instead of summarizing them away.

Keep the main ticket sections concise. Add `## Handoff Appendix` after
`## Related Files` when needed.

Use this appendix structure:

- `### Settled Decisions` — concrete decisions from the discussion.
- `### Participant Flow Details` — page, form fields, validation, wait-page
  behavior, resulting field changes.
- `### Model And Payoff Notes` — `C` constants, model fields and types, payoff
  arithmetic, grouping, round structure.
- `### Test Scenarios` — specific scenarios and target test modules.
- `### Deferred Decisions` — details intentionally left for a later ticket.

Do not put unresolved questions in the appendix. Keep unresolved questions in
`## Open Questions`. Do not use the appendix as a raw transcript; rewrite
discussion details as implementation handoff notes.

Skip `## Resolution` until the ticket is resolved.

## Refining Tickets

- Preserve `id`, `created`, and filename.
- If title changes, update frontmatter and `# Heading`; do not rename the file.
- AskUserQuestion about existing Open Questions before rewriting them.
- Keep old uncertainty unless the user answers it.
- Regenerate the index only if frontmatter changed.

## Resolving Tickets

A ticket may only move to `resolved` (or `wont_fix`) when its closure is
complete. Before changing the status:

1. Every Acceptance Criteria box is checked — or explicitly rewritten with a
   note explaining why it no longer applies. Never leave a silently unchecked
   box; the `Spec promoted` box in particular is the promotion step, and
   skipping it silently creates handover debt.
2. Add a `## Resolution` section: what was done, what was deliberately not done,
   and which `demo/modules/` and `doc/validated-doc/` files were updated.
3. Fill the `resolved: YYYY-MM-DD` frontmatter date.
4. Regenerate the index. The generator files the ticket and rebuilds
   `doc/issues/promotion-debt.md` — the list of completed tickets that violate
   the rules above. Your resolution must not add a row to that page; ideally,
   remove existing rows while you are there. The page must be empty before
   `doc/validated-doc/` is treated as the settled specification.

## Handoff

End with:

- Ticket id/title/path, and the upstream `REQ-XXXX` if there is one.
- Remaining Open Questions.
- Any visual question left for `artifacts/` to answer.
- Prototype doc target, page-flow story or epic roadmap item, and formal
  `doc/validated-doc/guide/` target.
- Reminder that this skill only writes requirements; implementation should
  happen separately from the ticket.
