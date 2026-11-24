---
name: to-brag
description: Build or rebuild evidence/<company>/brag-document.md, a readable account of everything done at one company, from its evidence files.
disable-model-invocation: true
argument-hint: "<company>"
---

# To brag

Turn one company's evidence files into `evidence/<company>/brag-document.md`: a brag document
that a person reads in one sitting, for interviews, reviews, LinkedIn or cover letters. The
resume keeps a handful of bullets; the brag document keeps the rest, grouped by theme across
projects.

The brag document is a **view** of the evidence, never a source. It adds no claim of its own:
every line traces to an evidence file, and the only new writing is how the themes connect.
Never edit it by hand, except its `user:` blocks: change the evidence through verify or
steer, then rebuild.
No skill reads it to back a resume claim, and `verify`, `to-resume` and `steer` skip it when
they list `evidence/*/*.md`.

Read these first:

- [`../../reference/evidence.md`](../../reference/evidence.md): the evidence schema, the
  Summary, Numbers & Impact rules, and the anonymisation rules.
- The `resume` skill (`.claude-dev/skills/resume/SKILL.md`): the writing rules for every
  sentence of the brag document.

## Format

The sections follow Julia Evans's brag-document template ("Get your work recognized: write a
brag document", 2019), fed from evidence. Two blocks hold what evidence cannot: your goals and
your work outside the job. They sit between `<!-- user:<name>:start -->` and
`<!-- user:<name>:end -->` markers; you own them, and every rebuild keeps them byte for byte.

```markdown
---
company: <company>
period: yyyy-mm ~ yyyy-mm | present     # earliest to latest evidence period
role: <role arc, from the files' role: lines>
built_from: <n> evidence files (<m> reviewed)
updated: yyyy-mm-dd
---

# Brag document: <company>

> Built from `evidence/<company>/*.md` by `/resume-evidence:to-brag`. Do not edit by hand,
> except inside the `user:` blocks: change the evidence and rebuild. Draft: <n − m> of <n>
> evidence files are not yet verified.

## At a glance
Three to five sentences in the first person: what I did there, the main themes, the
strongest results.

<!-- user:goals:start -->
## Goals
### This year
- <goal, in your words>
### Next year
- <goal>
<!-- user:goals:end -->

## Projects by theme
### <Theme> (yyyy → yyyy)
One to three sentences on how the work in this theme grew across projects.

**<Project title>** · <period> · <status> · [<short-id>](<file>.md)
My part: <role, and what others built, from role: and Not mine>.
- ★★★ <bullet> (B1)
- ★★ <bullet> (B3: <the caveat that limits it, from Remarks>)

**Other <theme> work**
- <bullet> ([<short-id>](<file>.md) B4)

### Decisions and production support
- **<Kind>**: <short pointer> ([<short-id>](<file>.md) B2)

## Collaboration & mentorship
- <pointer or user item> ([<short-id>](<file>.md) I4)

## Design & documentation
- <pointer> ([<short-id>](<file>.md) What I Did 6)

## Company building
- <pointer or user item> ([<short-id>](<file>.md) B5)

## What I learned
- <skill, not a tool> ([<short-id>](<file>.md) Tools, Learned)

| Year | Tools first used | Where |
| ---- | ---------------- | ----- |

## Interview stories
### <Story title>
- **Situation**: …
- **Task**: …
- **Action**: …
- **Result**: …
Source: [<id>](<file>.md) Context, What I Did 2–4, N1, I2

## Timeline
| Period | Project | My role | Status | Headline |
| ------ | ------ | ------- | ------ | -------- |

<!-- user:outside:start -->
## Outside of work
- <blog post, talk, open source, recognition, in your words>
<!-- user:outside:end -->

## Not yet confirmed
- <file or claim>: <what verify must settle>
```

A section with nothing behind it says so in one line ("Nothing recorded in evidence yet:
verify asks about it.") and stays in the document, so the gap is visible.

## Section sources

| Section | Source |
| ------- | ------ |
| Front matter | `period`, `role` and `reviewed:` of every file |
| At a glance | The ★★★ Summary bullets across all files |
| Goals, Outside of work | The user, asked in step 2; kept on every rebuild. Never evidence, never a resume claim |
| Projects by theme | Summary bullets, grouped across files by area of work; My part from `role:` and Not mine |
| Decisions and production support | Impact rows of type avoided waste, reliability, security, rescue / takeover; in older files, Summary bullets with that result |
| Collaboration & mentorship | Impact rows of type team enablement and knowledge transfer, and `user` items on helping, mentoring, onboarding or reviewing; code others built on |
| Design & documentation | What I Did items on ADRs, design docs, RFCs, specs, runbooks and developer docs; Impact rows of type maintainability |
| Company building | Work used beyond one project: shared templates and libraries, process or supply-chain rules, Impact rows of type adoption and governance / compliance, `user` items on interviewing or onboarding |
| What I learned | `Learned:` lines under each file's `## Tools`, then the `tools:` lines by the start year of each file's `period`; never "Studied, not used" |
| Interview stories | Context, What I Did and Numbers & Impact of the strongest projects |
| Timeline | Front matter (`period`, `role`, `status`, `title`) and each file's strongest bullet |
| Not yet confirmed | Files without `reviewed:`, Impact rows with Status `assessed`, outcomes the Remarks mark "to confirm" |

## Steps

1. **Pick the company.** Take `<company>` from the user's message. If none is given, list the
   folders under `evidence/` and ask. List `evidence/<company>/*.md` except
   `brag-document.md`; read each file's front matter, Summary, Remarks, Numbers & Impact,
   Tools and Not mine. Read Context and What I Did for the projects you pick for stories, and
   scan What I Did of every file for design and documentation work.
   If `brag-document.md` exists, copy out its `user:` blocks before you write anything.
   _Done when_ every evidence file of the company is read.

2. **Ask what evidence cannot hold.** If a `user:` block is missing or empty, ask the user
   for it: goals for this year and next; work outside the job (blog posts, talks, open source,
   recognition). Then ask the template's prompts: "If you were trying to convince a friend to
   join your team, what would you tell them about your work?" and "Did anybody tell you that
   you did something well recently?" Answers about a project's work are work claims: they go
   into its evidence file through `/resume-evidence:verify` first, never straight into the
   brag document. An empty answer leaves the block with one line saying it is empty.

3. **Group the themes.** Sort every Summary bullet into themes across projects: two to six
   areas of work that do not overlap, split on one axis, as the `resume` skill's Labels rule
   asks. Start from the files' own Summary areas and merge those that name the same work. A
   theme spans the years of its projects. Order themes by their strongest bullets.
   Inside a theme, group bullets under a project line, strongest project first; a project
   whose bullets span themes gets a project line in each, and only the first carries My part.
   Gather projects with only one or two bullets in a theme under an "Other <theme> work"
   group, each bullet citing its file.
   _Done when_ every Summary bullet sits under exactly one theme.

4. **Pick the stories.** Pick three to six projects for interview stories: ★★★ work first,
   then a spread across themes, then the work with the most Numbers & Impact behind it.
   Prefer reviewed files.

5. **Write the document.** Fill the [format](#format), following these rules:
   - **Trace.** Every bullet, pointer, Timeline row and story names its evidence file and the
     IDs it uses (`B2`, `N1`, `I3`, `What I Did 4`). Link the file by its relative name.
   - **Wording.** Keep each Summary bullet's wording, stars and caveats, apart from a fix the
     `resume` skill's rules require. Theme intros, My part, At a glance and stories are new
     prose: first person, past tense for finished work, British English. They join facts the
     evidence already states and add none.
   - **Pointers.** Decisions, Collaboration, Design & documentation and Company building point
     to bullets or What I Did items in a few words each; they never repeat a bullet's full
     text. A What I Did item with no Summary bullet may be pointed to directly.
   - **Fuzzy work.** For collaboration and company-building items, give the goal, what I did
     towards it and any effect seen, when the evidence states them.
   - **Impact.** A `fact` or `user` Impact item may appear anywhere. An `assessed` item goes
     only under Not yet confirmed. A Remark caveat holds here as on the resume.
   - **Ownership.** Parts listed under Not mine are never claimed. Shared work keeps "with a
     teammate" or "contributed to"; `wip` or `dropped` work reads as prototyped or evaluated.
   - **Numbers.** Only measured or user-reported values, with their scope. A configured value
     reads "designed for".
   - **Drafts.** Mark each project line, and each bullet outside one, from an unreviewed
     file `(draft)`. Count the reviewed files in the front matter and the banner. When every
     file is a draft, the banner says so and the lines carry no mark.
   - **Older evidence files** have no stars, no Impact table and no `Learned:` lines (see
     evidence.md). Leave out the stars, keep each file's bullet order, and build the pointer
     sections from Summary bullets and What I Did items with that kind of result. Say in the
     banner that no `assessed` rows exist yet.
   - **User blocks.** Paste each `user:` block back exactly as copied in step 1, or as the
     user gave it in step 2. Nothing outside a block cites it.
   - **Privacy.** Never read `raw/<company>/notes/`. Names stay anonymised as the evidence
     has them, and the user blocks follow the same anonymisation rules.

6. **Check it.**
   1. For each company, read `raw/<company>/mapping.yml` and grep the brag document for every
      `internal_name`, real repo name (the last segment of each source `url`), source host,
      org name and Jira site. Fix every hit, including a generic phrase that only matches
      an internal name, by rewording it. The company slug itself is allowed, as in
      to-resume.
   2. Check every citation: the file exists and holds each ID it names.
   3. Check that each `user:` block is unchanged from step 1, or holds only the user's answers.
   4. Check each sentence against the `resume` skill's grammar and spelling rules.
   _Done when_ the search returns zero hits and every citation resolves.

7. **Show the user.** Rebuild the skill graph with `uv run scripts/skill_graph.py <company>`
   (`evidence/<company>/skill-graph.html`, a view like this one). If it stops on a missing
   project, add the project to `evidence/<company>/skill-graph.yml`: a label, its areas and a
   10–20 word description that restates the file's bullets. Give the path and a short account: the themes, the stories picked, the
   sections with nothing behind them yet, and how many claims sit under Not yet confirmed.
   Suggest `/resume-evidence:verify` for the files those rest on. Commit only when the user
   asks.

8. **Learn.** Apply [`../../reference/learning.md`](../../reference/learning.md). Typical
   lessons here: themes the user renames or merges, stories they swap, sections they want
   added or dropped.

## Completion

`evidence/<company>/brag-document.md` holds every section of the format; every Summary bullet
of the company sits under one theme; the `user:` blocks match what the user wrote; every line cites an evidence file and IDs that exist;
no `assessed` Impact item appears outside Not yet confirmed; and the banned-term search
returns zero hits.
