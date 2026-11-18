# Evolution blueprint: from atlas to a knowledge intelligence platform

The first release is intentionally useful without AI, a paid service or user accounts. The next architecture should add intelligence only where it measurably improves discovery and trust.

## 1. Typed knowledge graph

Extend the current domain/subject/resource model into explicit entities: `Domain`, `Discipline`, `Topic`, `Concept`, `Resource`, `Provider`, `LearningPath`, `PathStep`, `Prerequisite`, `Application`, `RelatedConcept`, `Review`, and `ResourceVersion`.

Every relationship should have a type, provenance, curator, review timestamp and confidence. Example edge types: `prerequisite_of`, `part_of`, `applied_in`, `uses_tool`, `related_to`, `contrasts_with`, and `co_appears_in`. Co-occurrence must remain distinct from a real prerequisite.

## 2. Search evolution

**Now:** token-based search over catalog metadata with controlled filters.

**Next:** SQLite FTS5 or PostgreSQL full-text search, typo tolerance, aliases and query suggestions.

**Later:** hybrid retrieval that combines exact lexical retrieval, semantic embeddings, taxonomy filters and curated relation expansion. Preserve deterministic ranking controls and show why a result matched.

## 3. Responsible AI layer

An eventual Atlas Guide could help users translate goals into learning paths, explain prerequisites and compare learning resources. Its retrieval must be restricted to maintained Atlas records and clearly identified first-party source content. It should:

- cite each resource and distinguish source facts from generated recommendations;
- state when metadata is missing instead of filling gaps;
- explain why a resource/path was suggested;
- never invent a course price, completion credential, syllabus, duration or quality score;
- route new resource claims into a curator review queue rather than directly publishing them;
- keep personal preferences local by default, with explicit consent before any server-side profile.

## 4. Adaptive pathways

Move from static sequences to optional branches: diagnostic self-check → recommended starting stage → core route → elective branches → project milestone → reflection. Keep the learner in control. A route should show required prerequisites separately from optional enrichment.

## 5. Quality and provenance system

Resource quality should not collapse into one opaque star rating. Track dimensions separately: source authority, content depth, pedagogical clarity, maintenance recency, accessibility, cost/access transparency and evidence of learning outcomes. Add a human-reviewed confidence state and a review due date.

## 6. Global access

Add language/locale and subtitles/transcript availability when sourced. Build a lightweight mode, downloadable catalog snapshots and keyboard/screen-reader support. Regional access restrictions must be recorded with scope and review date rather than inferred from the provider's homepage.

## 7. Infrastructure migration triggers

Do not split into microservices early. Keep one API and replace its internals as needed:

- Move SQLite to PostgreSQL when writes, concurrent curation or deployments require it.
- Add a dedicated search service when full-text/vector search needs justify it.
- Add a graph database only when typed traversals become a real bottleneck.
- Add a queue for link checks, metadata refreshes and AI-assisted review when the catalog and contributor volume require asynchronous jobs.
- Add user identity and sync only after threat modelling, privacy design, export and deletion workflows are ready.

## 8. Defensibility

The most valuable asset is not the code or an AI wrapper. It is a high-quality, transparent, continually reviewed map of useful learning resources and the relationships that help people learn. Invest in curation, contributor trust, accessibility and measurable learner outcomes before chasing feature count.
