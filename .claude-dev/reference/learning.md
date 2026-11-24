# Learning: shared reference

Read by every skill. The pipeline learns from each session in two places, and you update them
as you go: in the same turn as the steer that teaches you something, not at the end.

| Place | Holds | Committed |
| ----- | ----- | --------- |
| `me.md` (repo root) | This user's preferences and needs | No: gitignored, may hold personal details |
| `.claude-dev/` skills and references | Rules that help any user of the pipeline | Yes: no personal details, no client names |

`CLAUDE.md` loads `me.md` into every session. Follow it in every task; when it conflicts with
a skill, `me.md` wins for this user.

## What counts as a lesson

- **A preference**: the user steers, corrects, rejects or confirms something: a wording, a
  label, an order, an emphasis, a format, how much to ask before acting.
- **A need**: the user states a goal or constraint: a target role, a page limit, a deadline,
  a kind of job ad.
- **A pipeline lesson**: a rule a skill missed, a step that failed or misled, a check worth
  adding, a script bug or a missing script option.

Not a lesson: a fact about the user's work. That goes into evidence, cited `[me: yyyy-mm-dd]`,
through `verify` or `steer`. Do not record what the repo already records: evidence, resume
YAML, git history.

## Steps

1. **Record the preference or need** in `me.md` with the script, one fact per bullet, in the
   user's terms:

   ```bash
   uv run scripts/me.py add preference "<text>"
   uv run scripts/me.py add need "<text>"
   ```

   The script dates the bullet and skips a duplicate. To change or delete a bullet that turned
   out different or wrong, edit `me.md` directly.

2. **Fix the pipeline** when the lesson would help any user. Edit the skill, reference file or
   script it belongs to; keep its style and rules (scripts: `workflow.md` "Scripts"). Keep the
   docs in step, as `CLAUDE.md` "Documents" says. When a `me.md` bullet prompted the fix, record
   where the rule now lives:

   ```bash
   uv run scripts/me.py add preference "<text>" --skill <skill or reference>
   ```

   or edit the existing bullet to end "Now in the `<skill>` skill."

3. **Tell the user** in one line what you recorded or changed, at the end of your reply.

_Done when_ every steer in the session is in `me.md` or in a skill, and no committed file holds
anything only `me.md` should know.
