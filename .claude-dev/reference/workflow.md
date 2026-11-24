# Evidence workflow: shared reference

Read by the `ingest`, `distill` and `verify` skills. The evidence file's own format is in
[`evidence.md`](evidence.md). How every skill learns from the user is in
[`learning.md`](learning.md).

## Steps

| Step | Skill | Reads | Writes |
| ---- | ----- | ----- | ------ |
| 1. Ingest | `/resume-evidence:ingest <company>` | `raw/<company>/mapping.yml` | `raw/<company>/repos/<id>/<slug>/`, `commit-summary.json`, `jira/<yyyy>.json`, `jira/merged.json`, `TODO.md` |
| 2. Distill | `/resume-evidence:distill <company> <id>` | the project's repos and Jira tickets, or, with no repos, the user's account in an interview | `evidence/<company>/<yyyy>-<id>.md` with a draft Summary |
| 3. Verify | `/resume-evidence:verify <company> <id>` | the evidence file, the user's answers | the same file, Summary confirmed, `reviewed:` set |
| 4. To resume | `/resume-evidence:to-resume [base \| <slug>]` | evidence files, the user's job facts | `resume/data/resume.yml` or `resume/versions/<slug>/resume.yml`, built PDF |
| 5. Review resume | `/resume-evidence:review-resume [slug] [template]` | the built PDF and its YAML | `resume/review/<slug>.html` (`index.html` for base) |
| 6. Steer | `/resume-evidence:steer [base \| <slug>] <what to change>` | the user's changes, evidence files | the target `resume.yml`; evidence files, for accounts the user gives |

Steps 4–6 use the `resume` skill for wording. Their rules are in each skill and in
`resume/README.md`.

## Layout

All paths are relative to the repo root.

```
raw/                                   # gitignored except the example
├── repository-mapping.example.yml     # schema with fake values
└── <company>/
    ├── mapping.yml                    # config, written by the user only
    ├── TODO.md                        # todos for this company's data
    ├── commit-summary.json            # per-repo load status and my commit counts (ingest)
    ├── jira/<yyyy>.json               # my Jira tickets, trimmed, by year created (ingest)
    ├── jira/merged.json               # every year merged, oldest first (ingest)
    ├── notes/<id>.md                  # private notes: limits of my own work (distill, verify)
    └── repos/<id>/<slug>/             # git clones of the sources, named by slug (ingest)
evidence/<company>/<yyyy>-<id>.md      # committed, anonymised
scripts/                               # committed helpers
wiki/                                  # LLM wiki: raw/ (gitignored), notes/, logs/
└── me.md                              # the user's preferences and needs (gitignored)
```

- `raw/` holds real client names and a Jira token. It stays local.
- Clones sit under `repos/`, so no project `id` can collide with `jira/` or a file the
  scripts write.
- `evidence/` and `scripts/` are committed, so they carry no real names, hosts or credentials.

## mapping.yml

Schema and an example: `raw/repository-mapping.example.yml`.

- `company`: folder name under `raw/` and `evidence/`.
- `me.names`, `me.emails`: my commit identity. Match them case-insensitively against git
  author name and email; a name matches as a substring.
- `jira`: `site`, `email`, `api_token`. Optional; without it, skip Jira.
- `projects[]`: `id` (path slug), `internal_name` (real name), `title` (anonymised name),
  `sources`, and optionally `jira`.
- `sources[]`: `url` (the git URL) and `slug` (the repo's anonymised name, by its role:
  `backend`, `worker`, `detection-lib`). A slug is lowercase kebab-case and unique within its
  project. Ingest clones into `repos/<id>/<slug>/`; evidence cites the repo by slug, in
  citations and in `verified:`. The user picks each slug once, so every distill run uses the
  same name. The real repo name, the last segment of `url`, stays banned in evidence.
- `jira`: a list of selectors that pick the project's
  tickets from `jira/merged.json`. `{project: X}` picks every ticket in Jira project X (key or
  name); `{project: X, epic: Y}` picks only the tickets under epic Y. Older projects usually
  have their own Jira project; newer ones are epics in a shared project.

The user owns `mapping.yml`. To change it, tell the user what to change.

## TODO.md

`raw/<company>/TODO.md` records what `mapping.yml` and `evidence/` cannot show. A project in
`mapping.yml` with no evidence file is already a todo, so it is not listed. Sections:

- **Projects to add to mapping.yml**: work with no repo found yet, with what is known about it.
- **Leads for distill**: facts to cover for a project, keyed by `id`. A lead points at
  evidence to find; it is not evidence.
- **Done**: ticked items, with the `id` they resolved to.

Tick an item and move it to Done in the same step that resolves it.

## Scripts

Write a helper into `scripts/` when a step needs one and none there fits. Check `scripts/`
first and reuse or extend what exists.

- Python, one file per command. Declare dependencies in `pyproject.toml` with `uv add <pkg>`;
  run with `uv run scripts/<name>.py`.
- First argument is `<company>`. Read paths, `me` and credentials from
  `raw/<company>/mapping.yml` at run time.
- Every client name, host, path and credential comes from `mapping.yml` or the arguments, so
  the script is safe to commit.
- A module docstring with usage examples.
- Lint and format with `uvx ruff check` and `uvx ruff format`.
