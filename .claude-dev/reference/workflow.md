# Evidence workflow: shared reference

Read by the `ingest`, `distill` and `verify` skills. Three steps: **ingest** loads raw data,
**distill** turns it into evidence, **verify** confirms it with the user and adds resume
bullets. The evidence file's own format is in [`evidence.md`](evidence.md).

## Layout

All paths are relative to the repo root.

```
raw/                                   # gitignored except the example
├── repository-mapping.example.yml     # schema with fake values
└── <company>/
    ├── mapping.yml                    # config, written by the user only
    ├── TODO.md                        # todos for this company's data
    ├── summary.json                   # per-repo load status and my commit counts (ingest)
    ├── jira/<yyyy>.json               # my Jira tickets, trimmed, by year created (ingest)
    ├── jira/merged.json               # every year merged, oldest first (ingest)
    └── <id>/<repo-name>/              # git clones of the sources
evidence/<company>/<yyyy>-<id>.md      # committed, anonymised
scripts/                               # committed helpers
```

- `raw/` holds real client names and a Jira token. It stays local.
- `evidence/` and `scripts/` are committed, so they carry no real names, hosts or credentials.

## mapping.yml

Schema and an example: `raw/repository-mapping.example.yml`.

- `company`: folder name under `raw/` and `evidence/`.
- `me.names`, `me.emails`: my commit identity. Match them case-insensitively against git
  author name and email; a name matches as a substring.
- `jira`: `site`, `email`, `api_token`. Optional; without it, skip Jira.
- `projects[]`: `id` (path slug), `internal_name` (real name), `title` (anonymised name),
  `sources` (git URLs).

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
