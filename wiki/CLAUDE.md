# Wiki: schema

A personal knowledge base the LLM writes and keeps current, after Karpathy's LLM Wiki pattern.
The user curates sources and asks questions; the LLM summarises, files, cross-links and keeps
every note consistent. Open `wiki/` as an Obsidian vault to browse it.

Scope: what the user learns around the job search and their field: job ads, companies, roles,
interview and resume advice, technologies, papers, talks. It is not about the user's own past
work: that is `evidence/`, and **a wiki note never backs a resume claim**. A note may point
to evidence; evidence never cites the wiki.

## Layout

```
wiki/
├── CLAUDE.md          # this schema; the user and the LLM evolve it together
├── me.md              # the user's preferences and needs; gitignored, kept by scripts/me.py
├── raw/               # sources, immutable: read, never edit, rename or delete
│   └── <yyyy-mm-dd>-<slug>.<ext>   # the date the user added it
├── notes/             # distilled knowledge, written only by the LLM
│   ├── index.md       # entry point: every note, one line each, by type
│   └── <slug>.md      # one note per source, entity, concept, topic or answer
└── logs/
    └── <yyyy-mm-dd>.md   # what happened that day: ingests, queries, lint passes
```

- `me.md` is not a note: the root `CLAUDE.md` loads it each session, and
  `.claude-dev/skills/resume-auto-mode/references/learning.md` says how to keep it. Follow it here too.
- Everything here except `me.md` is committed and pushed: `raw/`, `notes/` and `logs/`. So
  `raw/` holds only public sources, saved in full, and nothing in the wiki carries a sensitive
  detail: see [Sensitive data](#sensitive-data).
- Slugs are lowercase kebab-case and unique across `notes/`. A note's slug never changes;
  to rename, change its `title`.

## Note format

```markdown
---
title: Retrieval-augmented generation
type: concept            # source | entity | concept | topic | answer
sources: [raw/2026-11-24-rag-survey.pdf]   # raw files this note draws on; [] if none
created: 2026-11-24
updated: 2026-11-24
tags: [llm, retrieval]
---

# Retrieval-augmented generation

One-paragraph summary first: what it is and why it matters to the user.

## …sections the type needs…

## Open questions
```

| Type | One per | Holds |
| ---- | ------- | ----- |
| `source` | raw file | Summary, key claims, what it changes in the wiki; slug matches the raw file's |
| `entity` | company, person, product, tool | Facts about it, linked to the sources stating them |
| `concept` | idea, method, technique | Definition, how it works, trade-offs, where the sources disagree |
| `topic` | theme spanning many notes | Synthesis: the current view, the evidence for it, what would change it |
| `answer` | filed query | The question, the answer, the notes it drew on |

Rules for every note:

- **Cite.** Each claim ends with its source: `[[source-slug]]` for a source note, or
  `(raw/<file>, p. 3)` for a place in a raw file. A claim with no source is the LLM's
  inference and says so: "Inference: …".
- **Link.** Link the first mention of every other note in each section with `[[slug]]`. Make
  a note for any entity or concept that two or more notes mention.
- **Contradictions.** When sources disagree, keep both claims, each cited, under a
  `> [!warning] Contradiction` callout, and add the question to Open questions. Never
  silently overwrite an older claim; mark it superseded and cite what superseded it.
- Write in British English, plain and specific, by the `resume` playbook's Grammar rules.

## Sensitive data

The repo-root `raw/` holds the user's work data: git clones, Jira exports, `mapping.yml` with
credentials, and private notes. Everything in `wiki/raw/`, `wiki/notes/` and `wiki/logs/` is
committed and pushed, so none of it may carry a detail from there. Keep the knowledge; drop what identifies
it.

1. **Never ingest the repo-root `raw/`.** The wiki's sources are `wiki/raw/` only. Do not
   copy, quote, summarise or link a file from `raw/<company>/`. For knowledge from the user's
   own work, link the anonymised evidence file instead (`evidence/<company>/<file>.md`), and
   copy nothing from it that its own rules would not allow.
2. **Banned in every note and log entry**, whatever the source:
   - each `internal_name`, real repo name, source org and private host in any
     `raw/<company>/mapping.yml`, and the Jira site;
   - the `<company>` slug and any client, brand or product name met through the user's work;
   - credentials, tokens, keys, env values, and the emails in `me.emails` or `jira.email`;
   - infra identifiers: IPs, internal hostnames, bucket names, account IDs, ports, internal
     paths;
   - names, emails and phone numbers of colleagues, clients or recruiters: write the role
     ("a recruiter", "a teammate");
   - exact business figures of a client or employer: round them ("1,200+ stores").
3. **Public facts stay.** A company, person or product named in a public source the user
   chose (a published job ad, article, paper, talk) may have an `entity` note. The line is the
   source: public knowledge is allowed; anything learned through the user's job is not.
4. **`wiki/raw/` holds public sources only.** It is committed, so never save a private source
   there: a call transcript, an internal doc, a recruiter's email, anything learned through
   the user's job. If the user wants the lesson of a private source kept, write it straight
   into a note with `sources: []`, cited as the user's account (`(user, yyyy-mm-dd)`), with
   no identifiers. Name each raw file by its topic.
5. **Replace, don't hint.** Use the placeholders from `.claude-dev/skills/resume-auto-mode/references/evidence.md`
   "Anonymisation": a client → "a retail client"; a repo → its role ("the backend repo").
   No initials, partial names or nicknames that point back.
6. **Check before you finish.** `uv run scripts/wiki.py lint` searches notes, logs and the text
   files in `wiki/raw/` for every term from `raw/*/mapping.yml` and fails on a hit. It cannot
   know client or person names met while reading, nor read a PDF, so read each note and
   source you added for them too.
7. **If a detail was already committed**, remove it, tell the user which commit holds it, and
   let the user decide whether to rewrite history. Do not push until they decide.

## index.md

The catalog the LLM reads first for every query. One section per type, one bullet per note,
sorted by title: `- [[slug]] — one-line summary (updated yyyy-mm-dd)`. Every note appears
exactly once. Update it in the same change as the notes.

## logs/

One file per day, append-only. Each entry starts with a fixed prefix so the log is
greppable (`grep -h '^## \[' wiki/logs/*.md | tail -5`):

```markdown
## [2026-11-24 14:05] ingest | RAG survey
- Source: raw/2026-11-24-rag-survey.pdf
- Created: [[rag-survey]], [[reranking]]
- Updated: [[retrieval-augmented-generation]], [[index]]
- Note: contradicts [[vector-search]] on hybrid recall.
```

Operations: `ingest`, `query`, `lint`, `schema` (a change to this file). Write entries with
`uv run scripts/wiki.py log <op> "<title>" --line "…"`.

## Operations

Run them through the `wiki` skill: `/resume-builder:resume-auto-mode wiki ingest | query | lint`. The skill
holds the steps; this file holds the rules they follow.
