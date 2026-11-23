---
name: ingest
description: Load a company's repositories and Jira tickets into raw/<company>/ from its mapping.yml.
disable-model-invocation: true
---

# Ingest

Load everything `raw/<company>/mapping.yml` names into `raw/<company>/`. Ingest only
copies data; reading it is the distill skill's job.

Read [`../../reference/workflow.md`](../../reference/workflow.md) first: it defines the layout,
the mapping schema and the rules for scripts.

## Steps

1. **Find the config.** Take `<company>` from the user's message; if it is missing, list the
   folders in `raw/` and ask. If `raw/<company>/mapping.yml` does not exist, copy
   `raw/repository-mapping.example.yml` there, ask the user to fill it in, and stop.
   _Done when_ `mapping.yml` parses and every project has `id`, `internal_name`, `title` and
   `sources`. Report each missing field to the user and stop until it is fixed.

2. **Load repository data.** Run `uv run scripts/ingest_repos.py <company>`; it does this step
   and step 4 and writes `raw/<company>/summary.json`. For every source of every project, the target is
   `raw/<company>/<id>/<repo-name>/`, where `<repo-name>` is the URL's last path segment
   without `.git`.
   - Target missing: `git clone <url> <target>`.
   - Target present: `git -C <target> fetch --all --prune`.
   - A clone or fetch fails (auth, wrong URL): record it and continue with the rest.

   _Done when_ every source is either cloned and fetched, or recorded as failed with its error.

3. **Load Jira data.** Skip this step if `jira:` is absent. `scripts/ingest_jira.py` writes
   one file per year created, `raw/<company>/jira/<yyyy>.json`, then merges them into
   `raw/<company>/jira/merged.json`. Each ticket keeps only `key`, `title`, `detail`, `type`,
   `status`, `project`, `epic`, `parent`, `assignee`, `created` and `resolved`. Pick the source:
   - `jira.api_token` is set: run `uv run scripts/ingest_jira.py <company>`. It searches
     `assignee = currentUser() ORDER BY created ASC` through the REST API, following every page.
   - No token, and the Atlassian MCP is connected: search with `searchJiraIssuesUsingJql`, JQL
     `assignee = currentUser() ORDER BY created ASC`, fields `summary`, `description`,
     `issuetype`, `status`, `project`, `parent`, `assignee`, `created`, `resolutiondate`,
     following every page. Save each page's JSON response as is to the scratchpad, then run
     `uv run scripts/ingest_jira.py <company> --from-raw <page files>`. Delete the page files.
   - Neither: tell the user to add an API token to `mapping.yml` or connect the Atlassian MCP,
     and skip Jira.

   _Done when_ `merged.json` exists and its ticket count equals the total the search reported.

4. **Check authorship coverage.** For each cloned repo, count my commits:
   `git -C <repo> log --all --format='%an <%ae>'`, matched against `me` as the reference
   describes. `ingest_repos.py` records the counts and date ranges per repo and per project in
   `raw/<company>/summary.json`, replacing the previous summary.

   _Done when_ `summary.json` lists every source in `mapping.yml`.

5. **Report** to the user from `summary.json`, as a table per project:
   - each repo: cloned / fetched / failed, my commit count, date range of my commits;
   - repos with zero commits of mine, flagged: the URL is wrong or `me` lacks a name or email;
   - Jira: ticket count per year and per Jira project, as `ingest_jira.py` prints them.

6. **Update `raw/<company>/TODO.md`.** Move to Done each "Projects to add" item that now has
   repos loaded under its `id`. Add each Jira project with tickets of mine but no matching
   project in `mapping.yml` to "Projects to add", with its ticket count and date range.

## Completion

Every source in `mapping.yml` appears in `summary.json` and the report as loaded or failed, Jira is downloaded or
skipped, every zero-commit repo is flagged, and `TODO.md` is updated.
