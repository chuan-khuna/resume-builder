# Spec: brag document per company

Status: resolved (2026-11-24: format, path and skill approved as proposed)

Proposed 2026-11-24. Nothing is built yet: this spec waits for the three decisions at the end.

## What a brag document is

A brag document is a running list of what you did at work, written by you, so you don't have to
remember it when it counts. Julia Evans popularised the idea in 2019. People use it for reviews,
promotions and job searches. It covers:

- **Projects and their results:** what shipped, with numbers where you have them.
- **Work that doesn't show up in commits:** mentoring, writing docs, taking over legacy code,
  unblocking teammates.
- **What you learned:** new skills, stacks or domains.
- **Recognition:** praise, adoption by other teams, client feedback.

It's written in plain prose for a reader to understand. Nobody expects it to fit on one page.

## Why build one from evidence

The evidence files already hold the content of a brag document, with stricter rules. What they
lack is the brag doc's shape: they are split by project, built for the pipeline (tables, IDs,
citations), and nothing connects them across the years.

A brag document is therefore a **readable view of the evidence**, not a new source of truth. It
adds three things the per-project files cannot:

- **Themes across projects.** For example, computer-vision analytics recurs from 2023 to 2026
  (crowd counting, event booths, CCTV, road safety, retail shelves), and LLM and RAG work picks
  up in 2026.
- **Interview stories.** The resume keeps 4 to 6 bullets. The brag doc keeps the rest, ready for
  "tell me about a time when…" questions.
- **Material for other uses:** LinkedIn, cover letters, salary negotiation.

## Where it lives

`evidence/<company>/brag-document.md`, for example `evidence/themather/brag-document.md`.

**Problem:** `verify`, `to-resume` and `steer` list `evidence/*/*.md` as project files. Without a
change they would read the brag document as one more project, with no `id:`, no `period:` and no
evidence sections behind it.

**Fix:** add one rule to each of the three skills and to `.claude-dev/skills/resume-auto-mode/references/evidence.md`:
"Skip `brag-document.md`: it is a view built from evidence, not evidence."

## Format

```markdown
---
company: themather
period: 2023-xx ~ 2026-xx           # earliest to latest evidence period
role: <role arc, e.g. backend → AI / backend engineer>
built_from: 22 evidence files (0 reviewed)
updated: 2026-11-24
---

# Brag document: themather

> Built from evidence/themather/*.md. Do not edit by hand: change the evidence and rebuild.

## At a glance
Three to five sentences: what I did there, the main themes, the strongest results.

## Themes
### Computer vision analytics (2023 → 2026)
- One or two sentences on how the work grew: crowd-counting PoC → event-booth analytics →
  CCTV security → road safety → retail shelves.
- ★★★ <strongest Summary bullet in this theme>  ([cctv-platform](2025-realtime-cctv-….md) B3)
- ★★ …
### LLM, RAG and agents (2026)
### Backend and data platforms
### Websites and CMS backends

## Timeline
| Period | Project | My role | Status | Headline |
| ------ | ------- | ------- | ------ | -------- |
One row per project, newest first.

## Beyond the code
Team enablement, knowledge transfer, legacy takeovers, governance: taken from Impact rows
of those types.

## Skills grown
| Year first used | Tools | Where |
Taken from each file's `## Tools`, never from "Studied, not used".

## Interview stories
Three to six STAR stories: Situation (Context), Task, Action (What I Did),
Result (Numbers & Impact), each citing its file and IDs.

## Not yet confirmed
Each claim that rests on a draft file or an `assessed` Impact row, as a to-do for verify.
```

### What each section is built from

| Section | Source in the evidence files |
| ------- | ---------------------------- |
| Front matter | `period`, `role` and `reviewed` of every file |
| At a glance | The ★★★ Summary bullets across all files |
| Themes | Summary bullets, grouped across files by area of work; the themes may differ from any one file's areas |
| Timeline | Front matter (`period`, `role`, `status`, `title`) and the file's top bullet |
| Beyond the code | Impact rows of type team enablement, knowledge transfer, rescue / takeover, governance / compliance, adoption |
| Skills grown | `## Tools` lines, by the year of each file's `period` |
| Interview stories | Context, What I Did, Numbers & Impact of the strongest projects |
| Not yet confirmed | Files without `reviewed:`; Impact rows with Status `assessed` |

## Rules

- **Every line traces to evidence.** Each bullet cites its file and its B, N or I IDs. The brag
  doc adds no claims of its own; the only new writing is how the themes connect.
- **Unconfirmed impact stays out.** An `assessed` Impact row only appears under "Not yet
  confirmed". Parts listed under "Not mine" are never claimed.
- **The prose follows the `resume` skill's writing rules**, as `CLAUDE.md` requires.
- **Draft status is visible.** The header counts reviewed files. Today all 22 themather files
  are drafts, so the first build is a draft too; rebuilding after verify updates it.
- **No private notes.** The brag document never reads `raw/<company>/notes/`, like every other
  output of the pipeline.

## Decisions needed

1. **Format:** is it right, or do you want sections added, removed or reordered (for example,
   Timeline before Themes)?
2. **Path:** keep `evidence/<company>/brag-document.md` and add the skip rule to `verify`,
   `to-resume`, `steer` and `evidence.md`?
3. **One-off or skill:** write it once now, or add a `resume-builder:resume-auto-mode to-brag` skill you rerun
   after verify? Recommended: the skill, because the doc goes stale each time evidence changes.
   A skill also means updating `CLAUDE.md`'s pipeline line and `docs/documents/` in the same
   change.
