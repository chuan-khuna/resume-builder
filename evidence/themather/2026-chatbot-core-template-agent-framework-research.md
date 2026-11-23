---
id: chatbot-core-template-agent-framework-research
title: Standardised Chatbot Core Template — Agent-Framework Research & Prototype
company: themather
period: 2026-11 ~ 2026-11   # first to last commit: 2026-11-13 ~ 2026-11-20
role: AI engineer (sole author of the research and prototype repo)
status: wip   # research and prototype on an unmerged branch; design doc still in draft
verified:
  chatbot-template: 3a450e54828c09dc53215a302747f9d98d205d99   # tip of the unmerged prototype feature branch (main holds only the initial commit)
reviewed:
---

## Summary
### Resume bullets
- Prototyped a reusable Python chatbot core that each client installs as a version-pinned
  wheel, proving two mock clients (insurance, real estate) could add business tools without
  changing the core.
- Compared agent frameworks (Tau, Pydantic AI, LangGraph, a TypeScript option) and wrapped the
  chosen Tau agent loop behind one bridge module, enforced by import-linter contracts.
- Designed an extension standard (tools, skills, instructions, guardrails) and fail-closed
  message guardrails, used by a mock insurance client to block political and violent topics
  with a decision model.
- Built conversation persistence, streaming events, per-reply token usage and cost, an MCP
  server adapter, and a CLI and Streamlit app for developers to chat with each client's agent.
- Wrote the versioned developer docs site in Astro Starlight and drafted the design-doc
  response to the engineering brief, including the trade-offs the prototype exposed.
### Remarks
- B1: traces to the core package, mock clients and wheel registry bullets · the central result
  of the prototype · prototype only: upgrade across a minor version (0.1 → 0.2) was not tried,
  and the MVP features (chat channels, KB, inbox, audit trail, deploy) were not built; do not
  claim a delivered product · roles: AI infra, backend.
- B2: traces to the framework research and Tau bridge bullets · a reasoned framework choice
  with a written fallback plan (Pydantic AI spike) · the choice was a proposal, not signed off
  · roles: AI infra, backend.
- B3: traces to the extension standard and guardrail bullets · concrete safety pattern with
  audit data · the decision-model guardrail runs on a mock client only; no accuracy or
  block-rate figure · roles: AI infra, backend.
- B4: traces to the conversation, model layer, MCP and developer-tooling bullets · breadth ·
  developer tooling, not a Customer-facing app · roles: backend, AI infra.
- B5: traces to the docs-site and design-doc bullets · documentation and design writing ·
  the design doc was still in draft at the last commit · roles: AI infra, tech lead.
- `21 DX review findings (3 blocking)`: left out; a self-review of my own docs, so it counts
  my defects, not a result. Mention as "reviewed the developer docs from an agent developer's
  view and fixed the blocking issues", only if confirmed fixed.
- `1 business day per new client`: a target in the brief that the prototype did not test.
  Leave out.
- `5 s guardrail timeout`: configured value; B3 describes the guardrail without it.
- `2 mock clients in 2 business types`: prototype scope, quoted in B1 as "two mock clients".
- Scope caveat: all work lives on an unmerged feature branch; the Jira ticket was still
  In Progress. The brief asked each engineer to design and prototype a core, so this may be one
  of several parallel proposals: to confirm.

## Context
An internal research-and-design task: a standard template for client chatbots that the company
deploys once per client (one repository and one deployment per client, no multi-tenancy) for
mid-size to large Thai organisations whose customers ask repeat questions on LINE and Facebook.
A written engineering brief set the MVP (chat channels, an approved-documents knowledge base,
an operator inbox, an audit trail, lead capture, pre-deploy evaluation) and asked the team for a
design doc within two weeks. A shorter "minimal requirements" note then scoped the round to two
proof levels: (1) the core is one package that two clients install and configure, and (2) the
core has an extension standard that clients implement without changing the core. The brief
required the core to be new code, not copied from earlier client chatbots.
[chatbot-template:docs/<kb-vault> 100%] [TT-1723]

All of my work is on an unmerged feature branch (a second branch, for the knowledge-base
layout, is already contained in it); `main` holds only the initial project setup, so the work
reads as unshipped. The last design-doc progress note records that a lead asked for
documentation before more code, so coding stopped on 2026-11-19 and the design doc became the
focus. [chatbot-template:docs/<kb-vault> 100%]

Repository paths that contain the internal codename are written with placeholders
(`packages/<core>`, `docs/<kb-vault>`).

## What I Did
- **Researched agent frameworks for the core**: studied the layering of pi, its Python rewrite
  Tau, Flue and Hermes, the generic agent loop, and compared Tau, Pydantic AI,
  LangChain/LangGraph and a TypeScript option (Flue or pi). Proposed Python 3.14 + Tau, and on
  2026-11-20 re-reviewed Pydantic AI (semver policy, built-in model fallback, gated hooks) and
  proposed a spike behind the same bridge before the next minor release.
  [chatbot-template@327083f1b] [chatbot-template@399429e82] [chatbot-template@1481db5d3]
  [chatbot-template@2a35694c1] [chatbot-template@3a450e548] [chatbot-template:docs/<kb-vault> 100%]
- **Drafted a full tech stack for the core** (30 numbered decisions with draft answers to the
  brief's open questions, including RAG and KB indexing and vector-index options), each marked
  "proposed". [chatbot-template@465a9c64b] [chatbot-template@1637138d7] [chatbot-template@39ff4d9ef]
- **Built the core as an installable Python package** (versions 0.1.0 to 0.1.3, built as wheels
  into a local package index that each client project pins with uv). An earlier keyword-matching
  design without an LLM was dropped after one day and the package restarted at 0.1.0 on the new
  standard. [chatbot-template:packages/<core> 100%] [chatbot-template@a5d33345b]
  [chatbot-template@e0986d459] [chatbot-template@e421a184c]
- **Wrapped Tau's agent loop behind one bridge module**: the agent class drives Tau's agent
  harness, converts Tau messages and events to the core's own types (Reply, Item, events), and
  is the only module allowed to import Tau. import-linter contracts enforce this and a layered
  import order; Tau is pinned to one exact version because a patch release had added a breaking
  change. [chatbot-template@e0986d459] [chatbot-template@a28ecbed6] [chatbot-template@d7380cbc3]
  [chatbot-template:packages/<core> 100%]
- **Designed the extension standard**: an Extension is a named set of tools, skills,
  instructions and guardrails passed to the agent; tools are typed functions behind a `@tool`
  decorator, skills are `SKILL.md` files loaded from the package and fetched by the model with a
  `load_skill` tool, and the agent validates names and duplicates at construction. Built-in
  calculator and clock (time-zone aware) extensions.
  [chatbot-template@e4a72dc0e] [chatbot-template@a898d356a] [chatbot-template@c2d121161]
  [chatbot-template@1e1bd8b5a]
- **Added user-message and agent-message guardrails** as the first extension point: guardrails
  from the agent and from Extensions run concurrently per stage, an exception or timeout counts
  as a block (fail closed), and every check is saved in the reply with its verdict, duration
  and token usage for the audit trail and per-conversation cost.
  [chatbot-template@13a90be97] [chatbot-template@2000af7ee] [chatbot-template@aa647b059]
  [chatbot-template@f87e79216] [chatbot-template@db2a78e0e]
- **Built conversations as data**: streaming events, tool-call duration, thinking at three
  reasoning levels, per-reply usage and cost, replies serialised to versioned JSON and a saved
  conversation continued later, model timeouts and retries, and OpenRouter or any
  OpenAI-compatible endpoint as the provider.
  [chatbot-template@9ead2ecd5] [chatbot-template@73355bf7e] [chatbot-template@b99daa0cc]
  [chatbot-template@ebc2916ac] [chatbot-template@1b80eebc6] [chatbot-template@a5346e6b4]
  [chatbot-template@eab417b5d]
- **Added an MCP adapter** that turns the tools of one MCP server (stdio or HTTP) into an
  Extension, opening a fresh connection per tool call so the server can restart between calls.
  [chatbot-template@f644914f9]
- **Built two mock client projects on the package** to prove the two proof levels: a real-estate
  client (listing search tool, viewing-booking skill) and an insurance client (mock car and
  health insurance quote tools, a claim-guide skill, and a guardrail that asks a decision model
  through OpenRouter whether a message is about politics or violence and blocks it before the
  agent's model sees it). Each client is a separate project with one package per Extension,
  registered through a Python entry point, and adds its behaviour without changing the core.
  [chatbot-template@7049a84af] [chatbot-template@7b9747056] [chatbot-template@af5c8ef5d]
  [chatbot-template@ed3ceba19] [chatbot-template@ced4f2565] [chatbot-template:prototype 100%]
- **Built developer tooling**: a CLI that prints an agent's setup, answers one message or opens
  a chat; a scripted fake provider so client tests run without an API key; terminal UIs for the
  mock clients, later replaced by a Streamlit app that chats with each client's agent, shows
  guardrail blocks and saves conversations.
  [chatbot-template@9bbe2d231] [chatbot-template@dafe51505] [chatbot-template@31fcf7740]
  [chatbot-template@0051deb3f] [chatbot-template@4a9331d48]
- **Built the developer docs site in Astro Starlight**: API pages, guides (getting started,
  write a guardrail, connect an MCP server), internals showing how the core maps to Tau, a
  per-minor-version changelog, version archiving, and custom Markdown features (foldable trees,
  diagrams, glossary cards, status badges). Reviewed the docs from an agent developer's view
  and logged findings by severity.
  [chatbot-template@6a0a1b956] [chatbot-template@62971a15a] [chatbot-template@53aff64dc]
  [chatbot-template@2a6a65c4e] [chatbot-template@fc775a5d6] [chatbot-template@e88784335]
  [chatbot-template:docs/starlight 100%]
- **Drafted the design-doc response to the brief** in Thai for management readers: goals and
  constraints, architecture overview, extension points, deploy and ops, test and evaluation, a
  tech-stack summary, and the points where the prototype departs from the brief (channel
  adapters, KB, inbox and audit trail left to each client project for now).
  [chatbot-template@ad994de73] [chatbot-template@ae082edd8] [chatbot-template@83930e305]
  [chatbot-template@e0683cce7] [chatbot-template:docs/<kb-vault> 100%]
- **Researched Nix for per-client deploys** (uv2nix builds, encrypted secrets in a shared repo,
  image scanning); notes only. [chatbot-template@c4c310e19]

## Numbers
| Value | Scope | Source |
| ----- | ----- | ------ |
| 2 mock clients, 2 business types (insurance, real estate) | prototype scope set by the minimal requirements (configured) | [chatbot-template:prototype 100%] |
| 21 findings (3 blocking, 8 friction, 5 polish, 5 API changes) | my review of the developer docs site (measured, self-review) | [chatbot-template@e88784335] |
| 1 business day per new client | deploy target in the brief, not tested by the prototype | [chatbot-template:docs/<kb-vault> 100%] |
| 5 s | decision-model guardrail timeout (configured) | [chatbot-template@ed3ceba19] |

## Tools
tools: Python 3.14, uv (wheel builds, local package index), Tau (tau-ai, tau-agent), OpenRouter,
OpenAI-compatible APIs, MCP Python SDK, Pydantic, httpx, Rich, Streamlit, pytest,
pytest-asyncio, mypy (strict), import-linter, ruff, just, mise, Astro Starlight,
starlight-versions, bun, Obsidian (research vault), Claude Code
Studied, not used: Pydantic AI, LangChain/LangGraph, Flue, pi, Hermes, Nix (uv2nix, sops-nix,
agenix)

## Architecture
```mermaid
flowchart LR
  subgraph Client project, one per client
    A[agent.py: agent config] --> X[Client Extensions:<br/>tools, skills, guardrails]
  end
  R[(Local wheel index<br/>pinned core version)] -->|uv add| Core
  subgraph Core[Core package]
    AG[Agent + Conversation] --> G[Guardrail runner]
    AG --> E[Extension standard<br/>+ built-ins, MCP adapter]
    AG --> B[Bridge module]
  end
  A --> AG
  B --> T[Tau agent loop]
  T --> P[OpenRouter / OpenAI-compatible model]
  Dev[CLI / Streamlit app] --> AG
```
Each client project pins one core version from a local wheel index and defines its agent in code,
adding business tools, skills and guardrails as Extensions. The core runs user-message guardrails,
then the Tau agent loop through a single bridge module, then agent-message guardrails, and returns
a Reply that holds every item, tool call, guardrail check and its token usage.

## Not mine
- The engineering brief and the minimal-requirements note were written by others (the brief is
  addressed to the dev team); copied into the repo as sources. [chatbot-template:docs/<kb-vault> 100%]
- Vendored third-party agent skills under `.claude/skills` and `.agents/skills`, installed from
  public skill repos; committed by me but not written by me. [chatbot-template@bbc66d5fe]
  [chatbot-template@3e9da235f]
- Tau, the open-source agent library the core wraps.

## Open questions
- Was this one of several parallel core designs (the minimal requirements say each person designs
  a core), and was the proposal adopted, merged or presented?
- Does TT-1695 ("Research agent framework", 2026-11-04 to 2026-11-09, before the first commit)
  belong to this project, or to the earlier move of another client chatbot to Tau?
- The insurance mock client's guardrail uses a decision model: was its blocking tested beyond the
  unit tests with a fake model (any block-rate or false-block figure)?
- Was the 0.1 → 0.2 upgrade (proof level 1's last check) ever tried, and was the design doc
  finished and reviewed?
- Several records name an AI coding assistant as a co-writer: confirm which parts you wrote by
  hand versus directed, so B2–B5 use the right verbs.
- TODO lead "car-insurance quote skill (mock client)": confirmed in git as a mock car (and health)
  insurance quote tool in the insurance mock client, plus a claim-guide skill; it is in What I Did.
