---
name: distill
description: Distill one project's raw repositories and Jira tickets into an anonymised, cited evidence file.
disable-model-invocation: true
---

# Distill

Turn one project's data in `raw/<company>/` into `evidence/<company>/<yyyy>-<id>.md`: the
ground truth of **what I did**, where every claim cites its evidence and no real name leaks.

Read [`../../reference/workflow.md`](../../reference/workflow.md) first: it defines the layout,
the mapping schema and the rules for scripts.

## Steps

1. **Pick the project.** Take `<company>` and `<id>` from the user's message; if either is
   missing, list the projects in `raw/<company>/mapping.yml` and ask. If
   `raw/<company>/<id>/` has no repos, tell the user to run ingest and stop.
   - An evidence file matching `evidence/<company>/*-<id>.md` exists: **update** mode. Read it;
     its `verified:` shas mark where the new commits start.
   - None exists: **new** mode.

   Read the project's items under "Leads for distill" in `raw/<company>/TODO.md`: each is a
   fact to confirm or reject in steps 2–4.

2. **Establish authorship.** Use the authorship script in `scripts/`; write it first if none
   exists. Per repo it reports, with `--all` on every git command:
   - authors: `git shortlog -sne --all`;
   - per directory, two levels deep: my commit count and my share of `git blame` lines at HEAD;
   - my commits: sha, date, message, files touched;
   - in update mode, only commits after the `verified:` sha.

   Claim only paths where my share is real. Project-wide files (README, `pyproject.toml`,
   lock files, CI) describe the project, not my part.
   _Done when_ every top-level area of every repo is classed as **mine**, **shared** or
   **not mine**.

3. **Read the sources.** For each area classed mine or shared: its code, the diffs of my main
   commits, dependency files, README and in-repo docs. Read enough to state what each part does,
   the pattern behind it, and the trade-off taken.

4. **Read Jira.** Use the Jira query script in `scripts/`; write it first if none exists. Find
   the project's tickets by `internal_name`, repo names, Jira project and epic. A ticket proves
   assignment and dates, not authorship: cite it beside git evidence, and send a claim backed
   only by tickets to Open questions.

5. **Write the evidence file** at `evidence/<company>/<yyyy>-<id>.md`, where `yyyy` is the
   year of my first commit in the project. Use the [schema](#evidence-file). In update mode,
   add new bullets and keep the existing ones as written.
   _Done when_ every What I Did bullet carries at least one [citation](#citations).

6. **Anonymise.** Apply the [rules](#anonymisation), then search the file for every banned
   term. _Done when_ the search returns zero hits.

7. **Review with the user.** Show the file and list the Open questions. When the user's
   account differs from git ("I committed it, but a teammate wrote the logic"), the user's
   account wins: record it with a `[me: yyyy-mm-dd]` citation.
   _Done when_ the user confirms the file.

8. **Update `raw/<company>/TODO.md`.** Move this project's leads to Done, each noting whether
   it went into the file or into Open questions.

## Evidence file

```markdown
---
id: <id>
title: <title from mapping.yml>
company: <company>
period: yyyy-mm ~ yyyy-mm | present   # first to last commit of mine, or the user's account
role: <role>
status: shipped | wip | dropped
verified:
  <repo-name>: <HEAD sha read>
---

## Context
Who it was for, the problem, rough scale. May describe the whole project.

## What I Did
- One item per thing I owned, decided or built: module, pattern, trade-off. <citation>

## Numbers
| Value | Scope | Source |
| ----- | ----- | ------ |
Measured outcomes and business scale only (latency, users, streams, clients), each with its
scope. Counts of my own code (commits, files, endpoints) stay out.

## Tools
tools: <only tech actually used: dependency files, scripts, commands really run>
Studied, not used: <researched or compared only>

## Architecture
A Mermaid diagram of the system or data flow, plus a short explanation.

## Not mine
- Parts built by others, named by role ("a teammate"), with their citation.

## Open questions
- Claims backed only by tickets, gaps git cannot answer, facts to confirm with the user.
```

## Citations

| Form | Means |
| ---- | ----- |
| `[<repo>:<path> 92%]` | my share of blame lines under that path |
| `[<repo>@<sha>]` | one of my commits |
| `[<KEY-123>]` | a Jira ticket |
| `[me: yyyy-mm-dd]` | the user's account, given on that date |

Repo names in citations are the anonymised form used throughout the file.

## Anonymisation

Anonymise the label, keep the engineering.

- **Banned terms**: `company`, every `internal_name`, repo names, the hosts and org names in
  source URLs, the Jira site, and any client, brand, product or person name found while
  reading.
- **Replace** with consistent generic placeholders that keep each thing's role: a client →
  "a retail client"; `shelf-lens.acme.co.th` / `shelf-lens-backend.acme.co.th` →
  `shelf-app.example.com` / `shelf-api.example.com`; a repo → its role ("the backend repo",
  `backend`); a person → their role ("a teammate").
- **Remove** infra identifiers: IPs, server hostnames, tunnel IDs, bucket names, account IDs,
  ports, credentials, env values, internal paths.
- **Keep** architecture, stack, patterns and scale figures: "behind a Cloudflare Tunnel on a
  single EC2 box" stays; the domain and IP go.
- Write in neutral wording that describes the work and the data, not people.

## Completion

The file follows the schema, every What I Did bullet is cited, the banned-term search returns
zero hits, `verified:` holds the HEAD sha read for every repo, the user has confirmed it, and the
project's leads in `TODO.md` are resolved.
