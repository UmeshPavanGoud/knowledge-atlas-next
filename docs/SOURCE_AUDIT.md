# Source repository audit

**Source reviewed:** the uploaded `knowledge-hub.zip` archive, extracted as a repository snapshot.

## What was actually inspected

- **144 files** across the repository snapshot.
- **415 resource records** across 23 YAML resource files.
- **21 declared subjects** in the source taxonomy, plus the legacy `databases` subject value found in resource data.
- **9 existing learning-path documents**.
- Five Python scripts: catalog builder, catalog validator, duplicate checker, internal-link checker, and optional external-link checker.
- The root README, start guide, resource schema, build manifest, catalog and curation documents, taxonomy files, research notes, contribution templates and CI workflow.

## Existing strengths worth retaining

1. A central structured catalog already exists. This is a better source of truth than manually maintained duplicate lists.
2. The 415 records have 415 distinct URL strings according to the repository's existing validator. The duplicate checker also reports no exact duplicate canonical URLs.
3. All 415 resources have IDs, a description, a `best_for` note, subject values, an access value, a verification-status string and provenance.
4. There are nine starter pathways covering mathematics, physics, programming, computer science, AI engineering, machine learning, electronics, game development and independent research.
5. Curation limitations and upstream provenance are unusually explicit for an early-stage resource project.

## Structural and product issues confirmed in the data

| Finding | Measured result | Product consequence |
|---|---:|---|
| Resource records | 415 | Enough material for a useful first searchable release. |
| YouTube records | 257 (61.9%) | The catalog is heavily video-channel weighted; the interface must expose format and source confidence rather than treating every result as equivalent. |
| Difficulty marked Unknown | 240 (57.8%) | Difficulty cannot be a mandatory filter or be used to imply reliable level coverage. |
| Access marked Unknown | 301 (72.5%) | “Free” must never be inferred from a missing access value. |
| Distinct free-text `resource_type` values | 123 | Resource formats are too granular and inconsistent for a clean user-facing filter. |
| Distinct free-text `category` values | 120 | The category label combines provider identity, content type and topic-like labels. |
| Declared subject values | 22 | A subject tag can be precise, but should not force a separate top-level navigation page. |
| Source verification labels | 9 distinct strings | Verification is not a consistent workflow state; the raw value should be preserved but mapped to a smaller display vocabulary. |

The leading source-verification groups include 238 YouTube entries marked as extracted from an upstream index without independent channel-page verification and 59 records whose direct destination verification is pending. This matters: a URL collected from another repository is not equivalent to a page checked by a curator.

## Classification problems

The source uses several competing labels: `subjects`, `category`, `platform_type`, `resource_type`, `difficulty`, `focus_area`, and `source_categories`. This is not inherently wrong as metadata, but the old experience exposes too many of these as parallel browsing structures. `category` and `resource_type` are free text with 120 and 123 distinct values respectively. They should remain descriptive metadata, while the user-facing interface should use a small controlled set of formats and subject tags.

The resource tag `databases` does not match the declared `database-systems` taxonomy ID. The replacement normalizes it to `database-systems` while retaining `subjects_original` for traceability.

Repeated names are not automatically duplicate records: examples include `3Blue1Brown`, `GitHub Ranking`, and `MIT OpenCourseWare`, which can represent different destinations or contexts. URL identity and curator review should be used before merging.

## Validation results from the supplied code

Commands executed inside the extracted source repository:

```text
python scripts/validate-catalog.py
VALIDATION PASSED: 415 resources across 23 YAML files; 415 unique destinations.

python scripts/check-duplicates.py
No duplicate canonical URLs found.

python scripts/check-internal-links.py
Internal Markdown links passed.
```

These are useful baseline checks, but they do not prove all external destinations currently work, that all providers still offer the described material, or that the resources have been evaluated for quality. The external link checker is optional and reports per-URL failures; it is not a complete curation workflow.

## New handling in this rebuild

- All 415 source records are retained in `data/catalog.json`. Original descriptions, resource type, category, raw difficulty, access, URL, raw verification string, notes, source categories and provenance remain available.
- A single `databases` → `database-systems` alias resolves the taxonomy mismatch.
- Eight broad navigation domains replace the old many-page subject-first experience. Precise subjects remain filterable, including cross-disciplinary tagging.
- A small display vocabulary is derived for format, access, difficulty and source confidence. Raw values remain preserved for detail views.
- The knowledge map uses actual subject co-occurrence on the same resource record. It is explicitly not represented as a prerequisite or causal graph.
- The nine existing pathways are converted to structured JSON steps. The original Markdown snapshot is retained in the archive for comparison.

## Not done in this build

- No blanket live-link verification of all 415 URLs.
- No independent ranking or quality scoring of all providers.
- No new AI/LLM model, semantic embedding service or personalised algorithm.
- No public user accounts, cloud progress sync, submissions or moderation dashboard.
- No repository-wide license choice; none was present in the supplied repository.
