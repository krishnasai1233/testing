from llm.llm_client import call_llm


def diff_checker_node(state: dict) -> dict:
    """
    Node 3 — Diff Checker (LLM-Powered)
    - If no existing doc: mark has_changes=True, proceed to generation
    - If hash matches exactly: no changes at all
    - Otherwise: ask LLM to intelligently compare code vs existing doc
      and find what is NEW, CHANGED, or REMOVED that is NOT reflected in the doc
    """
    print("\n🔍 [Node 3] Diff Checker: Detecting changes...")

    code = state.get("code_content", "")
    existing_doc = state.get("existing_doc")
    last_hash = state.get("last_hash")
    current_hash = state.get("current_hash")

    # No doc at all — first time
    if not existing_doc:
        print("✅ [Node 3] No existing doc. Will generate fresh documentation.")
        return {
            "has_changes": True,
            "change_summary": "Initial documentation — no prior doc exists."
        }

    # Hash identical — definitely no change
    if last_hash and last_hash == current_hash:
        print("⚡ [Node 3] Hash match. Code unchanged. Skipping generation.")
        return {
            "has_changes": False,
            "change_summary": "No changes detected. Code hash matches last saved hash."
        }

    # Hash differs — ask LLM to do intelligent diff
    print("🤖 [Node 3] LLM performing intelligent diff analysis...")

    diff_prompt = f"""
You are a senior technical writer and code reviewer.

Compare the following Python source code against its existing documentation.

Your job:
1. Identify what is NEW in the code that is NOT documented.
2. Identify what has CHANGED in the code that makes the doc outdated.
3. Identify what was REMOVED from code that is still mentioned in the doc.
4. Determine if a documentation update is REQUIRED or NOT.

Respond STRICTLY in this format:
---
NEEDS_UPDATE: YES or NO
NEW_ITEMS:
- list each new function/class/feature not in doc
CHANGED_ITEMS:
- list each changed part
REMOVED_ITEMS:
- list each removed part
SUMMARY:
One paragraph summarising all changes for a release note.
---

Source Code:
```python
{code}
```

Existing Documentation:
{existing_doc}
"""

    llm_response = call_llm(
        prompt=diff_prompt,
        system="You are a precise technical documentation auditor. Never guess. Only report facts visible in the code and doc."
    )

    # Parse LLM response
    needs_update = "NEEDS_UPDATE: YES" in llm_response.upper()

    # Extract SUMMARY block
    summary = ""
    if "SUMMARY:" in llm_response:
        summary = llm_response.split("SUMMARY:")[-1].strip()

    if needs_update:
        print(f"⚠️  [Node 3] Changes detected. Doc update required.")
    else:
        print("✅ [Node 3] LLM confirmed: doc is up to date.")

    return {
        "has_changes": needs_update,
        "change_summary": summary or llm_response.strip()
    }
