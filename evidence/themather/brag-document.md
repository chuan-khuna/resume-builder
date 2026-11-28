---
company: themather
period: 2023-02 ~ 2026-11            # earliest to latest evidence period
role: data and backend developer (2023–2024) → AI and backend engineer (2025–2026)
built_from: 22 evidence files (0 reviewed)
updated: 2026-11-24
---

# Brag document: themather

> Built from `evidence/themather/*.md` by `/resume-builder:resume-auto-mode to-brag`, after Julia Evans's
> brag-document template. Do not edit by hand, except inside the `user:` blocks: change the
> evidence and rebuild. Draft: 22 of 22 evidence files are not yet verified, so
> every line below is a draft claim. The files use the older evidence format, with no
> strength stars, no Impact table and no `Learned:` lines: bullets keep each file's own order.

## At a glance

I worked on 22 client and internal projects between 2023 and 2026, at a Thai software
consultancy. I started on Django backends and data analytics, then moved to computer vision,
data pipelines and, in 2026, LLM applications and AI infrastructure. My strongest work is a
retail-shelf analytics platform I designed and built alone, which a client trialled in
2026-09. I also measured a vision decision model at 89% top-1 accuracy on 739 labelled shelf
crops. On a support chatbot, I measured a new retrieval source against the old one and kept it
switched off when it scored 56.8% recall@1 against 91.3%.

<!-- user:goals:start -->
## Goals

### This year

- Not written yet: run `/resume-builder:resume-auto-mode to-brag themather` and answer, or write your goals
  here in your own words.

### Next year

- Not written yet.
<!-- user:goals:end -->

## Projects by theme

### Computer vision and video analytics (2023 → 2026)

The work grew from a face-analytics demo for a marketing event (2023) to face-embedding visitor
counts from 13 cameras at a motor-show booth (2024), then road-safety and CCTV detection services (2025). In 2026 it
became a shelf-analytics platform in client trial, a classroom attention pipeline run on real
recordings, and an evaluation of hosted vision decision models.

**Retail shelf analytics platform** · 2026-03 ~ 2026-11 · shipped, client trial ·
[retail-shelf](2026-retail-shelf-computer-vision-analytics-platform.md)
My part: sole committer, from design to deployment. The frontend started from an open-source admin template, and the training labels came from a public dataset.
- Designed and built a multi-tenant shelf-photo analytics platform end to end: one-pass YOLO
  product/logo/empty detection and DINOv2 brand matching on Modal serverless GPUs, Django REST
  API, and Next.js dashboards. (B1)
- Diagnosed a detection accuracy plateau by training YOLO11m-AMF and RF-DETR-small: both reached
  the same per-class profile (logo AP50 0.54 against product 0.92), tracing the limit to the
  data. (B5)
- Built a benchmark system that imports labelled YOLO datasets, runs the production pipeline
  over them, and scores detection and brand recognition separately, with confusion matrices.
  (B4)
- Integrated a hosted vision decision model as a second brand recognizer beside logo matching,
  with additive storage, a read-time brand-source switch for charts and exports, and
  fingerprinted re-runs that skip unchanged crops. (B6: unmerged branch, write "integrated" or
  "prototyped")

**Decision-model R&D** · 2026-09 ~ 2026-11 · wip ·
[decision-model](2026-decision-model-rd-reapplying-past-projects.md)
- Evaluated a vision decision model for retail-shelf brand recognition on 739 labelled product
  crops in 6 categories, reaching 89% top-1 accuracy, with per-brand precision, recall, F1 and
  confusion matrices. (B1, N1)
- Compared two vision decision models on the same labelled images: both matched all 44 images
  against a 200-brand choice set, and the second cost about one-ninth as much per image. (B2)
- Built an image send policy for a vision model API (resize, JPEG-quality steps, budget halving
  on 413 retries) and fingerprinted prediction stores, so evaluations re-ran only changed
  images. (B3)

**Classroom video attention analysis** · 2026-02 ~ 2026-06 · shipped ·
[classroom](2026-classroom-video-attention-and-survey-analysis-system.md)
My part: main developer of both repos. A teammate wrote the recorder's Windows build script and some of its styling.
- Built a RabbitMQ worker pipeline that scored student attention in ~930 webcam recordings
  (~64 h) from 2 schools, using MediaPipe face landmarks for gaze, blinks, head pose and
  emotion. (B1)
- Built a PyQt6 desktop recorder that plays lesson videos while recording the student's webcam,
  logs playback events to JSON, and switches between Qt and VLC playback backends. (B4)

**CCTV people and security analytics** · 2025-11 ~ 2026-03 · shipped ·
[cctv](2025-realtime-cctv-people-and-security-analytics-platform.md)
My part: main developer of the backend and the AI service. Teammates built the QR scanner bridge, gate control, the later third-party integration and the frontends.
- Built face-recognition check-in: InsightFace embeddings of registered visitors stored in
  pgvector and matched by cosine distance against Hikvision camera webhooks, limited to the
  appointment day. (B2)
- Built a multi-camera RTSP detection service with YOLO and ByteTrack that reports weapon,
  violence and fall events only after an object stays tracked across consecutive frames,
  attaching face embeddings for later search. (B3)

**Road-safety video analytics** · 2025-05 ~ 2026-01 · wip, demo stage ·
[road-safety](2025-ai-road-safety-video-analytics-platform.md)
My part: main developer across most of the system. The backend's first commit came from a company starter template.
- Designed and built a demo-stage road-safety video analytics system on footage from 3 roadside
  camera sites: queued detection workers, TimescaleDB time-series storage and a Django REST
  dashboard API. (B1)
- Trained an RF-DETR accident-detection model to replace a YOLO model with frequent false
  positives, and built a lane-straddling detector from per-lane polygon zones and per-track
  dwell timers. (B3)
- Wrote an internal Python detection library (composable processing chains, YOLO/RF-DETR behind
  one interface, ByteTrack tracking, plate OCR), versioned by git tag, ending copy-paste between
  PoC and production code. (B4)
- Built LINE and Discord accident alerts with duplicate suppression, replacing pgvector
  embedding-similarity checks with tracker-ID, site and time-window deduplication. (B5)

**Exhibition booth visitor analytics** · 2024-11 ~ 2025-02 · shipped ·
[event-booth](2024-event-booth-visitor-cv-analytics.md)
- Designed a unique-visitor estimate from face embeddings: Facenet512 vectors via DeepFace,
  daily HDBSCAN clustering on cosine distance, and rules that drop staff, screen images, noise
  and oversized clusters. (B2)
- Built repeat-visitor search over ChromaDB: each face cluster's average embedding queries
  similar clusters from other days, giving a per-visitor visit frequency and dwell time. (B3)

**Crowd and face-analytics camera PoC** · 2023-04 ~ 2024-07 · wip, event demos ·
[crowd-poc](2023-realtime-crowd-analytics-camera-poc.md)
My part: main developer and nearly sole author of the five repos. A teammate wrote the age, gender and emotion model wrappers.
- Built a real-time audience-analytics demo for a marketing event: Kafka topics carried face
  results, a pandas analyser aggregated age, gender and emotion, and Flask-SocketIO pushed them
  to a Next.js dashboard. (B1)
- Prototyped camera-frame streaming through Kafka to a face-analysis worker running MediaPipe
  detection and ONNX age, gender and emotion models, switching frames from PNG to JPEG for
  about 10x smaller messages. (B2, N1)
- Prototyped short-term visitor re-identification with face embeddings in Weaviate and per-face
  attribute counts in PyFlink tumbling windows, giving one age, gender and emotion label per
  visitor on the dashboard. (B3)
- Prototyped crowd heatmaps from person detections, accumulated as bounding-box masks over the
  video and a top-view, batched per minute in PyFlink and replayed on a React dashboard. (B4)
- Built a crowd-flow visualisation prototype with YOLOv8 and supervision: tracked-people
  heatmaps, per-zone activity over time, and zone-to-zone Sankey charts in a Streamlit video
  replay app. (B5)

### LLM applications and AI infrastructure (2026)

In 2026 the work moved to LLM systems: a support chatbot's retrieval and evaluation, a
comparison of three RAG strategies, a serving-engine evaluation, decision-model prototypes and a
reusable chatbot core. Most of it is research or prototype work, and the bullets say so.

**Human-in-the-loop support chatbot** · 2026-09 ~ 2026-11 · wip ·
[hitl-chatbot](2026-hitl-customer-support-chatbot-rag.md)
My part: one of four engineers; I joined a running proof of concept in 2026-09. Teammates built the webhook core, most dashboard pages and the intent router.
- Evaluated the new retrieval against the existing knowledge base on the client's test
  questions before switching (recall@1 56.8% vs 91.3%) and kept it behind a default-off switch
  with one-variable rollback. (B2)
- Built a second RAG knowledge source for a human-in-the-loop support chatbot: operator
  text/PDF upload, a background indexer chunking and embedding into Qdrant, live SSE progress,
  and generation-safe re-indexing. (B1)
- Built chatbot evaluation tooling: a runner executing the client's 633-case multi-turn test set
  with concurrency and resume, and a React/TypeScript app comparing runs and grading answers.
  (B4)
- Prototyped an agent answer engine (tool loop over the existing rate, branch and knowledge
  resolvers) beside the fixed chain, keeping must-not-fail rules in code: step cap, admin
  handoff on failure, reply guardrails. (B3)

**Parallel LLM serving evaluation** · 2026-10 · wip, one-day spike ·
[llm-serving](2026-parallel-llm-serving-engine-evaluation.md)
My part: sole author of a one-day spike.
- Built a concurrent streaming load tester for OpenAI-compatible LLM servers (Python asyncio +
  httpx) reporting per-request TTFT and throughput; it showed Ollama serving 4 concurrent
  requests one at a time (TTFT 0.1 → 4.4 s). (B1)
- Root-caused Ollama's failure to parallelise Qwen 3.5: its scheduler pins hybrid-architecture
  models to a single slot, traced to an unfixed upstream llama.cpp recurrent-state issue, plus a
  desktop-app setting forcing one parallel slot. (B2)
- Designed a continuous-batching test (long request at 0 s, short at 5 s) that separates
  continuous from static batching; on vLLM the late request got its first token 0.4 s after
  send. (B3)
- Evaluated vLLM, SGLang, llama.cpp and Ollama against six serving requirements for a 5–10
  concurrent-request target, recommending vLLM for the GPU server and advising against MTP
  speculative decoding at that load. (B4)

**RAG strategy comparison: Simple RAG, GraphRAG, LightRAG** · 2026-10 · wip ·
[graphrag](2026-graphrag-lightrag-rag-strategy-comparison.md)
My part: sole developer, working with an AI coding agent.
- Built a research prototype that compares Simple RAG, GraphRAG and LightRAG side by side over
  one Neo4j-backed corpus, holding chunks, embeddings, LLMs, prompt and an 8k-token context
  budget constant. (B1)
- Implemented GraphRAG from its paper without the official library: LLM entity extraction with
  gleaning, hierarchical Leiden communities, community reports, and local and map-reduce global
  query modes. (B2)
- Implemented LightRAG's dual-level retrieval: question keyword extraction, entity- and
  relationship-level vector search in Neo4j, and local, global and hybrid query modes fitted to
  a shared token budget. (B3)
- Built an indexing pipeline with a disk cache of LLM calls keyed by model and prompt, 1–8
  worker threads, live progress, and per-call token and cost tracking in SQLite. (B4)
- Built a FastAPI and Next.js comparison UI that streams three answers in parallel over
  Server-Sent Events, with each strategy's retrieved context, a knowledge-graph browser and a
  scored question history. (B5)
- Analysed indexing at 100k-chunk scale, estimating about $255 of GraphRAG extraction cost, and
  proposed range indexes, windowed embedding writes and a streaming merge. (B6: estimated and
  proposed, not built)

**Chatbot core template** · 2026-11 · wip ·
[chatbot-core](2026-chatbot-core-template-agent-framework-research.md)
My part: sole author of the research and the prototype. The engineering brief was written by others.
- Prototyped a reusable Python chatbot core that each client installs as a version-pinned
  wheel, proving two mock clients (insurance, real estate) could add business tools without
  changing the core. (B1)
- Compared agent frameworks (Tau, Pydantic AI, LangGraph, a TypeScript option) and wrapped the
  chosen Tau agent loop behind one bridge module, enforced by import-linter contracts. (B2)
- Designed an extension standard (tools, skills, instructions, guardrails) and fail-closed
  message guardrails, used by a mock insurance client to block political and violent topics
  with a decision model. (B3)
- Built conversation persistence, streaming events, per-reply token usage and cost, an MCP
  server adapter, and a CLI and Streamlit app for developers to chat with each client's agent.
  (B4)
- Wrote the versioned developer docs site in Astro Starlight and drafted the design-doc
  response to the engineering brief, including the trade-offs the prototype exposed. (B5)

**Decision-model R&D** · [decision-model](2026-decision-model-rd-reapplying-past-projects.md)
My part: sole developer of the repo. The decision and chat models are third-party hosted models.
- Prototyped a task-delegation tool: a decision model picks owner, type and severity, code
  checks capacity caps against live Jira load, and a chat model streams the reasoning. (B5)
- Prototyped a support-chatbot intent router on a decision model (15 intents plus handoff and
  notify probabilities), matching the expected action on 42 of 43 labelled messages. (B6: the
  router was tuned on the same messages, so this is not held-out accuracy)

### Data pipelines and analytics (2023 → 2026)

This theme runs through the whole period: customer segmentation for loyalty and point-of-sale
clients, Airflow pipelines for exhibition, retail and energy data, and time-series storage for
detection and sensor results.

**Sensor telemetry aggregation pipeline** · 2025-08 ~ 2026-07 · shipped ·
[sensor-pipeline](2025-time-series-sensor-data-aggregation-pipeline.md)
My part: sole developer of the pipeline. The InfluxDB ingestion and the dashboard sit outside it.
- Built an Apache Airflow pipeline that aggregates raw InfluxDB energy telemetry (solar, grid,
  time-of-use, voltage, current, power) into 15-minute, hourly and daily TimescaleDB tables, in
  production since 2025-09. (B1)
- Traced intermittent production task failures and lost top-of-hour points (13 of 24 on one
  day) to 9 DAGs firing in the same minute on a 2-vCPU host, then staggered the schedules. (B3)
- Found a 1.84 GB Airflow XCom table caused by tasks returning whole DataFrames, and changed the
  final task to return a row count; merged batched `ON CONFLICT` upserts after verifying 0
  duplicates. (B4)
- Investigated a solar feed silent for about six months, using per-day row counts to show all 4
  inverters stopped within minutes, pointing to a site gateway fault rather than the pipeline.
  (B5)
- Designed a thin-DAG pattern: each metric shares one Flux query, transform and upsert module
  across its resolutions, with local-time (UTC+7) windows and a 5-minute ingestion-delay offset.
  (B2)
- Added Discord failure alerts, a weekly heartbeat DAG and 30-day log cleanup, and fixed a
  heartbeat task that sent duplicate messages and false failure alerts. (B6)

**Legacy point-of-sale sync and membership analytics** · 2024-08 ~ 2025-02 · shipped ·
[legacy-pos](2024-legacy-pos-cdc-sync-and-membership-analytics-dashboard.md)
My part: data sync, analytics pipelines and dashboard APIs. A teammate built the member app and the first Debezium setup.
- Built Airflow ELT that copies 7 sales and payment tables daily from a legacy MySQL 5.5
  point-of-sale database into PostgreSQL, after Debezium change data capture proved unworkable
  on the old MySQL version. (B1)
- Built an Airflow Recency, Frequency, Monetary (RFM) segmentation pipeline that identifies
  customers by payment card, scores them into quantile segments every 12 hours and stores the
  cut-offs for the dashboard. (B2)
- Moved a slow top-products dashboard query into a 12-hourly Airflow pre-aggregation table with
  indexes, serving daily or monthly rankings by product group and by delivery or dine-in sales.
  (B3)
- Built Django REST dashboard APIs for revenue by payment type and bank, average customers per
  bill and spend per customer, with gap-filled daily and monthly time series. (B4)

**Exhibition booth visitor analytics** · [event-booth](2024-event-booth-visitor-cv-analytics.md)
My part: main developer of the ETL pipeline and the dashboard API. Teammates built most of the dashboard frontend.
- Built an Apache Airflow ETL pipeline that turned IP camera face-capture events from 12 booth
  camera zones into hourly visitor-count and age/gender aggregates for an exhibition analytics
  dashboard. (B1; Numbers: 13 cameras at the booth, the 12 zones plus 1 wide-angle,
  user-reported)
- Precomputed dashboard data as Airflow cache collections, so API requests read daily and
  per-cluster summaries instead of recomputing clusters. (B5)

**LINE loyalty platform: RFM segmentation** · 2023-02 ~ 2023-05 · shipped ·
[line-crm](2023-line-crm-loyalty-rfm-segmentation.md)
My part: owner of the analytics and segmentation module in a team project. Teammates built the member app, receipts, points and the React app shell.
- Built an RFM customer-segmentation module for a LINE loyalty platform: quintile scoring of
  approved receipts, 125 score codes mapped to 11 segments, and spend-based tiers, run as a
  scheduled Celery task. (B1)
- Built Django REST analytics APIs in pandas for the admin dashboard: revenue time series by
  shop type, member demographics, RFM value distributions per segment, and member and revenue
  totals by province. (B2)
- Built the admin analytics dashboard in React with Nivo and Leaflet: daily and monthly revenue
  lines, gender-age and RFM segment bar charts, spend and frequency histograms, and a province
  map. (B3)

**Time-series storage for detection and counting**
- Modelled detections as TimescaleDB hypertables with continuous aggregates serving dashboard
  summaries, removing the need for a separate Airflow aggregation pipeline.
  ([road-safety](2025-ai-road-safety-video-analytics-platform.md) B6)
- Built people counting per camera zone into a TimescaleDB hypertable with minute, hourly and
  daily continuous aggregates, serving time-slot heat-map APIs to the dashboard.
  ([cctv](2025-realtime-cctv-people-and-security-analytics-platform.md) B4)

**Other analytics and data collection**
- Aggregated per-video attention and comment sentiment by school, grade, subject and lesson into
  report tables, and wrote Thai runbooks from raw recordings to results.
  ([classroom](2026-classroom-video-attention-and-survey-analysis-system.md) B5)
- Audited the client's rate database read-only before building on it, found three client bugs
  and data contradicting the client's own answers, and limited the source to rate numbers.
  ([hitl-chatbot](2026-hitl-customer-support-chatbot-rag.md) B6)
- Built Django REST dashboard aggregations of permit requests by type, status, month, building
  type and staff position, tested on generated mock requests.
  ([municipal-permit](2024-municipal-building-permit-pdf-and-approval-backend.md) B4)
- Built an internal forum-scraping service: a Django REST API queues keyword jobs on RabbitMQ, a
  multi-process worker collects topics and comments, and MongoDB stores the raw results.
  ([forum-scraper](2023-internal-social-forum-scraping-pipeline.md) B1, wip)
- Rewrote an ad hoc forum scraper as a functional-style Python library, chaining requests and
  parsing through Either monads so failed pages return errors as values instead of stopping a
  scrape. ([forum-scraper](2023-internal-social-forum-scraping-pipeline.md) B2)
- Split each scrape result across paged MongoDB documents to stay under the document size limit,
  merging the pages back when a user reads the result.
  ([forum-scraper](2023-internal-social-forum-scraping-pipeline.md) B5)
- Extracted survey responses from SQL Server with pandas and pivoted them into a
  responder-by-question table for analysing scale and demographic answers.
  ([survey](2023-survey-engagement-text-analytics.md) B4)

### Backend systems (2023 → 2026)

Django REST backends run through every year: content management systems, a permit system and
a warranty tracker in 2023–2024, then the queues, workers and event streams behind the AI
systems in 2025–2026.

**Life-insurance website CMS backend** · 2023-08 ~ 2026-05 · shipped, still in use ·
[life-insurance-cms](2023-life-insurance-website-cms-backend.md)
My part: one of three to four backend developers, and the largest committer in the build phase. Teammates built the LDAP login and most product modules.
- Built the content APIs of a life-insurance company's corporate website CMS in Django REST
  Framework: news, articles, careers, investor reports and policy pages, each with admin CRUD
  and public read endpoints. (B1)
- Designed the CMS's role-based access control: per-controller none/read/write permissions
  checked by a DRF permission class from the JWT session, per-request access logs and
  role-filtered admin navigation. (B2)
- Built reusable base models and viewsets for drag-and-drop ordering, soft delete with restore
  and static pages, shared by the content modules of the CMS. (B3)
- Added editor workflows: expiring JWT preview links for unpublished content, product drafts
  with history, and a rich-text image upload API with HTML sanitising against script injection.
  (B4)
- Diagnosed a production LDAP login failure for new staff accounts with reproduction scripts,
  fixed an over-strict Active Directory filter that returned HTTP 500, and recorded the
  decision. (B5)
- Wrote the code tests first with pytest and shared base test classes, and wrote the seed
  scripts that loaded content, roles and permissions for UAT and production. (B6)

**Municipal building-permit backend** · 2024-02 ~ 2024-04 · shipped ·
[municipal-permit](2024-municipal-building-permit-pdf-and-approval-backend.md)
My part: one of three backend developers; I owned PDF generation, authentication and logging, and the dashboard API. Teammates wrote most form models and later form templates.
- Built the PDF generation service for a municipal building-permit system in Django and
  WeasyPrint: HTML components render Thai official forms, merge officer review pages and ship
  attachments as a zip. (B1)
- Designed the authentication and audit layer: bearer-token sessions with a logout token
  blacklist, first-login password reset tokens, superadmin-only permission management and a
  filterable access log. (B2)
- Profiled a slow member-forms API with cProfile and PyInstrument and rewrote its per-row
  fetch-and-save loop as filtered querysets that skip drafts and already-expired requests. (B3)
- Built a single create-and-update API for permit requests that saves nested addresses,
  buildings, engineers, architects and multi-file attachments in one call. (B5)
- Added Prometheus metrics and a Grafana service to the Docker Compose stack, and replaced print
  debugging with a central logging configuration. (B6)

**Truck dealer warranty backend and website CMS** · 2024-04 ~ 2024-10 · shipped ·
[truck-warranty](2024-truck-dealer-website-cms-and-warranty-tracking-backend.md)
My part: main developer of the warranty backend and a contributor to the website CMS. Teammates built the website's other apps and the warranty notifications.
- Built a Django REST backend for truck dealers to track vehicle warranties and maintenance,
  auto-scheduling service visits and coupons per vehicle from per-model configuration when a
  sale is recorded. (B1)
- Designed the warranty data model: per-model maintenance periods, items and coupons, with JSON
  snapshots on each vehicle's history so later configuration edits leave existing schedules
  unchanged. (B2)
- Built authentication for four account types (admin, dealer, sales, customer) on shared base
  classes and mixins, with a per-controller read/write permission model seeded from scripts.
  (B3: the checks were later switched off by a teammate, so do not claim they were enforced)
- Built the product-specification CMS for a truck brand's website: ordered spec and summary
  templates per powertrain (diesel or electric), a backfill API and a side-by-side
  model-comparison API. (B4)
- Loaded the client's production catalogue (15 truck variants, their warranty coupons and
  service schedules) from spreadsheets with seed scripts, and configured the Docker Compose
  production deployment. (B5)

**Voice and video media-merge service** · 2025-07 ~ 2025-09 · shipped ·
[media-merge](2025-voice-video-media-merge-service.md)
My part: main developer of the worker; the API was built with three teammates. A teammate set up the NVIDIA runtime and the first GPU re-render.
- Built a RabbitMQ-driven ffmpeg worker that turns a chatbot session into a personalised video:
  text-to-speech greeting, preset clips with transitions, and a 9:16 version with Thai text
  overlays. (B1)
- Replaced MoviePy with ffmpeg and added encoder auto-selection (NVIDIA NVENC, Apple
  VideoToolbox, others) with per-call CPU fallback, so one worker runs on a Mac or an NVIDIA
  server. (B2)
- Fixed duplicate processing across parallel GPU workers with an atomic Postgres task claim,
  database-tracked retries with requeue, and per-worker temp directories. (B3)
- Designed preset-video selection from three chatbot answers, then made it prefer the preset the
  chatbot sends and report the preset used, fixing mismatched video covers. (B4)
- Wrote the worker's error-handling layer as an Either-monad pipeline with retry decorators and
  Discord failure alerts, so failed sessions surface with their error message. (B5)

**Queues, workers and event streams behind the AI systems**
- Replaced in-process daemon-thread dispatch with a Celery + Redis job queue (chunked chord
  tasks, idempotent retries, row locks, stale-job reaper), so inference jobs survive restarts
  and out-of-memory kills.
  ([retail-shelf](2026-retail-shelf-computer-vision-analytics-platform.md) B2)
- Moved server-sent progress events to a Redis pub/sub broker with per-user channels, fixing
  lost events across 5 web workers and closing a cross-tenant event leak.
  ([retail-shelf](2026-retail-shelf-computer-vision-analytics-platform.md) B3)
- Migrated the pipeline from Kafka frame streaming to a RabbitMQ task queue when requirements
  moved to upload-then-process, adding manual ack, heartbeats for multi-minute jobs and task
  progress tracking. ([road-safety](2025-ai-road-safety-video-analytics-platform.md) B2)
- Wrote a reusable long-running RabbitMQ task worker with a heartbeat thread, manual ack/nack and
  PostgreSQL task-status and progress tracking, so multi-minute video jobs ran on parallel
  workers. ([classroom](2026-classroom-video-attention-and-survey-analysis-system.md) B2)
- Moved the Django backend from WSGI to ASGI (gunicorn + uvicorn workers), chosen over a
  threaded WSGI server because long-lived SSE connections would exhaust its thread pool.
  ([hitl-chatbot](2026-hitl-customer-support-chatbot-rag.md) B5)

**Other backend work**
- Built the Django REST and TimescaleDB backend of an on-premises CCTV visitor and security
  platform: visitor check-in and check-out, anomaly events, zone counts, dashboard APIs and
  WebSocket live feeds. ([cctv](2025-realtime-cctv-people-and-security-analytics-platform.md) B1)
- Built a stand-in registration API for a third-party visitor system so the check-in flow could
  be tested end to end, with face embeddings generated on save and old photos purged by date.
  ([cctv](2025-realtime-cctv-people-and-security-analytics-platform.md) B5)
- Developed the Django REST dashboard API over MongoDB: visitor, demographic, wide-angle camera
  and cluster endpoints with filters, pagination, Swagger docs and Excel export.
  ([event-booth](2024-event-booth-visitor-cv-analytics.md) B4)
- Deployed the backend with Docker Compose on the client's server and added a self-hosted CI
  deploy pipeline for the admin frontend.
  ([legacy-pos](2024-legacy-pos-cdc-sync-and-membership-analytics-dashboard.md) B5)
- Added date-range CSV exports of members, receipts and shipping addresses for the admin team,
  and a public shop-ranking API that ranks onsite shops by approved revenue.
  ([line-crm](2023-line-crm-loyalty-rfm-segmentation.md) B4)
- Built a dev-only data-seeding app that loads mock members, receipts and the client's shop list
  through SQL migrations, and wrote Django tests for the analytics and member APIs.
  ([line-crm](2023-line-crm-loyalty-rfm-segmentation.md) B5)
- Added per-user accounts and usage tracking: JWT bearer sessions, argon2 password hashing,
  password-reset tokens, and scrape, credit and top-up logs that admins manage.
  ([forum-scraper](2023-internal-social-forum-scraping-pipeline.md) B4)

### Thai text analytics (2023 → 2026)

Thai free-text analysis recurs across survey and forum projects: dictionary-based tokenising and
n-gram word clouds from 2023, then local LLMs and hosted decision models for spelling correction
and sentiment.

**Employee survey text analytics** · 2023-05 ~ 2025-05 · shipped ·
[survey](2023-survey-engagement-text-analytics.md)
My part: the survey's free-text analytics, one of several developers on the report backend. Teammates built the report calculations, PDF export and deployment.
- Built the Thai free-text word-cloud engine for an employee-survey reporting backend:
  PyThaiNLP tokenising with a custom dictionary, gensim phrase detection for bigrams and
  trigrams, and stopword filtering. (B1)
- Extended survey word clouds to per-topic views: per-survey topic keywords, stopwords and
  custom terms stored in MongoDB, comments filtered by keyword group, and a keyword-search API
  for the matching comments. (B2)
- Prototyped a Streamlit app comparing four ways to group 500+ open-ended survey comments by
  topic: tunable n-gram word clouds, LDA, thai2fit embedding similarity and local-LLM scoring.
  (B3)

**Other Thai text work**
- Built a Thai survey-comment pipeline: LLM spelling correction and sentiment classification on
  a local Typhoon2 8B model, then PyThaiNLP and gensim n-gram wordclouds and keyword rankings.
  ([classroom](2026-classroom-video-attention-and-survey-analysis-system.md) B3)
- Rebuilt a Streamlit sentiment prototype as a FastAPI and Next.js app classifying Thai
  employee-survey comments with one decision-model call per comment, streamed to the browser as
  NDJSON. ([decision-model](2026-decision-model-rd-reapplying-past-projects.md) B4)
- Built a Streamlit front end to submit scrape jobs and turn results into Thai n-gram word
  clouds, using PyThaiNLP tokenisation with user keywords and gensim phrase detection.
  ([forum-scraper](2023-internal-social-forum-scraping-pipeline.md) B3)

### Websites and frontend (2026)

Two pieces of website work in 2026, both built with Claude Code: a rebuild of the company's
marketing site, and an upgrade of the live corporate site with new product pages.

**Corporate marketing website rebuild** · 2026-05 ~ 2026-06 · wip, not live ·
[marketing-site](2026-corporate-marketing-website-astro.md)
My part: sole developer, building with Claude Code. Site copy and client logos came from the live site.
- Rebuilt the company's marketing website in Astro, Tailwind and React islands, moving every
  page section into schema-validated content collections and adding careers, blog, projects and
  announcement pages. (B1)
- Built a scroll-driven company-profile page as a React slide deck: a custom wheel and touch
  hook drives per-scene animation progress, overscroll changes scene, and scenes load lazily.
  (B2)
- Designed a print-first 16:9 credential deck on a 12-column, 8 px baseline grid, with a
  print-to-PDF page rule, auto-paginated client slides and a live presenter mode. (B3)
- Set up an AI-assisted content workflow: a Claude Code content skill, per-collection authoring
  guides and two project agents, with a rule that schema changes update the guides. (B4)
- Built a theme system of 8 CSS colour presets with a switcher, applied before first paint to
  prevent a theme flash, and configured Cloudflare Workers deployment. (B5)

**Live corporate website upgrade and product pages** · 2026-11 · shipped ·
[website-upgrade](2026-corporate-website-astro-upgrade-and-product-pages.md)
My part: about 10% of a team-owned site's commits: the upgrade, the product pages and the docs. Teammates built the site, its CMS integration and its deployment.
- Upgraded the company's live website from Astro 5 to Astro 7 and Tailwind 3 to 4, removing
  unused dependencies and checking page layouts against the old build on desktop and mobile.
  (B1)
- Built a Products navigation menu and a bilingual product page for the company's AI
  video-analytics product, with keyboard-accessible dropdowns, a mobile accordion, light and
  dark themes and a datasheet download. (B2)
- Added a 7-day minimum release age to the npm and Bun configs and regenerated the lockfiles
  under it, so newly published, possibly compromised packages are not installed. (B3)
- Centralised site-wide settings in one typed config and added a switchable mourning mode, with
  the greyscale filter on the root element so fixed elements stay in place. (B4)
- Wrote onboarding, project-structure and styling docs and Thai content-update guides for the
  team site, and specified the product menu as tickets before building it. (B5)

### Decisions and production support

Pointers to bullets above where the result was a decision, a fix in production or a security
gain.

- **Decisions backed by measurement**: kept a weaker retrieval source switched off
  ([hitl-chatbot](2026-hitl-customer-support-chatbot-rag.md) B2); traced a detection plateau to the data, not the model
  ([retail-shelf](2026-retail-shelf-computer-vision-analytics-platform.md) B5); chose batch sync after change data capture proved unworkable
  ([legacy-pos](2024-legacy-pos-cdc-sync-and-membership-analytics-dashboard.md) B1); audited a client database before building on it
  ([hitl-chatbot](2026-hitl-customer-support-chatbot-rag.md) B6); advised against speculative decoding at the target load
  ([llm-serving](2026-parallel-llm-serving-engine-evaluation.md) B4).
- **Production support**: diagnosed task failures, table growth and a silent sensor feed in a
  live pipeline ([sensor-pipeline](2025-time-series-sensor-data-aggregation-pipeline.md) B3–B5); fixed a production LDAP login failure
  ([life-insurance-cms](2023-life-insurance-website-cms-backend.md) B5).
- **Security**: closed a cross-tenant event leak ([retail-shelf](2026-retail-shelf-computer-vision-analytics-platform.md) B3); sanitised rich-text
  HTML against script injection ([life-insurance-cms](2023-life-insurance-website-cms-backend.md) B4).

## Collaboration & mentorship

Nothing about mentoring, onboarding or helping teammates is recorded in evidence yet: verify
asks about it for each project. What evidence shows is code written for others to build on:

- An internal detection library that ended copy-paste between proof-of-concept and production
  code ([road-safety](2025-ai-road-safety-video-analytics-platform.md) B4; one consumer project so far).
- A reusable long-running RabbitMQ task worker for multi-minute video jobs
  ([classroom](2026-classroom-video-attention-and-survey-analysis-system.md) B2).
- A chatbot core that each client project installs as a pinned wheel, with an extension
  standard for tools and guardrails ([chatbot-core](2026-chatbot-core-template-agent-framework-research.md) B1, B3; prototype).
- Evaluation tooling that runs the client's 633-case test set and compares graded runs ([hitl-chatbot](2026-hitl-customer-support-chatbot-rag.md) B4).

## Design & documentation

- **Design records**: ADRs, RFCs, plans and handoffs for the shelf-analytics platform
  ([retail-shelf](2026-retail-shelf-computer-vision-analytics-platform.md) What I Did 20); ADRs on the rate-data scope, serving over ASGI and the
  agent answer engine ([hitl-chatbot](2026-hitl-customer-support-chatbot-rag.md) What I Did 5, 6, 10); a written decision for a
  production login fix ([life-insurance-cms](2023-life-insurance-website-cms-backend.md) B5).
- **Design writing**: a design-doc response to an engineering brief and a versioned developer
  docs site ([chatbot-core](2026-chatbot-core-template-agent-framework-research.md) B5); specs and vertical-slice tickets before code
  ([decision-model](2026-decision-model-rd-reapplying-past-projects.md) Context); the product menu specified as tickets before building it
  ([website-upgrade](2026-corporate-website-astro-upgrade-and-product-pages.md) B5).
- **Runbooks and guides**: an issue write-up and an eight-change remediation plan
  ([sensor-pipeline](2025-time-series-sensor-data-aggregation-pipeline.md) What I Did 8), plus its architecture guide and deploy how-to
  (What I Did 14); Thai runbooks from raw recordings to results ([classroom](2026-classroom-video-attention-and-survey-analysis-system.md) B5);
  onboarding map, deploy guide and manuals for the chatbot ([hitl-chatbot](2026-hitl-customer-support-chatbot-rag.md) What I Did 13);
  onboarding docs and Thai content-update guides for the company site
  ([website-upgrade](2026-corporate-website-astro-upgrade-and-product-pages.md) B5).

## Company building

Work for the company itself, beyond one client project:

- **The company's own websites**: rebuilt the marketing site ([marketing-site](2026-corporate-marketing-website-astro.md) B1) and
  upgraded the live site with pages for the company's video-analytics product
  ([website-upgrade](2026-corporate-website-astro-upgrade-and-product-pages.md) B1–B2).
- **Engineering standards**: a 7-day minimum package release age for the live site
  ([website-upgrade](2026-corporate-website-astro-upgrade-and-product-pages.md) B3); a proposal for a standard chatbot core across client projects
  ([chatbot-core](2026-chatbot-core-template-agent-framework-research.md) B1–B2; prototype).
- **Internal tools and R&D**: a task-delegation tool for the tech team
  ([decision-model](2026-decision-model-rd-reapplying-past-projects.md) B5; prototype); R&D on decision models that the shelf-analytics
  product then took in as a second brand recognizer ([retail-shelf](2026-retail-shelf-computer-vision-analytics-platform.md) B6; unmerged branch).
- **Content workflow**: a Claude Code skill and authoring guides for content editors who are
  not developers ([marketing-site](2026-corporate-marketing-website-astro.md) B4; adoption to confirm).

## What I learned

Nothing recorded yet: the evidence files have no `Learned:` lines. Verify asks what you learned
on each project, a skill and not a tool, such as performance analysis or a new domain.

### Tools first used

Tools by the start year of the project that first used them, from each file's `tools:` line.
Tools a later project used again are not repeated.

| Year | First used | Where |
| ---- | ---------- | ----- |
| 2023 | Django, Django REST Framework, PostgreSQL, Celery, Redis, pandas, React, Nivo, Leaflet | [line-crm](2023-line-crm-loyalty-rfm-segmentation.md) |
| 2023 | Kafka, Apache Flink (PyFlink), MediaPipe, ONNX Runtime, Weaviate, Ultralytics YOLOv8, supervision, Next.js, Flask-SocketIO, cProfile | [crowd-poc](2023-realtime-crowd-analytics-camera-poc.md) |
| 2023 | PyThaiNLP, gensim (Phrases, LDA), SQL Server, MongoDB, Streamlit | [survey](2023-survey-engagement-text-analytics.md) |
| 2023 | ldap3, graphene-django (GraphQL), pytest, Bitbucket Pipelines | [life-insurance-cms](2023-life-insurance-website-cms-backend.md) |
| 2023 | RabbitMQ, PyMonad, argon2 | [forum-scraper](2023-internal-social-forum-scraping-pipeline.md) |
| 2024 | WeasyPrint, Prometheus, Grafana, PyInstrument, Django Channels | [municipal-permit](2024-municipal-building-permit-pdf-and-approval-backend.md) |
| 2024 | Apache Airflow, Debezium (Kafka Connect), SQLAlchemy, MySQL | [legacy-pos](2024-legacy-pos-cdc-sync-and-membership-analytics-dashboard.md) |
| 2024 | DeepFace (Facenet512), scikit-learn (HDBSCAN), ChromaDB, Recharts | [event-booth](2024-event-booth-visitor-cv-analytics.md) |
| 2025 | PyTorch, Ultralytics YOLO11, RF-DETR, EasyOCR, Ollama + LangChain, Weights & Biases, TimescaleDB, pgvector, uv | [road-safety](2025-ai-road-safety-video-analytics-platform.md) |
| 2025 | ffmpeg (NVENC, VideoToolbox), FastAPI, AWS S3, text-to-speech API | [media-merge](2025-voice-video-media-merge-service.md) |
| 2025 | InfluxDB + Flux, Airflow 3 | [sensor-pipeline](2025-time-series-sensor-data-aggregation-pipeline.md) |
| 2025 | InsightFace, Podman, Cloudflare Tunnel | [cctv](2025-realtime-cctv-people-and-security-analytics-platform.md) |
| 2026 | PyQt6, Typhoon2 8B, PyInstaller | [classroom](2026-classroom-video-attention-and-survey-analysis-system.md) |
| 2026 | Modal (serverless GPU), DINOv2, YOLO11-AMF, Playwright, Claude Code | [retail-shelf](2026-retail-shelf-computer-vision-analytics-platform.md) |
| 2026 | Astro, Tailwind CSS 4, Cloudflare Workers, Three.js | [marketing-site](2026-corporate-marketing-website-astro.md) |
| 2026 | OpenRouter decision models, NDJSON streaming | [decision-model](2026-decision-model-rd-reapplying-past-projects.md) |
| 2026 | Qdrant, Langfuse, ASGI (gunicorn + uvicorn) | [hitl-chatbot](2026-hitl-customer-support-chatbot-rag.md) |
| 2026 | Neo4j, hierarchical Leiden (graspologic) | [graphrag](2026-graphrag-lightrag-rag-strategy-comparison.md) |
| 2026 | vLLM | [llm-serving](2026-parallel-llm-serving-engine-evaluation.md) |
| 2026 | Tau agent library, MCP Python SDK, import-linter, Astro Starlight | [chatbot-core](2026-chatbot-core-template-agent-framework-research.md) |

## Interview stories

### Measuring a new retrieval source before switching to it

- **Situation**: In 2026-09 I joined a running proof of concept: a human-in-the-loop support
  chatbot for a currency-exchange chain with about 25 branches, answering customers on LINE and
  Messenger.
- **Task**: Add a second knowledge source that operators manage themselves, without risking the
  answers customers already got.
- **Action**: I built the source end to end: upload, a background indexer into Qdrant, live
  progress over SSE and generation-safe re-indexing. Its retrieval sat behind a switch that
  returns the same context shape as the old path. Before switching, I wrote an evaluation
  command and a relabelled test set, and ran old against new on the same question pool.
- **Result**: The new source was much weaker: recall@1 56.8% against 91.3%, and 90.8% → 56.3%
  on the 174 cases both could score. I traced it to short articles that attract unrelated
  questions and to overlapping score distributions. The switch shipped default-off, with
  rollback by one environment variable.

Source: [hitl-chatbot](2026-hitl-customer-support-chatbot-rag.md) Context, What I Did 1–3,
Numbers row 1–2, B1–B2

### Finding why a production pipeline lost data

- **Situation**: An Airflow pipeline I built alone aggregates energy telemetry from InfluxDB into
  TimescaleDB, in production since 2025-09. In 2026-07 the production host kept raising alerts.
- **Task**: Find the cause of the task failures and the missing data points.
- **Action**: From logs, container state and the database, I showed that 9 DAGs fired in the
  same minute on a 2-vCPU host with no swap. That pushed DAG imports past their timeout and
  dropped top-of-hour points. I staggered the schedules. I also found a 1.84 GB XCom table
  caused by tasks returning whole DataFrames, and checked for 0 duplicate keys before adding a
  unique index.
- **Result**: The root cause and an eight-change remediation plan are written up, and the fixes
  merged. Whether the data loss stopped after deploy is not yet confirmed.

Source: [sensor-pipeline](2025-time-series-sensor-data-aggregation-pipeline.md) Context, What I
Did 8–11, Numbers rows 4, 5, 6, 9, B3–B4

### Building a shelf-analytics platform alone

- **Situation**: A retail-research client collects smartphone photos of store shelves and wanted
  to sell shelf analytics reports to consumer brands. A proof of concept existed.
- **Task**: Rebuild it as a multi-tenant product: detect products, logos and empty slots, name
  the brands, and show analytics per survey.
- **Action**: As sole committer, I designed and built it end to end: one-pass YOLO detection and
  DINOv2 brand matching on Modal GPUs, a Django REST API and Next.js dashboards. I replaced
  daemon-thread dispatch with a Celery and Redis queue so jobs survive restarts, and moved
  progress events to Redis pub/sub, which closed a cross-tenant event leak. When accuracy
  stalled, I trained two architectures to test whether the model was the limit.
- **Result**: The platform runs on a production host, and the client was trialling it in
  2026-09. Both architectures reached the same per-class profile, logo AP50 0.54 against product
  0.92 on 23 validation images, which pointed to the data, not the model.

Source: [retail-shelf](2026-retail-shelf-computer-vision-analytics-platform.md) Context, B1–B3,
B5, Numbers rows 1–2

### Testing a hosted vision model on real shelf images

- **Situation**: An internal R&D project tried hosted "decision models" on problems from the
  company's earlier projects, including brand recognition for the retail-shelf product.
- **Task**: Measure whether a vision decision model could name brands on real shelf crops, and
  at what cost.
- **Action**: I built the model client and an image send policy after the vendor rejected large
  images, stored predictions by fingerprint so re-runs skipped unchanged images, and built
  evaluation pages with per-brand metrics. I then compared a second model on the same images.
- **Result**: 89% top-1 accuracy on 739 labelled crops in 6 categories (74%–96% per category).
  The second model matched all 44 comparison images at about one-ninth of the cost. The
  retail-shelf project then took the model in as a second brand recognizer, on a branch not yet
  merged.

Source: [decision-model](2026-decision-model-rd-reapplying-past-projects.md) Context, B1–B3,
Numbers rows 1–4; [retail-shelf](2026-retail-shelf-computer-vision-analytics-platform.md) B6

### Finding why an LLM server answered one request at a time

- **Situation**: A team needed a self-hosted Qwen 3.5 server for 5–10 concurrent requests. On
  Ollama, concurrent requests ran one after another.
- **Task**: Find out why, and choose a serving engine, in a one-day spike.
- **Action**: I built a streaming load tester that reports time to first token per request. It
  showed a staircase: 0.1, 1.5, 2.9 and 4.4 s for four requests. I traced the cause to Ollama's
  scheduler, which pins hybrid-architecture models to one slot because of an unfixed upstream
  llama.cpp issue. I also designed a test that tells continuous batching from static batching.
- **Result**: On vLLM the late request got its first token 0.4 s after sending. I recommended
  vLLM for the GPU server and advised against speculative decoding at that load. The GPU-server
  run is still pending.

Source: [llm-serving](2026-parallel-llm-serving-engine-evaluation.md) Context, What I Did 1–4,
Numbers rows 3–4, B1–B4

## Timeline

| Period | Project | My role | Status | Headline |
| ------ | ------- | ------- | ------ | -------- |
| 2026-11 | [Chatbot core template](2026-chatbot-core-template-agent-framework-research.md) | AI engineer, sole author | wip | Prototyped a chatbot core that clients install as a pinned wheel |
| 2026-11 | [Live website upgrade](2026-corporate-website-astro-upgrade-and-product-pages.md) | contributor to a team site | shipped | Upgraded the live site to Astro 7 and added product pages |
| 2026-10 | [RAG strategy comparison](2026-graphrag-lightrag-rag-strategy-comparison.md) | sole developer | wip | Compared Simple RAG, GraphRAG and LightRAG on one corpus |
| 2026-10 | [LLM serving evaluation](2026-parallel-llm-serving-engine-evaluation.md) | AI engineer, sole author | wip | Root-caused Ollama's one-at-a-time serving and recommended vLLM |
| 2026-09 ~ 2026-11 | [Decision-model R&D](2026-decision-model-rd-reapplying-past-projects.md) | AI / backend engineer, sole developer | wip | Measured 89% top-1 brand recognition on 739 shelf crops |
| 2026-09 ~ 2026-11 | [Support chatbot RAG](2026-hitl-customer-support-chatbot-rag.md) | AI / backend engineer, one of four | wip | Measured a new retrieval source and kept the weaker one off |
| 2026-05 ~ 2026-06 | [Marketing website rebuild](2026-corporate-marketing-website-astro.md) | sole developer | wip | Rebuilt the marketing site in Astro with content collections |
| 2026-03 ~ 2026-11 | [Retail shelf analytics](2026-retail-shelf-computer-vision-analytics-platform.md) | AI / full-stack engineer, sole committer | shipped | Designed and built a shelf-photo analytics platform in client trial |
| 2026-02 ~ 2026-06 | [Classroom attention analysis](2026-classroom-video-attention-and-survey-analysis-system.md) | AI / data engineer, main developer | shipped | Scored attention in ~930 student webcam recordings |
| 2025-11 ~ 2026-03 | [CCTV security analytics](2025-realtime-cctv-people-and-security-analytics-platform.md) | AI / backend engineer, main developer | shipped | Built face check-in and multi-camera threat detection |
| 2025-08 ~ 2026-07 | [Sensor telemetry pipeline](2025-time-series-sensor-data-aggregation-pipeline.md) | data engineer, sole developer | shipped | Built and debugged an Airflow energy-telemetry pipeline in production |
| 2025-07 ~ 2025-09 | [Media-merge service](2025-voice-video-media-merge-service.md) | backend engineer, main worker developer | shipped | Built a GPU ffmpeg worker that renders personalised videos |
| 2025-05 ~ 2026-01 | [Road-safety video analytics](2025-ai-road-safety-video-analytics-platform.md) | AI / backend engineer, main developer | wip | Built a demo road-safety system on 3 camera sites |
| 2024-11 ~ 2025-02 | [Exhibition visitor analytics](2024-event-booth-visitor-cv-analytics.md) | data / backend engineer, main developer | shipped | Estimated unique visitors by clustering face embeddings |
| 2024-08 ~ 2025-02 | [Legacy POS sync and RFM](2024-legacy-pos-cdc-sync-and-membership-analytics-dashboard.md) | data / backend engineer | shipped | Synced a legacy MySQL 5.5 POS into PostgreSQL with Airflow |
| 2024-04 ~ 2024-10 | [Truck warranty backend](2024-truck-dealer-website-cms-and-warranty-tracking-backend.md) | backend developer, main warranty developer | shipped | Built warranty and service scheduling for truck dealers |
| 2024-02 ~ 2024-04 | [Municipal permit backend](2024-municipal-building-permit-pdf-and-approval-backend.md) | backend engineer, one of three | shipped | Built PDF generation for Thai official permit forms |
| 2023-12 ~ 2024-08 | [Forum scraping pipeline](2023-internal-social-forum-scraping-pipeline.md) | sole developer | wip | Built a queued forum-scraping service with Thai word clouds |
| 2023-08 ~ 2026-05 | [Life-insurance CMS](2023-life-insurance-website-cms-backend.md) | backend developer, one of three to four | shipped | Built CMS content APIs and role-based access control |
| 2023-05 ~ 2025-05 | [Survey text analytics](2023-survey-engagement-text-analytics.md) | data scientist / backend developer | shipped | Built the Thai word-cloud engine for survey reports |
| 2023-04 ~ 2024-07 | [Crowd analytics PoC](2023-realtime-crowd-analytics-camera-poc.md) | AI / data engineer, main developer | wip | Built a real-time audience-analytics demo for a marketing event |
| 2023-02 ~ 2023-05 | [LINE loyalty RFM](2023-line-crm-loyalty-rfm-segmentation.md) | data analyst / backend developer | shipped | Built RFM customer segmentation for a loyalty platform |

<!-- user:outside:start -->
## Outside of work

- Not written yet: blog posts, talks, open source or recognition, in your own words.
<!-- user:outside:end -->

## Not yet confirmed

All 22 evidence files are drafts. Run `/resume-builder:resume-auto-mode verify themather <id>` to confirm them.
The files use the older format, so no `assessed` Impact rows exist yet. Collaboration,
mentorship and what I learned have no answers yet: verify asks about them. These outcomes are
marked "to confirm" in the files and matter most:

- **Production use and go-live**:
  [cctv](2025-realtime-cctv-people-and-security-analytics-platform.md),
  [municipal-permit](2024-municipal-building-permit-pdf-and-approval-backend.md),
  [legacy-pos](2024-legacy-pos-cdc-sync-and-membership-analytics-dashboard.md),
  [media-merge](2025-voice-video-media-merge-service.md),
  [event-booth](2024-event-booth-visitor-cv-analytics.md),
  [line-crm](2023-line-crm-loyalty-rfm-segmentation.md),
  [truck-warranty](2024-truck-dealer-website-cms-and-warranty-tracking-backend.md) (still in
  use?), [classroom](2026-classroom-video-attention-and-survey-analysis-system.md) (delivery to
  the client).
- **Sensor pipeline**: "in production since 2025-09" rests on a deploy ticket; the 2026-07
  stagger and its effect on data loss are not confirmed
  ([sensor-pipeline](2025-time-series-sensor-data-aggregation-pipeline.md) B1, B3).
- **Retail shelf**: whether the benchmark system ran in production (B4), and the adoption scale
  of the client trial (B1)
  ([retail-shelf](2026-retail-shelf-computer-vision-analytics-platform.md)).
- **Speed-ups with no measured result**: the "10x" member-forms speed-up is in a ticket title
  only ([municipal-permit](2024-municipal-building-permit-pdf-and-approval-backend.md) B3).
- **Authorship**: who labelled the shelf crops
  ([decision-model](2026-decision-model-rd-reapplying-past-projects.md) B1); whether I designed
  the attention-scoring method or ported it
  ([classroom](2026-classroom-video-attention-and-survey-analysis-system.md) B1); role and team
  size on the support chatbot ([hitl-chatbot](2026-hitl-customer-support-chatbot-rag.md)).
- **Adoption of R&D**: whether vLLM was adopted on the GPU server
  ([llm-serving](2026-parallel-llm-serving-engine-evaluation.md) B4); whether the chatbot core
  was one of several parallel proposals
  ([chatbot-core](2026-chatbot-core-template-agent-framework-research.md)).
