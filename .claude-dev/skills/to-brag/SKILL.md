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
Never edit it by hand: change the evidence through verify or steer, then rebuild.
No skill reads it to back a resume claim, and `verify`, `to-resume` and `steer` skip it when
they list `evidence/*/*.md`.

Read these first:

- [`../../reference/evidence.md`](../../reference/evidence.md): the evidence schema, the
  Summary, Numbers & Impact rules, and the anonymisation rules.
- The `resume` skill (`.claude-dev/skills/resume/SKILL.md`): the writing rules for every
  sentence of the brag document.

## Format

```markdown
---
company: <company>
period: yyyy-mm ~ yyyy-mm | present     # earliest to latest evidence period
role: <role arc, from the files' role: lines>
built_from: <n> evidence files (<m> reviewed)
updated: yyyy-mm-dd
---

# Brag document: <company>

> Built from `evidence/<company>/*.md` by `/resume-evidence:to-brag`. Do not edit by hand:
> change the evidence and rebuild. Draft: <n − m> of <n> evidence files are not yet verified.

## At a glance
Three to five sentences in the first person: what I did there, the main themes, the
strongest results.

## Themes
### <Theme> (yyyy → yyyy)
One to three sentences on how the work in this theme grew across projects.

**<Project title>** · <period> · <status> · [<short-id>](<file>.md)
- ★★★ <bullet> (B1)
- ★★ <bullet> (B3: <the caveat that limits it, from Remarks>)

**Other <theme> work**
- <bullet> ([<short-id>](<file>.md) B4)

## Timeline
| Period | Project | My role | Status | Headline |
| ------ | ------- | ------- | ------ | -------- |
One row per evidence file, newest first. The headline is the file's strongest bullet, cut
to about 12 words.

## Beyond the code
- **<Kind>**: <short pointer> ([<short-id>](<file>.md) I3); <short pointer> (… B5)

## Skills grown
| Year | First used | Where |
| ---- | ---------- | ----- |

## Interview stories
### <Story title>
- **Situation**: …
- **Task**: …
- **Action**: …
- **Result**: …
Source: [<id>](<file>.md) Context, What I Did 2–4, N1, I2

## Not yet confirmed
- <file or claim>: <what verify must settle>
```

## Section sources

| Section | Source |
| ------- | ------ |
| Front matter | `period`, `role` and `reviewed:` of every file |
| At a glance | The ★★★ Summary bullets across all files |
| Themes | Summary bullets, grouped across files by area of work |
| Timeline | Front matter (`period`, `role`, `status`, `title`) and each file's strongest bullet |
| Beyond the code | Impact rows of type team enablement, knowledge transfer, rescue / takeover, governance / compliance, adoption and avoided waste |
| Skills grown | The `tools:` lines, by the start year of each file's `period`; never "Studied, not used" |
| Interview stories | Context, What I Did and Numbers & Impact of the strongest projects |
| Not yet confirmed | Files without `reviewed:`, and Impact rows with Status `assessed` |

## Steps

1. **Pick the company.** Take `<company>` from the user's message. If none is given, list the
   folders under `evidence/` and ask. List `evidence/<company>/*.md` except
   `brag-document.md`; read each file's front matter, Summary, Remarks, Numbers & Impact,
   Tools and Not mine. Read Context and What I Did for the projects you pick for stories.
   _Done when_ every evidence file of the company is read.

2. **Group the themes.** Sort every Summary bullet into themes across projects: two to six
   areas of work that do not overlap, split on one axis, as the `resume` skill's Labels rule
   asks. Start from the files' own Summary areas and merge those that name the same work. A
   theme spans the years of its projects. Order themes by their strongest bullets.
   Inside a theme, group bullets under a project line, strongest project first; a project
   whose bullets span themes gets a project line in each. Gather projects with only one or
   two bullets in a theme under an "Other <theme> work" group, each bullet citing its file.
   _Done when_ every Summary bullet sits under exactly one theme.

3. **Pick the stories.** Pick three to six projects for interview stories: ★★★ work first,
   then a spread across themes, then the work with the most Numbers & Impact behind it.
   Prefer reviewed files.

4. **Write the document.** Fill the [format](#format), following these rules:
   - **Trace.** Every bullet, Timeline row and story names its evidence file and the IDs it
     uses (`B2`, `N1`, `I3`, `What I Did 4`). Link the file by its relative name.
   - **Wording.** Keep each Summary bullet's wording, stars and caveats, apart from a fix the
     `resume` skill's rules require. Theme intros, At a glance and stories are new prose:
     first person, past tense for finished work, British English. They join facts that the
     bullets already state and add none.
   - **Impact.** A `fact` or `user` Impact item may appear anywhere. An `assessed` item goes
     only under Not yet confirmed. A Remark caveat holds here as on the resume.
   - **Ownership.** Parts listed under Not mine are never claimed. Shared work keeps "with a
     teammate" or "contributed to"; `wip` or `dropped` work reads as prototyped or evaluated.
   - **Numbers.** Only measured or user-reported values, with their scope. A configured value
     reads "designed for".
   - **Drafts.** Mark each project line, and each bullet outside one, from an unreviewed
     file `(draft)`. Count the reviewed files in the front matter and the banner. When every
     file is a draft, the banner says so and the lines carry no mark.
   - **Older evidence files** have no stars and no Impact table (see evidence.md). Leave out
     the stars and keep each file's bullet order. Build Beyond the code from Summary bullets
     whose result is team enablement, documentation, a decision backed by measurement,
     production support or security. Say in the banner and in Not yet confirmed that no
     `assessed` rows exist yet.
   - **Beyond the code** points to bullets the themes already hold, in a few words each; it
     never repeats a bullet's full text or adds a fact.
   - **Privacy.** Never read `raw/<company>/notes/`. Names stay anonymised as the evidence
     has them.

5. **Check it.**
   1. For each company, read `raw/<company>/mapping.yml` and grep the brag document for every
      `internal_name`, real repo name (the last segment of each source `url`), source host,
      org name and Jira site. Fix every hit, including a generic phrase that only matches
      an internal name, by rewording it. The company slug itself is allowed, as in
      to-resume.
   2. Check every citation: the file exists and holds each ID it names.
   3. Check each sentence against the `resume` skill's grammar and spelling rules.
   _Done when_ the search returns zero hits and every citation resolves.

6. **Show the user.** Give the path and a short account: the themes, the stories picked, and
   how many claims sit under Not yet confirmed. Suggest `/resume-evidence:verify` for the
   files those claims rest on. Commit only when the user asks.

7. **Learn.** Apply [`../../reference/learning.md`](../../reference/learning.md). Typical
   lessons here: themes the user renames or merges, stories they swap, sections they want
   added or dropped.

## Completion

`evidence/<company>/brag-document.md` holds every section of the format; every Summary bullet
of the company sits under one theme; every line cites an evidence file and IDs that exist;
no `assessed` Impact item appears outside Not yet confirmed; and the banned-term search
returns zero hits.
