---
name: resume-auto-mode
description: Run the resume pipeline in one mode. Matches the request to a playbook (ingest, distill, verify, to-resume, to-brag, steer, review-resume, wiki, resume, or the full pipeline) and follows its steps. Use for /resume-builder:resume-auto-mode or any request to build, change or review the resume or its evidence.
disable-model-invocation: true
argument-hint: "<what you want, e.g. 'full pipeline for <company>' or 'steer: tighten the summary'>"
---

# Resume auto mode

Each pipeline step is a playbook, a step list in `playbooks/<name>.md`. Match the user's request
to one playbook, open its file, copy its steps into the todo list verbatim, and run them. A step
you choose not to do stays in the list as `skip: <reason>`.

Read [`references/workflow.md`](references/workflow.md) once per session for the layout
and the mapping schema. `CLAUDE.md` holds the rules that bind every playbook:

- Evidence is the ground truth. No resume claim traces to memory or to `raw/`.
- `raw/` stays local. Evidence and committed files carry no real client names or credentials.
- All prose follows the writing rules in the [`resume`](playbooks/resume.md) playbook.
- Follow `wiki/me.md` in every task. It wins over a playbook for this user.

## Playbooks

| Request | Playbook |
| ------- | -------- |
| Take a company from raw data to a reviewed resume | [`full-pipeline`](playbooks/full-pipeline.md) |
| Load repos and Jira tickets into `raw/<company>/` | [`ingest`](playbooks/ingest.md) |
| Turn one project's raw data into an evidence file | [`distill`](playbooks/distill.md) |
| Interview the user, fold answers in, confirm the Summary | [`verify`](playbooks/verify.md) |
| Write `resume.yml` from evidence, then build and check | [`to-resume`](playbooks/to-resume.md) |
| Change the resume as the user directs, backed by evidence | [`steer`](playbooks/steer.md) |
| Review the built PDF | [`review-resume`](playbooks/review-resume.md) |
| Build the readable brag document for a company | [`to-brag`](playbooks/to-brag.md) |
| Ingest a wiki source, query the wiki, or lint it | [`wiki`](playbooks/wiki.md) |
| Write or proofread resume text, with no pipeline | [`resume`](playbooks/resume.md) |

The order of the pipeline is ingest, distill, verify, to-resume, review-resume, steer. A step
whose input is missing routes back to the step that makes it. Say which one and why.

## Rules

- **Ask only for what you cannot observe.** The user answers about their own work in verify and
  steer. Everything else, such as which projects lack evidence, you find by reading files.
- **Prove it ran.** Quote the command output, the file written, or the build result. A claim of
  success without it is a guess.
- **One playbook at a time.** The full pipeline opens each playbook in turn. Do not merge their
  step lists.
- **Learn.** Each playbook ends with a Learn step that applies
  [`references/learning.md`](references/learning.md). Do it in the same turn as the
  steer, not at the end.

Run it as `/resume-builder:resume-auto-mode <playbook> <arguments>`, such as `ingest <company>` or `steer base tighten the summary`.
