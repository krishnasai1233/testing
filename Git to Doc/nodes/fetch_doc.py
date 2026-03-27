import os
from utils.version_utils import get_latest_doc

DOCS_PATH = "data/docs"
HASH_FILE = "data/docs/.last_hash"


def fetch_doc_node(state: dict) -> dict:
    """
    Node 2 — Fetch Doc
    - Loads the latest saved documentation (if any)
    - Loads the last saved code hash (if any)
    """
    print("\n📄 [Node 2] Fetch Doc: Loading existing documentation...")

    file, content, version = get_latest_doc(DOCS_PATH)

    last_hash = None
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as f:
            last_hash = f.read().strip()

    if content:
        print(f"✅ [Node 2] Found existing doc: {file} ({version})")
    else:
        print("ℹ️  [Node 2] No existing documentation found. Will create Version_1.")

    return {
        "existing_doc": content,
        "existing_version": version,
        "last_hash": last_hash
    }
