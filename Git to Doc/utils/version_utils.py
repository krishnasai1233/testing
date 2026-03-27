import os


def get_latest_doc(path: str):
    """
    Returns (filename, content, version_string) for the latest doc,
    or (None, None, None) if no docs exist.
    """
    if not os.path.exists(path):
        return None, None, None

    files = [f for f in os.listdir(path) if f.endswith(".md")]
    if not files:
        return None, None, None

    def version_num(fname):
        try:
            return int(fname.split("_")[-1].replace(".md", ""))
        except ValueError:
            return 0

    versions = sorted(files, key=version_num)
    latest = versions[-1]

    with open(os.path.join(path, latest), "r") as f:
        content = f.read()

    version = latest.replace("doc_", "").replace(".md", "")
    return latest, content, version


def next_version(existing_version: str) -> str:
    """Given 'Version_1' returns 'Version_2'."""
    try:
        num = int(existing_version.split("_")[-1])
        return f"Version_{num + 1}"
    except Exception:
        return "Version_1"
