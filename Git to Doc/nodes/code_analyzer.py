from utils.hash_utils import generate_hash
from llm.llm_client import call_llm


def code_analyzer_node(state: dict) -> dict:
    """
    Node 1 — Code Analyzer
    - Reads the source code file
    - Generates a hash for change detection
    - Uses LLM to produce a structured analysis of the code (functions, classes, purpose, complexity)
    """
    print("\n📂 [Node 1] Code Analyzer: Reading source code...")

    with open(state["input_file_path"], "r") as f:
        code = f.read()

    current_hash = generate_hash(code)

    # LLM deeply analyses the code structure
    analysis_prompt = f"""
You are an expert code analyst. Analyse the following Python code thoroughly.

Return a structured JSON-like plain text with these sections:
- PURPOSE: What does this code do overall?
- FUNCTIONS: List each function/class with name, parameters, return type, and what it does.
- DEPENDENCIES: What modules or packages are imported?
- COMPLEXITY: Rate complexity as Low / Medium / High and explain briefly.
- EDGE_CASES: Any notable edge cases or potential issues?
- CHANGES_HINT: Key areas a maintainer should watch for in future updates.

Code:
```python
{code}
```
Be concise, precise, and technical.
"""

    print("🤖 [Node 1] LLM analysing code structure...")
    code_analysis = call_llm(
        prompt=analysis_prompt,
        system="You are a senior software engineer doing a deep technical code review. Be structured and precise."
    )

    return {
        "code_content": code,
        "current_hash": current_hash,
        "code_analysis": code_analysis.strip()
    }
