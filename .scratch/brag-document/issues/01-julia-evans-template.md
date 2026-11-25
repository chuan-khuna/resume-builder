# 01: Bring Julia Evans's brag-document template into to-brag

Status: resolved (2026-11-24: applied with the recommended defaults: block inside the brag document, verify questions added now)

Proposed 2026-11-24. Source: Julia Evans, "Get your work recognized: write a brag document"
(2019), saved as `wiki/raw/2026-11-24-brag-documents.md`.

## Her template against ours

| Her section | to-brag today | Proposal |
| ----------- | ------------- | -------- |
| Goals for this year | missing | **New: Goals.** User-owned, see "Where non-evidence content lives" |
| Goals for next year | missing | Part of Goals |
| Projects: your contribution and its impact | Themes + Timeline | Keep. Add one line per project line: "My part: …" from its role and Not mine |
| Collaboration & mentorship | partly in Beyond the code | **New section**, from evidence: Impact rows of type team enablement and knowledge transfer, plus `[me: …]` answers verify collects |
| Design & documentation | partly in Beyond the code | **New section**, from What I Did bullets about ADRs, design docs, specs, runbooks, docs |
| Company building | missing | **New section**, from evidence: internal tools, templates, supply-chain or process changes used beyond one project, plus `[me: …]` answers (interviewing, onboarding) |
| What you learned | Skills grown (tools only) | **Rename to What I learned**: skills (performance analysis, a new domain) from verify answers, then the tools table |
| Outside of work | missing | **New: Outside of work.** User-owned |
| General prompts | missing | Ask them in verify and in to-brag's interview step |
| Fill in results later | Not yet confirmed | Keep |
| Fuzzy work: goal → actions → effects | missing | Collaboration and Company building items use this shape when the evidence has it |

"Beyond the code" goes away: its five kinds move into Collaboration & mentorship, Design &
documentation, Company building, and a "Decisions and production support" list under Themes.

## Where non-evidence content lives

Goals and outside-of-work are about me, not about a project, so evidence has no place for them.

**Proposal:** a user-owned block in the brag document itself, between
`<!-- user:start -->` and `<!-- user:end -->` markers. to-brag asks for it on the first build,
and keeps it byte for byte on every rebuild. It holds Goals and Outside of work. Nothing in
it may back a resume claim.

Work facts stay in evidence: mentorship, interviewing or onboarding on a project go in through
verify as `[me: yyyy-mm-dd]` items, never into the user block.

## Changes, across the pipeline

- `to-brag` SKILL.md: new format and section sources; an interview step for the user block and
  the general prompts; the preserve-on-rebuild rule.
- `verify` SKILL.md: new questions per file: whom did you help or mentor, what did you write
  that others used, what did you learn, did anyone praise the work.
- `evidence.md`: no schema change; answers land as What I Did items or `user` Impact rows of
  type team enablement or knowledge transfer, as today.
- Docs: README, user manual and workflow doc sections for to-brag.
- `evidence/themather/brag-document.md`: rebuild; the user block starts empty until you answer.

## Decisions needed

1. Approve the section mapping above, or change it.
2. User-owned block inside the brag document, or a separate file (`evidence/<company>/brag-me.md`)?
3. Add the new verify questions now, or only when you next run verify?
