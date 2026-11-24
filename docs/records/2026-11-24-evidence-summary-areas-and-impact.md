# Evidence Summary by area, and Numbers & Impact

Date: 2026-11-24

## Discussed

- The evidence Summary held three to six bullets, strongest first. Since the resume picks
  bullets from evidence anyway, the cap dropped work worth picking.
- `## Numbers` held only measured outcomes and scale. Impact without a figure (a leak closed, a
  feature delivered in a day, an R&D result adopted by a product) had no place, and impact
  figures such as bugs fixed were excluded as counts of own work.
- Whether a Claude-assessed impact (for example "delivered a rushed project") can sit beside
  facts without the facts being lost when the assessment is wrong.

## Decided

- The Summary groups bullets under areas of work that do not overlap, with no fixed count, each
  bullet starred by strength (★★★, ★★, ★). Bullet IDs `B1`, `B2`, … run across the whole file.
- `## Numbers` becomes `## Numbers & Impact`:
  - `### Numbers`: every figure once, with an ID (`N1`), a Kind (before → after, performance,
    accuracy, cost, scale, bugs / incidents, delivery speed, configured, estimated) and a scope.
    Bug and incident counts are allowed; commit, file and line counts stay out of bullets.
  - `### Impact`: one row per change the work made, with an ID (`I1`), a Kind (`fact`,
    `assessed`, `user`), a type, a basis, a confidence and a status. An `assessed` row rests on
    `fact` or Numbers rows by ID, so rejecting it leaves the facts in place. It reaches a resume
    bullet only after verify confirms it.
- Existing evidence files migrate the next time distill or verify runs on them.
- Changed together: `evidence.md`, the distill, verify, to-resume, steer and review-resume
  skills, the workflow and user-manual documents, and `wiki/me.md`.

## Open questions

- Whether to migrate all 22 existing evidence files in one pass rather than one by one.
