# Evidence file: shared reference

Read by the `distill` and `verify` skills. One file per project at
`evidence/<company>/<yyyy>-<id>.md`.

## Schema

Distill writes every section, including a **draft** `## Summary`. Verify confirms the Summary
with the user, rewrites it, sets `reviewed:` and edits the other sections with the user's
answers. While `reviewed:` is empty, the Summary is a draft.

`## Summary` comes first because it is what a resume is written from; every section below it is
the evidence it rests on.

```markdown
---
id: <id>
title: <title from mapping.yml>
company: <company>                     # the folder slug under evidence/
period: yyyy-mm ~ yyyy-mm | present   # first to last commit of mine, or the user's account
role: <role>
status: shipped | wip | dropped
verified:
  <slug>: <HEAD sha read>              # one per source, by its slug in mapping.yml
reviewed: yyyy-mm-dd                   # set by verify when the user confirms the file
---

## Summary
### Resume bullets
- <resume bullet>                      # 3–6, strongest first; see Summary rules
### Remarks
- B1: traces to <What I Did bullet, short> · strength · caveat · fits which roles
- `<number left out>`: why it is not quoted, and how to make the point without it
- <scope caveat: joined an existing project, wip, prototype only, …>

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
```

## Summary rules

Shared by distill (draft) and verify (confirmed).

- **Source**: condense What I Did only. Never claim what What I Did does not list; one bullet
  may merge several What I Did bullets.
- **Bullets**: three to six, one per outcome, strongest first. Each starts with a past-tense
  verb and names what I built or decided, how, and the result, in about 25 words. Number them
  `B1`, `B2`, … only inside Remarks, not in the bullet text.
- **Numbers in bullets**: only measured or user-reported values from Numbers, with their scope.
  A change (before → after) beats scale, scale beats activity. At most two per bullet.
  Configured values describe design capacity: write "designed for", never as results. Counts of
  my own code (commits, files, endpoints, tests) stay out.
- **No measured impact**: name a verifiable outcome instead (shipped, still in use, adopted by
  another team, a failure removed). In a draft with no such outcome, write the bullet without
  one and add a Remark that the outcome is to confirm.
- **Shared work**: "with a teammate" or "led" only as the evidence supports; a shared area gets
  "contributed to" or names my part.
- **Unfinished work**: a `wip` or `dropped` project, or a feature that never shipped, reads as
  evaluated, prototyped or proposed, never as delivered.
- **Remarks**: one item per bullet (`B<n>: traces to … · strength · caveat · roles it fits:
  backend, ML, AI infra, data`); one item per number in Numbers that no bullet quotes, saying
  why and how to phrase the point without it; one item per scope caveat. Neutral wording:
  describe the work or the data, never a person.

## Citations

| Form | Means |
| ---- | ----- |
| `[<repo>:<path> 92%]` | my share of blame lines under that path |
| `[<repo>@<sha>]` | one of my commits |
| `[<KEY-123>]` | a Jira ticket |
| `[me: yyyy-mm-dd]` | the user's account, given on that date |

`<repo>` in a citation is the source's `slug` from `mapping.yml`, the anonymised name used
throughout the file. When the user's
account differs from git ("I committed it, but a teammate wrote the logic"), the user's account
wins: record it with a `[me: yyyy-mm-dd]` citation.

## Anonymisation

Anonymise the label, keep the engineering.

- **Banned terms**: every `internal_name`, real repo names (the last segment of each source
  `url`), the hosts and org names in source URLs,
  the Jira site, and any client, brand, product or person name found while reading. The
  `<company>` slug is allowed only in the `company:` field and the file path; it is banned
  everywhere else in the file.
- **Replace** with consistent generic placeholders that keep each thing's role: a client →
  "a retail client"; `shelf-lens.acme.co.th` / `shelf-lens-backend.acme.co.th` →
  `shelf-app.example.com` / `shelf-api.example.com`; a repo → its `slug` from `mapping.yml`
  (`backend`, "the backend repo"); a person → their role ("a teammate").
- **Remove** infra identifiers: IPs, server hostnames, tunnel IDs, bucket names, account IDs,
  ports, credentials, env values, internal paths.
- **Round** exact business figures that could identify a client ("1,247 stores" → "1,200+
  stores").
- **Keep** architecture, stack, patterns and scale figures: "behind a Cloudflare Tunnel on a
  single EC2 box" stays; the domain and IP go.
- Write in neutral wording that describes the work and the data, not people.

The **banned-term search** greps the file for every banned term. It passes at zero hits.
