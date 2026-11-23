# Evidence workflow: shared reference

Read by the `ingest` and `distill` skills. Two steps: **ingest** loads raw data, **distill**
turns it into evidence.

## Layout

All paths are relative to the repo root.

```
raw/                                   # gitignored except the example
├── repository-mapping.example.yml     # schema with fake values
└── <company>/
    ├── mapping.yml                    # config, written by the user only
    ├── jira/<yyyy>.json               # Jira tickets, by year created
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

## Scripts

Write a helper into `scripts/` when a step needs one and none there fits. Check `scripts/`
first and reuse or extend what exists.

- Python, one file per command, with PEP 723 inline metadata for dependencies; run with
  `uv run scripts/<name>.py`.
- First argument is `<company>`. Read paths, `me` and credentials from
  `raw/<company>/mapping.yml` at run time.
- Every client name, host, path and credential comes from `mapping.yml` or the arguments, so
  the script is safe to commit.
- A module docstring with usage examples.
- Lint and format with `uvx ruff check` and `uvx ruff format`.
