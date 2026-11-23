# .claude-dev

A local Claude Code plugin, `resume-evidence`, in the marketplace `resume-builder-local`.

```
.claude-dev/
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── reference/workflow.md     # layout, mapping schema, script rules (shared by both skills)
└── skills/
    ├── ingest/SKILL.md       # /resume-evidence:ingest <company>
    └── distill/SKILL.md      # /resume-evidence:distill <company> <id>
```

Both skills are user-invoked. The design is in
[`docs/documents/ingest-distill-workflow.html`](../docs/documents/ingest-distill-workflow.html).

## Install

Try it for one session:

```bash
claude --plugin-dir ./.claude-dev
```

Install it for this repo:

```bash
claude plugin marketplace add ./.claude-dev --scope project
claude plugin install resume-evidence@resume-builder-local --scope project
```

The CLI saves the marketplace path in `.claude/settings.json` as an absolute path. Change it to
`"path": "./.claude-dev"` before you commit.

After you change a skill:

```bash
claude plugin marketplace update resume-builder-local
```
