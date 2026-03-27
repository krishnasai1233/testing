from llm.llm_client import call_llm


def doc_regenerator_node(state: dict) -> dict:
    """
    Node 6 — Doc Regenerator (QC Retry)
    - Called only when QC fails
    - Uses the QC feedback to improve the document
    """
    print("\n🔁 [Node 6] Doc Regenerator: Improving doc based on QC feedback...")

    doc = state.get("generated_doc", "")
    code = state.get("code_content", "")
    feedback = state.get("qc_feedback", "")
    version = state.get("new_version", "")

    fix_prompt = f"""
You are a senior technical writer.

The documentation you generated previously FAILED quality control.

QC Feedback:
{feedback}

Fix ALL issues mentioned in the feedback and regenerate the complete documentation.

Version: {version}
Source Code:
```python
{code}
```

Previous (flawed) doc:
{doc}

Generate improved, complete, release-note quality Markdown documentation.
No filler. No generic sentences. Be precise, professional, and thorough.
"""

    improved_doc = call_llm(
        prompt=fix_prompt,
        system="You are a senior technical writer. Fix every QC issue precisely and regenerate perfect documentation."
    )

    print("✅ [Node 6] Regenerated improved documentation.")

    return {
        "generated_doc": improved_doc.strip()
    }
