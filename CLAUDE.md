# CLAUDE.md

## Purpose

This repo helps the user build their resume.

- `raw/<company>/` holds the raw data: git clones, Jira exports, `mapping.yml`. It stays local
  (gitignored) because it carries real client names and credentials.
- `evidence/<company>/` holds what is distilled from `raw/`, anonymised. **Evidence is the
  ground truth for the resume**: every resume claim must trace to an evidence file, never to
  memory or to `raw/` directly.
- Pipeline: `resume-evidence:ingest` (load raw data) → `resume-evidence:distill` (raw →
  evidence) → `resume-evidence:verify` (interview the user, add resume bullets) →
  `resume-evidence:to-resume` (evidence → resume YAML) → `resume-evidence:review-resume`
  (review the built PDF). Shared rules: `.claude-dev/reference/workflow.md` and
  `.claude-dev/reference/evidence.md`.
- `resume/` holds the Typst resume: `data/resume.yml` is the resume's ground truth, built with
  `mise -C resume run build`. See `resume/README.md`. `.reference/` holds gitignored reference
  clones.
- When you format the Typst resume, use the Kami skill's design rules (`.claude/skills/kami/`)
  as `.claude-dev/reference/kami.md` describes. This repo's evidence, writing and review rules
  win over Kami's.
- Python helpers live in `scripts/`; their dependencies are declared in `pyproject.toml`.

## Agent skills

### Issue tracker

Issues and specs live as local markdown files under `.scratch/<feature>/`. See `docs/agents/issue-tracker.md`.

### Triage labels

The five default triage roles (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`), recorded as a `Status:` line in each issue file. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `GLOSSARY.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.

## Project docs

### Documents

Documents about this project, including how it is implemented, live in
docs/documents/<slug>.md (or .html). docs/documents/INDEX.md is the entry point: it lists
every document as one bullet, `- Title — one-line summary`.

- Read the index before working on an area, and open the documents relevant to it.
- When you add, rename or remove a document, update INDEX.md in the same change.
- Keep documents in step with the code they describe: if a change makes a document wrong,
  fix the document in the same change.

### HTML documents

When you write a document in `docs/` as HTML, follow the page contract at the top of
`docs/shared/doc.js`. Linking `globals.css` and `doc.js` gives the page its themes, Shiki
highlighting, Pele diagrams, table of contents and glossary cards.

- Shared code: link `docs/shared/` files by relative path; add new shared CSS/JS there.
- Colour: write every colour in `oklch()`; derive with `color-mix(in oklch, …)`.
- Glossary: define each term once, in `<dl class="glossary">` or a table marked
  `data-glossary`, with id `term-<slug>`. Link its first use in each `h2` section with
  `<a class="term" href="#term-<slug>">`, only for terms that have an entry.
- Technical manuals (setup guides, runbooks, how-to, API guides): ASD-STE100 at about 60%.
  Numbered steps, one action each, starting with a verb; condition before action; active
  voice; 20 words or fewer; warnings before their step; the glossary term every time.
  Explanations may read naturally. Thai text follows the same principles.

### Records

Discussion records live at docs/records/yyyy-mm-dd-<slug>.md, dated the day the discussion
took place. Each record captures one discussion: what was discussed, what was decided, and
any open questions.

## Tools

### Python

Use `uv` for everything Python: `uv run <script>`, `uv add <pkg>`, `uv sync`. Run it
instead of calling `python`, `pip` or `venv` directly. Lint and format with ruff
(`uvx ruff check`, `uvx ruff format`), configured by `ruff.toml` at the project root.

### Node

Use `bun` as the package manager (`bun install`, `bun add`, `bun run`). Fall back to `npm`
only when bun can't do the job.

When you set up a Node project or add a package manager config, set a minimum release age
of 7 days for both tools, so freshly published (possibly compromised) versions are never
installed:

- `bunfig.toml`:
  ```toml
  [install]
  minimumReleaseAge = 604800 # 7 days, in seconds
  ```
- `.npmrc` (needs npm >= 11.10):
  ```ini
  min-release-age=7
  ```
