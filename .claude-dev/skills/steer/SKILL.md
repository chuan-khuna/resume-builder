---
name: steer
description: Change the resume ground truth as the user directs (sections, projects, education, the experience bullets they want), backing each work claim with evidence and suggesting evidence-backed wording.
disable-model-invocation: true
argument-hint: "[base | <slug>] <what to change>"
---

# Steer

The user steers `resume.yml`; evidence keeps it honest. The user says what the resume should
hold: which sections print and in what order, a project, an education line, the experience
bullet they want to write. You make the change. For every claim about work, you find the
evidence behind it, and where the evidence is thinner or stronger than the user's wording, you
suggest the wording it supports.

Use it for targeted edits to an existing resume. A first build from the evidence is
`/resume-evidence:to-resume`.

Read these first:

- [`../../reference/evidence.md`](../../reference/evidence.md): the Summary rules (numbers,
  shared work, unfinished work) and the anonymisation rules.
- `resume/README.md` and `resume/data/resume.schema.json`: the YAML keys and versions.
- The `resume` skill (`.claude-dev/skills/resume/SKILL.md`): the writing rules for every bullet.

## Steps

1. **Pick the target and list the changes.** Take `base` or a `<slug>` from the user's message;
   default `base`. `base` edits `resume/data/resume.yml`; a slug edits
   `resume/versions/<slug>/resume.yml`, over the base. Read the target YAML. Write the user's
   request as a numbered change list, one item per change. If the message names no change, ask
   what to change.
   _Done when_ every change the user asked for is one item.

2. **Sort each change.**
   - **User facts**: `sections`, order, `maxPages`, `hidden`, `header`, `educations`,
     `activities`, `interests`, and a personal project with no evidence file. The user is the
     source; these need no evidence.
   - **Work claims**: an experience bullet, a work project, a skill, a job title or date range
     the evidence contradicts. Each must trace to an evidence file.

   _Done when_ every item is a user fact or a work claim.

3. **Match each work claim to evidence.** Search `evidence/*/*.md`, except `brag-document.md`: the Summary bullets, What I
   Did, Numbers & Impact, Tools and the Remarks. Grade the claim:
   - **backed**: What I Did supports every part, each number is in Numbers with the same
     scope, and each impact claim is a `fact`, `user` or `confirmed` Impact item;
   - **stretched**: part of it outruns the evidence: `wip` or `dropped` work read as delivered,
     shared work read as mine alone, a configured value read as a result, a number with a wider
     scope, an impact that is only `assessed`, or a claim a Remark caveat rules out;
   - **unbacked**: no evidence file holds it.

   A skill is backed only when a used file's `tools:` line lists it; "Studied, not used" is
   unbacked.
   _Done when_ every work claim has a grade and the evidence lines behind it.

4. **Suggest.** Show the user, item by item:
   - their wording, the grade, and the evidence behind it (file and bullet);
   - for **stretched**: a rewrite inside the evidence, naming what changed and the Remark or
     Numbers row that requires it;
   - for **unbacked**: two routes. Record the user's account in an evidence file now (step 5),
     then write the bullet; or leave it out;
   - stronger evidence the user did not mention: a measured number, a `fact` Impact item, a
     related Summary bullet in the same area, a project that fits the same topic.

   Ask the user to choose per item: their wording (backed only), the rewrite, record and write,
   or leave out.
   _Done when_ every work claim has the user's decision.

5. **Record the user's account.** For each item routed to evidence, edit the evidence file the
   way verify folds in an answer: a What I Did bullet citing `[me: yyyy-mm-dd]`, a number as a
   user-reported Numbers row with its ID, Kind and scope, an outcome as a `user` Impact item. If the file has `reviewed:` set, add an Open
   question that its Summary predates the new account. If no evidence file fits (a project or
   employer with none), stop for that item and point the user to
   `/resume-evidence:distill` in interview mode. Run the banned-term search from `evidence.md`
   on every evidence file you edit.
   _Done when_ each recorded account is cited and each edited file returns zero banned-term hits.

6. **Write the YAML.** Apply every change the user approved. Leave the rest of the file as it
   is.
   - User facts: write them as given; quote values YAML would misread (`time: "2025"`).
   - Work bullets: follow the `resume` skill's writing rules, including its Labels rule, and
     the `{label, text}` form when the entry's other bullets use it. A new label must not
     overlap the entry's other labels. Put a trace comment above each bullet, as to-resume
     does: `# evidence/<company>/<file>.md B2`, or `What I Did: <short> [me: yyyy-mm-dd]` for an
     account recorded in step 5. Add `(draft)` when the file has no `reviewed:`.
   - Skills: update the comment above `skills` so it names every evidence file the list draws on.

7. **Check and build.**
   1. Run the banned-term search from to-resume step 7 on the target YAML.
   2. Run `mise -C resume run check`, then `mise -C resume run build` for `base` or
      `mise -C resume run version <slug>`.
   3. If the build fails on page count, propose what to cut or hide; raise `maxPages` only when
      the user agrees.
   4. Read every page image in `resume/build/<slug>/`.

8. **Show the result.** Show the YAML diff, the page images, and any item the user left out or
   routed to distill. Commit only when the user asks.

9. **Learn.** Apply [`../../reference/learning.md`](../../reference/learning.md). Every steer
   shows a preference: record each wording, label, order or emphasis the user chose or
   rejected. When the same lesson would help any user, fix the skill it belongs to as well.

## Completion

Every change the user asked for is applied or declined by the user, every work claim in the
YAML carries a trace comment to evidence, every account the user gave is recorded in evidence
with a `[me: …]` citation, the banned-term searches return zero hits, `check` passes, and the
build fits `maxPages`.
