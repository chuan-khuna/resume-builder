# Resume

The resume, typeset with [Typst](https://typst.app) from structured YAML. Copied from
[chuan-khuna/typst-resume](https://github.com/chuan-khuna/typst-resume) at `9f299b1`.

Every work claim in the YAML traces to an evidence file in `../evidence/`. The
`/resume-evidence:to-resume` skill writes the YAML from the evidence, and
`/resume-evidence:review-resume` reviews the built PDF. See
`../docs/documents/user-manual.html`.
The content lives in YAML files and the layout lives in Typst templates, so you
can make a version for each job application without touching the design.
The styling is based on [Kami](https://github.com/tw93/kami).

## Quick start

You need [mise](https://mise.jdx.dev). This folder's `mise.toml` pins Typst;
Bun and uv come from the repo root's `mise.toml`. Run the commands below from
inside `resume/`, or from the repo root with `mise -C resume …`.

```sh
mise trust            # once: allow this folder's mise.toml
mise install          # install Typst, Bun and uv
mise run build        # build the base resume -> build/base/classic.pdf
```

## Project layout

```
templates/<template>.typ        page layouts you can compile
  classic.typ                   one column, headings above each section
  rail.typ                      section headings in a narrow left column
lib/                            shared Typst used by every template
  data.typ                      loads data/resume.yml and the version file
  style.typ                     fonts, sizes, colours, header, page-count check
  sections.typ                  renders each section in the order you list
data/
  resume.yml                    the base resume: everything you might print
  resume.schema.json            JSON schema for the base resume and versions
versions/<slug>/resume.yml      overrides for one version of the resume
versions/<slug>/job-ad.md       the job ad a version targets
scripts/check.py                checks the YAML files against the schema
fonts/                          fonts kept in the repo; system fonts are ignored
review/                         review pages, shared styles, REVIEW_TEMPLATE.html
build/<slug>/<template>.pdf     generated output, plus one PNG per page (gitignored)
```

`<slug>` is a version's folder name, such as `2026-jul-dev`. Builds of the base
resume, with no version, go in `build/base/`.

`data/resume.yml` is the source of truth for the content. A version file
overrides it one top-level key at a time, the schema defines which fields are
allowed, and the templates only lay the content out. Everything in `build/` is
regenerated on each build, so edit the YAML, not the output.

## Build

```sh
mise run build                  # base resume      -> build/base/classic.pdf
mise run build rail             # rail template    -> build/base/rail.pdf
mise run version <slug>         # a version        -> build/<slug>/classic.pdf
mise run version <slug> rail    # version, rail    -> build/<slug>/rail.pdf
mise run watch                  # rebuild build/base/classic.pdf on every save
mise run watch rail             # the same for the rail template
mise run check                  # check every resume.yml against the schema
```

Each build writes a PDF and a PNG of each page, for example
`build/base/classic.pdf` and `build/base/classic-1.png`.

**The build fails if the resume is too long.** A resume must fit on one page
unless its data sets `maxPages`. To fix a failed build, cut text, hide entries,
or raise `maxPages`.

## Edit the content

Everything is in `data/resume.yml`. Its first line,
`# yaml-language-server: $schema=resume.schema.json`, gives you autocomplete
and validation in VS Code with the YAML extension (Red Hat). To check every
resume file from the command line, run `mise run check`. It also catches what
the editor misses: duplicate keys, and unquoted values such as `no` or `2025`
that YAML reads as a boolean or a number. Quote those: `time: "2025"`.

| Key | What it does |
|---|---|
| `header` | Name, job title, contact details, `location`. Optional `headline` (printed in medium weight) and `introduction` make up the summary. |
| `sections` | Which sections to print, in order: `skills`, `experiences`, `projects`, `educations`, `activities`, `interests`. A section you leave out is not printed. |
| `maxPages` | The most pages the resume may use. Default 1. |
| `experiences`, `projects`, … | The entries in each section. |

Add `hidden: true` to an experience or project entry to keep it in the data
without printing it.

## Make a version for an application

A version file replaces whole top-level keys of `data/resume.yml`. Keys are
not merged field by field. For example, a version that contains `experiences`
replaces the whole experiences list.

1. Create `versions/<slug>/resume.yml` that starts like this:

   ```yaml
   # yaml-language-server: $schema=../../data/resume.schema.json
   ```

2. Add only the keys you want to change, for example `header`, `sections` or
   `maxPages`.
3. Run `mise run version <slug>`.

## Fonts and options

Fonts load only from `fonts/` (`TYPST_FONT_PATHS` and
`TYPST_IGNORE_SYSTEM_FONTS` in `mise.toml`), so the PDF looks the same on
every machine.

| Folder | Font | Used for | Licence |
|---|---|---|---|
| `fonts/geist/` | Geist | body text | SIL OFL, committed |
| `fonts/geist/` | Geist Serif | name and section headings | SIL OFL, committed |

The mise tasks use the default fonts and size. To try others, run Typst
yourself through `mise exec` so the environment from `mise.toml` applies:

```sh
mise exec -- typst compile templates/classic.typ build/base/try.pdf \
  --input "serif=Geist" --input size=9
```

A font must be in `fonts/` to load. Other fonts change how much text fits on a page, so the page check still
applies. If a font makes the resume too long, pass a smaller `size`. Build into
a folder that already exists, because Typst doesn't create folders.

| Input | Default | What it sets |
|---|---|---|
| `version` | none | version folder in `versions/` |
| `sans` | `Geist` | body font |
| `serif` | `Geist Serif` | font for the name and section headings |
| `size` | `8.8` | body size in points |

## Agent skills

The skills are in the `resume-evidence` plugin in `../.claude-dev/skills/`:

- `/resume-evidence:to-resume [base | <slug>]` writes `data/resume.yml` or a
  version from the evidence files, with a trace comment above each bullet.
- `/resume-evidence:steer [base | <slug>] <what to change>` changes the YAML
  as you direct (sections, projects, education, the bullets you want) and
  checks each work claim against the evidence, suggesting wording it supports.
- `/resume-evidence:resume` writes and proofreads resume text in British
  English. Copied from [chuan-khuna/altr-stack](https://github.com/chuan-khuna/altr-stack).
- `/resume-evidence:review-resume [slug] [template]` measures a built resume
  and writes an HTML review to `review/`.

`kami`, the design system this styling is based on, installs with the other
vendored skills: `mise run skills` at the repo root.
