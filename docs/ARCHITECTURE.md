# Technical architecture

## Components

| Layer | Technology | Responsibility |
|---|---|---|
| Web client | React, TypeScript, Vite | Discovery UI, cards, filters, detail drawers, pathways and map. |
| API | FastAPI | Read-only resource search, facets, pathway and graph endpoints. |
| Read model | SQLite | Indexed resource records and normalized subject relationships. |
| Source data | Versioned JSON | Portable, reviewable dataset independent of the runtime database. |
| Local state | Browser localStorage | Bookmarks, completed pathway stages and theme preference. |
| Local deployment | Docker Compose | API and web development services. |

## Data flow

`data/catalog.json` + `data/taxonomy.json` + `data/pathways.json` are loaded into SQLite when the catalog version changes. The database is a read model, not the canonical source. Curators should edit reviewed source data and regenerate the JSON.

## API surface

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | Service health. |
| GET | `/api/v1/overview` | Catalog and coverage counts. |
| GET | `/api/v1/facets` | Domain, subject, format, level and access facets. |
| GET | `/api/v1/resources` | Search and filter resources. |
| GET | `/api/v1/resources/{id}` | Resource detail. |
| GET | `/api/v1/resources/{id}/related` | Transparent shared-subject recommendations. |
| GET | `/api/v1/pathways` | Pathway summaries. |
| GET | `/api/v1/pathways/{id}` | Full staged pathway with attached resources. |
| GET | `/api/v1/knowledge-map` | Subject nodes and co-occurrence edges. |

Search query supports `q`, `domain`, `subject`, `type`, `level`, `access`, `verification`, `sort`, `limit` and `offset`. The current relevance rank is a lightweight text match, not semantic vector retrieval.

## Deliberate constraints in v1

- No accounts or personally identifiable learner profiles.
- No write endpoints exposed to the public client.
- No AI provider keys or external paid services required.
- No external analytics SDK.
- No popularity score until usage measurement and privacy policy are defined.

## Scale-up path

When catalog and traffic justify it, keep the same API contracts while adding PostgreSQL, a dedicated search index, optional embeddings, a contributor review queue and an account service. Search and recommendations should remain replaceable adapters; do not bind core catalog records to one LLM provider.
