from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fastapi.testclient import TestClient
from app.main import app

def test_catalog_and_discovery_endpoints():
    with TestClient(app) as client:
        assert client.get("/api/health").json()["status"] == "ok"
        overview = client.get("/api/v1/overview").json()
        assert overview["resource_count"] == 415
        assert overview["domain_count"] == 8
        assert overview["pathway_count"] == 9
        search = client.get("/api/v1/resources", params={"q": "linear algebra"}).json()
        assert search["total"] >= 1
        assert any("linear algebra" in r["name"].lower() for r in search["items"])
        filtered = client.get("/api/v1/resources", params={"domain": "ai-data", "limit": 5}).json()
        assert len(filtered["items"]) <= 5
        assert all("ai-data" in r["domain_ids"] for r in filtered["items"])

def test_pathway_and_related_resource():
    with TestClient(app) as client:
        path = client.get("/api/v1/pathways/ai-engineering")
        assert path.status_code == 200
        body = path.json()
        assert body["steps"]
        assert all(resource["id"] for step in body["steps"] for resource in step["resources"])
        resource = client.get("/api/v1/resources/math-mit-1806")
        assert resource.status_code == 200
        related = client.get("/api/v1/resources/math-mit-1806/related")
        assert related.status_code == 200
        assert related.json()["items"]

def test_unknown_records_return_404():
    with TestClient(app) as client:
        assert client.get("/api/v1/resources/does-not-exist").status_code == 404
        assert client.get("/api/v1/pathways/does-not-exist").status_code == 404


def test_source_confidence_and_pagination():
    with TestClient(app) as client:
        facets = client.get("/api/v1/facets").json()
        assert {row["id"] for row in facets["verification"]} >= {"upstream-only", "pending"}
        first = client.get("/api/v1/resources", params={"limit": 5, "offset": 0}).json()
        second = client.get("/api/v1/resources", params={"limit": 5, "offset": 5}).json()
        assert len(first["items"]) == 5 and len(second["items"]) == 5
        assert first["items"][0]["id"] != second["items"][0]["id"]
