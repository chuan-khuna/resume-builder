# Evidence file: shared reference

Read by the `distill` and `verify` skills. One file per project at
`evidence/<company>/<yyyy>-<id>.md`.

## Schema

Distill writes every section except `## Resume`; verify writes `## Resume`, sets `reviewed:` and
edits the other sections with the user's answers.

```markdown
---
id: <id>
title: <title from mapping.yml>
company: <company>                     # the folder slug under evidence/
period: yyyy-mm ~ yyyy-mm | present   # first to last commit of mine, or the user's account
role: <role>
status: shipped | wip | dropped
verified:
  <repo-name>: <HEAD sha read>
reviewed: yyyy-mm-dd                   # set by verify when the user confirms the file
---

## Context
Who it was for, the problem, rough scale. May describe the whole project.

## What I Did
- One item per thing I owned, decided or built: module, pattern, trade-off. <citation>

## Numbers
| Value | Scope | Source |
| ----- | ----- | ------ |
Measured outcomes and business scale only (latency, users, streams, clients), each with its
scope. The Scope says whether the value is measured, configured, estimated or user-reported.
Counts of my own code (commits, files, endpoints) stay out.

## Tools
tools: <only tech actually used: dependency files, scripts, commands really run>
Studied, not used: <researched or compared only>

## Architecture
A Mermaid diagram of the system or data flow, plus a short explanation.

## Not mine
- Parts built by others, named by role ("a teammate"), with their citation.

## Open questions
- Claims backed only by tickets, gaps git cannot answer, facts to confirm with the user.

## Resume
### Context
One or two lines a recruiter reads first: the client type, the product, the setting.
### Issue
The problem the work solved and why it mattered, in one or two lines.
### Bullets
- <resume bullet>
  - Remark: <traces to · strength · caveat · fits which roles>
```

## Citations

| Form | Means |
| ---- | ----- |
| `[<repo>:<path> 92%]` | my share of blame lines under that path |
| `[<repo>@<sha>]` | one of my commits |
| `[<KEY-123>]` | a Jira ticket |
| `[me: yyyy-mm-dd]` | the user's account, given on that date |

Repo names in citations are the anonymised form used throughout the file. When the user's
account differs from git ("I committed it, but a teammate wrote the logic"), the user's account
wins: record it with a `[me: yyyy-mm-dd]` citation.

## Anonymisation

Anonymise the label, keep the engineering.

- **Banned terms**: every `internal_name`, repo names, the hosts and org names in source URLs,
  the Jira site, and any client, brand, product or person name found while reading. The
  `<company>` slug is allowed only in the `company:` field and the file path; it is banned
  everywhere else in the file.
- **Replace** with consistent generic placeholders that keep each thing's role: a client →
  "a retail client"; `shelf-lens.acme.co.th` / `shelf-lens-backend.acme.co.th` →
  `shelf-app.example.com` / `shelf-api.example.com`; a repo → its role ("the backend repo",
  `backend`); a person → their role ("a teammate").
- **Remove** infra identifiers: IPs, server hostnames, tunnel IDs, bucket names, account IDs,
  ports, credentials, env values, internal paths.
- **Round** exact business figures that could identify a client ("1,247 stores" → "1,200+
  stores").
- **Keep** architecture, stack, patterns and scale figures: "behind a Cloudflare Tunnel on a
  single EC2 box" stays; the domain and IP go.
- Write in neutral wording that describes the work and the data, not people.

The **banned-term search** greps the file for every banned term. It passes at zero hits.
