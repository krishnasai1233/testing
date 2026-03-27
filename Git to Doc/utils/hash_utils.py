import hashlib


def generate_hash(content: str) -> str:
    return hashlib.md5(content.encode()).hexdigest()
