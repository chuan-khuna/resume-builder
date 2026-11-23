# .claude-dev

A local Claude Code plugin, `resume-evidence`, in the marketplace `resume-builder-local`.

```
.claude-dev/
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── reference/
│   ├── workflow.md           # layout, mapping schema, script rules (all skills)
│   └── evidence.md           # evidence file schema, citations, anonymisation (distill, verify)
└── skills/
    ├── ingest/SKILL.md       # /resume-evidence:ingest <company>
    ├── distill/SKILL.md      # /resume-evidence:distill <company> <id>
    └── verify/SKILL.md       # /resume-evidence:verify <company> <id>
```

All skills are user-invoked. The design is in
[`docs/documents/ingest-distill-workflow.html`](../docs/documents/ingest-distill-workflow.html).

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
