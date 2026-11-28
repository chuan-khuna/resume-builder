---
name: help
description: Answer a question about the resume pipeline, say where it stands and what to do next, and hand back a prompt to send. Use for /resume-builder:help, or when the user asks what to do next, which playbook fits, why a run went wrong, or how to word a request.
disable-model-invocation: true
argument-hint: "[<company> | <question>]"
---

# Resume help

Answer the user's question about the pipeline, hand them a prompt they can send, and link the file the answer came from. For a help question, don't start the work. The user asked how or what next, and a playbook run spends tokens and may edit files, so let them send the prompt.

A message that asks for work, such as "distill company-a", is not a help question. Read [`../resume-auto-mode/SKILL.md`](../resume-auto-mode/SKILL.md) and run the playbook.

This file maps questions to the playbooks and references that hold the answers. Those files own the details. Read the file you route to before you quote it, and trust it when it disagrees with this map. The playbooks are in `../resume-auto-mode/playbooks/` and the references in `../resume-auto-mode/references/`.

## Find out what they need

Infer the need from the message and the repo. A named situation, such as "how do I tailor the resume to a job ad?", goes straight to its section. If the need is still unclear, ask one multiple-choice question with these options, then answer only the section they pick:

- Get set up
- Start a task with `/resume-builder:resume-auto-mode`
- Pick a playbook for a situation
- Fix a run that went wrong
- Make the pipeline my own

Check the state that changes the answer, by reading files. Never ask for a fact you can observe. Take `<company>` from the arguments; with none, use every folder under `raw/` and `evidence/`.

## What to do next

| What you see | Next step | Prompt |
| ------------ | --------- | ------ |
| No `raw/<company>/mapping.yml` | The user writes it from `raw/repository-mapping.example.yml`. You cannot. | none, say what to fill in |
| `mapping.yml`, no `raw/<company>/repos/` | Ingest | `/resume-builder:resume-auto-mode ingest <company>` |
| A project in `mapping.yml` with no `evidence/<company>/*-<id>.md` | Distill | `... distill <company> <id>` |
| An evidence file with an empty `reviewed:` | Verify | `... verify <company> <id>` |
| All evidence reviewed, `resume/data/resume.yml` missing or older than the evidence | To resume | `... to-resume` |
| A built resume with no `resume/review/index.html` newer than `resume.yml` | Review resume | `... review-resume` |
| A review with open fixes | Steer, or to-resume for a big change | `... steer <what to change>` |
| Verified evidence and no `evidence/<company>/brag-document.md` | To brag, optional | `... to-brag <company>` |
| A job ad the user pastes or names | To resume with a slug | `... to-resume <slug>` |

Check dates with `git log -1 --format=%cs -- <path>` or file times. Name the evidence you used, for example "3 of 14 files have no `reviewed:`". Give the first row that matches, not the whole table. Add a second suggestion only when two steps are independent.

## Get set up

1. Install the plugin with `mise run plugins`, then restart Claude Code. Type `/resume-builder` and check that `help` and `resume-auto-mode` appear.
2. Write `raw/<company>/mapping.yml` from `raw/repository-mapping.example.yml`. The user owns it. It holds real client names and a Jira token, so it stays local.
3. Run `/resume-builder:resume-auto-mode full-pipeline <company>`, or one step at a time in the order ingest, distill, verify, to-resume, review-resume, steer.

[`workflow.md`](../resume-auto-mode/references/workflow.md) has the layout and the `mapping.yml` schema. [`resume/README.md`](../../../resume/README.md) covers building the PDF. Offer to word their first prompt with them, per [`references/prompting.md`](references/prompting.md).

## Start a task with `/resume-builder:resume-auto-mode`

The skill matches the request to one playbook, copies its steps into the todo list, and runs them. A step it skips stays in the list as `skip: <reason>`. A good prompt names the playbook and gives the facts only the user holds: the company, the project id, the job ad, the target role. It does not list steps, because a hand-written sequence tends to drop or reorder steps the playbook keeps. Read [`references/prompting.md`](references/prompting.md) before you help word one, and [`references/recipes.md`](references/recipes.md) for prompts to copy.

## Pick a playbook

The default answer is `full-pipeline` for a new company, and a single playbook for one change. Read the playbook before you recommend it, and give one example prompt.

| The user wants to | Playbook |
| ----------------- | -------- |
| Go from raw data to a reviewed resume | [`full-pipeline`](../resume-auto-mode/playbooks/full-pipeline.md) |
| Load repos and Jira tickets into `raw/` | [`ingest`](../resume-auto-mode/playbooks/ingest.md) |
| Turn one project's raw data into an evidence file | [`distill`](../resume-auto-mode/playbooks/distill.md) |
| Add work that has no repo, from memory | [`distill`](../resume-auto-mode/playbooks/distill.md) in interview mode |
| Confirm a draft evidence file and set `reviewed:` | [`verify`](../resume-auto-mode/playbooks/verify.md) |
| Write the base resume, or one for a job ad | [`to-resume`](../resume-auto-mode/playbooks/to-resume.md) |
| Change the resume the way they say | [`steer`](../resume-auto-mode/playbooks/steer.md) |
| Check the built PDF for gaps, length, ATS and readability | [`review-resume`](../resume-auto-mode/playbooks/review-resume.md) |
| Get a readable account of one company for interviews | [`to-brag`](../resume-auto-mode/playbooks/to-brag.md) |
| Keep notes on the job search or their field | [`wiki`](../resume-auto-mode/playbooks/wiki.md) |
| Write or proofread resume text with no pipeline | [`resume`](../resume-auto-mode/playbooks/resume.md) |
| Find their way around | `/resume-builder:help` |

If a playbook is missing from this table, read its first lines and route by what it says.

Close calls:

- `distill` reads raw data. `verify` asks the user. A claim moves from draft to ground truth only in `verify`.
- `to-resume` rewrites the YAML from evidence. `steer` changes it as the user directs and backs each work claim with evidence. A new job ad is `to-resume <slug>`. A tweak is `steer`.
- `review-resume` judges the built PDF. `steer` applies the fixes the user accepts.
- `to-brag` is a view of the evidence for interviews. It never backs a resume claim.
- `wiki` notes never back a resume claim. Only evidence does.

Not in this plugin:

- Layout and design rules for the Typst resume come from the Kami skill in `.claude/skills/kami/`, as [`kami.md`](../resume-auto-mode/references/kami.md) describes.
- The git, planning and code-review skills belong to Claude Code and other plugins.

## Fix a run that went wrong

| Symptom | Fix |
| ------- | --- |
| `/resume-builder` shows no skills | The plugin is not installed. Run `mise run plugins`, then restart Claude Code. |
| A command named `/resume-evidence:...` does not exist | The plugin was renamed. Use `/resume-builder:resume-auto-mode <playbook>`. |
| A claim is refused for lack of evidence | Only evidence backs a resume claim. Run `distill`, or `distill` in interview mode, then `verify`. |
| The resume cites a draft evidence file | Run `verify` on it. `review-resume` flags it as `warn` until `reviewed:` is set. |
| A real client name or host appears in evidence | Anonymise it by the banned-term rules in [`evidence.md`](../resume-auto-mode/references/evidence.md) and rerun the search. |
| The build fails on the page count | Cut text with `steer`. Do not shrink the font. |
| Ingest fails on one repo | Check the `url` and credentials in `mapping.yml`. The user owns that file. |
| The agent keeps asking what it could read | Say "read the repo, don't ask". Then fix the playbook that let it ask. |
| A claim was added from memory | Remove it, or run `verify` so the user confirms it into the evidence file first. |

For a run that drifts, [`references/prompting.md`](references/prompting.md) has one-line steers.

## Make the pipeline my own

- The user's preferences go to `wiki/me.md` through `uv run scripts/me.py add preference|need "<text>"`. They apply to this user only.
- A lesson that helps anyone goes into the playbook or reference it belongs to. [`learning.md`](../resume-auto-mode/references/learning.md) says which place holds what.
- To change a playbook, edit its file under `../resume-auto-mode/playbooks/`, then keep `docs/documents/` in step.

## Reply

Lead with the answer. Give the next step and at most one example prompt in a code block, adapted from [`references/recipes.md`](references/recipes.md) when one fits, then the link to the file the answer came from. Keep it short unless the user asked for the whole map.
