# Atlas API

FastAPI service backed by SQLite. It loads the curated catalog JSON and structured pathways at startup.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r services/api/requirements.txt
uvicorn app.main:app --app-dir services/api --reload --port 8000
```

Health: `GET /api/health` · OpenAPI: `http://localhost:8000/docs`.

The current API is read-only by design. Personal bookmarks and pathway progress remain in the browser; no learner profile or activity is sent to the API.

Run automated smoke tests from the repository root with `PYTHONPATH=services/api pytest -q services/api/tests` after installing `pytest` and `httpx`.
