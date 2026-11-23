---
name: distill
description: Distill one project's raw repositories and Jira tickets into an anonymised, cited evidence file.
disable-model-invocation: true
---

# Distill

Turn one project's data in `raw/<company>/` into `evidence/<company>/<yyyy>-<id>.md`: the
ground truth of **what I did**, where every claim cites its evidence and no real name leaks.

Read [`../../reference/workflow.md`](../../reference/workflow.md) first: it defines the layout,
the mapping schema and the rules for scripts. The evidence file's schema, citation forms and
anonymisation rules are in [`../../reference/evidence.md`](../../reference/evidence.md).

## Steps

1. **Pick the project.** Take `<company>` and `<id>` from the user's message; if either is
   missing, list the projects in `raw/<company>/mapping.yml` and ask. If
   `raw/<company>/<id>/` has no repos, tell the user to run ingest and stop.
   - An evidence file matching `evidence/<company>/*-<id>.md` exists: **update** mode. Read it;
     its `verified:` shas mark where the new commits start.
   - None exists: **new** mode.

   Read the project's items under "Leads for distill" in `raw/<company>/TODO.md`: each is a
   fact to confirm or reject in steps 2–4.

2. **Establish authorship.** Use the authorship script in `scripts/`; write it first if none
   exists. Per repo it reports, with `--all` on every git command:
   - authors: `git shortlog -sne --all`;
   - per directory, two levels deep: my commit count and my share of `git blame` lines at HEAD;
   - my commits: sha, date, message, files touched;
   - in update mode, only commits after the `verified:` sha.

   Claim only paths where my share is real. Project-wide files (README, `pyproject.toml`,
   lock files, CI) describe the project, not my part.
   _Done when_ every top-level area of every repo is classed as **mine**, **shared** or
   **not mine**.

3. **Read the sources.** For each area classed mine or shared: its code, the diffs of my main
   commits, dependency files, README and in-repo docs. Read enough to state what each part does,
   the pattern behind it, and the trade-off taken.

4. **Read Jira.** Use the Jira query script in `scripts/`; write it first if none exists. Find
   the project's tickets by `internal_name`, repo names, Jira project and epic. A ticket proves
   assignment and dates, not authorship: cite it beside git evidence, and send a claim backed
   only by tickets to Open questions.

5. **Write the evidence file** at `evidence/<company>/<yyyy>-<id>.md`, where `yyyy` is the
   year of my first commit in the project. Use the schema in `evidence.md`, without `## Resume`.
   In update mode, add new bullets and keep the existing ones as written; if the file has a
   `## Resume` section, keep it and add an Open question that it predates the new commits.
   _Done when_ every What I Did bullet carries at least one citation.

6. **Anonymise.** Apply the anonymisation rules in `evidence.md`, then run the banned-term
   search. _Done when_ it returns zero hits.

7. **Review with the user.** Show the file and list the Open questions. Fold in any account the
   user gives with a `[me: yyyy-mm-dd]` citation. _Done when_ the user confirms the file; the
   Open questions left are for `/resume-evidence:verify`.

8. **Update `raw/<company>/TODO.md`.** Move this project's leads to Done, each noting whether
   it went into the file or into Open questions.

## Completion

The file follows the schema, every What I Did bullet is cited, the banned-term search returns
zero hits, `verified:` holds the HEAD sha read for every repo, the user has confirmed it, and the
project's leads in `TODO.md` are resolved.
