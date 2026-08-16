---
name: schema-writer
description: Maintain the data-schema docs under doc/validated-doc/data-schema/ for the oTree apps in demo/. Use whenever a model field, constant, page form_fields list, session config, or PARTICIPANT_FIELDS/SESSION_FIELDS entry is added, removed, renamed, retyped, or has its validation changed — and when asked to write, refresh, or audit the schema docs.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# schema-writer

Keeps `doc/validated-doc/data-schema/` a faithful, human-readable description of the
data every oTree app in `demo/` produces: one doc per app, plus an index.

The schema is **derived from source, never invented**. Every row in every table
must come from a line you actually read in `demo/`. If a field's meaning is not
recoverable from the code, write `TODO: confirm with author` rather than
guessing.

## When to run

Run after any change to:

- `demo/<app>/__init__.py` — `C`, `Subsession`, `Group`, `Player`, functions
  that assign fields, or `page_sequence` / `form_fields`
- `demo/settings.py` — `SESSION_CONFIGS`, `SESSION_CONFIG_DEFAULTS`,
  `PARTICIPANT_FIELDS`, `SESSION_FIELDS`, `USE_POINTS`,
  `REAL_WORLD_CURRENCY_CODE`
- a new app added by `otree startapp`

A template rename or a pure-CSS change does not require a schema update. A
template change that adds or drops a `{{ formfield }}` does, because it changes
which fields are player-entered.

## Files this skill owns

```text
doc/validated-doc/data-schema/
  README.md              # index: apps, session configs, project-wide fields
  <app_label>.md         # one per package in demo/ (e.g. public_goods_simple.md)
```

Do not write anywhere else. In particular never edit `doc/otree-doc/` — it is a
vendored Sphinx build.

## Procedure

1. **Scope the change.** `git status` and
   `git diff -- demo/` to see what moved. For a full refresh, treat every app as
   changed.

2. **Enumerate apps.** Every directory in `demo/` holding an `__init__.py` and
   listed in some `app_sequence` in `demo/settings.py`. The app *label* is the
   directory name; `C.NAME_IN_URL` is a separate, URL-only alias — record both.

   **Then prune.** Any `<app_label>.md` in this directory with no matching
   package is an orphan documenting an app that no longer exists: delete the
   file, drop its row from the `README.md` app and session-config tables, and
   add a `README.md` change-log line naming the app and saying it was removed.
   Do this without being asked — nobody will mention that an app was deleted,
   and a stale doc describing a vanished app is worse than no doc, because it
   reads as current.

3. **Read the source.** For each in-scope app read `demo/<app>/__init__.py` in
   full, plus its `.html` templates when you need to know which fields a page
   actually renders. Read `demo/settings.py` once.

4. **Extract, per app:**
   - `C` constants — name, value, and what they constrain
   - fields on `Subsession`, `Group`, `Player` — name, oTree field type, and
     every kwarg (`initial`, `min`, `max`, `choices`, `label`, `blank`, `doc`)
   - which fields are **entered** (appear in a page's `form_fields`) vs
     **computed** (assigned in a function such as `set_payoffs`) vs **built-in**
   - the writer of each computed field: function name + the page or wait page
     that calls it (`after_all_players_arrive`, `before_next_page`, etc.)
   - `C.NUM_ROUNDS` and `C.PLAYERS_PER_GROUP`, which set row multiplicity

5. **Write the doc** using the template below. Overwrite the whole file rather
   than patching around stale prose, but preserve the Notes and Change log
   sections.

6. **Update `README.md`** — the app table, session configs, and the
   project-wide field lists.

7. **Verify** before reporting done:
   - every `models.` assignment in the app appears exactly once in the doc:
     `grep -n "models\." demo/<app>/__init__.py`
   - every `form_fields` entry maps to a documented field
   - no field documented that no longer exists in source
   - no `<app_label>.md` without a matching package in `demo/`, and no
     `README.md` row pointing at a deleted app
   - if models changed, the app's bots still pass:
     `cd demo && uv run --project .. --with requests otree test <app>`

## oTree facts to encode correctly

- **Field types** are only: `BooleanField`, `CurrencyField`, `IntegerField`,
  `FloatField`, `StringField`, `LongStringField`. Use the exact oTree name in
  the Type column — no SQL or Python types.
- **Default initial value is `None`**, not `0` / `""` / `False`, unless
  `initial=` is given. Say so explicitly; it is the most common misreading.
- **Built-in fields exist on every model** and show up in exports even though
  they are not declared in `__init__.py`: `Player.id_in_group`,
  `Player.payoff`, `Player.round_number`, `Group.id_in_subsession`,
  `Subsession.round_number`, and the `participant.*` and `session.*` columns.
  List them once in `README.md`, not repeated in every app doc — but do
  document `payoff` per app, since *how* it is computed is app-specific.
- **`C` constants are not columns.** They are parameters. Keep them in their own
  section and reference them from the Range column (e.g. `0 – C.ENDOWMENT`)
  rather than hardcoding the number twice.
- **`PARTICIPANT_FIELDS` and `SESSION_FIELDS` are untyped** (`participant.vars`
  / `session.vars`). oTree cannot report their type, so document each one's
  intended type, writer, and reader by hand.
- **Row granularity**: the per-app export is one row per player per round —
  `num_participants × NUM_ROUNDS`. State this in each app doc.
- **Currency**: `USE_POINTS = True` means `CurrencyField` values are points,
  converted at `real_world_currency_per_point`. Note the unit in the doc so
  payoff numbers are not read as dollars.

When unsure about oTree semantics, check the vendored docs before writing:
`doc/otree-doc/models.html`, `forms.html`, `pages.html`, `currency.html`,
`rounds.html`, `multiplayer/`.

## Per-app template

````markdown
# Data schema — `<app_label>`

**Source:** [demo/<app_label>/__init__.py](../../../demo/<app_label>/__init__.py)
**URL name:** `<C.NAME_IN_URL>`
**Rounds:** `<C.NUM_ROUNDS>` · **Players per group:** `<C.PLAYERS_PER_GROUP>`
**Export granularity:** one row per player per round
**Currency unit:** points (`USE_POINTS = True`)

## Constants (`C`)

| Constant | Value | Purpose |
| --- | --- | --- |
| `ENDOWMENT` | `cu(100)` | Per-round budget; upper bound on `player.contribution` |

## Player

| Field | Type | Initial | Range / choices | Source | Set by | Description |
| --- | --- | --- | --- | --- | --- | --- |
| `contribution` | `CurrencyField` | `None` | `0 – C.ENDOWMENT` | entered | `Contribute` (form) | Amount the player puts into the public pot |
| `payoff` | built-in `CurrencyField` | `0` | — | computed | `set_payoffs()` | `C.ENDOWMENT - contribution + group.individual_share` |

## Group

| Field | Type | Initial | Range / choices | Source | Set by | Description |
| --- | --- | --- | --- | --- | --- | --- |
| `total_contribution` | `CurrencyField` | `None` | ≥ 0 | computed | `set_payoffs()` | Sum of all members' `contribution` |

## Subsession

_No app-defined fields._

## Page flow → fields

| # | Page | Kind | Reads | Writes |
| --- | --- | --- | --- | --- |
| 1 | `Contribute` | Page | `C.ENDOWMENT` | `player.contribution` |
| 2 | `ResultsWaitPage` | WaitPage | all members' `contribution` | group fields, `player.payoff` |
| 3 | `Results` | Page | group + player fields | — |

## Notes

<!-- Hand-written caveats. Preserved across regenerations. -->

## Change log

| Date | Change |
| --- | --- |
| YYYY-MM-DD | Initial schema doc |
````

Use the same column set for every table so the docs diff cleanly. Drop a
section only when it has no fields — replace it with `_No app-defined fields._`
rather than deleting the heading.

## Style

- Backtick every identifier; use oTree's exact casing.
- Descriptions are one line, present tense, about meaning — not about types the
  Type column already gives.
- Prefer relative markdown links to source (`../../../demo/...`) so the docs are
  navigable from the repo.
- Dates absolute (`2026-08-15`), never "today" or "recently".
- Append to the Change log; never rewrite past entries.

## Reporting

Finish by listing which docs you wrote, which fields were added/removed/changed,
and anything you marked `TODO: confirm with author`.
