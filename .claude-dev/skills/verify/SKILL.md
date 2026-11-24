---
name: verify
description: Interview the user on a distilled evidence file, fold the answers in, and confirm its Summary (resume bullets and remarks).
disable-model-invocation: true
---

# Verify

Turn one distilled evidence file into a confirmed one: close its gaps by asking the user, then
confirm the `## Summary` (resume bullets and remarks) at the top of it. Git told distill what I
did; verify asks me what it was worth.

Read [`../../reference/evidence.md`](../../reference/evidence.md) first: it holds the schema,
the citation forms and the anonymisation rules. Evidence stays the ground truth: every resume
bullet traces to a What I Did bullet, and every answer the user gives lands in the evidence
sections before it reaches a bullet.

## Steps

1. **Pick the file.** Take `<company>` and `<id>`, or a path, from the user's message. If none
   is given, list `evidence/*/*.md` with, for each, whether it has `reviewed:` and how many Open
   questions it holds, and ask which to verify. Read the whole file.

2. **Build the question list.** One question per gap:
   - every item under Open questions;
   - frontmatter values marked "to confirm", or a `period`/`role` git could only guess;
   - every Numbers row that is configured or estimated, or a measured value with no baseline;
   - every `assessed` Impact item: is the reading right, and may it back a bullet? Ask for the
     numbers that would turn it into a measured row (for a rushed delivery: the deadline and
     who set it; for a performance or cost gain: the before and after);
   - every What I Did bullet with no outcome: ask for the before → after, the scale (users,
     requests, data volume, clients), the money or hours saved, and whether it shipped;
   - every Not mine item whose author is uncertain;
   - every draft Summary bullet: is it correct, is there a number I don't want shown?
   - one question for the whole file: what held the work back (time, a skill I lacked then,
     interest, a scope cut)? The answer goes in the private note.

   Rank them: questions that decide a bullet (authorship, shipped or not, an outcome number)
   first, then context (role, team size, who asked), then detail.
   _Done when_ every gap in the file maps to a question.

3. **Interview the user.** Ask in rounds of at most four, highest rank first, with
   AskUserQuestion when the answers are choices (yes / no / partly, shipped / dropped) and as
   plain numbered questions when they are free text or numbers. State in each question what the
   file currently says and which bullet depends on it. Accept "don't know" as an answer.
   _Done when_ every question has an answer or the user stops the interview.

4. **Fold the answers in.** Edit the evidence sections, citing each answer `[me: yyyy-mm-dd]`:
   - a confirmed or corrected claim → its What I Did bullet, Not mine item or frontmatter field;
   - a number → a Numbers row with its ID, Kind and scope, marked user-reported;
   - an `assessed` Impact item the user confirms → Status `confirmed`, with the answer cited in
     its Basis; one the user rejects → delete the row (its basis rows stay); a new outcome →
     a `user` Impact item;
   - a "don't know" → stays under Open questions, suffixed "(asked yyyy-mm-dd: unknown)";
   - a limit of my own work → `raw/<company>/notes/<id>.md`, by the Private notes rules in
     `evidence.md`; if it narrows a bullet's claim, also a neutral caveat Remark;
   - an answer that names a missing repo or Jira project → tell the user what to add to
     `mapping.yml`, and add it to "Projects to add to mapping.yml" in `raw/<company>/TODO.md`.

   Remove each answered item from Open questions.

5. **Rewrite `## Summary`.** Follow the Summary rules in `evidence.md`, starting from distill's
   draft: areas that do not overlap, starred bullets, and confirmed Impact items now usable in
   bullets. A file in the older format is migrated here, as `evidence.md` says. Replace the
   section whole and drop every `(draft)` mark. _Done when_ every bullet has a Remark naming the
   What I Did bullet and the Numbers and Impact IDs it uses.

6. **Anonymise.** Apply the anonymisation rules in `evidence.md` to the whole file, then run the
   banned-term search. Answers are where new client and person names arrive. _Done when_ the
   search returns zero hits.

7. **Review with the user.** Show the Summary, the diff of the evidence sections and the
   private note.
   Apply corrections, then set `reviewed:` to today. _Done when_ the user confirms the file.

8. **Learn.** Apply [`../../reference/learning.md`](../../reference/learning.md). The facts the
   user gives go into the evidence file, not `wiki/me.md`. Typical lessons here: how they like to be
   interviewed (round size, which questions to skip), and Summary wording they rewrote.

## Completion

Every gap from step 2 is answered or left as a dated unknown, every answer is cited in the
evidence sections, `## Summary` holds confirmed bullets grouped by area that each carry a
Remark, no Impact item is left `assessed`, the
banned-term search returns zero hits, and `reviewed:` holds the date the user confirmed it.
