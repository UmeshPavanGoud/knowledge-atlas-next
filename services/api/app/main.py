from __future__ import annotations
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from .config import API_PREFIX
from .database import initialize_database
from . import catalog

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield

app=FastAPI(title="Atlas Knowledge API",version="1.0.0",description="Searchable knowledge catalog and learning-path API.",lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:5173","http://127.0.0.1:5173","http://localhost:4173"],allow_credentials=False,allow_methods=["GET"],allow_headers=["*"])

@app.get("/api/health")
def health():
    return {"status":"ok","service":"atlas-api"}

@app.get(f"{API_PREFIX}/overview")
def overview():
    return catalog.overview()

@app.get(f"{API_PREFIX}/facets")
def facets():
    return catalog.get_facets()

@app.get(f"{API_PREFIX}/resources")
def resources(q: str|None=None,domain: str|None=None,subject: str|None=None,type: str|None=None,level: str|None=None,access: str|None=None,verification: str|None=None,sort: str="relevance",limit: int=Query(24,ge=1,le=500),offset: int=Query(0,ge=0)):
    if sort not in {"relevance","name"}: raise HTTPException(400,"sort must be relevance or name")
    return catalog.list_resources({"q":q,"domain":domain,"subject":subject,"type":type,"level":level,"access":access,"verification":verification,"sort":sort,"limit":limit,"offset":offset})

@app.get(f"{API_PREFIX}/resources/{{resource_id}}")
def resource(resource_id: str):
    item=catalog.get_resource(resource_id)
    if not item: raise HTTPException(404,"Resource not found")
    return item

@app.get(f"{API_PREFIX}/resources/{{resource_id}}/related")
def related(resource_id: str,limit: int=Query(6,ge=1,le=20)):
    result=catalog.recommendations(resource_id,limit)
    if result is None: raise HTTPException(404,"Resource not found")
    return result

@app.get(f"{API_PREFIX}/pathways")
def pathways():
    return {"items":catalog.list_paths()}

@app.get(f"{API_PREFIX}/pathways/{{path_id}}")
def pathway(path_id: str):
    item=catalog.get_path(path_id)
    if not item: raise HTTPException(404,"Learning path not found")
    return item

@app.get(f"{API_PREFIX}/knowledge-map")
def knowledge_map():
    return catalog.graph()
