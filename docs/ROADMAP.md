# Roadmap: from strong foundation to global knowledge platform

## Phase 0 — foundation (this build)

- [x] Unified source catalog and normalized domain navigation.
- [x] Responsive client, API, SQLite read model and local progress.
- [x] Honest metadata and verification disclosure.
- [x] Structured pathways, related resources and tag co-occurrence map.
- [x] Docker-based local launch.

## Phase 1 — curation quality (highest priority)

- [ ] Define a formal resource-quality rubric: authority, pedagogical clarity, completeness, accessibility, maintenance and learner fit.
- [ ] Review the highest-traffic/highest-value records at the destination, not just the source index.
- [ ] Replace free-text level/access/resource-type strings with controlled values and explicit `unknown` states.
- [ ] Add reviewed-at, reviewer, review-method and next-review-due metadata.
- [ ] Add an automated URL check with retries, redirect capture and an exception queue; never auto-delete on one failed HEAD request.
- [ ] Resolve same-title resources and canonical URL aliases through human review.
- [ ] Add language, modality, prerequisites, syllabus coverage, estimated effort and license only when they can be sourced.

## Phase 2 — learning intelligence

- [ ] Expand pathways into explicit prerequisite graphs with curator-authored edges.
- [ ] Add learning outcomes, project milestones and self-check questions to each stage.
- [ ] Build a transparent recommendation model using user-chosen interests and declared goals.
- [ ] Add optional semantic search behind an independent embedding adapter and a reproducible evaluation set.
- [ ] Add a “why this result?” explanation to every recommendation.

## Phase 3 — open contribution system

- [ ] Add a schema-backed resource submission form and preview.
- [ ] Add duplicate detection, URL safety checks, attribution checks and required provenance.
- [ ] Add curator review states: submitted → triaged → checked → accepted/rejected → scheduled review.
- [ ] Publish a public changelog for metadata changes and removed/redirected links.
- [ ] Establish maintainer roles, moderation policy and a response-time expectation.

## Phase 4 — global ecosystem

- [ ] Internationalisation and locale-aware resource metadata.
- [ ] Accessible reading modes and low-bandwidth catalogue mode.
- [ ] Optional account-based sync only after a privacy/security design review.
- [ ] Public read API with rate limits, versioning and usage policy.
- [ ] University, educator and open-source project partnerships.
- [ ] Export formats: JSON, CSV, BibTeX-style citations where appropriate, and offline snapshots.

## Phase 5 — research-grade knowledge graph

- [ ] Distinguish topic relationships, prerequisites, applications, analogies and shared tools.
- [ ] Capture edge provenance, confidence, author and review date.
- [ ] Build graph exploration with user-controlled depth and explainable connections.
- [ ] Add AI-assisted curation only as a draft suggestion; human approval remains required.

## Priority rule

Do not build AI chat, social feeds, leaderboards or gamification before the core records are trustworthy, searchable and explainable. A smaller reliable atlas will be more useful than a larger but unmaintainable one.
