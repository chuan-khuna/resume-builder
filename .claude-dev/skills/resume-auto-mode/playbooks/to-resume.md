# To resume playbook

Turn the evidence files into the resume's content: `resume/data/resume.yml` (the base resume)
or `resume/versions/<slug>/resume.yml` (one version, for one job ad). The YAML is the ground
truth for the printed resume, and every work claim in it traces to an evidence file.

Read these first:

- [`../references/evidence.md`](../references/evidence.md): the evidence schema, the
  Summary rules and the anonymisation rules.
- `resume/README.md`: the resume layout, the YAML keys, versions and the build commands.
- `resume/data/resume.schema.json`: the fields the YAML may hold.
- [`../references/kami.md`](../references/kami.md): how to use the Kami skill's design
  rules on the Typst resume. Read it before you change the layout or fit content to the page.

Run every `mise` command from the repo root as `mise -C resume …`, or from inside `resume/`.

## Sources

| Resume part | Source |
| ----------- | ------ |
| `experiences[].bullets` | The `## Summary` bullets of the evidence files, and the What I Did and Numbers & Impact they trace to |
| `skills` | The `tools:` lines of the evidence files used. Never "Studied, not used". |
| `experiences[]`: `company`, `jobTitle`, `time` | The user. Evidence holds only the company slug and project periods. |
| `header`, `educations`, `activities`, `interests` | The user. Keep the values already in the YAML unless the user changes them. |
| `projects` | An evidence file when one exists; otherwise the user |

Never take a claim from memory, from `raw/`, or from an old resume. If the user gives a new fact
about work, it goes into the evidence file first, through `/resume-builder:resume-auto-mode verify`, and then
into the YAML.

## Steps

1. **Pick the target.** Take `base` or a `<slug>` from the user's message; default `base`.
   - `base` writes `resume/data/resume.yml`.
   - A slug (like `2026-dec-acme-ml`) writes `resume/versions/<slug>/resume.yml`. The job ad
     goes beside it as `resume/versions/<slug>/job-ad.md`. If it is missing, ask the user to
     paste the ad, and save it there.

   Read the current YAML for the target and, for a version, the base YAML under it.

2. **Pick the evidence.** List `evidence/*/*.md`, except `brag-document.md`, with each file's `title`, `period`, `status`
   and whether `reviewed:` is set. Use every reviewed file. For each file without `reviewed:`,
   ask the user: verify it first (recommended), include its draft bullets, or leave it out.
   Read each file used in full: Summary and Remarks first, then the sections they rest on.
   The Summary is a pool grouped by area and starred by strength: pick from it, do not copy
   it whole.
   _Done when_ every evidence file is used, marked draft, or left out by the user.

3. **Fill the facts evidence lacks.** For each company slug in the files used, find its entry
   in `experiences` by `id`. Ask the user for what is missing: the employer name as it should
   print, the job title or titles, and the dates of employment (`Mon yyyy - Mon yyyy` or
   `- Present`). A change of title at one employer gets its own entry. Ask once for any
   `header` field that is empty.

4. **Plan the content.** Write the plan and show it to the user before you write YAML:
   - each experience entry, and the evidence bullets picked for it, strongest first: start
     from the ★★★ bullets, then ★★ ones the role or job ad calls for; a ★ bullet only when it
     fills a gap;
   - for each entry, whether it uses labels, by the `resume` playbook's Labels rule. When it
     does, list its labels: areas of work that do not overlap, with each evidence bullet
     under exactly one. Start from the evidence areas, merging areas across projects that
     name the same work;
   - for a version, the `job-ad.md` requirements sorted as Direct, Bridge or Gap, as the
     `resume` playbook's Tailoring steps define. A Gap is a question, never a bullet;
   - the Remarks that limit a bullet (a scope caveat, a number not to quote, a role it fits);
   - what to leave out or set `hidden: true` to fit `maxPages`.

   Stop until the user approves the plan.

5. **Write the bullets.** For each planned bullet, start from its evidence Summary bullet and
   apply the `resume` playbook (`.claude-dev/skills/resume-auto-mode/playbooks/resume.md`): British English, a plain
   verb first, one result, 25 words or fewer, present tense for the current role and past for
   the rest. Use the `{label, text}` form for an entry the plan labels, and `{text}` alone
   for one it does not. Then check each bullet against its source:
   - it claims nothing the evidence bullet and its What I Did bullet do not support;
   - each number appears in the evidence Numbers with the same scope; a configured value reads
     "designed for";
   - each impact claim is a `fact`, `user` or `confirmed` Impact item; an `assessed` one stays
     out;
   - shared work keeps "with a teammate" or "contributed to"; `wip` or `dropped` work reads
     as prototyped or evaluated, never as delivered;
   - names stay anonymised as the evidence has them.

   Put a trace comment on the line above each bullet:

   ```yaml
   bullets:
     # evidence/company-a/2025-retail-shelf-cv.md B2
     - label: Computer vision
       text: Trained YOLO and RF-DETR detectors for retail shelf products, reaching 0.92 product AP50.
     # evidence/company-a/2026-support-chatbot.md B1 (draft)
     - label: LLM applications
       text: Built an eval runner that replays 633 client test cases against the support chatbot.
   ```

   An entry without labels writes each bullet as `- text: …`.

   One bullet may merge several evidence bullets: list each, as in `B1 + B3`. Mark a bullet
   from an unreviewed file `(draft)`.
   _Done when_ every experience bullet has a trace comment and passes the checks above.

6. **Write the skills.** Group the `tools:` of the evidence files used into the existing
   `skills` categories. Add a tool only if an evidence file lists it as used. For a version,
   order each category by the job ad. Put a comment above `skills` naming the evidence files.

7. **Search for banned terms.** For each company used, read `raw/<company>/mapping.yml` and
   grep the target YAML for every `internal_name`, real repo name (the last segment of each
   source `url`), source host, org name and Jira site. The employer name in `company:` is allowed. _Done when_ the search returns zero hits.

8. **Check and build.**
   1. Run `mise -C resume run check`. Fix every error.
   2. Run `mise -C resume run build` for `base`, or `mise -C resume run version <slug>`.
   3. If the build fails on page count, cut or hide the lowest-ranked bullets. Raise
      `maxPages` only when the user agrees.
   4. Read every page image in `resume/build/<slug>/`.

9. **Review with the user.** Show the diff of the YAML and the page images. Apply
   corrections; each changed bullet keeps its trace comment. Then suggest
   `/resume-builder:resume-auto-mode review-resume <slug>`. Commit only when the user asks.

10. **Learn.** Apply [`../references/learning.md`](../references/learning.md). Typical
    lessons here: changes the user made to the plan (order, labels, what to cut), bullet
    wording they rewrote, and the roles or job ads they target.

## Completion

The target YAML passes `check`, builds within `maxPages`, every experience bullet carries a
trace comment to an evidence Summary bullet, every skill comes from an evidence `tools:` line,
the banned-term search returns zero hits, and the user has approved the content.
