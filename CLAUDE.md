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
- Record the outcome in `DECISION.md`: which variant won, why, what was rejected, and what the real implementation must keep.

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

Use the browser tooling available in the current agent environment. Run the dev server first (`cd demo && uv run --project .. otree devserver`), then drive `http://localhost:8000` — participant pages via the session's start links, and the admin UI for session creation and data export.

Visual QA is **desktop only**. Standard viewport: **1555 × 885 CSS px at 100% zoom**.

## Commands

All commands go through `uv run` so they resolve against `.venv`. Every `otree` command must run from [demo/](demo/) (the project root that holds `settings.py`), so they take `--project ..` to point uv back at [pyproject.toml](pyproject.toml).

```sh
uv sync                                  # create/refresh .venv from uv.lock (repo root)
uv lock --check                          # verify uv.lock matches pyproject.toml (repo root)
uv run pytest                            # run the test suite (repo root)

cd demo
uv run --project .. otree devserver      # dev server on http://localhost:8000
uv run --project .. otree resetdb        # drop and recreate the database
uv run --project .. otree startapp <name>  # scaffold a new app package
uv run --project .. otree test <app>     # run one app's bots; omit <app> for all
uv run --project .. otree browser_bots   # run bots through a real browser
```

Production is served via [Procfile](Procfile), which splits the server across two processes: `otree prodserver1of2` (web) and `otree prodserver2of2` (worker).

## Tests

Two layers, both run by `uv run pytest` from the repo root:

- **pytest** ([tests/](tests/)) for model and payoff logic — assertions about `set_payoffs`, constants, and field values. Put new logic tests here.
- **oTree bots** (`demo/<app>/tests.py`) for page-flow coverage — form validation, wait pages, page sequence. Put new page-flow expectations here. [tests/test_bots.py](tests/test_bots.py) runs every session config's bots as a parametrized pytest case, so `uv run pytest` covers both layers; `otree test` remains available for bot-only runs.

[tests/conftest.py](tests/conftest.py) does the bootstrapping the `otree` CLI would otherwise do:

- Sets `OTREE_IN_MEMORY`, chdirs into [demo/](demo/), and calls `otree.main.setup()` — all before the first `import otree.*`, since both are read at import time and cannot be changed after.
- An autouse fixture keeps each test running under `demo/`, because oTree resolves `import settings`, `_static/`, app layout, and page templates relative to the cwd — several of them `lru_cache`d on first use.
- The `otree_session_factory` / `public_goods_session` fixtures build real sessions in the in-memory database. Tests touching `Player` / `Group` fields need one, since those are ORM objects rather than plain Python.

Gotcha: because `OTREE_IN_MEMORY` loads `demo/db.sqlite3` into memory at startup, a database left by a different oTree version aborts the run with `oTree has been updated. Please delete your database (db.sqlite3)`. Delete `demo/db.sqlite3` and rerun. This hits `otree test` and `pytest` identically; it is oTree behavior, not something the test setup adds.

There is no lint config.

## Structure

An oTree project expects a `settings.py` at its root defining `SESSION_CONFIGS`, plus one package per app (each with `__init__.py` holding `C`/`Player`/`Group` models and page classes, and `.html` templates alongside).

**The repo root has no `settings.py`** — commit `541a310` removed the sample games that `otree startproject` generates. The oTree project lives in [demo/](demo/) instead:

```text
demo/
  settings.py                 # SESSION_CONFIGS -> public_goods_simple
  public_goods_simple/        # oTree's built-in sample, copied verbatim
    __init__.py               # C / Group / Player / set_payoffs / pages
    Contribute.html
    Results.html
    tests.py                  # PlayerBot
  modules/                    # stage 4 — implementation notes, markdown only
    README.md                 # what exists and what each piece does
    page-flow.md              # page_sequence, wait pages, form fields, rounds
  _static/global/empty.css
tests/                        # pytest suite (repo root, outside the oTree project)
  conftest.py                 # oTree bootstrap + session fixtures
  test_public_goods_payoffs.py
  test_bots.py                # runs demo/<app>/tests.py bots under pytest
```

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
  otree-doc/                  # vendored oTree docs (build artifact, do not edit)
artifacts/                    # stage 3 — disposable spikes, probes, and visual variants
  <OT-XXXX>-<slug>/           # variant-*.html, shots/, DECISION.md
```

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
