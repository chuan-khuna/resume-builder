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

2. **Load repository data.** For every source of every project, the target is
   `raw/<company>/<id>/<repo-name>/`, where `<repo-name>` is the URL's last path segment
   without `.git`.
   - Target missing: `git clone <url> <target>`.
   - Target present: `git -C <target> fetch --all --prune`.
   - A clone or fetch fails (auth, wrong URL): record it and continue with the rest.

   _Done when_ every source is either cloned and fetched, or recorded as failed with its error.

3. **Load Jira data.** Skip this step if `jira:` is absent. Use the Jira download script in
   `scripts/`; write it first if none exists. It must:
   - authenticate with basic auth `jira.email:jira.api_token` against
     `https://<jira.site>`;
   - search `assignee = currentUser() ORDER BY created ASC`, following every page;
   - fetch `summary`, `status`, `issuetype`, `project`, `parent`, `labels`, `created`,
     `resolutiondate`, `description`, `comment`;
   - write one file per year created to `raw/<company>/jira/<yyyy>.json`, replacing the
     previous download.

   _Done when_ the yearly files exist and their ticket total equals the total the search
   reported.

4. **Check authorship coverage.** For each cloned repo, count my commits:
   `git -C <repo> log --all --format='%an <%ae>'`, matched against `me` as the reference
   describes.

5. **Report** to the user, as a table per project:
   - each repo: cloned / fetched / failed, my commit count, date range of my commits;
   - repos with zero commits of mine, flagged: the URL is wrong or `me` lacks a name or email;
   - Jira: ticket count per year, and ticket count per Jira project.

6. **Update `raw/<company>/TODO.md`.** Move to Done each "Projects to add" item that now has
   repos loaded under its `id`. Add each Jira project with tickets of mine but no matching
   project in `mapping.yml` to "Projects to add", with its ticket count and date range.

## Completion

Every source in `mapping.yml` appears in the report as loaded or failed, Jira is downloaded or
skipped, every zero-commit repo is flagged, and `TODO.md` is updated.
