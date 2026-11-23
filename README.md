# resume-builder

A format and a standard for letting an LLM agent summarise **what you have done** at work,
from your repositories and Jira tickets.

The output is **evidence**: one Markdown file per project that states what you built, decided
or owned. Each claim cites the commit, path or ticket that proves it, and client names are
anonymised. Evidence is the ground truth you write a resume, CV or portfolio from, and every
line can be defended in an interview.

## How it works

Three steps, each a Claude Code skill:

1. **Ingest** (`/resume-evidence:ingest <company>`)
   - Update the config: you list your projects and their git repos in `mapping.yml`.
   - Load repository data: the agent clones every repo into `raw/<company>/`.
   - Load Jira data: the agent downloads the tickets assigned to you.
2. **Distill** (`/resume-evidence:distill <company> <project-id>`)
   - The agent uses the data in `raw/<company>/`. Git authorship decides what is yours; a
     ticket shows assignment, not authorship.
   - The agent writes `evidence/<company>/<yyyy>-<project-id>.md`. Every claim is cited and
     anonymised, and you review the file once.
3. **Verify** (`/resume-evidence:verify <company> <project-id>`)
   - The agent interviews you on the gaps git cannot answer: outcomes, scale, what shipped.
   - It folds your answers into the evidence and writes the file's `## Resume` section:
     context, issue, and resume bullets, each with a remark on what it traces to.

The full design is in
[`docs/documents/ingest-distill-workflow.html`](docs/documents/ingest-distill-workflow.html).

## Layout

```
raw/                                   # local only; commit only the example
├── repository-mapping.example.yml     # mapping schema with fake values
└── <company>/
    ├── mapping.yml                    # you write this: identity, Jira login, projects
    ├── TODO.md                        # projects still to add, leads for distill
    ├── jira/<yyyy>.json
    └── <project-id>/<repo>/
evidence/<company>/<yyyy>-<id>.md      # committed: anonymised, cited ground truth
scripts/                               # committed: helpers the agent writes as needed
.claude-dev/                           # the resume-evidence plugin: ingest and distill skills
```

`raw/` holds real client names and a Jira token, so it stays on your machine. Only
`evidence/` and `scripts/` carry your work into git, and both are free of real names.

## Get started

1. Install the tools and the plugin:
   ```bash
   mise install
   mise run plugins
   ```
2. Copy `raw/repository-mapping.example.yml` to `raw/<company>/mapping.yml`.
3. Fill in `me` (the names and emails you commit with), `jira`, and one entry per project.
4. Restart Claude Code, then run `/resume-evidence:ingest <company>`.
5. Run `/resume-evidence:distill <company> <project-id>` for each project.
6. Run `/resume-evidence:verify <company> <project-id>` to answer its questions and get bullets.

To update a project after new work, run distill again. It reads only the commits after the
`verified:` sha in the evidence file and adds new bullets.

## The standard

An evidence file is done when:

- every **What I Did** bullet cites `[repo:path]`, `[repo@sha]`, `[TICKET-123]` or
  `[me: yyyy-mm-dd]`;
- it claims only paths git confirms are yours, and names others' parts under **Not mine**;
- **Numbers** holds measured outcomes and business scale only, each with its scope;
- no client, brand, person, host or infra identifier remains;
- you have reviewed it.

Resume wording (which bullets, which numbers to quote) is the verify step, written into the
file's `## Resume` section on top of the evidence.
