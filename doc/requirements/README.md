# Requirements

Stage 1 of the [workflow](../../CLAUDE.md#workflow). One file per idea:
`REQ-XXXX-short-slug.md`, written by the
[`refine-requirement`](../../.claude/skills/refine-requirement/SKILL.md) skill.

A requirement is the record of a conversation — what the experiment should do,
in language the person who asked for it can still recognize, plus the
translation notes a developer needs to write a ticket against it. It is not a
ticket and not a specification:

- **Tickets** ([doc/issues/](../issues/)) say what to build next and how it will
  be verified. A ticket links back to its requirement with a `requirement:`
  frontmatter field.
- **Validated docs** ([doc/validated-doc/](../validated-doc/)) describe the
  experiment to the researcher at the architecture and system-design level,
  written only after a prototype has validated it.

There is no generated index — the folder is the index. Frontmatter carries
`status` (`draft`, `settled`, `superseded`) and `tickets`, the ids written
against it.

A requirement stays the record of the original intent. When the intent itself
changes, edit it and note the change; when it is replaced wholesale, mark it
`superseded` and name the requirement that replaced it.
