import os

DOCS_PATH = "data/docs"
HASH_FILE = "data/docs/.last_hash"


def save_doc_node(state: dict) -> dict:
    """
    Node 7 — Save Doc
    - Saves the final documentation as a versioned .md file
    - Updates the hash file for future change detection
    - Skips save if no changes were detected
    """
    print("\n💾 [Node 7] Save Doc: Saving documentation...")

    # If no changes, nothing to save
    if not state.get("has_changes", True):
        print("⚡ [Node 7] No changes detected. Nothing to save.")
        return {"final_output_path": None}

    if state.get("qc_status") != "passed":
        print("❌ [Node 7] QC not passed. Skipping save.")
        return {"final_output_path": None}

    os.makedirs(DOCS_PATH, exist_ok=True)

    version = state["new_version"]
    filename = f"doc_{version}.md"
    path = os.path.join(DOCS_PATH, filename)

    with open(path, "w") as f:
        f.write(state["generated_doc"])

    # Save current hash
    with open(HASH_FILE, "w") as f:
        f.write(state["current_hash"])

    print(f"✅ [Node 7] Documentation saved: {path}")
    return {"final_output_path": path}
