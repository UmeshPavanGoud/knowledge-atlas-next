from pathlib import Path
import os

PROJECT_ROOT = next((parent for parent in Path(__file__).resolve().parents if (parent / "data").is_dir()), Path(__file__).resolve().parents[-1])
DATA_DIR = Path(os.getenv("ATLAS_DATA_DIR", PROJECT_ROOT / "data")).resolve()
DB_PATH = Path(os.getenv("ATLAS_DB_PATH", PROJECT_ROOT / ".local" / "atlas.db")).resolve()
API_PREFIX = "/api/v1"
