# Data schema — index

Describes the data every oTree app in [demo/](../../../demo/) produces. Derived
from source ([demo/settings.py](../../../demo/settings.py) and each
`demo/<app>/__init__.py`); maintained by the `schema-writer` skill
([.claude/skills/schema-writer/SKILL.md](../../../.claude/skills/schema-writer/SKILL.md)).

## Apps

| App label | URL name | Rounds | Players/group | Doc |
| --- | --- | --- | --- | --- |
| `public_goods_simple` | `public_goods_simple` | `1` | `3` | [public_goods_simple.md](public_goods_simple.md) |

## Session configs

| Name | Display name | App sequence | Demo participants |
| --- | --- | --- | --- |
| `public_goods_simple` | Public Goods (simple) | `['public_goods_simple']` | `3` |

### `SESSION_CONFIG_DEFAULTS`

| Key | Value | Meaning |
| --- | --- | --- |
| `real_world_currency_per_point` | `1.00` | Conversion rate from points to `REAL_WORLD_CURRENCY_CODE` |
| `participation_fee` | `0.00` | Flat show-up payment, added outside `player.payoff` |
| `doc` | `""` | Free-text session description shown in the admin UI |

## Project-wide settings

| Setting | Value | Effect on the data |
| --- | --- | --- |
| `USE_POINTS` | `True` | Every `CurrencyField` — including `player.payoff` — is denominated in points, not dollars |
| `REAL_WORLD_CURRENCY_CODE` | `'USD'` | Currency that points convert into at payout |
| `LANGUAGE_CODE` | `'en'` | UI language; no effect on stored data |

## Project-wide fields

### `PARTICIPANT_FIELDS`

_Empty._ No entries in `participant.vars` are declared, so nothing app-defined
is carried across apps or rounds.

### `SESSION_FIELDS`

_Empty._ No entries in `session.vars` are declared.

### Built-in columns

These exist on every model and appear in exports even though no app declares
them. Per-app docs list only `payoff`, since how it is computed is
app-specific.

| Model | Fields |
| --- | --- |
| `Player` | `id_in_group`, `payoff`, `round_number` |
| `Group` | `id_in_subsession`, `round_number` |
| `Subsession` | `round_number` |
| `participant.*` | `code`, `label`, `id_in_session`, `payoff`, `_is_bot`, visit/progress timestamps |
| `session.*` | `code`, `label`, `config` keys (including the `SESSION_CONFIG_DEFAULTS` above) |

## Export granularity

The per-app export is one row per player per round —
`num_participants × C.NUM_ROUNDS`.

## Change log

| Date | Change |
| --- | --- |
| 2026-08-15 | Initial index |
