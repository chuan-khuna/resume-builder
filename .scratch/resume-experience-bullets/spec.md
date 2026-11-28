# Proposal: The Mather experience bullets, scope + result

Status: done (superseded: the bullets in resume.yml at 9e8419c follow the scope-only format agreed later; kept as the record of the discussion)

Target: `resume/data/resume.yml`, entry `themather-datascientist`.

Format (agreed 2026-11-24): **label + at most 2 sentences**, 30 words or fewer with the label.

1. **Scope sentence**, present tense: the systems built and the tools, like the user's pasted
   set.
2. **Result sentence** (optional): one result that reads without context, past tense for
   finished work.

Every claim below was checked against the evidence files, not only the brag document. All 22
files are drafts (no `reviewed:`), so each trace comment gets `(draft)`.

Superseded: the first version of this spec (one incident per sentence, "depth over lists").

## Proposed bullets

Ordered by relevance to a data scientist / AI role. Word counts include the label.

### 1. Computer vision (29)

> Build vision pipelines for road safety, CCTV security, classroom attention, and retail
> shelves with YOLO and DINOv2. Traced a shelf-model plateau to the data by training two
> architectures.

- Scope: road-safety B1, cctv B1–B3, classroom B1, retail-shelf B1.
- Result: retail-shelf B5 (YOLO11m-AMF and RF-DETR-small reached the same per-class profile).
- "Build", not "co-develop": main developer or sole committer on all four.

### 2. LLM applications

**2a, scope + result (28)**

> Build a Qdrant RAG source and an evaluation runner for a client's support chatbot. Kept the
> new source off after it scored 56.8% recall@1 against 91.3%.

**2b, scope only, more breadth (24)**

> Build a Qdrant RAG source and an evaluation runner for a client's support chatbot, and
> compare GraphRAG, LightRAG, and LLM serving engines.

- Scope: hitl-chatbot B1 + B4; 2b adds graphrag B1 and llm-serving B4 (both `wip` research).
- Result: hitl-chatbot B2. The first sentence now names "the new source", so the number reads
  without a back story.
- Open: role on the chatbot is "one of four engineers (to confirm)"; the RAG source and the
  runner are yours in evidence.

### 3. Data science (28)

> Analyse customer data with Recency, Frequency, Monetary (RFM) segmentation, and Thai survey
> comments with n-grams, LDA, and LLMs. Estimated unique exhibition visitors by clustering face
> embeddings.

- Scope: line-crm B1, legacy-pos B2 (RFM); survey B1 + B3 (n-grams, LDA in a Streamlit
  comparison); classroom B3 and decision-model B4 (LLM spelling correction and sentiment).
- Result: event-booth B2 (Facenet512 embeddings, daily HDBSCAN clustering).
- Not used from your pasted set: "cohort analysis" (no evidence file holds it) and
  "association rule learning" (only in legacy-pos tickets; line-crm lists it as studied, not
  used).

### 4. Data engineering (29)

> Build Airflow pipelines that move energy telemetry, legacy point-of-sale data, and
> booth-camera events into TimescaleDB, PostgreSQL, and MongoDB. Traced lost data points to 9
> jobs starting in one minute.

- Scope: sensor-pipeline B1, legacy-pos B1, event-booth B1.
- Result: sensor-pipeline B3. It claims the cause, not that the stagger stopped the loss (not
  confirmed).
- Alternative result (27): "Synced the point-of-sale data with batch ELT after change data
  capture proved unworkable on MySQL 5.5." (legacy-pos B1). Pick whichever reads clearer to
  you.

### 5. Backend (27)

> Develop Django REST backends for a life-insurance CMS, a building-permit system, and dealer
> warranty tracking. Moved AI inference jobs to a Celery and Redis queue so they survive
> restarts.

- Scope: life-insurance-cms B1, municipal-permit B1, truck-warranty B1.
- "Develop", not "Build": the CMS and the permit system were shared (one of three or four
  backend developers).
- Result: retail-shelf B2.
- Not used from your pasted set: "Build and maintain a Django starter template". Evidence says
  projects started *from* the company's starter template, not that you built it. If you did,
  it needs an evidence entry first.

### 6. Deployment, optional (16)

> Deploy services with Docker Compose, Podman, and Cloudflare Tunnel, and automate
> deployments with Bitbucket Pipelines.

- Evidence: Docker Compose in truck-warranty B5 and legacy-pos B5; Podman and Cloudflare
  Tunnel in a cctv Remark ("on-premises deployment … fits as a sub-clause of B1"); Bitbucket
  Pipelines in legacy-pos B5 (self-hosted CI deploy for the admin frontend).
- Not used from your pasted set: "Nginx on AWS and DigitalOcean". No file names DigitalOcean,
  and the Nginx in the company site was deployed by teammates.
- Leave it out if the page is tight. Five labels already cover the role.

## Skill change (needs approval)

The new format conflicts with two rules in `.claude-dev/skills/resume-auto-mode/playbooks/resume.md`. `to-resume`
and `steer` point to the `resume` skill's rules and restate none of them, so this one file is
the whole change.

1. **One result per bullet** (Content). Add: "A labelled bullet may open with a scope
   sentence (the systems built and their tools) before its result, or hold the scope alone."
2. **Labels** (Content). Add a sub-bullet: "A labelled bullet holds at most two sentences: the
   scope sentence first, then at most one result that reads without context. Keep a result
   that needs a back story, such as the cause of a production incident, for an interview
   story."
3. **Tense** (Person and tense). Change "keep one tense within a bullet" to "keep one tense
   within a sentence: in a labelled bullet, the scope sentence is present tense and a finished
   result is past tense".

## Questions outside the bullets

1. **Job title.** The entry says "Data Scientist"; the evidence records "data and backend
   developer" (2023–2024) and "AI and backend engineer" (2025–2026). Which is yours on paper?
2. **Start date.** The entry starts Jul 2022; the earliest evidence is 2023-02. Keep Jul 2022
   if it is your real start date.
3. **Skills.** Refresh the skills list from the brag document's tools table too?
