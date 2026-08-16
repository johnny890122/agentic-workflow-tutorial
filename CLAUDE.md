# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

An [oTree](https://otree.readthedocs.io) 6.0.15 experiment project, managed with [uv](https://docs.astral.sh/uv/). Python is pinned to 3.11 via [.python-version](.python-version) (`requires-python = ">=3.11"`).

Document-first, and frontend-heavy. The people who ask for features are researchers rather than developers: their first description is usually vague, and clarifying it is a stage of the work rather than a preamble to it. How a screen looks is part of the experimental design, so visual choices are built and shown before they are committed to.

## Workflow

Five stages, each with a home on disk. Work moves forward through them and never runs ahead of its stage, but not every stage fires on every task — the Required column says when each one applies.

| Stage | Home | What lands there | Required |
| --- | --- | --- | --- |
| 1. Requirement | [doc/requirements/](doc/requirements/) — `REQ-XXXX` | What the experiment should do, in the requester's own language | Non-trivial or vaguely described work |
| 2. Ticket | [doc/issues/](doc/issues/) — `OT-XXXX` | The problem, the intent, acceptance criteria | Anything more than a small fix |
| 3. Artifact | [artifacts/](artifacts/) | Spikes and visual variants, all disposable | Per [Stage 3 is conditional](#stage-3-is-conditional) |
| 4. Prototype | [demo/](demo/) + [demo/modules/](demo/modules/) | The working oTree app, plus the implementation detail an agent needs | Always |
| 5. Validated doc | [doc/validated-doc/](doc/validated-doc/) | What the researcher needs to know | When a requirement settles |

Rules that make the flow hold:

- **Requirement first.** [`refine-requirement`](#refine-requirement) interviews the user in plain language and writes `REQ-XXXX`. Nothing downstream starts until they confirm it reads right.
- **Then the ticket.** [`ticket-system`](#ticket-system) writes `OT-XXXX` against the settled requirement, carrying `requirement: REQ-XXXX` in frontmatter. Ticket status drives filing: change the `status` field and rerun the generator — never move ticket files by hand.
- **Validation gates promotion.** "Validation passes" means `uv run pytest` is green (both layers — see [Tests](#tests)) *and* the behavior has been seen working, not merely tested. Never write into `doc/validated-doc/` on the strength of an unvalidated prototype.
- **Promote the deliberate, not the incidental.** Stage 5 records requirements the experiment must meet. A bug fix that changes no requirement promotes nothing.
- **Keep the chain in sync.** Code diverging from its requirement, ticket, or validated doc is a defect in the docs as much as in the code. Fix both in the same turn, or say plainly which one you left behind. A requirement that turns out to be wrong gets corrected at stage 1, not silently overridden downstream.
- **Work moves backward too, and nothing will remind you.** A later stage regularly learns something the earlier stage could not have known — an answer that retires an option the requirement listed, or a rule that turns out to be *unimplementable as written* rather than wrong. Both go back to stage 1. Nothing detects this: the ticket generator cannot see requirements, and `promotion-debt.md` only tracks closure hygiene. The discipline is the mechanism. When you cannot correct it in the same turn, say so in the ticket's `## Resolution` in plain words.
- **Requirement rule numbers are load-bearing.** Tickets cite them (`REQ-0001 rule 7`), so the numbered list is effectively append-only: add at the end, never renumber. Renumbering silently repoints every citation and no tool will catch it.
- **Validated is not the same as ready to run.** The promotion gate asks whether the prototype demonstrates the requirement, not whether the experiment is fit to put in front of participants. A validated doc may legitimately carry open decisions — promote it with them listed plainly rather than withholding promotion or quietly resolving them.

### Stage 3 is conditional

Stage 3 exists to answer a question the ticket cannot answer on paper. It is **required** when either holds:

- The ticket turns on **what a screen should look like**. That choice belongs to the user, and they need to see the options to make it — see [Visual variants](#visual-variants).
- The mechanism has **no precedent in the repo** and must be proven before it is built.

It is **skipped** otherwise. Model fields, payoff arithmetic, grouping rules, session config, data and export changes, tests, bug fixes, and pages following an existing pattern are all settled on paper and go straight from stage 2 to stage 4.

The ticket makes this call, not the implementer, and says so either way: an artifact-backed ticket names what the spike must demonstrate and carries an acceptance-criteria checkbox for it, while a ticket that skips stage 3 says so in one line with the reason. Arriving at implementation unsure whether an artifact was expected means the ticket is underspecified — fix the ticket, don't guess.

Nothing in `artifacts/` is a deliverable and nothing is promoted verbatim; what survives is rewritten into `demo/`.

### Visual variants

When a ticket carries a visual question:

- Build **two or three** standalone `.html` files under `artifacts/<OT-XXXX>-<slug>/`, one per variant. Self-contained — no build step, no devserver, no oTree, no external assets — with hardcoded stand-in data where player values would go.
- Screenshot each at the standard viewport (**1555 × 885**, see [Visual QA](#visual-qa)) into `shots/`.
- Present them together and ask the user to choose. Variants must differ on the question being asked; three shades of one layout is not a choice. Say what each trades away.
- Record the outcome in `DECISION.md`: which variant won, why, what was rejected, and what the real implementation must keep — plus **who decided and on what evidence**.

That last part is not bookkeeping. A `DECISION.md` reading "ring — symmetric, simplest to verify" is indistinguishable from a design decision, and it gets promoted to `doc/validated-doc/` as one. If nobody looked at alternatives, or an implementer picked for convenience because the stage could not run, the file must say so in those words, and say what was rejected unexamined. Otherwise the fact that nobody chose is lost at exactly the point the document becomes authoritative.

Mark such a decision **provisional** and name the condition for revisiting it.

The winner is a decision, not code. It gets rewritten as a real oTree page in `demo/` against real fields and real data, while the artifact folder stays behind as the record of why the screen looks the way it does. Fold the decision into the requirement when promoting to stage 5.

The test for whether variants are needed is not "does this touch the frontend" but **"is there a choice here the user should make by looking"**.

### Two doc homes

[demo/modules/](demo/modules/) is stage 4, written **for the next agent**: which piece does what, which page writes which field, why the implementation went the way it did. Markdown only, kept beside the code it describes. Update [README.md](demo/modules/README.md) when prototype work adds files, apps, or pages; keep `page_sequence`, wait pages, form fields, and round structure in [page-flow.md](demo/modules/page-flow.md); add `<app>.md` when one app needs more than a line.

[doc/validated-doc/](doc/validated-doc/) is stage 5, written **for the researcher**: how the experiment is put together and why, at the architecture and system-design level. `guide/` is hand-written; `data-schema/` is generated by [`schema-writer`](#schema-writer) and never hand-edited, during promotion or otherwise.

Both stay short, and both record decisions rather than restating code. Class names, function signatures, and template internals belong in stage 4 and never get promoted — a stage 5 doc that only makes sense to someone reading the code has promoted the wrong thing.

## Agent behavior

Guidelines to reduce common mistakes. Bias toward caution; use judgment on trivial tasks.

- **Think before coding.** State assumptions. Ask when uncertain. Surface tradeoffs instead of picking silently. Push back if a simpler approach exists.
- **Align before acting.** When a task is vague or the product intent is unclear, use `AskUserQuestion` before proceeding. Ask in the requester's terms — a researcher describing an experiment should never have to answer a question phrased in oTree vocabulary.
- **Simplicity first.** The minimum code that solves the problem. No speculative features, abstractions, or error handling for impossible cases.
- **Readable structure.** Split view models, templates, styles, fixtures, and helpers by responsibility once a file starts mixing concerns. No source file may exceed 1,000 lines — split by domain before it grows past that.
- **Surgical changes.** Touch only what the request requires. Match existing style. Don't refactor unrelated code. Clean up only orphans your own changes created.
- **Goal-driven execution.** Turn tasks into verifiable goals. For multi-step work, state brief steps and how each will be verified.

### Visual QA

Run the dev server first (`cd demo && uv run --project .. otree devserver`), then drive it — participant pages via the session's start links, and the admin UI for session creation and data export.

Visual QA is **desktop only**. Standard viewport: **1555 × 885 CSS px at 100% zoom**.

**Check for browser tooling before promising a screenshot.** This needs a real browser driver in the agent environment — something that can navigate and capture at a set viewport. Not every environment has one, and its absence is not a small inconvenience: it blocks [stage 3](#visual-variants) outright, because there the screenshot *is* the deliverable.

When there is no browser, in order of preference:

1. **Build the variants anyway and hand the user the file paths** to open at 1555 × 885 themselves. The choice stays theirs, made by looking, which is the whole point. `shots/` stays empty and the reason goes in `DECISION.md`.
2. **Say the stage is blocked** and let the user decide whether to proceed without it. Record the outcome per [Visual variants](#visual-variants).

Never substitute a written description of a variant for the variant itself and call the stage done — a choice made by reading is not the choice this stage exists to obtain.

**Without a browser, `demo/` can still be exercised over HTTP**, which is worth doing and is not the same thing. Create a session with `POST /api/sessions`, read participant codes from `/SessionStartLinks/<code>`, then `GET`/`POST` the participant URLs to walk the page sequence and inspect the rendered HTML. That proves the flow, the fields, and the arithmetic. It proves nothing about whether the screen is any good to look at.

## Commands

All commands go through `uv run` so they resolve against `.venv`. Every `otree` command must run from [demo/](demo/) (the project root that holds `settings.py`), so they take `--project ..` to point uv back at [pyproject.toml](pyproject.toml).

```sh
uv sync                                  # create/refresh .venv from uv.lock (repo root)
uv lock --check                          # verify uv.lock matches pyproject.toml (repo root)
uv run pytest                            # run the test suite (repo root)

cd demo
uv run --project .. otree devserver      # dev server on http://localhost:8000
uv run --project .. otree devserver 8001 # ...or any free port; 8000 is only a default
uv run --project .. otree resetdb        # drop and recreate the database
uv run --project .. otree startapp <name>  # scaffold a new app package
uv run --project .. otree test <app>     # run one app's bots; omit <app> for all
uv run --project .. otree test <app> --export <dir>  # ...and write the CSVs it produced
uv run --project .. otree browser_bots   # run bots through a real browser
```

`8000` is a default, not a requirement — it is often taken by something else. Pass
a port. Everything below that says `localhost:8000` means "wherever the devserver
is listening".

`otree test <app> --export <dir>` is the working way to see the data an app
produces. The REST export endpoints need auth that is not set up here.

Production is served via [Procfile](Procfile), which splits the server across two processes: `otree prodserver1of2` (web) and `otree prodserver2of2` (worker).

## Tests

Two layers, both run by `uv run pytest` from the repo root:

- **pytest** ([tests/](tests/)) for model and payoff logic — assertions about payoff functions, constants, and field values. Put new logic tests here, named by topic (`test_<topic>.py`) rather than one file per app.
- **oTree bots** (`demo/<app>/tests.py`) for page-flow coverage — form validation, wait pages, page sequence. Put new page-flow expectations here. [tests/test_bots.py](tests/test_bots.py) runs every session config's bots as a parametrized pytest case, so `uv run pytest` covers both layers; `otree test` remains available for bot-only runs.

[tests/conftest.py](tests/conftest.py) does the bootstrapping the `otree` CLI would otherwise do:

- Sets `OTREE_IN_MEMORY`, chdirs into [demo/](demo/), and calls `otree.main.setup()` — all before the first `import otree.*`, since both are read at import time and cannot be changed after.
- An autouse fixture keeps each test running under `demo/`, because oTree resolves `import settings`, `_static/`, app layout, and page templates relative to the cwd — several of them `lru_cache`d on first use.
- The `otree_session_factory` fixture builds real sessions in the in-memory database. Tests touching `Player` / `Group` fields need one, since those are ORM objects rather than plain Python. Keep app-specific fixtures in the test module that uses them, not in `conftest.py` — a fixture naming an app outlives the app and breaks collection for everything.

**A test that imports an app at module scope breaks the whole suite when that app goes.** `from <app> import ...` at the top of a test file means pytest fails at *collection*, so nothing runs — not one failing test, a suite that cannot be built. When an app is deleted, delete or rewrite its tests in the same change.

Gotcha: because `OTREE_IN_MEMORY` loads `demo/db.sqlite3` into memory at startup, a database left by a different oTree version aborts the run with `oTree has been updated. Please delete your database (db.sqlite3)`. Delete `demo/db.sqlite3` and rerun. This hits `otree test` and `pytest` identically; it is oTree behavior, not something the test setup adds.

The same in-memory behavior applies to **`otree devserver`**, and it surprises people: the running server holds the database in memory, so a session created by an external script against `demo/db.sqlite3` is invisible to it and its start link 404s. To drive participants over HTTP, create the session through the server itself — `POST /api/sessions` with `{"session_config_name": ..., "num_participants": ...}` — and read the participant codes from `/SessionStartLinks/<code>`.

There is no lint config.

## Structure

An oTree project expects a `settings.py` at its root defining `SESSION_CONFIGS`, plus one package per app (each with `__init__.py` holding `C`/`Player`/`Group` models and page classes, and `.html` templates alongside).

**The repo root has no `settings.py`** — commit `541a310` removed the sample games that `otree startproject` generates. The oTree project lives in [demo/](demo/) instead:

Rows marked **required** are what oTree itself expects of any project here; the
rest is whatever apps happen to exist right now. Read the tree that way — the
app names change, the required shape does not.

```text
demo/
  settings.py                 # REQUIRED — SESSION_CONFIGS, currency, language
  _static/global/empty.css    # REQUIRED — oTree expects a global stylesheet
  modules/                    # REQUIRED — stage 4 notes, markdown only
    README.md                 # what exists and what each piece does
    page-flow.md              # page_sequence, wait pages, form fields, rounds
  <app>/                      # one package per app; currently network_public_goods
    __init__.py               # C / Subsession / Group / Player / functions / pages
    <Page>.html               # one template per page class
    tests.py                  # PlayerBot
tests/                        # pytest suite (repo root, outside the oTree project)
  conftest.py                 # REQUIRED — oTree bootstrap + session fixtures
  test_bots.py                # REQUIRED — runs demo/<app>/tests.py bots under pytest
  test_<topic>.py             # logic tests; one per area, not one per app
```

`demo/` needs **no `__init__.py`**. It is a working directory that oTree runs
from, not an importable package — `tests/conftest.py` puts it on `sys.path` and
chdirs into it. An empty one existed for a while and was removed once it was
established that nothing reads it.

**Scaffolding a new project is ordinary stage-4 work**, done before the first
feature ticket rather than as a stage of its own: create the required rows above,
plus one app and one session config so `tests/test_bots.py` has something to
parametrize over. An empty `SESSION_CONFIGS` collects zero bot tests and still
reports success, which is the failure mode worth designing out.

Two constraints explain that layout:

- **Apps cannot be nested inside a subfolder of their project.** oTree takes the app label as `import_path.split('.')[0]` ([common.py:108](.venv/lib/python3.11/site-packages/otree/common.py#L108)) and resolves templates as `<app_name>/<Page>.html` relative to the working directory — so `demo/` carries its own `settings.py` rather than being a folder of apps under a root project.
- **`tests/` sits at the repo root**, keeping pytest's rootdir and `testpaths` separate from the oTree project root.

Apart from `modules/`, `demo/` holds only what oTree itself expects. `modules/` is the deliberate exception — markdown kept next to the code it documents. It carries no `__init__.py` and appears in no `app_sequence`, so oTree never treats it as an app.

The rest of the document tree that carries the [workflow](#workflow) sits outside the oTree project:

```text
doc/
  requirements/               # stage 1 — REQ-XXXX, one per idea; folder is the index
  issues/                     # stage 2 — OT-XXXX tickets, filed by status
    README.md                 # GENERATED index; also pending/in-progress/done/promotion-debt.md
    pending/  in_progress/  resolved/  wont_fix/
  validated-doc/              # stage 5 — researcher-facing, promoted after validation
    guide/                    # hand-written: architecture, system design, why
    data-schema/              # GENERATED by schema-writer — do not hand-edit
  workflow-validation/        # meta: how this workflow itself performs
  otree-doc/                  # vendored oTree docs (build artifact, do not edit)
artifacts/                    # stage 3 — disposable spikes, probes, and visual variants
  <OT-XXXX>-<slug>/           # variant-*.html, shots/, DECISION.md
```

[doc/workflow-validation/](doc/workflow-validation/) is the standing home for
work *about* the workflow rather than about an experiment: validation runs,
friction logs, and the reasoning behind the rules on this page. It is permanent,
not an archive of any one run — a finding is only worth keeping because a later
run might contradict it, and records of rules that **worked** matter as much as
records of rules that failed.

It is not a stage and never gates anything. Nothing in `demo/` or
`doc/validated-doc/` should ever depend on it.

Running the server writes `db.sqlite3` and `__pycache__` into `demo/`; both are gitignored. Bots need `requests` (oTree's bot client is a starlette `TestClient`), which oTree does not declare; it is in the `dev` dependency group alongside `pytest`, so `uv sync` installs it. Keep it out of `[project.dependencies]` — it is not needed to serve the experiment.

## Skills

### `refine-requirement`

Writes stage-1 requirements (`REQ-XXXX`) under [doc/requirements/](doc/requirements/). Definition: [.claude/skills/refine-requirement/SKILL.md](.claude/skills/refine-requirement/SKILL.md).

**Fire it on request** whenever someone describes what they want the experiment to *do* rather than what to build — especially when the description is vague, told from the participant's point of view, or free of oTree vocabulary. Prefer it over `ticket-system` when no settled requirement exists; a request already specific enough to verify can go straight to a ticket.

It interviews in participant terms, never oTree terms, and defers anything that must be *seen* to be decided into visual questions for stage 3. It writes only under `doc/requirements/`, never sketches or mocks anything, and **stops for confirmation** rather than chaining into `ticket-system`.

### `ticket-system`

Writes and files stage-2 tickets (`OT-XXXX`) under [doc/issues/](doc/issues/). Definition: [.claude/skills/ticket-system/SKILL.md](.claude/skills/ticket-system/SKILL.md).

**Fire it on request** whenever a prompt asks to add, write, or refine a ticket, asks what to work on next, or discusses an experiment feature or problem before implementation — and after a `REQ-XXXX` is settled and the user says to proceed. It gathers requirements only; it never touches `demo/`, `tests/`, or `doc/validated-doc/`.

Tickets are Markdown with YAML frontmatter, following [assets/TICKET_TEMPLATE.md](.claude/skills/ticket-system/assets/TICKET_TEMPLATE.md). Filing and the index are automated — after any ticket edit, run:

```sh
uv run python .claude/skills/ticket-system/scripts/generate_issues_index.py
```

The generator validates the store (duplicate or malformed ids, story ids that don't extend their epic, unknown statuses, completed epics with active stories), exits non-zero on any error, then files each ticket into its status folder and rewrites the index pages. [doc/issues/promotion-debt.md](doc/issues/promotion-debt.md) lists completed tickets closed without checking their acceptance criteria or writing a `## Resolution`; it should be empty before `doc/validated-doc/` is treated as settled.

### `schema-writer`

Maintains the data-schema docs under [doc/validated-doc/data-schema/](doc/validated-doc/data-schema/) — one doc per app in [demo/](demo/), plus an index. Definition: [.claude/skills/schema-writer/SKILL.md](.claude/skills/schema-writer/SKILL.md).

**Fire it automatically** — without being asked, as the last step of the same turn — after editing any of:

- any `demo/<app>/__init__.py` in a way that touches `C`, `Subsession`, `Group`, `Player`, `form_fields`, `page_sequence`, or a function that assigns a model field
- [demo/settings.py](demo/settings.py) — `SESSION_CONFIGS`, `SESSION_CONFIG_DEFAULTS`, `PARTICIPANT_FIELDS`, `SESSION_FIELDS`, `USE_POINTS`, `REAL_WORLD_CURRENCY_CODE`
- a `.html` template, when the edit adds or removes a rendered form field
- a new app created by `otree startapp`

Finish the code change first, then invoke the skill so the docs land in the same commit. Skip it only for edits that cannot change the data model — comments, CSS, prose in templates.

**Fire it on request** whenever a prompt asks to align, refresh, regenerate, audit, or check the data schema, or asks what data an app produces.

## Reference docs

[doc/otree-doc/](doc/otree-doc/) is a vendored HTML build of the oTree documentation (tracked in git). Prefer it over guessing at the API — [doc/otree-doc/tutorial/](doc/otree-doc/tutorial/), [models.html](doc/otree-doc/models.html), [pages.html](doc/otree-doc/pages.html), and [bots.html](doc/otree-doc/bots.html) are the most useful entry points. These are build artifacts; do not hand-edit them.
