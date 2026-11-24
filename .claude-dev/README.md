# .claude-dev

A local Claude Code plugin, `resume-evidence`, in the marketplace `resume-builder-local`.

```
.claude-dev/
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── reference/
│   ├── workflow.md           # layout, mapping schema, script rules (all skills)
│   ├── evidence.md           # evidence file schema, citations, anonymisation (distill, verify)
│   ├── kami.md               # Kami design rules for the Typst resume (to-resume, review-resume)
│   └── learning.md           # how every skill learns: wiki/me.md and skill fixes (all skills)
└── skills/
    ├── ingest/SKILL.md       # /resume-evidence:ingest <company>
    ├── distill/SKILL.md      # /resume-evidence:distill <company> <id>
    ├── verify/SKILL.md       # /resume-evidence:verify <company> <id>
    ├── to-resume/SKILL.md    # /resume-evidence:to-resume [base | <slug>]
    ├── steer/SKILL.md        # /resume-evidence:steer [base | <slug>] <what to change>
    ├── review-resume/        # /resume-evidence:review-resume [slug] [template]
    │   ├── SKILL.md
    │   └── measure.sh
    ├── wiki/SKILL.md         # /resume-evidence:wiki ingest | query | lint
    └── resume/SKILL.md       # /resume-evidence:resume (copied from chuan-khuna/altr-stack)
```

`to-resume`, `steer` and `review-resume` work on the Typst resume in `resume/` (see `resume/README.md`).

`wiki` maintains the knowledge base in `wiki/` (see `wiki/CLAUDE.md`). It is separate from
the evidence pipeline: no resume claim may rest on a wiki note.

The skills evolve: when a session teaches a lesson that holds for any user, Claude fixes the
skill it belongs to. The user's own preferences go to the gitignored `wiki/me.md`
instead, through `scripts/me.py`. Every skill ends with a Learn step that applies
`reference/learning.md`.

All skills are user-invoked. The design is in
[`docs/documents/resume-generation-workflow.html`](../docs/documents/resume-generation-workflow.html).

## Install

Try it for one session:

```bash
claude --plugin-dir ./.claude-dev
```

Install it for you, in this repo only (`mise run plugins` does this):

```bash
claude plugin marketplace add ./.claude-dev --scope local
claude plugin install resume-evidence@resume-builder-local --scope local
```

Local scope writes to `.claude/settings.local.json`, which is gitignored, so nothing about the
install is committed.

After you change a skill:

```bash
claude plugin marketplace update resume-builder-local
```
