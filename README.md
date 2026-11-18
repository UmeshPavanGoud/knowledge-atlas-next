# Atlas — Knowledge, connected.

**A new product architecture for Knowledge Atlas.** The repository has been rebuilt around the learner's journey rather than the source repository's old directory layout. It is a searchable catalog, a set of guided learning routes, and a cross-disciplinary map—not merely a collection of Markdown indexes.

![Atlas](apps/web/public/atlas-mark.svg)

## What is included

- **A redesigned responsive web app** with discovery home, catalog search, subject/domain filters, resource detail drawers, learning paths, a knowledge map, and a personal saved shelf.
- **A FastAPI backend** with a versioned `/api/v1` surface, SQLite storage, resource search, facets, learning-path detail, related-resource matches and cross-subject graph data.
- **The full source catalog**: all **415** source records are retained in `data/catalog.json`, with source provenance and original verification strings.
- **A new discovery taxonomy**: 8 broad domains and 21 precise subjects; the old `databases` tag is normalized to `database-systems`.
- **Structured learning pathways** translated from the supplied repository's nine pathway documents.
- **Privacy-first progress**: bookmarks and completed stages are stored in local browser storage; the backend does not receive learner profiles.
- **Docker Compose** for a one-command local environment.

## Start the platform

### Option A — Docker

```bash
docker compose up --build
```

Open `http://localhost:5173` for the web app and `http://localhost:8000/docs` for the API.

### Option B — Run each service locally

Backend (from the repository root):

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r services/api/requirements.txt
uvicorn app.main:app --app-dir services/api --reload --port 8000
```

Frontend (in a second terminal):

```bash
cd apps/web
npm install
npm run dev
```

Open `http://localhost:5173`.

## Product principles

1. **Intent before taxonomy.** Start with what a learner wants to do; expose deeper subject tags as filters instead of making every category a top-level destination.
2. **One resource, one canonical record.** A resource can appear in multiple subject contexts without being duplicated.
3. **Honest confidence.** `Unknown`, `not listed`, and `not independently checked` remain visible. A source index is not the same as a reviewed destination.
4. **Useful structure, not complexity for its own sake.** The knowledge map shows subject co-occurrence in catalog records; it does not pretend to know prerequisite relations.
5. **Learner privacy.** No login, tracking, or central progress database in the initial release.
6. **Composable evolution.** Search, recommendations, accounts, APIs and contributor workflows can be added behind clear service boundaries.

## Architecture

```text
Browser
  └── React + TypeScript + Vite (apps/web)
        ├── Discover / Explore / Paths / Knowledge Map / Saved
        ├── Browser-local bookmarks and progress
        └── /api/v1 requests
              │
              ▼
        FastAPI (services/api)
              │
              ▼
        SQLite read model (.local/atlas.db)
              ▲
              │ seed / versioned import
        JSON source data (data/)
```

The original 415-record catalog is also preserved as a YAML snapshot in `source-archive/catalog-original.yaml`. Use `python tools/build_catalog.py` after editing that archive, `python tools/build_pathways.py` after editing the archived pathway Markdown, then run `python tools/validate_data.py`.

See [the source audit](docs/SOURCE_AUDIT.md), [product and UX specification](docs/PRODUCT_VISION.md), [architecture](docs/ARCHITECTURE.md), [evolution blueprint](docs/EVOLUTION_BLUEPRINT.md), [roadmap](docs/ROADMAP.md), and [launch checklist](docs/LAUNCH_CHECKLIST.md).

## Catalog status

This build preserves source data; it does not newly verify the current availability, price, quality or licensing of all 415 destinations. The original source status and provenance are retained so the next curation cycle can prioritize high-value entries. Read the audit before describing the catalog as verified.

## Important before public launch

The supplied repository did not include a repository-wide license. No new license is invented here. Choose and add an appropriate project license after deciding what permissions you want to grant. Third-party descriptions, names, logos and destinations retain their respective rights and terms.
