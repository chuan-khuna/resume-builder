# .claude-dev

A local Claude Code plugin, `resume-builder`, in the marketplace `resume-builder-local`.

```
.claude-dev/
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
└── skills/
    └── resume-auto-mode/     # /resume-builder:resume-auto-mode <playbook> <arguments>
        ├── SKILL.md          # matches the request to a playbook
        ├── playbooks/
        │   ├── full-pipeline.md
        │   ├── ingest.md         # <company>
        │   ├── distill.md        # <company> <id>
        │   ├── verify.md         # <company> <id>
        │   ├── to-resume.md      # [base | <slug>]
        │   ├── to-brag.md        # <company>
        │   ├── steer.md          # [base | <slug>] <what to change>
        │   ├── review-resume.md  # [slug] [template]
        │   ├── wiki.md           # ingest | query | lint
        │   └── resume.md         # writing rules (copied from chuan-khuna/altr-stack)
        ├── references/
        │   ├── workflow.md       # layout, mapping schema, script rules (all playbooks)
        │   ├── evidence.md       # evidence file schema, citations, anonymisation
        │   ├── kami.md           # Kami design rules for the Typst resume
        │   ├── learning.md       # how every playbook learns: wiki/me.md and fixes
        │   └── skill-taxonomy.yml
        └── scripts/measure.sh    # builds and measures the resume (review-resume)
```

`to-resume`, `steer` and `review-resume` work on the Typst resume in `resume/` (see `resume/README.md`).

`wiki` maintains the knowledge base in `wiki/` (see `wiki/CLAUDE.md`). It is separate from
the evidence pipeline: no resume claim may rest on a wiki note.

The skills evolve: when a session teaches a lesson that holds for any user, Claude fixes the
skill it belongs to. The user's own preferences go to the gitignored `wiki/me.md`
instead, through `scripts/me.py`. Every playbook ends with a Learn step that applies
`skills/resume-auto-mode/references/learning.md`.

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
claude plugin install resume-builder@resume-builder-local --scope local
```

Local scope writes to `.claude/settings.local.json`, which is gitignored, so nothing about the
install is committed.

After you change a skill:

```bash
claude plugin marketplace update resume-builder-local
```
