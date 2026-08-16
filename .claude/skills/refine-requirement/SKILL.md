---
name: refine-requirement
description: "Turn a vague experiment idea into a settled requirement in `doc/requirements/` (`REQ-XXXX`). Use at the very start of any non-trivial work — when someone describes what they want the experiment to do in everyday language, before any ticket exists. Interview the user in plain language, pin down the rules and numbers, list what must be seen before it can be decided, and write the requirement. Never writes tickets, never implements."
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, AskUserQuestion
---

# refine-requirement

Stage 1 of the promotion flow in `CLAUDE.md`. This skill sits in front of
`ticket-system` and does one job: take an experiment idea described in ordinary
language and turn it into a requirement a developer can act on — without
changing what the person actually asked for.

Assume the person you are interviewing is a researcher, not a software
developer. They know the behavior they want to observe. They do not know what a
page, a field, a round, or a wait page is, and they should not have to. The
translation is your job, not theirs.

## Guardrails

- **Never implement.** Write only under `doc/requirements/`. Never touch
  `demo/`, `tests/`, `artifacts/`, `demo/modules/`, or `doc/validated-doc/`.
- **Never write the ticket.** Ticket authoring belongs to `ticket-system`, and
  only after the user confirms the requirement reads right.
- **Words only.** No mockups, no wireframes, no HTML, no screenshots. Anything
  that has to be *seen* to be decided is recorded as a visual question for the
  artifact stage — see [Visual questions](#visual-questions).
- **Translate, do not invent.** Every rule, number, and screen in the
  requirement must trace to something the user said or explicitly approved.
  Unasked-for behavior is the failure mode of this skill. If a gap needs filling
  to make the requirement coherent, propose it as a question, not as prose.
- **Uncertainty is content.** An unanswered question left visible in
  `## Open Questions` is a better requirement than a confident guess.
- Read before writing: `CLAUDE.md`, `doc/requirements/README.md`, the existing
  requirements, `assets/REQUIREMENT_TEMPLATE.md`, and — for grounding on what
  already exists — `doc/validated-doc/data-schema/README.md` and the relevant
  `demo/<app>/__init__.py`.
- `doc/otree-doc/` is read-only vendored documentation. Consult it to keep your
  translation notes honest; never edit it.

## Modes

Pick the mode first; ask with AskUserQuestion if it is unclear.

1. **New requirement** — a fresh idea, nothing written yet.
2. **Refine existing `REQ-XXXX`** — another pass over a draft, usually because
   the user answered an open question or changed their mind.
3. **Settle a requirement** — the user confirms a draft is right; flip
   `status: settled`, fill `settled:`, and hand off to `ticket-system`.

## The interview

Ask in the user's world, not oTree's. Never put `page_sequence`, `form_fields`,
`Player`, `Group`, or `C` in a question to the user; those belong in the
translation notes you write afterwards.

| Ask this | Not this |
| --- | --- |
| "What does a participant see on the first screen?" | "What pages are in `page_sequence`?" |
| "What do they type in or click?" | "Which `form_fields` does the page have?" |
| "Does everyone wait for the group before moving on?" | "Do you need a `WaitPage`?" |
| "Do they do this once, or repeat it?" | "What is `C.NUM_ROUNDS`?" |
| "How are their earnings worked out?" | "What does `set_payoffs` compute?" |

The line is **oTree vocabulary**, not technical vocabulary. Experimental-economics
terms a researcher already uses — *round*, *treatment*, *endowment*, *matching*,
*payoff* — are theirs, not oTree's, and are fine in a question. `page_sequence`,
`form_fields`, `Player`, `Group`, `WaitPage` and `C` are not. If you are unsure
which side a word falls on, ask whether the researcher would have used it before
this repo existed.

Method:

- **One topic at a time.** Batch at most three questions per AskUserQuestion
  call, all on the same topic, and always offer a defer option such as "Not sure
  — leave it open for now".
- **Offer concrete options, not open prompts.** "Should everyone see what the
  others chose, or only the group total?" gets an answer; "How should feedback
  work?" gets a shrug. Give two or three specific alternatives and let the user
  correct you.
- **Play it back.** After each round, restate what you now believe in two or
  three sentences and ask what is wrong with it. Corrections are cheaper than
  confirmations.
- **Chase the number.** Any quantity the user leaves out — how many people, how
  many rounds, how much money, how long — must end up either in the numbers
  table or in `## Open Questions`. Never silently pick one.
- **Stop when it is settled**, not when the template is full. See
  [Readiness](#readiness).

## What must be pinned down

Cover these before calling a requirement settled. Each maps to a section of the
template.

- **Purpose** — the behavior being observed and why it matters. If you cannot
  say what the experiment is *for*, everything downstream is guesswork.
- **Participant journey** — every screen in order: what is shown, what the
  participant does, what happens when they submit.
- **Rules** — the invariants, written so a single observed run can be judged
  against them. "Nobody can contribute more than their budget" is a rule;
  "contributions should be reasonable" is not.
- **Numbers** — group size, rounds, budgets, multipliers, currency, timing.
  Every one either has a value or is marked provisional.
- **Grouping and repetition** — who plays with whom, whether groups stay fixed
  across rounds, what participants know about each other.
- **Earnings** — how payoff is computed, in words, with a worked example if the
  arithmetic is non-obvious.
- **What is not being built** — at least one tempting nearby feature, named and
  excluded. This is the section that prevents scope creep two stages later.
- **Visual questions** — see below.
- **Conflicts with what exists** — anything here that contradicts the current
  `demo/` app or a promoted spec, called out plainly. This has no section of its
  own: it goes in the last bullet of `## Translation notes`. Write `**none**`
  there explicitly when there is nothing to conflict with — silence reads as an
  unchecked box.

Scaffolding, placeholder, and throwaway apps in `demo/` are **not** prior art.
An app with no fields, no form, and no payoff rule conflicts with nothing; say so
rather than treating its existence as a constraint.

## Visual questions

This project's experiments are frontend-heavy, and the artifact stage exists to
let the user *pick* from things they can see. That makes "I do not know what it
should look like" a valid, expected answer — not a gap to be filled with prose.

When the user cannot decide something from a description — a layout, a control,
how much information is on screen at once, how a result is revealed — do not
push for a verbal answer and do not sketch it. Record it under
`## Visual questions for the artifact stage`, phrased as the choice to be made,
and let stage 3 build variants for the user to choose between.

Write `How should each player's deduction be entered — one control per player,
or one shared total?`, not `The deduction UI should be intuitive.`

Anything the user *has* decided visually is a rule, not a visual question. Put
it under `## Rules the experiment must follow` so the artifact stage treats it
as a constraint rather than reopening it.

**An empty visual-questions section is a real answer**, not an oversight. Plenty
of requirements — a change to how earnings are computed, how participants are
grouped, what the data export records — have nothing to look at. Write
`_None — nothing here is decided by looking._` so the downstream ticket can skip
stage 3 with confidence instead of wondering whether the question was missed.

## Translation notes

The last section of the requirement, and the one the developer reads first. This
is where oTree vocabulary is allowed and expected: map screens to pages, the
things participants enter to fields with types and bounds, the earnings rules to
the function that computes them, and the repetition to `C.NUM_ROUNDS` /
`C.PLAYERS_PER_GROUP`.

Ground it. Read the relevant `demo/<app>/__init__.py` and
`doc/validated-doc/data-schema/` first so the notes name real fields where they
exist and say "new" where they do not. Consult `doc/otree-doc/` for any oTree
mechanism you name — a translation note that gets the API wrong sends the ticket
in the wrong direction.

Nothing here may introduce behavior absent from the sections above. If writing
the notes reveals a gap, go back and ask — but first work out which kind of gap
it is, because they need opposite handling:

- **A gap in what the user wants** — a rule that stops half-stated, a number
  nobody named. Go back and ask. This is the case the rule above is for.
- **A consequence of what they already said** — two reasonable answers that
  combine into something nobody intended, visible only once the arithmetic is
  written out. Do **not** send this back as an interview question: it usually
  cannot be posed in participant language without asking the researcher to hold
  the arithmetic in their head, which is your job. Write the consequence out
  plainly, with a worked example, and route it to whoever can actually settle
  it — a constraint on the artifact stage if it is decided by looking, an
  `## Open questions` entry with the alternatives spelled out if it is a
  judgment call.

## Readiness

**Hard gates.** A requirement cannot be settled while any of these fails. Fix it
or keep the requirement a draft.

- [ ] A reader who was not in the conversation can describe what a participant
      does, screen by screen, without asking a question.
- [ ] Every rule is checkable against a single observed run.
- [ ] Every number has a value or is explicitly marked provisional or open.
- [ ] Everything undecidable-in-words is a visual question, not vague prose.
- [ ] Translation notes name the app, the screens-to-pages mapping, the data
      entered, and the data computed.
- [ ] Nothing in the requirement is there because you assumed it — or, where an
      inference was unavoidable to make the requirement coherent, it is flagged
      inline **and** listed in `## Open questions`.

**Waivable, with the user's agreement.** These can be left open in a settled
requirement, as long as the requirement says so and names what each one blocks.

- [ ] The out-of-scope section names something real.
- [ ] The purpose is pinned down.

A requirement whose **design** is complete but whose **purpose** is not can be
settled: the researcher may know exactly what they want built and not yet know
which hypothesis they are testing. Say plainly in
`## What we are trying to learn` that the hypothesis is undecided, list the
candidates in `## Open questions`, and name what it blocks — usually the stage-5
promotion rather than the build. Do not invent a purpose to fill the section.

Say which boxes are unticked when you hand off, either way.

## Writing the file

1. Read the existing requirements and `assets/REQUIREMENT_TEMPLATE.md`.
2. Pick the next id: the highest `REQ-XXXX` in `doc/requirements/`, plus one.
3. Write `doc/requirements/REQ-XXXX-short-slug.md` — lowercase kebab filename,
   template sections exactly, `status: draft`, `created:` today's absolute date.
4. Keep the user's own words where they are clear. Rewriting a researcher's
   plain description into procedural prose loses the intent that made it useful.
5. Do not create the ticket. Do not regenerate the issues index.

## Refining an existing requirement

Expect this. A settled requirement gets corrected when a later stage learns
something stage 1 could not have known — a downstream answer that retires an
option this requirement listed, or a rule that turns out to be **unimplementable
as written** rather than wrong. Both come back here; neither is a failure of the
original requirement.

- Preserve `id`, `created`, and the filename, even if the title changes.
- Ask about existing open questions before rewriting them; keep the uncertainty
  unless the user resolves it.
- When intent changes rather than sharpens, note what changed and why — the
  requirement is the record of the decision, and a ticket may already reference
  the old version.
- **Note the change inline, next to what changed**, as a short italic aside
  carrying the date and the reason — not in a change log at the bottom. A reader
  hits the amended rule and the reason for it together, which is where the
  reason is useful. There is no change-log section in the template, on purpose.
- **Never renumber the rules.** Tickets cite them by number (`REQ-0001 rule 7`),
  so the list is append-only: a new rule goes at the end even when it belongs
  logically beside rule 4. Renumbering silently repoints every citation in the
  ticket store and nothing will catch it.
- After amending, check whether the tickets in `tickets:` now contradict the
  requirement, and say so if they do. Do not edit them — that is stage 2 — but
  the divergence must be stated rather than left for someone to trip over.
- When a requirement is replaced wholesale, set `status: superseded` and name
  its replacement rather than deleting it.

## Handoff

**Stop here and confirm.** Do not chain into `ticket-system` on your own.

End the turn with:

- The requirement's id, title, and path.
- A short plain-language playback of what it says — the version the user can
  check without opening the file.
- Any readiness box that is not ticked, and what would tick it.
- Remaining open questions, and the visual questions being deferred to
  `artifacts/`.
- One line offering the next step: settle the requirement and write the ticket
  with `ticket-system`, which adds `requirement: REQ-XXXX` to the ticket
  frontmatter.
