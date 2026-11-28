# Full pipeline playbook

Take one company from raw data to a reviewed resume. You own the run: each step is its own
playbook, and you open it, run it, and check its output before the next step starts.

1. **Ingest.** Run the [ingest](ingest.md) playbook for the company. Stop if `mapping.yml` is
   missing or a clone failed. Tell the user what to fix.
2. **Distill.** For each project in `mapping.yml` with no evidence file, run the
   [distill](distill.md) playbook. List the projects first and let the user drop any.
3. **Verify.** For each new or changed evidence file, run the [verify](verify.md) playbook. It
   interviews the user, so ask one project at a time. Never skip it: a draft Summary is not
   ground truth.
4. **To resume.** Run the [to-resume](to-resume.md) playbook for `base`, or for the job-ad slug
   the user names. Every claim must trace to a verified evidence file.
5. **Review.** Run the [review-resume](review-resume.md) playbook on the built PDF.
6. **Steer.** Apply the user's reaction to the review with the [steer](steer.md) playbook, then
   rebuild and review again until they accept.
7. **To brag.** Offer the [to-brag](to-brag.md) playbook for interviews. It is a view of the
   evidence, never a source.

Skip a step the user already finished and say `skip: <reason>`.

**Reply:** per step, what ran and what it wrote, what is waiting on the user, and the path of the
built PDF.
