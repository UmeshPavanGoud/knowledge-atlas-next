from __future__ import annotations
import json, sqlite3, hashlib
from contextlib import contextmanager
from pathlib import Path
from .config import DB_PATH, DATA_DIR


def connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=20)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    return conn

@contextmanager
def session():
    conn = connect()
    try:
        yield conn
    finally:
        conn.close()

def _load_json(name: str):
    path = DATA_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Required Atlas data file is missing: {path}")
    return json.loads(path.read_text(encoding="utf-8"))

def initialize_database(force: bool = False) -> None:
    catalog = _load_json("catalog.json")
    taxonomy = _load_json("taxonomy.json")
    pathways = _load_json("pathways.json")
    fingerprint = hashlib.sha256(b"".join((DATA_DIR / name).read_bytes() for name in ("catalog.json", "taxonomy.json", "pathways.json"))).hexdigest()
    conn = connect()
    try:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS catalog_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS domains (
            id TEXT PRIMARY KEY, name TEXT NOT NULL, eyebrow TEXT NOT NULL,
            icon TEXT NOT NULL, description TEXT NOT NULL, color TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS subjects (
            id TEXT PRIMARY KEY, name TEXT NOT NULL, domain_id TEXT NOT NULL,
            description TEXT NOT NULL, FOREIGN KEY(domain_id) REFERENCES domains(id)
        );
        CREATE TABLE IF NOT EXISTS resources (
            id TEXT PRIMARY KEY, name TEXT NOT NULL, category TEXT NOT NULL,
            description TEXT NOT NULL, difficulty TEXT NOT NULL, level TEXT NOT NULL,
            resource_type TEXT NOT NULL, kind TEXT NOT NULL, best_for TEXT NOT NULL,
            access TEXT NOT NULL, access_key TEXT NOT NULL, url TEXT NOT NULL,
            platform_type TEXT NOT NULL, verification_status TEXT NOT NULL,
            verification_level TEXT NOT NULL, verification_label TEXT NOT NULL,
            focus_area TEXT NOT NULL, notes TEXT NOT NULL,
            provenance_json TEXT NOT NULL, source_categories_json TEXT NOT NULL,
            source_file TEXT NOT NULL, search_text TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS resource_subjects (
            resource_id TEXT NOT NULL, subject_id TEXT NOT NULL,
            PRIMARY KEY(resource_id, subject_id),
            FOREIGN KEY(resource_id) REFERENCES resources(id) ON DELETE CASCADE,
            FOREIGN KEY(subject_id) REFERENCES subjects(id)
        );
        CREATE INDEX IF NOT EXISTS idx_resources_kind ON resources(kind);
        CREATE INDEX IF NOT EXISTS idx_resources_level ON resources(level);
        CREATE INDEX IF NOT EXISTS idx_resources_access ON resources(access_key);
        CREATE INDEX IF NOT EXISTS idx_resource_subjects_subject ON resource_subjects(subject_id);
        CREATE TABLE IF NOT EXISTS pathways (
            id TEXT PRIMARY KEY, title TEXT NOT NULL, description TEXT NOT NULL,
            domain_ids_json TEXT NOT NULL, resource_count INTEGER NOT NULL,
            stage_count INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS pathway_steps (
            pathway_id TEXT NOT NULL, position INTEGER NOT NULL, title TEXT NOT NULL,
            description TEXT NOT NULL, resource_ids_json TEXT NOT NULL,
            PRIMARY KEY(pathway_id, position),
            FOREIGN KEY(pathway_id) REFERENCES pathways(id) ON DELETE CASCADE
        );
        """)
        current = conn.execute("SELECT value FROM catalog_meta WHERE key='catalog_version'").fetchone()
        if not force and current and current[0] == fingerprint:
            conn.close()
            return
        conn.execute("PRAGMA foreign_keys = OFF")
        for table in ["pathway_steps", "pathways", "resource_subjects", "resources", "subjects", "domains"]:
            conn.execute(f"DELETE FROM {table}")
        conn.execute("PRAGMA foreign_keys = ON")
        for d in taxonomy["domains"]:
            conn.execute("INSERT INTO domains VALUES (?,?,?,?,?,?)", (d["id"],d["name"],d["eyebrow"],d["icon"],d["description"],d["color"]))
        for s in taxonomy["subjects"]:
            if s.get("domain_id"):
                conn.execute("INSERT INTO subjects VALUES (?,?,?,?)", (s["id"],s["name"],s["domain_id"],s.get("description","")))
        for r in catalog:
            subjects = [s for s in r.get("subjects", []) if conn.execute("SELECT 1 FROM subjects WHERE id=?",(s,)).fetchone()]
            search_text = " ".join([r.get("name",""),r.get("description",""),r.get("best_for",""),r.get("focus_area",""),r.get("notes","")," ".join(subjects),r.get("category","")]).lower()
            values=(r["id"],r.get("name",""),r.get("category",""),r.get("description",""),r.get("difficulty","Unknown"),r.get("level","unknown"),r.get("resource_type",""),r.get("kind","other"),r.get("best_for",""),r.get("access","Unknown"),r.get("access_key","unknown"),r.get("url",""),r.get("platform_type",""),r.get("verification_status",""),r.get("verification_level","source-identified"),r.get("verification_label",""),r.get("focus_area",""),r.get("notes",""),json.dumps(r.get("provenance",[]),ensure_ascii=False),json.dumps(r.get("source_categories",[]),ensure_ascii=False),r.get("source_file",""),search_text)
            conn.execute("INSERT INTO resources VALUES (" + ",".join(["?"]*len(values)) + ")", values)
            for s in subjects:
                conn.execute("INSERT OR IGNORE INTO resource_subjects VALUES (?,?)",(r["id"],s))
        for p in pathways:
            conn.execute("INSERT INTO pathways VALUES (?,?,?,?,?,?)",(p["id"],p["title"],p["description"],json.dumps(p.get("domain_ids",[])),p.get("resource_count",0),p.get("stage_count",0)))
            for i,step in enumerate(p.get("stages",[]),1):
                conn.execute("INSERT INTO pathway_steps VALUES (?,?,?,?,?)",(p["id"],i,step.get("title",""),step.get("description",""),json.dumps(step.get("resource_ids",[]))))
        conn.execute("INSERT OR REPLACE INTO catalog_meta VALUES ('catalog_version',?)",(fingerprint,))
        conn.execute("INSERT OR REPLACE INTO catalog_meta VALUES ('resource_count',?)",(str(len(catalog)),))
        conn.commit()
    finally:
        conn.close()
