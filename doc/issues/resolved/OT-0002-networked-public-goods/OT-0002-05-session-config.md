---
id: OT-0002-05
title: Session config, and removing the scaffolding app
type: story
status: resolved
priority: medium
created: 2026-08-15
resolved: 2026-08-15
area: session-config
requirement: REQ-0001
tags:
  - session-config
parent: OT-0002
---

# Session config, and removing the scaffolding app

## Description

Point `SESSION_CONFIGS` at the real app and delete the disposable scaffolding
app that was standing in for it.

## Details

- One config: `network_public_goods`, `num_demo_participants=4`.
- Delete `demo/scaffold_check/` and its `SESSION_CONFIGS` entry.
- Let `schema-writer` prune the scaffolding app's data-schema doc.
- **No artifact** — session-config work, no visual question, no unproven
  mechanism.

## Acceptance Criteria

- [x] `SESSION_CONFIGS` names `network_public_goods` with 4 demo participants.
- [x] `demo/scaffold_check/` is deleted and no config references it.
- [x] `doc/validated-doc/data-schema/scaffold_check.md` is gone and the index no
      longer lists it, done through `schema-writer` rather than by hand.
- [x] `uv run pytest` green.
- [x] Prototype docs updated when implemented: `demo/modules/README.md`.

## Open Questions

- None.

## Related Files

- `demo/settings.py`
- `demo/scaffold_check/` (deleted)
- `doc/validated-doc/data-schema/README.md`
- `demo/modules/README.md`

## Resolution

Config replaced, `demo/scaffold_check/` deleted, `schema-writer` run.

**The pruning test this story existed to run: `schema-writer` does not prune.**
It was invoked with a deliberately neutral prompt — "demo/ has changed — refresh
the data-schema docs" — with no mention that an app had been removed. Its
procedure enumerates apps from `demo/` and `SESSION_CONFIGS` and updates the
index, but nothing in it says what to do with a doc whose app has disappeared.
Deleting `scaffold_check.md` was inferred from the skill's "one doc per package
in `demo/`", not read off an instruction.

This is the clean confirmation of friction-log F-05, which the first attempt at
stage 0 could not provide because the operator had named the deleted app in the
prompt.
