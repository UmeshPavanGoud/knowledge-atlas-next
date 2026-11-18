from __future__ import annotations
import json, re, sqlite3
from typing import Any
from .database import session

RESOURCE_SELECT = """
SELECT r.*, GROUP_CONCAT(s.id, '|') AS subject_ids,
       GROUP_CONCAT(s.name, '|') AS subject_names,
       GROUP_CONCAT(DISTINCT s.domain_id) AS domain_ids
FROM resources r
LEFT JOIN resource_subjects rs ON rs.resource_id=r.id
LEFT JOIN subjects s ON s.id=rs.subject_id
"""

def _resource(row: sqlite3.Row) -> dict[str, Any]:
    d = dict(row)
    d["provenance"] = json.loads(d.pop("provenance_json", "[]"))
    d["source_categories"] = json.loads(d.pop("source_categories_json", "[]"))
    d["subjects"] = [] if not d.get("subject_ids") else [
        {"id": sid, "name": name}
        for sid, name in zip(d["subject_ids"].split("|"), d["subject_names"].split("|"))
    ]
    d["domain_ids"] = [] if not d.get("domain_ids") else d["domain_ids"].split(",")
    for key in ["subject_ids", "subject_names", "search_text"]:
        d.pop(key, None)
    return d

def _where(params: dict[str, Any]):
    clauses=[]; values=[]
    q=(params.get("q") or "").strip()
    if q:
        tokens=[x.lower() for x in re.findall(r"[\w+#.-]+",q) if len(x)>1][:8]
        for token in tokens:
            clauses.append("r.search_text LIKE ?")
            values.append(f"%{token}%")
    if params.get("domain"):
        clauses.append("EXISTS (SELECT 1 FROM resource_subjects rs JOIN subjects s ON s.id=rs.subject_id WHERE rs.resource_id=r.id AND s.domain_id=?)")
        values.append(params["domain"])
    if params.get("subject"):
        clauses.append("EXISTS (SELECT 1 FROM resource_subjects rs WHERE rs.resource_id=r.id AND rs.subject_id=?)")
        values.append(params["subject"])
    for key,col in [("type","kind"),("level","level"),("access","access_key"),("verification","verification_level")]:
        if params.get(key):
            clauses.append(f"r.{col}=?"); values.append(params[key])
    return (" WHERE " + " AND ".join(clauses) if clauses else ""), values

def list_resources(params: dict[str, Any]):
    where, values = _where(params)
    sort=params.get("sort","relevance")
    order="r.name COLLATE NOCASE ASC"
    if sort=="relevance" and params.get("q"):
        tokens=[x.lower() for x in re.findall(r"[\w+#.-]+",params["q"]) if len(x)>1][:8]
        if tokens:
            score_parts=[]; score_values=[]
            for token in tokens:
                score_parts.append("(CASE WHEN lower(r.name) LIKE ? THEN 8 WHEN lower(r.best_for) LIKE ? THEN 4 WHEN lower(r.description) LIKE ? THEN 2 ELSE 0 END)")
                score_values += [f"%{token}%"]*3
            order="("+" + ".join(score_parts)+") DESC, r.name COLLATE NOCASE ASC"
            values_for_order=score_values
        else: values_for_order=[]
    else: values_for_order=[]
    try:
        limit=max(1,min(int(params.get("limit",24)),500)); offset=max(0,int(params.get("offset",0)))
    except (TypeError,ValueError): limit,offset=24,0
    with session() as conn:
        count=conn.execute("SELECT COUNT(*) FROM resources r"+where,values).fetchone()[0]
        sql=RESOURCE_SELECT+where+" GROUP BY r.id ORDER BY "+order+" LIMIT ? OFFSET ?"
        rows=conn.execute(sql,values+values_for_order+[limit,offset]).fetchall()
    return {"items":[_resource(r) for r in rows],"total":count,"limit":limit,"offset":offset,"has_more":offset+len(rows)<count}

def get_resource(resource_id: str):
    with session() as conn:
        row=conn.execute(RESOURCE_SELECT+" WHERE r.id=? GROUP BY r.id",(resource_id,)).fetchone()
    return _resource(row) if row else None

def get_facets():
    with session() as conn:
        domains=conn.execute("SELECT d.id,d.name,d.eyebrow,d.icon,d.description,d.color,COUNT(DISTINCT rs.resource_id) AS count FROM domains d LEFT JOIN subjects s ON s.domain_id=d.id LEFT JOIN resource_subjects rs ON rs.subject_id=s.id GROUP BY d.id ORDER BY count DESC,d.name").fetchall()
        subjects=conn.execute("SELECT s.id,s.name,s.domain_id,COUNT(rs.resource_id) AS count FROM subjects s LEFT JOIN resource_subjects rs ON rs.subject_id=s.id GROUP BY s.id ORDER BY count DESC,s.name").fetchall()
        kinds=conn.execute("SELECT kind AS id,COUNT(*) AS count FROM resources GROUP BY kind ORDER BY count DESC").fetchall()
        levels=conn.execute("SELECT level AS id,COUNT(*) AS count FROM resources GROUP BY level ORDER BY count DESC").fetchall()
        accesses=conn.execute("SELECT access_key AS id,COUNT(*) AS count FROM resources GROUP BY access_key ORDER BY count DESC").fetchall()
        verification=conn.execute("SELECT verification_level AS id,COUNT(*) AS count FROM resources GROUP BY verification_level ORDER BY count DESC").fetchall()
    return {"domains":[dict(x) for x in domains],"subjects":[dict(x) for x in subjects],"types":[dict(x) for x in kinds],"levels":[dict(x) for x in levels],"access": [dict(x) for x in accesses],"verification":[dict(x) for x in verification]}

def overview():
    with session() as conn:
        total=conn.execute("SELECT COUNT(*) FROM resources").fetchone()[0]
        verified=conn.execute("SELECT COUNT(*) FROM resources WHERE verification_level='page-check-recorded'").fetchone()[0]
        youtube=conn.execute("SELECT COUNT(*) FROM resources WHERE kind='video'").fetchone()[0]
        unknown_access=conn.execute("SELECT COUNT(*) FROM resources WHERE access_key='unknown'").fetchone()[0]
        domains=conn.execute("SELECT COUNT(*) FROM domains").fetchone()[0]
        subjects=conn.execute("SELECT COUNT(*) FROM subjects").fetchone()[0]
        paths=conn.execute("SELECT COUNT(*) FROM pathways").fetchone()[0]
    return {"resource_count":total,"domain_count":domains,"subject_count":subjects,"pathway_count":paths,"video_resources":youtube,"access_not_listed":unknown_access,"page_checks_recorded":verified,"progress_storage":"local-device-only"}

def list_paths():
    with session() as conn:
        rows=conn.execute("SELECT * FROM pathways ORDER BY title").fetchall()
    return [{**{k:v for k,v in dict(r).items() if k != "domain_ids_json"},"domain_ids":json.loads(r["domain_ids_json"])} for r in rows]

def get_path(path_id: str):
    with session() as conn:
        p=conn.execute("SELECT * FROM pathways WHERE id=?",(path_id,)).fetchone()
        if not p: return None
        steps=conn.execute("SELECT * FROM pathway_steps WHERE pathway_id=? ORDER BY position",(path_id,)).fetchall()
    result={**dict(p),"domain_ids":json.loads(p["domain_ids_json"]),"steps":[]}
    result.pop("domain_ids_json",None)
    for st in steps:
        step={**dict(st),"resource_ids":json.loads(st["resource_ids_json"])}
        step.pop("resource_ids_json",None)
        step["resources"]=[x for rid in step["resource_ids"] if (x:=get_resource(rid))]
        result["steps"].append(step)
    return result

def recommendations(resource_id: str, limit: int=6):
    base=get_resource(resource_id)
    if not base: return None
    subject_ids=[x["id"] for x in base["subjects"]]
    if not subject_ids: return {"items":[],"reason":"No shared subject tags are available for this resource."}
    placeholders=",".join("?" for _ in subject_ids)
    with session() as conn:
        rows=conn.execute(RESOURCE_SELECT+f" WHERE r.id<>? AND EXISTS (SELECT 1 FROM resource_subjects rx WHERE rx.resource_id=r.id AND rx.subject_id IN ({placeholders})) GROUP BY r.id ORDER BY COUNT(DISTINCT s.id) DESC,r.name COLLATE NOCASE LIMIT ?",[resource_id,*subject_ids,limit]).fetchall()
    return {"items":[_resource(x) for x in rows],"reason":"Related by shared subject tags in the catalog; this is a metadata-based match, not an AI judgement."}

def graph():
    with session() as conn:
        nodes=conn.execute("SELECT s.id,s.name,s.domain_id,COUNT(DISTINCT rs.resource_id) AS count FROM subjects s LEFT JOIN resource_subjects rs ON rs.subject_id=s.id GROUP BY s.id").fetchall()
        edges=conn.execute("SELECT a.subject_id AS source,b.subject_id AS target,COUNT(DISTINCT a.resource_id) AS weight FROM resource_subjects a JOIN resource_subjects b ON a.resource_id=b.resource_id AND a.subject_id<b.subject_id GROUP BY a.subject_id,b.subject_id HAVING weight>0 ORDER BY weight DESC LIMIT 70").fetchall()
    return {"nodes":[dict(x) for x in nodes],"edges":[dict(x) for x in edges],"method":"Edges represent catalog resources tagged with both subjects. They are co-occurrence signals, not claims of prerequisite or causal relationships."}
