# Wording a prompt

A prompt for `/resume-builder:resume-auto-mode` has three parts: the playbook, the target, and any fact only the user holds.

```
/resume-builder:resume-auto-mode <playbook> <target> <facts>
```

## Rules

- **Name the playbook.** `distill`, `to-resume`, `steer`. With no name the skill guesses from the words.
- **Name the target.** `<company>` and `<id>` for evidence steps, `base` or a `<slug>` for resume steps. The skill lists the choices when it can't tell, but a named target saves a turn.
- **Give the facts the repo can't show.** The job ad, the target role, the page limit, the claim you want and what you did. Never give what the repo already records.
- **Don't list the steps.** The playbook orders them. A hand-written sequence drops or reorders steps.
- **Say what done looks like when it isn't obvious.** "One page", "for a backend role", "no change to the experience section".
- **Paste a job ad whole.** Don't summarise it. The gaps are in the details.

## One-line steers for a run that drifts

- "Read the repo. Don't ask me what you can find yourself."
- "That claim has no evidence file. Distill or verify it first."
- "Run the real build and quote the output."
- "Keep the page count. Cut text, don't shrink it."
- "Do only the `<playbook>` playbook. Stop after it."
