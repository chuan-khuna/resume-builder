---
name: distill
description: Distill one project's raw repositories and Jira tickets, or an interview with the user when there are none, into an anonymised, cited evidence file.
disable-model-invocation: true
---

# Distill

Turn one project's data in `raw/<company>/` into `evidence/<company>/<yyyy>-<id>.md`: the
ground truth of **what I did**, where every claim cites its evidence and no real name leaks,
topped by a draft Summary of the resume bullets it supports.

Read [`../../reference/workflow.md`](../../reference/workflow.md) first: it defines the layout,
the mapping schema and the rules for scripts. The evidence file's schema, citation forms and
anonymisation rules are in [`../../reference/evidence.md`](../../reference/evidence.md).

## Steps

1. **Pick the project.** Take `<company>` and `<id>` from the user's message; if either is
   missing, list the projects in `raw/<company>/mapping.yml` and ask. Each repo
   folder is named by its `slug` from `mapping.yml`: cite the repo by that slug, in
   citations and in `verified:`.
   - An evidence file matching `evidence/<company>/*-<id>.md` exists: **update** mode. Read it;
     its `verified:` shas mark where the new commits start.
   - None exists: **new** mode.

   If `raw/<company>/repos/<id>/` has no repos, ask the user: run ingest first, or build the
   file from an interview (**interview mode**, below), for when the user has no repo access or
   the work left no code. In interview mode, skip steps 2 and 3; step 4 still reads any Jira
   tickets.

   Read the project's items under "Leads for distill" in `raw/<company>/TODO.md`: each is a
   fact to confirm or reject in steps 2–4.

   **Interview mode.** Interview the user on their responsibilities in the project, in rounds of
   at most four questions, as verify step 3 does. Cover, in this order:
   - the context: who it was for, the problem, the team and my role in it, the period;
   - each responsibility: what I owned, decided or built, how, and the trade-off taken;
   - what others built (Not mine), outcomes and numbers with their scope, the tools I used,
     and the system's shape (for the Architecture diagram);
   - what held the work back, for the private note.

   Write each responsibility as one What I Did bullet, citing `[me: yyyy-mm-dd]`. A
   responsibility the user describes only vaguely goes to Open questions, not to What I Did.
   For anonymisation, the real names the user gives (employer, client, product) are banned
   terms. If the project has no `mapping.yml` entry, tell the user to add one with its `id`,
   `internal_name` and `title` and no `sources`.
   _Done when_ every responsibility is a cited What I Did bullet or an Open question.

2. **Establish authorship.** Use the authorship script in `scripts/`; write it first if none
   exists. Per repo it reports, with `--all` on every git command:
   - authors: `git shortlog -sne --all`;
   - per directory, two levels deep: my commit count and my share of `git blame` lines at the
     checked-out branch, or at `--ref`;
   - my commits: sha, date, message, files touched;
   - in update mode, only commits after the `verified:` sha;
   - branches ahead: remote branches holding my commits that the checked-out branch lacks.

   Blame and the head sha read the checked-out branch. Commit lists read every branch. When
   branches ahead lists real work of mine, pick the ref that holds it (the newest branch with
   that work, often `dev` or a feature branch), rerun with `--ref <slug>=<ref>`, and record that
   ref's sha in `verified:` with a comment naming the branch. Say in Context which work lives
   only on unmerged branches; it reads as unshipped unless the user says otherwise.

   Claim only paths where my share is real. Project-wide files (README, `pyproject.toml`,
   lock files, CI) describe the project, not my part.
   _Done when_ every top-level area of every repo is classed as **mine**, **shared** or
   **not mine**.

3. **Read the sources.** For each area classed mine or shared: its code, the diffs of my main
   commits, dependency files, README and in-repo docs. Read enough to state what each part does,
   the pattern behind it, and the trade-off taken.

4. **Read Jira.** Run `uv run scripts/jira_tickets.py <company> <id>`: it prints the tickets
   the project's `jira` selectors pick from `raw/<company>/jira/merged.json`. Add
   `--text <term>` for each `internal_name` and real repo name (the last segment of each
   source `url`), to catch tickets outside the
   selected project or epic. If the project has no `jira` selectors, tell the user which to
   add to `mapping.yml`. A ticket proves
   assignment and dates, not authorship: cite it beside git evidence, and send a claim backed
   only by tickets to Open questions.

5. **Write the evidence file** at `evidence/<company>/<yyyy>-<id>.md`, where `yyyy` is the
   year of my first commit in the project, or in interview mode the first year of the
   `period` the user gave. Use the schema in `evidence.md`. Write the evidence
   sections first; in update mode, add new bullets and keep the existing ones as written.
   _Done when_ every What I Did bullet carries at least one citation.

6. **Draft the Summary.** From What I Did and Numbers, write `## Summary` at the top of the
   file, following the Summary rules in `evidence.md`. Every bullet traces to a What I Did
   bullet; every gap a bullet depends on (outcome, scale, shipped or not) is a Remark and an
   Open question.
   - New mode, or `reviewed:` is empty: write or replace the draft.
   - `reviewed:` is set: keep the confirmed bullets as written, add draft bullets for the new
     work marked `(draft)`, and add an Open question that the Summary predates the new commits.
   _Done when_ every bullet has a Remark naming the What I Did bullet it traces to, and every
   number in Numbers is either in a bullet or in a Remark.

7. **Anonymise.** Apply the anonymisation rules in `evidence.md`, then run the banned-term
   search. _Done when_ it returns zero hits.

8. **Review with the user.** Show the Summary first, then the file, and list the Open
   questions. Fold in any account the
   user gives with a `[me: yyyy-mm-dd]` citation; a limit of my own work goes in the private
   note, by the Private notes rules in `evidence.md`. _Done when_ the user confirms the file; the
   Open questions left are for `/resume-evidence:verify`.

9. **Update `raw/<company>/TODO.md`.** Move this project's leads to Done, each noting whether
   it went into the file or into Open questions.

10. **Learn.** Apply [`../../reference/learning.md`](../../reference/learning.md). Typical
    lessons here: how the user wants work anonymised or described, which kinds of work they
    want claimed or left out, and authorship cases the script misread.

## Completion

The file follows the schema, every What I Did bullet is cited, the draft Summary follows the
Summary rules, the banned-term search returns
zero hits, `verified:` holds the HEAD sha read for every repo (empty in interview mode), the
user has confirmed it, and the project's leads in `TODO.md` are resolved.
