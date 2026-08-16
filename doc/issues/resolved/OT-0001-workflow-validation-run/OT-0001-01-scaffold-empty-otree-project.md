---
id: OT-0001-01
title: Stage 0 — scaffold the empty oTree project so the workflow has a target
type: story
status: resolved
priority: high
created: 2026-08-15
resolved: 2026-08-15
area: session-config
tags:
  - workflow
  - validation
  - scaffolding
parent: OT-0001
---

# Stage 0 — scaffold the empty oTree project so the workflow has a target

## Description

`demo/` is empty, but every stage downstream of stage 2 assumes an oTree project
exists there. Restore the minimum skeleton so the validation run has somewhere to
land, and record the fact that the workflow has no stage for this.

## Details

- **Current state.** `demo/settings.py`, `demo/public_goods_simple/`, and
  `demo/_static/` are deleted in the working tree. `tests/conftest.py` chdirs
  into `demo/` and calls `otree.main.setup()`, so `uv run pytest` cannot
  currently collect. `demo/modules/` does not exist either.
- **Desired state.** The smallest skeleton that boots, collects, and runs a
  non-empty test suite — nothing more. This is not app work; the real app
  arrives in stage 4.
  - `demo/__init__.py` — empty, as it was before deletion.
  - `demo/settings.py` with `SESSION_CONFIG_DEFAULTS`, the language and currency
    settings oTree requires, and **one placeholder session config** (see below).
  - `demo/_static/global/empty.css`, per the layout in `CLAUDE.md#structure`.
  - `demo/scaffold_check/` — the throwaway app the placeholder config points at.
  - `demo/modules/README.md` and `demo/modules/page-flow.md` as stubs, so stage 4
    has a documented place to write into.

### The placeholder session config

`SESSION_CONFIGS` carries one entry rather than being left empty, so that
`tests/test_bots.py` has something to parametrize over and a green run means a
test actually ran. An empty list would collect zero bot tests and report
success, which is the failure mode worth designing out.

- **A placeholder config forces a placeholder app.** `otree/settings.py:51`
  builds `OTREE_APPS` from the `app_sequence` of every session config, and oTree
  imports each one — so a config pointing at a nonexistent app breaks startup,
  and an empty `app_sequence` yields nothing to import. The placeholder is
  therefore a real, minimal app package: `demo/scaffold_check/` with one page,
  no form fields, no model fields beyond what oTree requires, and a `PlayerBot`
  that advances through it.
- **Keep it obviously disposable.** One page, no game logic, a name that reads
  as scaffolding. It must not become a pattern stage 4 copies from — its only
  job is to prove the toolchain works end to end.
- **Stage 4 removes it** once the real app's session config exists. That removal
  is a second, controlled test of whether `schema-writer` prunes docs for apps
  that have disappeared. Note it in `demo/modules/README.md` so the stage-4
  agent knows to clean it up.

### Stale references

- **Remove** `doc/validated-doc/data-schema/public_goods_simple.md`. It documents
  a deleted app and is legacy. That directory is owned by `schema-writer` and
  `CLAUDE.md` forbids hand-editing it, so **run the skill and let it prune** — it
  should also drop the app's row from the data-schema `README.md` index. If the
  skill leaves the orphan behind, delete it by hand, and log that `schema-writer`
  has no pruning behavior; that gap belongs in the fix ticket.
- **Do not restore `public_goods_simple`.** The epic's starting state is
  deliberate. A full sample app in the tree would give stage 4 a pattern to copy
  and weaken the test.
- **Do not touch `CLAUDE.md`**, even though its structure tree still describes
  `public_goods_simple` and omits `doc/workflow-validation/`. It is the document
  under test. Log both; the fix lands via the ticket story `OT-0001-08` drafts.
- **No artifact** — restoring a documented file layout, no open visual question
  and no unproven mechanism.
- **Verification.** `uv run pytest` collects and passes (an empty or near-empty
  suite is fine at this point), and `cd demo && uv run --project .. otree
  devserver` boots and serves the admin UI at `http://localhost:8000`.
- **Gotcha to expect.** Per `CLAUDE.md#tests`, a leftover `demo/db.sqlite3` from
  a different oTree version aborts the run. Delete it and rerun.
- **Out of scope.** Any real game logic, any session config describing the
  network experiment, any model field beyond what `scaffold_check` needs to
  exist. Stage 4 owns all of it.

## Acceptance Criteria

- [x] `demo/__init__.py`, `demo/settings.py`, and
      `demo/_static/global/empty.css` exist and match the layout documented in
      `CLAUDE.md#structure`.
- [x] `demo/scaffold_check/` is a minimal one-page app with a `PlayerBot`, named
      by a single placeholder entry in `SESSION_CONFIGS`.
- [x] `demo/modules/README.md` and `demo/modules/page-flow.md` exist as stubs,
      and the README records that `scaffold_check` is disposable and must be
      removed in stage 4.
- [x] `uv run pytest` exits zero from the repo root and collects a **non-zero**
      number of tests — the bot test for `scaffold_check` actually ran.
      (`1 passed`, the `scaffold_check` bot case.)
- [x] `cd demo && uv run --project .. otree devserver` boots and the admin UI
      loads at `http://localhost:8000`. **Verified on port 8001, not 8000** —
      port 8000 was held by an unrelated application, so the server was booted
      as `otree devserver 8001`. `GET /demo` returned 200 and listed the
      `scaffold_check` session config. See friction-log entry F-06.
- [x] `doc/validated-doc/data-schema/public_goods_simple.md` is gone and the
      data-schema `README.md` index no longer lists it, done by running
      `schema-writer` rather than by hand-editing that directory.
- [x] `public_goods_simple` was **not** restored, and `CLAUDE.md` was not
      edited.
- [x] Friction log entry appended to
      `doc/workflow-validation/OT-0001-friction-log.md` covering: that the
      workflow has no stage for project setup, what `CLAUDE.md` had to be
      reverse-engineered for, whether `schema-writer` pruned the orphan on its
      own, and every stale reference encountered.

## Open Questions

- None. Both prior questions are settled: `SESSION_CONFIGS` carries a
  placeholder, and `demo/__init__.py` exists.

## Related Files

- `demo/__init__.py`
- `demo/settings.py`
- `demo/scaffold_check/`
- `demo/_static/global/empty.css`
- `demo/modules/README.md`
- `demo/modules/page-flow.md`
- `tests/conftest.py`
- `tests/test_bots.py`
- `doc/validated-doc/data-schema/public_goods_simple.md`
- `doc/otree-doc/tutorial/`
- `doc/workflow-validation/OT-0001-friction-log.md`
- `.venv/lib/python3.11/site-packages/otree/settings.py` (line 51 — `OTREE_APPS`
  is derived from every session config's `app_sequence`)

## Resolution

Scaffolded the oTree project from the layout in `CLAUDE.md#structure`, minus the
deleted sample app. `uv run pytest` is green with one collected case — the
`scaffold_check` bot, which renders and submits `Hello.html` through oTree's real
request stack. The devserver boots and serves the admin UI.

### Written

- `demo/__init__.py` (empty), `demo/_static/global/empty.css` (empty).
- `demo/settings.py` — one placeholder session config (`scaffold_check`,
  1 demo participant), plus the currency and language settings oTree requires.
  Carries a comment telling stage 4 to replace the entry and delete the app.
- `demo/scaffold_check/` — `__init__.py` (no model fields, `page_sequence =
  [Hello]`), `Hello.html`, `tests.py` (`PlayerBot` advancing one page).
- `demo/modules/README.md`, `demo/modules/page-flow.md` — stubs; the README
  carries the stage-4 removal checklist for `scaffold_check`.
- `doc/validated-doc/data-schema/scaffold_check.md` and the index update, via
  `schema-writer`.
- `doc/workflow-validation/OT-0001-friction-log.md` — created, with ten stage-0
  entries (F-01 … F-10).

### Deleted

- `doc/validated-doc/data-schema/public_goods_simple.md` and its index row, via
  `schema-writer`.
- `tests/test_public_goods_payoffs.py` and the `public_goods_session` fixture in
  `tests/conftest.py`. Not named in this ticket, but its module-scope
  `from public_goods_simple import ...` made pytest fail at *collection*, so the
  green-suite criterion was unreachable while it existed. Logged as F-04.

### Deliberately not done

- `public_goods_simple` was not restored, and `CLAUDE.md` was not edited — both
  forbidden by the epic. Every stale reference found in it is logged instead, for
  the fix ticket story `OT-0001-08` drafts.
- The devserver was verified on port 8001 rather than 8000, which was held by an
  unrelated application. Logged as F-06.
- No `artifacts/` folder — this story restores a documented layout; no visual
  question, no unproven mechanism.

### Findings worth carrying forward

- F-05: `schema-writer` was *told* the app had been deleted, so this run is not
  clean evidence that it prunes unprompted. Story `OT-0001-05` gets the clean
  test when it removes `scaffold_check`, and must invoke the skill without
  mentioning the removal.
- F-07: no browser tooling exists in this environment. HTTP checks covered
  stage 0, but stage 3 needs screenshots at 1555×885 and the epic's promotion
  gate needs the app *seen working*. This will block unless resolved.
- F-04 adds `CLAUDE.md#tests` to the list of sections carrying stale
  `public_goods_simple` references, alongside `CLAUDE.md#structure`.
