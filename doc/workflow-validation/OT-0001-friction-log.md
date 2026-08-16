# OT-0001 — friction log

The record of one end-to-end run of the five-stage workflow in
[CLAUDE.md](../../CLAUDE.md), driven by epic
[OT-0001](../issues/in_progress/OT-0001-workflow-validation-run.md).

Appended by each story **while the confusion is fresh**, not reconstructed
afterwards. One entry per friction point: which stage, what `CLAUDE.md` or the
skill said, what the operator actually did, and what would have prevented the
guess. Successes are recorded too — a verdict built only from complaints is not
a verdict.

Nothing here is fixed during the run. Story `OT-0001-08` drafts a ticket
carrying every change the log justifies.

**Legend** — `GAP`: the docs did not say. `STALE`: the docs said something no
longer true. `BLOCKER`: the run could not proceed as written. `OK`: the docs
were followed literally and worked.

---

## Stage 0 — scaffolding (`OT-0001-01`)

Ran 2026-08-15.

### F-01 · `GAP` · The workflow has no stage for project setup

- **What the docs say.** The workflow table lists five stages, the earliest of
  which is "Requirement". Stage 4 is marked *Always* and its home is `demo/`,
  but nothing anywhere says how `demo/` comes to exist. `CLAUDE.md#structure`
  describes the layout as a fact about the repo, not as something a stage
  produces.
- **What the operator did.** Followed the epic's own story `OT-0001-01`, which
  exists only because the epic author noticed the gap in advance. A new user
  starting from a genuinely empty repo would have no ticket telling them to do
  this, and no stage to file the work under.
- **What would have prevented it.** Either a stage 0 in the workflow table, or
  one line under `## Structure` saying that scaffolding is ordinary stage-4 work
  that precedes the first feature.
- **Confirms** the epic's suspected gap "No stage covers project scaffolding".

### F-02 · `STALE` · The structure tree is the only spec for the skeleton, and it describes a deleted app

- **What the docs say.** `CLAUDE.md#structure` shows `demo/settings.py`,
  `demo/public_goods_simple/` with four files, `demo/modules/README.md`,
  `demo/modules/page-flow.md`, and `demo/_static/global/empty.css`.
- **What the operator did.** Used that tree as the build spec — it is the only
  description of the layout in the repo — while ignoring the three
  `public_goods_simple/` rows, because the epic forbids restoring the sample.
  Reverse-engineering a skeleton from a tree that documents a deleted app means
  every row has to be individually judged as "still true" or "gone".
- **What would have prevented it.** The tree distinguishing what oTree
  *requires* from what the sample app *happened to contain*.
- **Confirms** the epic's suspected gap "`CLAUDE.md` and
  `doc/validated-doc/data-schema/` describe a deleted app".

### F-03 · `STALE` · `demo/__init__.py` is absent from the structure tree

- **What the docs say.** Nothing. The `## Structure` tree does not list
  `demo/__init__.py`, and no prose mentions it.
- **What the operator did.** Created it because story `OT-0001-01` said to
  ("empty, as it was before deletion"). Its purpose is still unexplained — oTree
  does not require it, since the project root is a working directory rather than
  an importable package.
- **What would have prevented it.** Either listing it in the tree with a reason,
  or establishing that it is unnecessary and dropping it.

### F-04 · `BLOCKER` · An orphaned test file stopped `pytest` from collecting, and no document mentions it

- **What the docs say.** `CLAUDE.md#tests` names `tests/test_public_goods_payoffs.py`
  in its structure tree as a current file. Story `OT-0001-01` lists
  `tests/conftest.py` and `tests/test_bots.py` under Related Files but not that
  file, and its acceptance criteria simply require `uv run pytest` to pass.
- **What the operator did.** `tests/test_public_goods_payoffs.py` does
  `from public_goods_simple import C, set_payoffs` at module scope, so pytest
  could not collect *anything* while the app was missing — the criterion was
  unreachable, not merely failing. Deleted the file, and deleted the
  `public_goods_session` fixture in `tests/conftest.py` that existed only to
  serve it. Both are orphans of the epic's deliberate starting state rather than
  of any change made here, so the deletion is a judgment call the ticket did not
  authorize in writing.
- **What would have prevented it.** The story naming the orphaned test file and
  the fixture explicitly, the same way it named the orphaned schema doc.
- **Note for `OT-0001-08`.** This is a second stale-reference site beyond the two
  the epic anticipated: the fix ticket must repair `CLAUDE.md#tests` as well as
  `CLAUDE.md#structure`.

### F-05 · `GAP` · `schema-writer` has no pruning behavior and had to be told the app was gone

- **What the docs say.** `SKILL.md` lists the files the skill owns as
  "`<app_label>.md` — one per package in `demo/`", and step 2 enumerates apps
  from `demo/` and `SESSION_CONFIGS`. Its step-7 verification checks that "no
  field documented that no longer exists in source" — about fields *within* an
  app. Nothing says what to do with a whole doc whose app has disappeared.
- **What the operator did.** Invoked the skill with the fact stated up front
  ("the previously documented `public_goods_simple` app has been deleted"), so
  the run is **not clean evidence** that the skill prunes unprompted. Deleting
  `public_goods_simple.md` and its index row was inferred from "one per package
  in `demo/`", not read off an instruction. Wrote a change-log line in the index
  recording the removal, which is also unspecified behavior.
- **What would have prevented it.** One line in the skill's procedure: after
  enumerating apps, delete any `<app_label>.md` with no matching package, drop
  its index row, and note the removal in the change log.
- **Partly confirms** the epic's suspected gap on pruning. Story `OT-0001-05`
  gets the clean test — it deletes `scaffold_check` and must invoke the skill
  **without** mentioning the removal.

### F-06 · `GAP` · `localhost:8000` is hardcoded and was already in use

- **What the docs say.** `CLAUDE.md#commands` and `CLAUDE.md#visual-qa` both
  give `http://localhost:8000` as a fixed address.
- **What the operator did.** Port 8000 was occupied by an unrelated application
  of the user's. `otree devserver` fails to bind and exits, so the acceptance
  criterion "the admin UI loads at `http://localhost:8000`" is not satisfiable
  without stopping someone else's process. Ran `otree devserver 8001` instead
  and verified there. `otree`'s positional port argument is not documented in
  `CLAUDE.md`.
- **What would have prevented it.** `CLAUDE.md#commands` noting the port
  argument and that the address is a default, not a requirement.

### F-07 · `BLOCKER` (deferred) · No browser tooling exists in this environment

- **What the docs say.** `CLAUDE.md#visual-qa` says "Use the browser tooling
  available in the current agent environment", and `CLAUDE.md#visual-variants`
  requires each variant screenshotted at 1555×885 into `shots/`. The epic's
  acceptance criteria require the app to be "**seen working** in a browser at
  1555×885, not only tested".
- **What the operator did.** There is no browser tool in this environment — no
  screenshot capability, no page driver. Stage 0 only needed "the admin UI
  loads", which was verified over HTTP: `GET /demo` returned 200 and listed the
  `scaffold_check` session config, and the bot test renders and submits
  `Hello.html` through oTree's real request stack.
- **Why it is logged now.** HTTP checks substitute for stage 0. They cannot
  substitute for stage 3, where the deliverable *is* a screenshot the user looks
  at, nor for the epic's promotion gate. Stage 3 will stall unless the operator
  supplies the screenshots or the requirement is relaxed.
- **What would have prevented it.** `CLAUDE.md#visual-qa` naming the specific
  tool it expects and what to do when it is absent.

### F-08 · `OK` · The placeholder-app reasoning was sound and needed no interpretation

The story's argument — that an empty `SESSION_CONFIGS` makes `tests/test_bots.py`
collect zero cases and report success, so the scaffold needs a real app — held
exactly as written. `OTREE_APPS` is built from every session config's
`app_sequence`, so a config naming a nonexistent app breaks startup. Building
`demo/scaffold_check/` from that paragraph required no guessing, and the
resulting `uv run pytest` run collects 1 test that genuinely exercises the page.

### F-09 · `OK` · The ticket generator behaved exactly as documented

`uv run python .claude/skills/ticket-system/scripts/generate_issues_index.py`
ran clean. Changing `status: pending` to `status: in_progress` on the epic and
the story moved both files into `doc/issues/in_progress/`, kept the still-pending
story `OT-0001-02` under `doc/issues/pending/<epic-folder>/`, and rewrote the
index — the mixed-status epic behavior described in `ticket-system/SKILL.md`,
observed working on the first try. No file was moved by hand.

### F-10 · `OK` · The `db.sqlite3` version gotcha did not fire

`CLAUDE.md#tests` warns that a database left by a different oTree version aborts
the run. `demo/db.sqlite3` did not exist at the start (it is gitignored and the
tree was clean), so the warning was never exercised. Recorded as untested rather
than as working.

---

## Stage 1 — requirement (`OT-0001-02`)

Ran 2026-08-15. Four `AskUserQuestion` rounds, twelve questions, one draft
requirement (`REQ-0001`). Not yet settled — see F-12 and F-17.

### F-11 · `OK` · Stage 1 caught a misreading that the ticket had already baked in

The single most valuable thing that happened in the run so far. Both the epic
and story `OT-0001-02` assumed "network setting" meant a **fixed topology** —
the epic asks "who each player is connected to, whether the topology is fixed or
varies", and the story lists "whether the structure is fixed for the whole
session or changes" as a gap to close.

The researcher's very first answer reframed it: *"this is repeated, every round,
they are paired randomly, so the network history is important for their
decision."* The network is not a wiring diagram at all — it is the accumulated
record of who met whom, with links redrawn every round. An implementer who had
skipped stage 1 and built from the ticket's own framing would have built the
wrong experiment.

This is direct evidence that stage 1 earns its place, and that the rule
"nothing upstream of `REQ-0001` may settle the design" was the right call.

### F-12 · `GAP` · The skill has no route for a researcher who knows the design but not the hypothesis

- **What the docs say.** `SKILL.md` lists Purpose first under "What must be
  pinned down": *"If you cannot say what the experiment is for, everything
  downstream is guesswork."* The template's first section is
  `## What we are trying to learn`, and it is not optional. `## Open questions`
  is offered for unanswered questions, but Readiness does not say whether an
  unpinned purpose blocks settling.
- **What the operator did.** Asked the purpose question twice. The first time
  the researcher answered with a *design fact* rather than a purpose; the second
  time they chose "Not sure — leave it open" outright, from three concrete
  candidate hypotheses. Wrote the design in full, wrote
  `## What we are trying to learn` as a description of the mechanism plus an
  explicit "the hypothesis is not yet decided", and put the three candidates in
  `## Open questions`.
- **Why it matters.** Everything downstream is buildable — the design is fully
  specified and every number has a value. But nothing tells the operator whether
  a requirement with no hypothesis may be *settled*, or must stay a draft. The
  guardrail "a draft is not a basis for a ticket" (`ticket-system/SKILL.md`)
  makes this decision expensive, and the skill gives no rule for it.
- **What would have prevented it.** Readiness naming which boxes are hard gates
  and which can be waived with the user's agreement.

### F-13 · `STALE` · `SKILL.md` and the template disagree about a section that does not exist

- **What the docs say.** `SKILL.md` lists "**Conflicts with what exists** —
  anything here that contradicts the current `demo/` app or a promoted spec,
  called out plainly" as one of the nine things that must be pinned down, and
  says each "maps to a section of the template". Story `OT-0001-02` goes
  further: *"`## Conflicts with what exists` is a live section here."*
- **What the operator did.** `assets/REQUIREMENT_TEMPLATE.md` has **no such
  section**. Conflicts appear only as a bullet inside `## Translation notes`
  ("Existing behavior this touches or conflicts with"). The skill's writing
  instructions say "template sections exactly", so the template won: the
  conflicts finding went into that bullet. The story's expectation of a
  top-level section could not be met.
- **What would have prevented it.** Either adding the section to the template or
  amending `SKILL.md` to say conflicts live inside the translation notes.

### F-14 · `OK` · "I don't know, show me" was handled correctly and never sketched

The skill says an undecidable-in-words answer is "a valid, expected answer — not
a gap to be filled with prose". The operator offered *"I don't know — show me
the options"* as an explicit choice on the topology question; the researcher
took it. It went straight to
`## Visual questions for the artifact stage`, phrased as a choice between three
named arrangements, with nothing sketched, drawn, or described as a layout. Two
further visual questions surfaced the same way. The requirement states stage 3
is required on both `CLAUDE.md` triggers, so stage 2 inherits an easy call — the
outcome story `OT-0001-02` was hoping for.

### F-15 · `OK` (weakly) · `scaffold_check` was not treated as prior art

`## Translation notes` reports "**none**" for existing behaviour and names
`scaffold_check` as disposable scaffolding that supplies no pattern. But this is
**weak evidence**: the same operator had built `scaffold_check` an hour earlier
in story `OT-0001-01` and knew exactly what it was. A fresh agent reading only
`demo/` and `doc/validated-doc/data-schema/` would find an app with a doc, an
index row, and a session config, and the word "disposable" in a Notes section it
may not read. Not the blind test the story wanted.

### F-16 · `OK` · App naming stayed out of the interview

The researcher was never asked to name an identifier. The proposed name
(`network_public_goods`) appears only in `## Translation notes`, flagged as
stage 2's to confirm, and nowhere in the researcher-facing body — exactly as
story `OT-0001-02` required.

### F-17 · `GAP` · Writing the translation notes revealed a design hole, and the skill's rule for that is impractical

- **What the docs say.** `SKILL.md`, on translation notes: *"If writing the
  notes reveals a gap, go back and ask."*
- **What the operator did.** Working out the payoff arithmetic exposed a real
  problem the researcher could not have foreseen: with a multiplier of 2, a
  participant who has exactly **one** link gets their entire contribution back,
  so contributing becomes free and the public-goods dilemma disappears for that
  person. This is a direct consequence of two separately-reasonable answers
  ("doubled" and "shared among you and your links") and only appears when the
  two are multiplied together.
  Rather than reopen the interview, the operator wrote the arithmetic out as a
  worked example, stated the consequence plainly, and turned it into a
  **constraint on the artifact stage** — any arrangement that can produce a
  degree-1 player must either avoid it or accept it deliberately.
- **Why "go back and ask" was the wrong move.** The question is not answerable
  in participant language. Asking a researcher "should the multiplier be 2 or
  should nobody ever have exactly one link?" requires them to hold the
  arithmetic in their head — precisely what the skill says is the agent's job.
  Deferring it to variants the researcher can *look at* is more faithful to the
  skill's own philosophy than obeying its literal instruction.
- **What would have prevented it.** The skill distinguishing a gap in *what the
  user wants* (go back and ask) from a consequence of *what they already said*
  (surface it, and route it to the stage that can show it).

### F-18 · `GAP` · The skill's guardrails cover inventing, but not the reverse

`## What we are not building` required "at least one tempting nearby feature,
named and excluded". Four candidates were offered; the researcher excluded only
punishment. The other three — participant-chosen links, chat, and a
fixed-partner control — were neither asked for nor ruled out. Not-excluded is
not the same as in-scope, and the skill says nothing about how to record that
middle state. The operator wrote them into `## What we are not building` as
explicitly *not excluded and not being built*, plus an open question. Both
alternatives (silently dropping them, or listing them as out of scope the
researcher never chose) would have misrepresented the conversation.

### F-19 · `?` · Borderline vocabulary leak: "round"

The skill's table forbids asking "What is `C.NUM_ROUNDS`?" and prescribes "Do
they do this once, or repeat it?". The operator asked "How many times do they go
through this?" — compliant — but every answer option used the word *round*
("10 rounds, known in advance"), and the word appears throughout the
requirement. *Round* is standard experimental-economics vocabulary rather than
oTree vocabulary, and the researcher used it comfortably, so this is recorded as
observed-and-judged-acceptable rather than as a violation. Worth a ruling in the
fix ticket, since the same argument could be stretched to cover *treatment*,
*endowment*, and *matching*.

### F-20 · `OK` · The skill stopped at the handoff

No attempt to chain into `ticket-system`. `doc/requirements/` was the only
directory written to; `demo/`, `tests/`, `artifacts/`, and
`doc/validated-doc/` were untouched by this story.

---

## Stage 2 — tickets (`OT-0001-03`)

Ran 2026-08-15. One `AskUserQuestion` round, three questions. Produced epic
`OT-0002` plus two child stories; five more stay roadmap bullets.

### F-21 · `BLOCKER` (resolved by judgment) · `ticket-system/SKILL.md` contradicts itself about `doc/requirements/`

- **What the docs say.** Guardrails: *"Do not edit `doc/requirements/`. That is
  stage 1, owned by the `refine-requirement` skill."* Upstream Requirement, four
  paragraphs later: *"Put `requirement: REQ-XXXX` in the ticket frontmatter and
  **add the ticket's id to the requirement's `tickets:` list**."* The second
  instruction cannot be carried out without breaking the first.
- **What the operator did.** Treated the specific instruction as a narrow
  exception to the general guardrail and edited only the `tickets:` frontmatter
  key, touching no prose. The requirement's `tickets:` list now reads `OT-0002`.
- **What would have prevented it.** The guardrail carrying its own exception:
  "never edit requirement prose; the `tickets:` frontmatter list is the sole
  exception."

### F-22 · `GAP` · "Settled but incomplete" has no rule, and it is the case that actually occurred

- **What the docs say.** Upstream Requirement handles exactly two states. A
  settled `REQ-XXXX`: read it and write the ticket. A draft: *"Say so and stop.
  Drafts have open questions by design; building a ticket on one buries them."*
- **What the operator did.** `REQ-0001` is `settled` **and** carries four open
  questions, including no hypothesis at all. The skill's reasoning for stopping
  on drafts — open questions get buried — applies here, but its trigger
  (`status: draft`) does not. Proceeded, on the grounds that the design is
  complete and every number has a value, and carried all four open questions
  onto the epic with a note that the missing hypothesis blocks promotion
  (`OT-0002-07`) but not the build.
- **What would have prevented it.** The rule keying on the *presence of open
  questions* rather than on the status field, and saying which kinds block a
  ticket.
- **Relates to F-12**, which is the same hole seen from stage 1's side.

### F-23 · `OK` · The stage-2 → stage-3 handoff gap did not materialise

The epic listed as a suspected gap: *"the stage-2 → stage-3 handoff depends on
the ticket making a call the ticket author may not have enough information to
make."* It was a non-event. `REQ-0001` stated both `CLAUDE.md` triggers
explicitly, so `OT-0002` restated them, named the spike folder, said what the
spike must demonstrate, and carried the required acceptance-criteria checkbox —
with nothing to weigh up.

Worth stating precisely: this gap is **contingent on requirement quality, not
structural**. Stage 2 had an easy call because stage 1 made it easy. A vaguer
`REQ-0001` would have reproduced the suspected gap exactly.

### F-24 · `GAP` (mild) · The requirement alone was not sufficient, and one gap was one stage 1 had already found

Three questions had to be asked before the epic could be written: the
`doc/validated-doc/guide/` target, the MVP scope, and what to do about the
degree-1 problem. The first two are ordinary stage-2 business — `SKILL.md`
prescribes asking about the spec target explicitly.

The third is more interesting. The degree-1 problem was **discovered at stage 1**
while writing translation notes (F-17), recorded faithfully as a constraint, and
then *not decided* — `REQ-0001` says the variants "must either avoid or
deliberately accept" it. So stage 1 surfaced a problem it could not resolve in
participant language, and stage 2 inherited the decision. That is probably the
right division of labour, but no document says so.

### F-25 · `GAP` · A stage-2 answer overrode a settled stage-1 requirement, and the workflow's rule for that points backwards

**The most consequential finding of stage 2, and it is unresolved as this story
closes.**

- **What happened.** Asked how to treat the degree-1 problem, the user chose
  "hard constraint — rule it out": every arrangement must give each participant
  at least two links. That eliminates **hub-and-spokes**, which `REQ-0001` names
  as one of three concrete alternatives for stage 3 to build.
- **Why it is defensible.** `REQ-0001` explicitly delegated the choice
  ("must either avoid or deliberately accept"). The user resolved a question the
  requirement left open rather than reversing one it had settled.
- **Why it is still a problem.** `REQ-0001`'s prose continues to name
  hub-and-spokes as a variant to build. `OT-0002` says it will not be built. A
  reader of the requirement alone would now be misled, which is exactly the
  divergence `CLAUDE.md` names: *"Code diverging from its requirement, ticket, or
  validated doc is a defect in the docs as much as in the code. Fix both in the
  same turn, or say plainly which one you left behind."*
- **What the docs say to do.** `CLAUDE.md`: *"A requirement that turns out to be
  wrong gets corrected at stage 1, not silently overridden downstream."*
  `ticket-system/SKILL.md`: *"If the requirement turns out to be wrong or
  incomplete, say so and send the user back to that skill rather than patching
  the gap inside the ticket."* Both point the same way — back to
  `refine-requirement` — and the skill running at the time is forbidden from
  doing it.
- **What the operator did.** Did **not** patch `REQ-0001` from inside
  `ticket-system`. Stated the divergence in this entry and in the story's
  resolution, and left the stage-1 correction as the next action.
- **What this measures.** This is the epic's "work moving backward" question
  arriving early and unplanned, in pass one rather than in the second pass. The
  workflow gave a clear and correct instruction; what it does not give is a
  *mechanism* — no stage owns "a downstream decision invalidated part of an
  upstream doc", and nothing in the ticket store records the debt.

### F-26 · `OK` · "Do not stub every story upfront" was easy to apply

`SKILL.md` says to create stories only when their scope is settled. Two of seven
qualified: the artifact story, and the constants/fields/payoff story — the
latter because the payoff rule takes an adjacency as input and does not care
where it came from, so its tests can set one by hand and run before the
arrangement exists. The other five depend on the unchosen arrangement or the
unchosen screen design, and stayed roadmap bullets in the epic's table. The rule
drew a clean line with no interpretation needed.

### F-27 · `OK` · The epic reads as ordinary work

`OT-0002` contains no reference to `OT-0001`, the friction log, or the fact that
a workflow validation run is happening. Someone picking it up would see a normal
feature epic with an upstream requirement.

### F-28 · `OK` · The backward path works, but only because someone walked it deliberately

Immediately after `OT-0001-03` closed, the F-25 divergence was repaired the way
`CLAUDE.md` prescribes: `refine-requirement` in refine mode on `REQ-0001`, not a
hand edit and not a downstream override.

What the correction did:

- Added **rule 12** — "No participant ever holds fewer than two links" — carrying
  the date and a note that it was previously delegated to the artifact stage.
  **Appended as rule 12 rather than inserted** near the other link rules,
  because `OT-0002-01` already cites `REQ-0001` rules 5, 6, 7 and 10 by number;
  inserting would have silently broken four cross-references.
- Replaced hub-and-spokes with the **diamond** in the visual question, with an
  inline *Revised 2026-08-15* note saying what changed and why. The question
  itself — which arrangement, chosen by looking — is unchanged.
- Rewrote the worked example's closing line from "the variants must avoid or
  accept this" to "rule 12 rules this out".
- Split the numbers table row into a settled floor of 2 and an open value above
  it.

`REQ-0001` and `OT-0002` now agree, and no reference broke.

**Three gaps this exposes, none of them fatal:**

- **The template has nowhere to record a change.** `REQUIREMENT_TEMPLATE.md` has
  no change-log section, and `refine-requirement/SKILL.md` says to "note what
  changed and why" without saying where. The note went inline, next to the thing
  that changed, which is arguably better than a log at the bottom — but it was
  the operator's invention, not the template's.
- **Rule numbering is load-bearing and nothing says so.** Tickets cite rules by
  number, so requirement rules are effectively an append-only list. Renumbering
  is a silent breaking change with no tooling to catch it. Nothing in either
  skill mentions this.
- **The debt was never recorded anywhere durable.** Between `OT-0001-03` closing
  and the correction landing, the only trace that `REQ-0001` contradicted
  `OT-0002` was prose in a resolution section and this log. Had the run stopped
  there, nothing would have surfaced it: the ticket store has no concept of a
  requirement needing a correction, `promotion-debt.md` tracks only closure
  hygiene, and the generator cannot see requirements at all.

The workflow's *instruction* for moving backward is clear and correct. What it
lacks is a *mechanism* — the correction happened because the operator chose to
walk back, not because anything would have complained if they hadn't.

---

## Stage 3 — artifact (`OT-0001-04`)

Ran 2026-08-15. **The stage did not execute.** Blocked on tooling; skipped by
the user's decision after being offered the alternatives.

### F-29 · `BLOCKER` · Stage 3 cannot run without a browser, and `CLAUDE.md` assumes one exists

- **What the docs say.** `CLAUDE.md#visual-variants` makes the screenshot the
  deliverable, not an accessory to it: build the variants, "screenshot each at
  the standard viewport (**1555 × 885**) into `shots/`", "present them together
  and ask the user to choose". `CLAUDE.md#visual-qa` says only "use the browser
  tooling available in the current agent environment" — assuming some is.
- **What the operator did.** There is none. Presented the user with three
  routes: build the variants for local viewing in their own browser; describe
  the variants in writing and let them choose by reading; or skip the stage and
  log it. **The user chose to skip and log.** No variants were built —
  producing three HTML files nobody would look at is worse than an honest gap.
- **What would have prevented it.** `CLAUDE.md#visual-qa` naming the tool it
  expects and stating the fallback when it is absent. This was flagged as a
  deferred blocker at stage 0 (F-07) and arrived exactly as predicted.

### F-30 · `GAP` · There is no `blocked` status, so a blocked ticket must lie

`OT-0002-01` needed to leave the active set without claiming completion or
abandonment. The generator recognises `pending`, `in_progress`, `resolved`, and
`wont_fix` only. `pending` would stall `OT-0002` indefinitely — the epic cannot
resolve until its stories close. `resolved` would be false. `wont_fix` was used
and **overstates the finality**: the work is worth doing and should be reopened
if tooling appears.

The acceptance criteria were rewritten with notes rather than ticked, per
`ticket-system/SKILL.md`'s rule against silently unchecked boxes, so
`promotion-debt.md` stays empty and the record stays honest. But the status
field itself now says something untrue.

### F-31 · `GAP` · Nothing distinguishes a decision made by looking from one made for convenience

The arrangement was picked by the **operator on implementation grounds** — ring,
because it is symmetric and easiest to assert against. `REQ-0001` assigns this
choice to the researcher explicitly, and the rejected **diamond** is the only
surviving arrangement where position is measurable, which is close to what the
researcher was asking about when they wondered whether some participants should
be better connected than others.

`DECISION.md` says all of this plainly, because the operator chose to write it
that way. Nothing in `CLAUDE.md` or the skills requires a `DECISION.md` to
record *who* decided or *on what basis*. A future reader of a terser
`DECISION.md` would see "ring — symmetric, simplest" and have no way to tell
that the researcher never saw the alternatives.

**Suggested for the fix ticket:** `DECISION.md` should carry who chose and on
what evidence, so a convenience pick cannot be mistaken for a design decision.

### F-32 · `?` · Two visual questions were silently absorbed, not answered

`REQ-0001` parked three things for stage 3: the arrangement, how the network is
drawn on the decision screen, and how nine rounds of itemised history for up to
three partners fit alongside it. Skipping the stage answered the first badly and
the other two not at all — stage 4 will now decide both by default, at full
load, having never seen them.

The third is a genuine layout problem that the artifact stage existed to catch
early. Recording it here so the stage-4 entry can report whether it caused
trouble, which is the only way this run learns what stage 3 was worth.

---

## Stage 4 — prototype (`OT-0001-05`)

Ran 2026-08-15. The app was built, tested, and observed running end to end.

### F-33 · `OK` · `schema-writer`'s automatic trigger is unambiguous

`CLAUDE.md` says to fire it "without being asked, as the last step of the same
turn" after touching `demo/<app>/__init__.py` or `SESSION_CONFIGS`. Both
happened, the trigger list named them explicitly, and the skill ran without any
judgment call about whether it applied. Nothing to interpret.

### F-34 · `GAP` (confirmed cleanly) · `schema-writer` does not prune

The clean re-test F-05 asked for. `demo/scaffold_check/` was deleted and the
skill invoked with a deliberately neutral prompt — *"demo/ has changed — refresh
the data-schema docs"* — with no mention that an app had gone.

Following the procedure literally: step 2 enumerates apps from `demo/` and
`SESSION_CONFIGS`, and finds one. Step 6 updates the index, so the row goes.
**Nothing in the procedure addresses the orphaned `scaffold_check.md` file.**
Deleting it was inferred from "Files this skill owns: `<app_label>.md` — one per
package in `demo/`". Confirmed: the pruning gap is real and the fix ticket should
close it.

### F-35 · `GAP` · Stage 4 discovered a requirement defect, and the workflow has no name for that

`REQ-0001` rule 8 said a contribution is "shared **evenly**". Points are whole
numbers, so this is not achievable: 50 into a neighbourhood of three gives three
shares of 33, not 33.33, and the remainder evaporates — 4 points per round, 40
over a session, if everyone contributes 50.

Nobody could have caught this at stage 1. It is not a mis-stated intention; it is
an arithmetic impossibility that only appears when the rule meets integer
currency. The same *shape* as F-17 and F-24: a later stage discovering something
an earlier stage could not have known.

**What was done:** the behaviour was pinned by a test named for it, documented in
`demo/modules/README.md` and the data-schema Notes, and — for consistency with
how F-25 was handled — `REQ-0001` rule 8 was **amended at stage 1** to say "as
evenly as whole points allow", with the discovery noted inline and the real
question ("is losing the remainder acceptable?") added to `## Open questions`.

**The gap:** `CLAUDE.md` covers a requirement that "turns out to be wrong". It
says nothing about a requirement that turns out to be *unimplementable as
written* — which is a different thing, arrives from a different direction, and
happened twice in this run.

### F-36 · `GAP` · The code was written before four of its tickets existed

`OT-0002` correctly left stories 03–06 as roadmap bullets, since their scope
depended on the arrangement. When the arrangement was settled (badly — see F-31)
their scope became settled too, and the correct move was to write the stories,
then implement. Instead the whole app was built in one pass and the four stories
were written afterwards, as records of completed work.

The resulting tickets are accurate, and the MVP decision ("the whole thing",
settled with the user) made a single build pass reasonable. But the tickets did
not *drive* the work, and nothing in the workflow noticed or would have. A
reviewer reading only the ticket store cannot tell the difference between a
story that specified work and a story that described it afterwards.

### F-37 · `?` · The "seen working" gate was met in spirit, not in letter

The epic requires the app "**seen working** in a browser at 1555×885, not only
tested". With no browser, the substitute was a full HTTP walkthrough: a session
created through the running server's REST API, then four participant sessions
driven through all thirty page loads, with the rendered HTML inspected at rounds
1 and 10 and the payoff checked against hand arithmetic (100 kept + 0 own + 67 +
20 = 187, matching the page).

That is arguably *stronger* evidence of correctness than a screenshot — it
exercised the real request stack, real templates, and real payoff code, and
confirmed rule 10 held in observation. It is *weaker* evidence of the thing the
gate is actually about: whether the screen is any good to look at. Both readings
should be recorded, and the fix ticket should say which one the gate means.

### F-38 · `STALE` · The devserver holds its database in memory, and only the test docs say so

`CLAUDE.md#tests` explains `OTREE_IN_MEMORY` as a property of the pytest setup.
It is also true of `otree devserver`: a session created by an external script
against `demo/db.sqlite3` is **invisible** to the running server, which returns
404 on the participant start link. Twenty minutes went into that before the
session was instead created through the server's own REST API
(`POST /api/sessions`).

Nothing in `CLAUDE.md#commands` or `#visual-qa` warns of it, and it will hit
anyone who tries to script a participant walkthrough. Related: the REST export
endpoints require auth that is not documented either;
`otree test <app> --export <dir>` is the working path and deserves a line in
`CLAUDE.md#commands`.

### F-39 · `OK` · The stage-4 doc split was clear

`CLAUDE.md#two-doc-homes` draws the line at "written for the next agent" versus
"written for the researcher", and it held under load. Everything that wanted
writing during implementation — why the network is not an oTree grouping, why
links are drawn in `creating_session`, why the diamond test must not be deleted,
what the `links` encoding is — is plainly agent-facing and went to
`demo/modules/`. No judgment call was needed, and nothing implementation-shaped
was tempting to promote.

---

## Stage 5 — promotion (`OT-0001-06`)

Ran 2026-08-15. Promoted to `doc/validated-doc/guide/network-public-goods.md`.

### F-40 · `OK` · The "never promote implementation detail" rule was easy to obey

`CLAUDE.md`: *"Class names, function signatures, and template internals belong
in stage 4 and never get promoted — a stage 5 doc that only makes sense to
someone reading the code has promoted the wrong thing."*

Applied without difficulty. The guide names no class, no field, no function and
no file under `demo/`. Everything that wanted saying — why the network is not an
oTree grouping, the `links` encoding, why the diamond test must survive
refactoring — was obviously agent-facing and stayed in `demo/modules/`. The
test the rule proposes works: read the promoted doc as someone who has never
opened the code, and see whether it still means anything.

### F-41 · `GAP` · Nothing says what to do with a validated doc full of open decisions

The promoted guide carries a five-row table of unsettled decisions: the
hypothesis, the arrangement, the rounding losses, the conversion rate, and
whether connections are mutual. Two of those (hypothesis, arrangement) go to the
heart of what the experiment is.

`CLAUDE.md` says stage 5 is "what the researcher needs to know" and fires "when a
requirement settles". `REQ-0001` **is** settled, the prototype **is** validated,
the tests **are** green, and the behaviour **has** been observed — every stated
gate is met. Yet the honest promoted document is one that tells the researcher
their experiment is not ready to run.

Writing it that way was the operator's call. The alternative readings are that
promotion should have been withheld, or that the open decisions should have been
resolved first. Nothing in the workflow distinguishes "validated" from "ready",
and this run suggests they are not the same thing.

### F-42 · `?` · Stage 5 inherited a decision nobody made, and had to say so

The most awkward paragraph in the promoted guide is the one admitting the ring
was chosen by an implementer for convenience rather than by the researcher from
alternatives — and that a diamond may be the better design.

That paragraph exists because the artifact stage was blocked (F-29) and because
`DECISION.md` was written honestly enough to carry the fact forward (F-31). With
a terser `DECISION.md`, stage 5 would have promoted "the network is a ring" as a
settled design decision, and the fact that nobody chose it would have been lost
permanently at exactly the point where the document becomes authoritative.

This is the clearest argument in the whole run for F-31's suggestion: a
`DECISION.md` should be required to record **who** decided and **on what
evidence**.

---

## Second pass — a changed requirement (`OT-0001-07`)

Ran 2026-08-15. The change was chosen by looking at the running app, then driven
back through the chain from stage 1.

**The change.** Watching round 10 render, the history table read "player 1 gave
100 in round 3" with no indication whether any of it reached the viewer. Because
links reshuffle every round, a partner's past generosity may have gone entirely
to other people — so reciprocity and general generosity were indistinguishable on
screen. That is the thing the design exists to observe, and it was invisible.

### F-43 · `OK` · The correction started at stage 1, and the pressure to skip it was real

`CLAUDE.md`: *"A requirement that turns out to be wrong gets corrected at stage 1,
not silently overridden downstream."*

It would have been faster to change `partner_history()` and the template and be
done — the whole change is fifteen lines of Python and a table cell. Nothing
would have caught the shortcut. The stage-1 amendment took longer than the code.

But going through stage 1 **changed the outcome**. Writing rule 7's amendment
surfaced a conflict the implementer would never have hit: marking a past round
raises the question of whether to show *who else* that partner was linked to, and
that would leak information about players the viewer is not currently linked to —
a direct collision with rule 10. Asked, the researcher chose to keep rule 10
intact, which settled the design as the minimal marker rather than the richer one.

A code-first change would have picked whichever was easier to write and never
noticed it was making a policy decision about participant privacy.

### F-44 · `OK` · The workflow gave a clear answer on which stages to revisit

The epic asked whether the workflow makes this call cleanly. It did.

- **Stage 1** — required, and productive. See F-43.
- **Stage 2** — a standalone `improvement` ticket, `OT-0003`, not an epic. The
  ticket-system rules for "settled `REQ-XXXX` exists" applied without ambiguity.
- **Stage 3** — **skipped**, with the one-line reason `CLAUDE.md` demands: a
  marker added to an existing table on an existing page, following the pattern
  already there. The researcher settled *what* the history must distinguish; how
  the marker is drawn is not a choice made by looking. The conditional was easy
  to apply in the skip direction, which the first pass never tested — stage 3
  fired on both triggers there, and was blocked rather than skipped.
- **Stage 4** — required. Implemented, tested, observed.
- **Stage 5** — required, because the change alters what a participant can know,
  which is a design fact rather than an implementation detail.

### F-45 · `OK` · The sync rule held, and the chain caught a stale doc

After the change, `REQ-0001`, `OT-0003`, `demo/`, `demo/modules/`,
`doc/validated-doc/data-schema/` and `doc/validated-doc/guide/` all agree. No
divergence was left behind.

The pass also caught documentation that had gone stale from the *first* pass:
`demo/modules/README.md` asserted that historical adjacency was not needed. It
had been true when written and was made false by `OT-0003`, which reads past
rounds' `links` to derive the marker. Corrected in the same change, as
`CLAUDE.md` requires.

### F-46 · `OK` · No new stored data, because the first pass happened to store enough

The marker needed each past round's adjacency. It was already there — `links` is
written per player *per round*, so round *r*'s network is just round *r*'s rows.
No migration, no new field, no change to the export.

Worth recording as luck rather than foresight. `OT-0002-02` chose per-round
storage because the payoff rule needed the current round's links and oTree
happens to store a row per round anyway. Had the adjacency been stored once per
session, this change would have been considerably larger.

### F-47 · `GAP` · The second pass had no ticket until after it ran

Same shape as F-36. `OT-0001-07` existed only as a roadmap bullet in the epic,
and by design — the epic says the change is chosen once the app exists. But that
means the story describing the second pass was written **after** the pass, from
the same operator's memory.

The friction-log rule ("appended while the confusion is fresh, not reconstructed
afterwards") was followed for the log itself. The ticket was not, and nothing in
the workflow distinguishes the two.

---

## Consolidation (`OT-0001-08`)

Ran 2026-08-15. Fix ticket drafted as `OT-0004`, filed pending.

### F-48 · Settling the standing question about this folder

`doc/workflow-validation/` should be the **standing home for workflow
meta-work**, not an archive of this one run.

The argument is this log's own second half. Roughly a third of its entries are
`OK` — records of rules that worked and needed no interpretation. Those are only
useful if something later contradicts them, which requires the folder to outlive
the run that produced it. F-23 in particular ("the stage-2 → stage-3 gap is
contingent on requirement quality, not structural") is a claim about the
workflow that a future run could refute, and refuting it is worth more than the
original finding.

Recommended to `OT-0004`, and carried there as an open question for confirmation
rather than asserted.

### Tally

48 entries across two passes.

| Verdict | Count | What it means |
| --- | --- | --- |
| `OK` | 19 | Followed literally, worked |
| `GAP` | 17 | The docs did not say |
| `STALE` | 4 | The docs said something no longer true |
| `BLOCKER` | 5 | Could not proceed as written |
| `?` | 3 | Judged, but arguable |

The five blockers: the orphaned test file that stopped collection (F-04), the
skill self-contradiction about `doc/requirements/` (F-21), the absent browser
tooling (F-07, F-29), and the missing `blocked` status (F-30). Only the third
actually stopped a stage from running.

### Where the run was weakest

Recorded so the verdict is not read as stronger than it is.

- **The operator was not a new user.** They wrote the epic's stories, and in two
  places knew things a fresh reader would not — `scaffold_check` was not treated
  as prior art partly because the same operator had built it an hour earlier
  (F-15).
- **Stage 3 never ran** (F-29). Of the five stages, the one whose value is
  hardest to argue on paper is the one this run cannot speak to. The second pass
  exercised the *skip* direction (F-44), which is not the same thing.
- **Two stages were ticketed after the fact** (F-36, F-47), so the ticket store
  overstates how much the tickets drove the work.
- **One operator, one app, one afternoon.** Findings about a workflow used by
  many people over months are not available from this.
