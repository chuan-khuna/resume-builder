# resume-builder

A format and a standard for letting an LLM agent summarise **what you have done** at work,
from your repositories and Jira tickets, and turn it into a resume.

The first output is **evidence**: one Markdown file per project that states what you built,
decided or owned. Each claim cites the commit, path or ticket that proves it, and client names
are anonymised. Evidence is the ground truth you write a resume, CV or portfolio from, and every
line can be defended in an interview.

The second output is the **resume**: YAML content typeset into a PDF with
[Typst](https://typst.app), where every work bullet traces to an evidence file.

## User manual

The step-by-step guide is
[`docs/documents/user-manual.html`](docs/documents/user-manual.html). It covers the
prerequisites, installing the plugin, writing `mapping.yml`, running ingest, distill and
verify, building the resume with `to-resume` and `review-resume`, and troubleshooting.

## How it works

Five steps, each a Claude Code skill in the `resume-evidence` plugin. The first three build the
evidence; the last two build the resume from it.

| Step | Skill | Output |
| ---- | ----- | ------ |
| 1. Ingest | `/resume-evidence:ingest <company>` | `raw/<company>/repos/<id>/<slug>/` clones, `commit-summary.json`, `jira/<yyyy>.json` and `jira/merged.json`, updated `TODO.md` |
| 2. Distill | `/resume-evidence:distill <company> <id>` | `evidence/<company>/<yyyy>-<id>.md` with a draft Summary |
| 3. Verify | `/resume-evidence:verify <company> <id>` | the same evidence file, Summary confirmed, `reviewed:` set |
| 4. To resume | `/resume-evidence:to-resume [base \| <slug>]` | `resume/data/resume.yml` or `resume/versions/<slug>/resume.yml`, and the PDF Typst builds in `resume/build/<slug>/` |
| 5. Review resume | `/resume-evidence:review-resume [slug] [template]` | `resume/review/<slug>.html` (`index.html` for base) |

```
mapping.yml ─ingest─▶ raw/ ─distill─▶ evidence (draft) ─verify─▶ evidence (reviewed)
                            ▲                                         │
  no repos: you ─interview──┘                                         │
                     review page ◀─review-resume─ PDF ◀─Typst─ resume.yml ◀─to-resume
```

1. **Ingest** (`/resume-evidence:ingest <company>`)
   - Update the config: you list your projects and their git repos in `mapping.yml`.
   - Load repository data: the agent clones every repo into `raw/<company>/repos/<id>/<slug>/`,
     or fetches it and fast-forwards the checked-out branch. `commit-summary.json` records my
     commit counts and the branches holding my commits that the checked-out branch lacks.
   - Load Jira data: the agent downloads the tickets assigned to you.
2. **Distill** (`/resume-evidence:distill <company> <project-id>`)
   - The agent uses the data in `raw/<company>/`. Git authorship decides what is yours; a
     ticket shows assignment, not authorship. Commits count on every branch; blame reads the
     checked-out branch, or the branch holding your work.
   - No repos (lost access, or the work left no code): the agent interviews you on each
     responsibility instead, and cites your answers `[me: yyyy-mm-dd]`.
   - The agent writes `evidence/<company>/<yyyy>-<project-id>.md`. Every claim is cited and
     anonymised.
   - The file opens with a draft `## Summary`: resume bullets, then remarks on what each traces
     to and which numbers to quote.
3. **Verify** (`/resume-evidence:verify <company> <project-id>`)
   - The agent interviews you on the gaps git cannot answer: outcomes, scale, what shipped.
   - It folds your answers into the evidence, confirms the `## Summary` and sets `reviewed:`.
4. **To resume** (`/resume-evidence:to-resume [base | <slug>]`)
   - `base` writes `resume/data/resume.yml`, the base resume. A slug such as
     `2026-dec-acme-ml` writes `resume/versions/<slug>/resume.yml`, a version tailored to the
     job ad saved beside it as `job-ad.md`.
   - The agent picks the evidence files, asks you for what evidence lacks (employer name, job
     title, dates), and shows you a plan before it writes anything.
   - Each bullet starts from an evidence Summary bullet and carries a trace comment, such as
     `# evidence/<company>/<file>.md B2`. Bullets from unreviewed files are marked `(draft)`.
   - Skills come only from the evidence `tools:` lines.
   - The agent greps the YAML for banned terms from `mapping.yml`, checks the YAML against the
     schema, then compiles the PDF with Typst (`mise -C resume run build`). The build fails if
     the resume runs past `maxPages` (default 1).
5. **Review resume** (`/resume-evidence:review-resume [slug] [template]`)
   - The agent measures the built PDF and writes an HTML review to `resume/review/`.
   - The review checks evidence traceability first, then screening, CV standards,
     readability, format, ATS, contrast and accessibility, and ends with a ranked list of
     fixes.

`/resume-evidence:resume` holds the writing rules the agent applies to every bullet: British
English, a plain verb first, one result, 25 words or fewer. You can also call it on its own to
proofread any resume text.

The design of all five steps, with each step's inputs and outputs, is in
[`docs/documents/resume-generation-workflow.html`](docs/documents/resume-generation-workflow.html).
The resume layout, YAML keys and build commands are in [`resume/README.md`](resume/README.md).

## Layout

```
raw/                                   # local only; commit only the example
├── repository-mapping.example.yml     # mapping schema with fake values
└── <company>/
    ├── mapping.yml                    # you write this: identity, Jira login, projects
    ├── TODO.md                        # projects still to add, leads for distill
    ├── commit-summary.json            # per-repo load status, my commit counts, branches ahead
    ├── jira/<yyyy>.json, merged.json  # my Jira tickets
    ├── notes/<id>.md                  # private notes: what held my work back
    └── repos/<id>/<slug>/             # git clones, named by their anonymised slug
evidence/<company>/<yyyy>-<id>.md      # committed: anonymised, cited ground truth
resume/
├── data/resume.yml                    # the base resume: every work bullet traced to evidence
├── versions/<slug>/                   # resume.yml overrides and job-ad.md for one application
├── templates/                         # Typst layouts that typeset the PDF: classic, rail
├── review/                            # HTML reviews written by review-resume
└── build/                             # generated PDFs and page images (gitignored)
scripts/                               # committed: helpers the agent writes as needed
docs/documents/                        # user manual and design documents
.claude-dev/                           # the resume-evidence plugin: skills and shared reference
```

`raw/` holds real client names and a Jira token, so it stays on your machine. Only
`evidence/`, `resume/` and `scripts/` carry your work into git, and all of them are free of
real names.

## Get started

1. Install the tools and the plugin:
   ```bash
   mise install
   mise run plugins
   mise -C resume trust
   mise -C resume install    # Typst, pinned in resume/mise.toml
   ```
2. Copy `raw/repository-mapping.example.yml` to `raw/<company>/mapping.yml`.
3. Fill in `me` (the names and emails you commit with), `jira`, and one entry per project.
   Give each source a `url` and a `slug`: the repo's anonymised name by its role, such as
   `backend`. Evidence cites the repo by its slug.
4. Restart Claude Code, then run `/resume-evidence:ingest <company>`.
5. Run `/resume-evidence:distill <company> <project-id>` for each project.
6. Run `/resume-evidence:verify <company> <project-id>` to answer its questions and confirm the
   bullets.
7. Run `/resume-evidence:to-resume` to write the base resume, and approve its plan.
8. Run `/resume-evidence:review-resume` and apply the fixes you agree with.
9. For a job application, run `/resume-evidence:to-resume <slug>` with the job ad, then
   `/resume-evidence:review-resume <slug>`.

To update a project after new work, run distill again. It reads only the commits after the
`verified:` sha in the evidence file and adds new bullets. Verify it, then run to-resume again.

## The standard

An evidence file is done when:

- every **What I Did** bullet cites `[repo:path]`, `[repo@sha]`, `[TICKET-123]` or
  `[me: yyyy-mm-dd]`;
- it claims only paths git confirms are yours, and names others' parts under **Not mine**;
- **Numbers** holds measured outcomes and business scale only, each with its scope;
- no client, brand, person, host or infra identifier remains;
- you have reviewed it.

Resume wording (which bullets, which numbers to quote) lives in the file's `## Summary` at the
top: drafted by distill, confirmed with you by verify.

A resume is done when:

- every experience bullet has a trace comment to an evidence Summary bullet, and claims nothing
  beyond it;
- every number has the same scope as in the evidence Numbers;
- every skill comes from an evidence `tools:` line;
- the banned-term search returns zero hits;
- it passes `mise -C resume run check` and builds within `maxPages`;
- you have approved the content.
