# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

An [oTree](https://otree.readthedocs.io) 6.0.15 experiment project, managed with [uv](https://docs.astral.sh/uv/). Python is pinned to 3.11 via [.python-version](.python-version) (`requires-python = ">=3.11"`).

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

## Tests

Two layers, both run by `uv run pytest` from the repo root:

- **pytest** ([tests/](tests/)) for model/payoff logic — assertions about `set_payoffs`, constants, and field values.
- **oTree bots** (`demo/<app>/tests.py`) for page-flow coverage — form validation, wait pages, page sequence. [tests/test_bots.py](tests/test_bots.py) runs every session config's bots as a parametrized pytest case, so `uv run pytest` covers both; `otree test` remains available for bot-only runs.

Put new logic tests in [tests/](tests/) and new page-flow expectations in the app's `tests.py`.

[tests/conftest.py](tests/conftest.py) does the bootstrapping the `otree` CLI would otherwise do — sets `OTREE_IN_MEMORY`, chdirs into [demo/](demo/), and calls `otree.main.setup()`, all before the first `import otree.*` (both are read at import time and can't be changed after). An autouse fixture keeps each test running under `demo/`, because oTree resolves `import settings`, `_static/`, app layout, and page templates relative to the cwd — several of them `lru_cache`d on first use. The `otree_session_factory` / `public_goods_session` fixtures build real sessions in the in-memory database; tests that touch `Player`/`Group` fields need one, since those are ORM objects rather than plain Python.

There is no lint config.

Gotcha: because `OTREE_IN_MEMORY` loads `demo/db.sqlite3` into memory at startup, a database left by a different oTree version aborts the run with `oTree has been updated. Please delete your database (db.sqlite3)`. Delete `demo/db.sqlite3` and rerun. This hits `otree test` and `pytest` identically; it is oTree behavior, not something the test setup adds.

Production is served via [Procfile](Procfile), which splits the server across two processes: `otree prodserver1of2` (web) and `otree prodserver2of2` (worker).

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
  _static/global/empty.css
tests/                        # pytest suite (repo root, outside the oTree project)
  conftest.py                 # oTree bootstrap + session fixtures
  test_public_goods_payoffs.py
  test_bots.py                # runs demo/<app>/tests.py bots under pytest
```

`tests/` sits at the repo root rather than inside `demo/`, so pytest's rootdir, `testpaths`, and the oTree project root stay separate; `demo/` holds only what oTree itself expects.

Apps cannot be nested inside a subfolder of their project: oTree takes the app label as `import_path.split('.')[0]` ([common.py:108](.venv/lib/python3.11/site-packages/otree/common.py#L108)) and resolves templates as `<app_name>/<Page>.html` relative to the working directory. That is why `demo/` carries its own `settings.py` rather than being a folder of apps under a root project.

Running the server writes `db.sqlite3` and `__pycache__` into `demo/`; both are gitignored. Bots need `requests` (oTree's bot client is a starlette `TestClient`), which oTree does not declare; it is in the `dev` dependency group alongside `pytest`, so `uv sync` installs it and `--with requests` is no longer needed. Keep it out of `[project.dependencies]` — it is not needed to serve the experiment.

## Skills

### `schema-writer`

Maintains the data-schema docs under [doc/demo-spec/data-schema/](doc/demo-spec/data-schema/) — one doc per app in [demo/](demo/), plus an index. Definition: [.claude/skills/schema-writer/SKILL.md](.claude/skills/schema-writer/SKILL.md).

**Fire it automatically** — without being asked, as the last step of the same turn — after editing any of:

- [`demo/public_goods_simple/__init__.py`](demo/public_goods_simple/__init__.py) (or any `demo/<app>/__init__.py`) in a way that touches `C`, `Subsession`, `Group`, `Player`, `form_fields`, `page_sequence`, or a function that assigns a model field
- [demo/settings.py](demo/settings.py) — `SESSION_CONFIGS`, `SESSION_CONFIG_DEFAULTS`, `PARTICIPANT_FIELDS`, `SESSION_FIELDS`, `USE_POINTS`, `REAL_WORLD_CURRENCY_CODE`
- a `.html` template, when the edit adds or removes a rendered form field
- a new app created by `otree startapp`

Finish the code change first, then invoke the skill so the docs land in the same commit. Skip it only for edits that cannot change the data model — comments, CSS, prose in templates.

**Fire it on request** whenever a prompt asks to align, refresh, regenerate, audit, or check the data schema / schema docs / `doc/demo-spec`, or asks what data an app produces.

## Reference docs

[doc/otree-doc/](doc/otree-doc/) is a vendored HTML build of the oTree documentation (tracked in git). Prefer it over guessing at the API — [doc/otree-doc/tutorial/](doc/otree-doc/tutorial/), [models.html](doc/otree-doc/models.html), [pages.html](doc/otree-doc/pages.html), and [bots.html](doc/otree-doc/bots.html) are the most useful entry points. These are build artifacts; do not hand-edit them.
