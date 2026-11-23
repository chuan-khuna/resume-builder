---
name: review-resume
description: Review a built resume for evidence traceability, screening, CV standards, readability, format, ATS, contrast and accessibility, as an HTML page in resume/review/.
disable-model-invocation: true
argument-hint: "[slug] [template]"
---

# Review a resume

Arguments: `slug` is `base` (`resume/data/resume.yml`) or a folder in `resume/versions/`; `template` is a file in `resume/templates/` without `.typ`. Defaults: `base classic`.

The resume lives in `resume/`; every path below is relative to it unless it starts with `.claude-dev/` or `evidence/`. Run commands from inside `resume/`, or from the repo root as `mise -C resume …`. The evidence files in `evidence/` are the ground truth: [`../../reference/evidence.md`](../../reference/evidence.md) holds their schema and the Summary rules.

Every result in the review is **measured**: it comes from `measure.sh` or from a command you ran, and the footer says how. The exceptions are the **career adviser's view** and **reader impressions**, labelled as opinion; anything else you can't measure is left out.

## Steps

1. **Measure.** From the repo root, run `bash .claude-dev/skills/review-resume/measure.sh <slug> <template>`. If the build fails (usually the page-count check), stop and report the failure: there is nothing to review yet. Then build the other template too and run `uv run review/scripts/line_lengths.py --slug <slug>` in `resume/`, which writes `review/<slug>-line-length.svg` and prints its numbers as a table. Done when the full report and the line-length table have printed.
2. **Read.** Look at every page image the report lists, then read the printed content. That's `versions/<slug>/resume.yml` over `data/resume.yml`: each top-level key in the version replaces the base key whole. If `versions/<slug>/job-ad.md` exists, read it; it is the target for the keyword check. Read the evidence file named in each bullet's trace comment (`# evidence/<company>/<file>.md B<n>`): its Summary, Remarks, What I Did and Numbers are the owner's figures and limits behind the bullet. Suggest only figures they record, and respect what the Remarks say not to claim. Done when you have read every printed entry.
3. **Judge.** Fill one row for every check in [Checks](#checks): measured result, status, and one concrete improvement. Before you recommend a fix as working, test it: build the change, measure it, then revert it. Done when every check has a row; a check that doesn't apply gets a row saying why.
4. **Write.** Copy `review/REVIEW_TEMPLATE.html` to `review/<slug>.html` (`base` writes `index.html`) and follow the comments at its top. Copy each page image to `review/<slug>-<template>-<page>.png` (`base` uses `resume.png` for one page) and use it as the preview. Fill the score cards, the summary table, the career adviser's view, one section per check group, and the fixes table, most important first. Then add **notes**: wrap the 8–12 phrases the reader must not miss in `data-note` spans, by the rules in the template comment (item 11). Done when no `[placeholder]` is left.

   The **career adviser's view** is 3–5 bullets on positioning, the things a careers adviser would say that no measurement shows: which job title the work earns, which track to aim each version at, whether the experience shows growth, whether public evidence backs the headline, and how to handle gaps. Each bullet opens with a short imperative in bold, then gives the reason from what the resume shows and what to do. It reads the resume against `job-ad.md` when one exists.

   Under it, **reader impressions** is a bulleted list with one bullet per reader, in the order they see the page: HR or recruiter (a fast first screen, often non-technical), hiring manager, technical interviewer, and others only when they matter for this role. Each reader's sub-bullets give the first impression, what that reader looks for, and the question or concern this resume will raise for them. Tie each impression to something on the page.
5. **Verify.** Screenshot the page with headless Chrome: `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --hide-scrollbars --window-size=1400,1000 --screenshot=<scratchpad>/review.png file:///<absolute path>`. Check that every contents link's `href` matches a heading `id`. To see the notes, take a second screenshot with `--force-prefers-reduced-motion --window-size=1400,7600 --virtual-time-budget=5000`: notes draw only when on screen, and only instantly with reduced motion. Done when the screenshots show the cards, tables and preview laid out correctly, and each note sits on its words.
6. **Report** to the user: the summary table, the top three fixes, and the page's path. Commit only when asked.

## Checks

Status badges: `pass` (meets the threshold), `warn` (improve or consider), `fail` (fix before sending).

### Evidence traceability

Put this group first: a claim the evidence does not back fails the resume whatever its layout.

| Check | Source | Threshold |
|---|---|---|
| Trace comments | YAML comments above each experience bullet | Every printed experience bullet has `# evidence/<company>/<file>.md B<n>`, the file exists and has that Summary bullet. A missing trace is `fail` |
| Claims | bullet vs its evidence Summary bullet and What I Did | Nothing claimed beyond them; shared work and `wip` or `dropped` status worded as the evidence says. An unsupported claim is `fail` |
| Numbers | bullet vs evidence Numbers | Each figure is in Numbers with the same scope; a configured value reads "designed for"; a Remark that says not to quote it is respected |
| Review state | evidence frontmatter, `(draft)` in trace comments | Every traced file has `reviewed:` set. A draft is `warn`: run `/resume-evidence:verify` |
| Skills | `skills` vs evidence `tools:` lines | Every work skill is listed as used in an evidence file; "Studied, not used" stays out |
| Untraced sections | `projects`, `activities` | Entries with no evidence file are the user's account: list them as `warn`, not `fail` |
| Banned terms | YAML vs `raw/<company>/mapping.yml` | Zero hits for every `internal_name`, repo name, source host and Jira site |

### Screening: the first look

| Check | Source | Threshold |
|---|---|---|
| Section positions | report: positions | First job title within the top third (about 33%); name, title and contact first |
| Employment gaps | report: `GAP` lines | Over 6 months unexplained is `fail` |
| Recency | content | Current role dated "– Present", easy to find in the date column |
| Title match | header vs jobs vs `job-ad.md` | The header job title fits the target role |
| Progression | experiences | One long entry with growing scope: suggest splitting by title or period |

### CV standards

| Check | Source | Threshold |
|---|---|---|
| Measurable outcomes | report: bullets with a number | The strongest 4–5 bullets each carry a real figure |
| Bullets per job | report: job lines | 6 or fewer |
| Headline | header | Doesn't repeat the job title; makes one claim |
| Verbs and tense | bullets | Each starts with a verb; present tense for the current job, past for the rest |
| Spelling | all text | British English, by the `resume` skill's rules (`.claude-dev/skills/resume/SKILL.md`) |
| Personal details | header | No photo, date of birth, nationality or marital status |
| Consistency | report: dates, links | Every date has a month; one full-stop style; every project has a link |

### Readability

| Check | Source | Threshold |
|---|---|---|
| Line length | report and line-length table | Median 45–90 characters `pass`, up to 100 `warn`, over 100 `warn` with a fix. Put the chart and its table under Readability |
| Bullet length | report: job lines | 25 words or fewer |
| Wrapped lines | report: wrapped bullets | Last line 3 words or more (no stranded words) |
| Summary | report: summary words | 30–50 words |

### Format and typography

| Check | Source | Threshold |
|---|---|---|
| Length | report: Pages, words | Pages ≤ `maxPages`; 1 page under about 10 years' experience |
| Paper and margins | report: page size; `lib/style.typ` | A4 (US Letter only for US roles); margins ≥ 12.7 mm |
| Type sizes | `lib/style.typ` | Body ≥ 9.5 pt; nothing below 8.5 pt |
| Fonts | report: fonts | All embedded, all with a Unicode map |
| File name | delivery | Suggest `<First>-<Last>-Resume.pdf` |

### ATS

| Check | Source | Threshold |
|---|---|---|
| Text | report: words, ligatures, U+FFFD | All text extracts; 0 ligatures; 0 replacement characters |
| Structure | page | One column; standard section names; contact details in the body |
| Skills order | report: both Skills extracts | Stored order (`-raw`) keeps each label with its skills = `pass`. Splitting by position (plain) is `warn` at most: any aligned label column splits there |
| Keywords | content vs `job-ad.md` | Each required skill in the ad that you have appears in Skills and in a bullet. Without an ad, list common terms for the role as "add only if you use them" |

### Contrast and accessibility

| Check | Source | Threshold |
|---|---|---|
| Text contrast | report: contrast | Every text colour ≥ 4.5:1 (AA); note AAA (7:1) |
| Decorative colours | report: contrast | Rules and separators are exempt; say so |
| Links | page | Give the link colour its swatch and ratio; link text is the address, so colour isn't the only cue |
| PDF accessibility | report: Tagged, Title, Lang | Tagged yes; title set; `/Lang` set (`en-GB` preferred for British English) |

## Known pitfalls

- **Text grouped by position.** `pdftotext` without `-raw` groups text by where it sits on the page, so any aligned column (like the Skills labels) comes out as its own block. Check `-raw` before calling it an ATS failure.
- **Scrolled screenshots.** Headless Chrome returns a blank image after a script scrolls the page. Screenshot the top, and open the pop-up by clicking `[data-lightbox]` from a temporary copy of the page.
- **Scratch files.** Typst reads only inside the project root (`resume/`). Put probe `.typ` files in `build/` (gitignored) and delete them after.
