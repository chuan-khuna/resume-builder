# Ingest playbook

Load everything `raw/<company>/mapping.yml` names into `raw/<company>/`. Ingest only
copies data; reading it is the distill skill's job.

Read [`../references/workflow.md`](../references/workflow.md) first: it defines the layout,
the mapping schema and the rules for scripts.

## Steps

1. **Find the config.** Take `<company>` from the user's message; if it is missing, list the
   folders in `raw/` and ask. If `raw/<company>/mapping.yml` does not exist, copy
   `raw/repository-mapping.example.yml` there, ask the user to fill it in, and stop.
   _Done when_ `mapping.yml` parses, every project has `id`, `internal_name`, `title` and
   `sources`, and every source has a `url` and a `slug`. Report each missing field to the user
   and stop until it is fixed. A bare URL in `sources` is the old format: tell the user to
   rewrite it as `{url, slug}`, and suggest a role slug for it (`backend`, `worker`), never the
   real repo name.

2. **Load repository data.** Run `uv run scripts/ingest_repos.py <company>`; it does this step
   and step 4 and writes `raw/<company>/commit-summary.json`. It checks every source's `url`
   and `slug` first and stops on an error. For every source of every project, the target is
   `raw/<company>/repos/<id>/<slug>/`.
   - Target missing: `git clone <url> <target>`.
   - Target present: `git -C <target> fetch --all --prune`, then fast-forward the checked-out
     branch to its upstream. A fetch alone moves only the remote branches, and blame reads the
     checked-out one. Skip the fast-forward when the working tree has changes or the branch has
     diverged, and record why.
   - A clone or fetch fails (auth, wrong URL): record it and continue with the rest.

   _Done when_ every source is either cloned and fetched, or recorded as failed with its error.

3. **Load Jira data.** Skip this step if `jira:` is absent. `scripts/ingest_jira.py` writes
   one file per year created, `raw/<company>/jira/<yyyy>.json`, then merges them into
   `raw/<company>/jira/merged.json`. Each ticket keeps only `key`, `title`, `detail`, `type`,
   `status`, `project`, `epic`, `parent`, `assignee`, `created` and `resolved`. Pick the source:
   - `jira.api_token` is set: run `uv run scripts/ingest_jira.py <company>`. It searches
     `assignee = currentUser() ORDER BY created ASC` through the REST API, following every page.
   - No token, and the Atlassian MCP is connected: first check that `currentUser()` is the
     user: take one ticket and match its assignee's display name against `me.names`. Get the
     total with `searchResultMode: count`. Then search with `searchJiraIssuesUsingJql`, JQL
     `assignee = currentUser() ORDER BY created ASC`, `view: full` (it includes the parent's
     issue type), `maxResults: 100`, fields `summary`, `description`, `issuetype`, `status`,
     `project`, `parent`, `assignee`, `created`, `resolutiondate`, following `nextPageToken`
     until `isLast`. A full page is too large to show, so the tool saves it to a file: copy
     each file to the scratchpad as `page-NN.json`. Then run
     `uv run scripts/ingest_jira.py <company> --from-raw <page files>`.
   - Neither: tell the user to add an API token to `mapping.yml` or connect the Atlassian MCP,
     and skip Jira.

   _Done when_ `merged.json` exists and its ticket count equals the total the search reported.

4. **Check authorship coverage.** For each cloned repo, count my commits:
   `git -C <repo> log --all --format='%an <%ae>'`, matched against `me` as the reference
   describes. `ingest_repos.py` records the counts and date ranges per repo and per project in
   `raw/<company>/commit-summary.json`, replacing the previous summary.

   _Done when_ `commit-summary.json` lists every source in `mapping.yml`.

5. **Report** to the user from `commit-summary.json`, as a table per project:
   - each repo, by slug: cloned / fetched / failed, my commit count, date range of my commits;
   - repos with zero commits of mine, flagged: the URL is wrong or `me` lacks a name or email;
   - repos whose checked-out branch was not fast-forwarded, with the reason;
   - per repo, the remote branches holding commits of mine the checked-out branch lacks
     (`branches_ahead`). Distill reads blame from one of them with `--ref`;
   - Jira: ticket count per year and per Jira project, as `ingest_jira.py` prints them.

6. **Update `raw/<company>/TODO.md`.** Move to Done each "Projects to add" item that now has
   repos loaded under its `id`. Run `uv run scripts/jira_tickets.py <company> --unmapped`: it
   lists the Jira projects and epics with tickets of mine that no project's `jira` selectors
   pick. For each that is real work, either tell the user which `jira` selector to add to an
   existing project in `mapping.yml`, or add it to "Projects to add" with its ticket count and
   date range.

7. **Learn.** Apply [`../references/learning.md`](../references/learning.md). Typical
   lessons here: a script that failed on a source or a Jira response (fix the script), and
   how the user wants projects split or named.

## Completion

Every source in `mapping.yml` appears in `commit-summary.json` and the report as loaded or failed, Jira is downloaded or
skipped, every zero-commit repo is flagged, and `TODO.md` is updated.
