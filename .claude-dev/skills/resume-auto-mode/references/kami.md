# Formatting the Typst resume with Kami

The Typst resume in `resume/` takes its styling from [Kami](https://github.com/tw93/kami). The
Kami skill is in `.claude/skills/kami/`. When you change how the resume looks or reads, use
Kami's design rules. Do not use its tools.

Kami builds HTML and renders it with WeasyPrint. This repo builds with Typst. So:

- Do not copy Kami's HTML templates, and do not run its `scripts/build.py`.
- Put each Kami rule into Typst, in `resume/lib/style.typ` or `resume/lib/sections.typ`.
- Build and measure with this repo's commands: `mise -C resume run build`, and
  `review-resume`'s `measure.sh`.

## What to read

Read the parts below before you change the layout, the type or the content of the resume.

| File in `.claude/skills/kami/` | Use it for |
| ------------------------------ | ---------- |
| `CHEATSHEET.md`: type scale, «Page margins», «Resume visual rule» | Sizes, line heights, margins, where rules go |
| `references/design.md` §1 Color, §2 Typography, §3 Spacing | The ink-blue accent, the warm neutrals, weights 400/500, the 4 pt spacing unit |
| `references/design.md` «Decoration density: subtractive by default» | Leave out a rule, box or colour when type and space can carry the structure |
| `references/resume-writing.md` | The recruiter pass, «Key-number highlight density», «Visual rhythm for resume templates», «Two-page balance», «Page 2 rhythm» |
| `references/anti-patterns.md` «Visual Excess», «Metric Fabrication» | What to avoid |

Translate the CSS terms into Typst terms. For example, a `.hl` span becomes one accent-coloured
`text(fill: accent, …)`, used once per bullet at most.

## When this repo's rules win

Kami is the style guide. Where it disagrees with the rules below, follow the rules below.

| Topic | Kami | This repo |
| ----- | ---- | --------- |
| Content | Writes from the material it is given | Every claim traces to an evidence file (`evidence.md`) |
| Writing | Its own writing guide | The `resume` playbook: British English, plain verbs, 25 words or fewer |
| Length | Exactly 2 pages | `maxPages` in the YAML (default 1) |
| Margins | Resume 11 · 13 · 11 · 13 mm | 12.7 mm or more (`review-resume`, Format and typography) |
| Type size | Body ≥ 9 pt; dense resume text 8–8.5 pt | `review-resume` thresholds: body ≥ 9.5 pt, nothing below 8.5 pt |
| Layout | Multi-column metrics and grids | One column for ATS (`review-resume`, ATS) |
| Colour | Its palette | Every text colour ≥ 4.5:1 contrast (`review-resume`, Contrast) |
