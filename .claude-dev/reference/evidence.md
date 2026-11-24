# Evidence file: shared reference

Read by the `distill` and `verify` skills. One file per project at
`evidence/<company>/<yyyy>-<id>.md`, plus an optional [private note](#private-notes) at
`raw/<company>/notes/<id>.md`.

## Schema

Distill writes every section, including a **draft** `## Summary`. Verify confirms the Summary
with the user, rewrites it, sets `reviewed:` and edits the other sections with the user's
answers. While `reviewed:` is empty, the Summary is a draft.

`## Summary` comes first because it is what a resume is written from; every section below it is
the evidence it rests on.

**Older files** have a flat Summary (three to six bullets, no areas or stars) and a plain
`## Numbers` table. Distill and verify migrate a file to this schema the next time they run on
it: group its bullets into areas, add stars, turn `## Numbers` into `## Numbers & Impact` with
IDs and a Kind per row, and assess its Impact. Until then, to-resume, steer and review-resume
read the old sections as they are.

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
### <Area of work>                     # areas that do not overlap; see Summary rules
- ★★★ <resume bullet>                  # strongest first inside the area
- ★★ <resume bullet>
### <Another area>
- ★ <resume bullet>
### Remarks
- B1: traces to <What I Did bullet, short> · N1, I1 · strength · caveat · fits which roles
- N3 / I2 not used: why it is not quoted, and how to make the point without it
- <scope caveat: joined an existing project, wip, prototype only, …>

## Context
Who it was for, the problem, rough scale. May describe the whole project.

## What I Did
- One item per thing I owned, decided or built: module, pattern, trade-off. <citation>

## Numbers & Impact
### Numbers
| ID | Value | Kind | Scope | Source |
| -- | ----- | ---- | ----- | ------ |
| N1 | 58 s → 15 s | before → after | 20 checkpoints' daily report (measured) | [repo@sha] |
Every figure in the file, once. See Numbers & Impact rules.

### Impact
| ID | Kind | Type | Claim | Basis | Confidence | Status |
| -- | ---- | ---- | ----- | ----- | ---------- | ------ |
| I1 | fact | reliability | <what changed, checkable> | <citation> | high | — |
| I2 | assessed | rushed delivery | <my reading> | N1, I1 | medium | assessed |
What the work changed, whether it has a number or not. See Numbers & Impact rules.

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

Shared by distill (draft) and verify (confirmed). The Summary is a pool the resume picks from,
not the resume itself: write every bullet worth picking.

- **Source**: condense What I Did, backed by Numbers & Impact. Never claim what What I Did does
  not list; one bullet may merge several What I Did bullets.
- **Areas**: group the bullets under `### <Area>` headings, one per area of work I was
  responsible for in the project (two to four words, sentence case, for example "ML / computer
  vision", "Backend & reliability", "Security"). Areas do not overlap: merge an area into the
  one that contains it, and split every area on the same axis, the area of work, never a
  practice such as "Testing" or "Documentation" (its results go under the area they served).
  Every What I Did bullet belongs to exactly one area; no fact repeats across areas. A project
  with one area of work has one heading.
- **Bullets**: no fixed count. One bullet per distinct outcome, strongest first inside each
  area. Each starts with a past-tense verb and names what I built or decided, how, and the
  result, in about 25 words. Number them `B1`, `B2`, … across the whole file (not per area),
  only inside Remarks, not in the bullet text.
- **Strength**: prefix each bullet `★★★` (a measured or confirmed outcome, or the project's
  defining work), `★★` (a solid outcome with a fact-kind Impact) or `★` (activity or a
  supporting detail). to-resume picks the strongest that fit the page and the role.
- **Numbers in bullets**: only measured or user-reported values from Numbers, with their scope.
  A change (before → after) beats scale, scale beats activity. At most two per bullet.
  Configured values describe design capacity: write "designed for", never as results. Counts of
  my own code (commits, files, endpoints, tests) stay out; a count of bugs or incidents fixed
  may go in.
- **Impact in bullets**: a `fact` or `user` Impact item may back a bullet's result. An
  `assessed` item backs a bullet only once verify sets its Status to `confirmed`; until then,
  the bullet leaves it out and its Remark names the item.
- **No measured impact**: name a verifiable outcome instead (shipped, still in use, adopted by
  another team, a failure removed), from a `fact` Impact item. In a draft with no such outcome,
  write the bullet without one and add a Remark that the outcome is to confirm.
- **Shared work**: "with a teammate" or "led" only as the evidence supports; a shared area gets
  "contributed to" or names my part.
- **Unfinished work**: a `wip` or `dropped` project, or a feature that never shipped, reads as
  evaluated, prototyped or proposed, never as delivered.
- **Remarks**: one item per bullet (`B<n>: traces to … · Numbers and Impact IDs it uses ·
  strength · caveat · roles it fits: backend, ML, AI infra, data`); one item per Numbers row
  and per Impact item that no bullet uses, saying why and how to phrase the point without it;
  one item per scope caveat. Neutral wording: describe the work or the data, never a person.
- **Caveats state the limit, not the reason.** A caveat says what a bullet must not claim
  ("tests are minimal: do not claim test coverage"). The personal reason behind it (time,
  skill, interest) goes in the [private note](#private-notes), never in the evidence file.

## Numbers & Impact rules

Shared by distill (draft) and verify (confirmed). Numbers holds every figure; Impact holds what
the work changed. A figure lives only in Numbers: an Impact item points to it by ID, so no
number is lost or copied out of step.

### Numbers

- One row per figure, `N1`, `N2`, … Collect every figure the sources give, including the ones
  no bullet will quote: they are what a Remark or an interview answer draws on.
- **Kind** says what the figure is: `before → after`, `performance` (latency, throughput),
  `accuracy` (precision, recall, mAP, top-1), `cost`, `scale` (users, records, streams,
  clients, workers), `bugs / incidents` (bugs or incidents fixed, from `fix:` commits or Jira
  Bug tickets), `delivery speed` (the span of a feature's commits, a ticket's created →
  resolved time), `configured` or `estimated`.
- **Scope** says what was measured, on what, and whether the value is measured, configured,
  estimated or user-reported.
- Counts of my own code (commits, files, lines, endpoints, tests) stay out, except as a
  `delivery speed` figure that backs an Impact item, and never in a bullet.

### Impact

One row per thing the work changed, `I1`, `I2`, … Every row has a Kind:

| Kind | Means | Used in a bullet |
| ---- | ----- | ---------------- |
| `fact` | Checkable in git, Jira, an ADR or a report: the change exists and does what it says | Yes, like a What I Did bullet |
| `assessed` | My reading of the work, built on at least one `fact` row or Numbers row | Only once verify sets Status to `confirmed` |
| `user` | The user's account, cited `[me: yyyy-mm-dd]` | Yes |

- **Basis** cites the evidence (a citation, a What I Did bullet) or, for `assessed`, the IDs it
  rests on (`N1, I3`). An `assessed` row with no `fact` or Numbers row under it is dropped.
- **Confidence** is `high`, `medium` or `low`: how strongly the basis supports the claim.
- **Status** is `—` for `fact` and `user`; `assessed` until verify confirms it (`confirmed`) or
  the user rejects it (delete the row; its basis rows stay).
- **Types**, with the signals that reveal them. Assess every type the sources support; a type
  with no basis is left out, never guessed:

  | Type | Example claim | Signals |
  | ---- | ------------- | ------- |
  | performance | report generation 58 s → 15 s | before → after figures in reports, commits, tickets |
  | cost | one-ninth the cost per image; re-runs skip unchanged inputs | provider prices, cost columns, caching or skip logic |
  | accuracy / quality | 89% top-1 on 739 labelled crops | evaluation reports, benchmark output |
  | reliability | jobs survive restarts and out-of-memory kills | ADRs, retry or queue code, `fix:` commits after incidents |
  | data correctness | stopped lost events; fixed wrong shelf counts | bug tickets, fixes with tests |
  | security | closed a cross-tenant data leak | permission fixes, security ADRs, pentest tickets |
  | bugs / incidents | fixed 12 production bugs | Jira Bug tickets resolved, `fix:` commits |
  | rushed delivery | delivered a full feature in one day | commit density, ticket created → resolved, deadlines in tickets |
  | sole ownership | owned design to deployment alone | authorship share across every area |
  | adoption | an R&D result taken into a product; a library used by another team | ADRs or commits in another project, imports, tickets |
  | avoided waste | analysis stopped a feature or a retrain that would not have helped | reports with a recommendation, rejected options in ADRs |
  | migration / modernisation | moved a queue from Kafka to RabbitMQ | migration commits, infra changes |
  | team enablement | one-command local stack, runbook, starter template, CI/CD | tooling commits, docs, runner config |
  | maintainability | API-level tests, ADRs comparing alternatives, specs before code | test files, `docs/adr`, specs |
  | production / client outcome | shipped; in client trial; still in use | deploy docs, tickets, the user |
  | governance / compliance | approval obtained before sending data to an outside service | ADRs, tickets |
  | knowledge transfer | taught labelling; wrote handoffs | docs, tickets, the user |
  | rescue / takeover | took over legacy code and stabilised it | authorship history, tickets |

## Private notes

`raw/<company>/notes/<id>.md` holds the honest account of the limits of my own work, so the
owner has the facts at hand, for example when asked in an interview. It is gitignored with
the rest of `raw/`. Verify and distill write it from the user's answers. No skill reads it to
write a resume claim: evidence stays the ground truth.

One bullet per limit, citing `[me: yyyy-mm-dd]`, and naming the evidence bullet or section it
explains:

```markdown
- B2: built under a two-week deadline, so tests were kept minimal. [me: 2026-11-23]
- What I Did 3: first project in Go; I learnt it on the job and the first version needed a
  refactor. [me: 2026-11-23]
```

- **Record**: what held my work back, stated as fact: too little time, a skill I lacked then,
  low interest that led to less effort, a scope cut. A cause outside my control is recorded as
  a condition of the work ("requirements changed twice mid-sprint").
- **Never record**: blame or criticism of anyone (a teammate, a manager, the client, the
  employer), offensive or insulting words, or wording that makes me look worse than the facts
  ("I was lazy" → "low priority for me; I spent less time on it").
- **Claim limits**: when a limit narrows what a bullet may claim, also add a caveat Remark in
  the evidence file that states the limit in neutral words, without the reason.

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
