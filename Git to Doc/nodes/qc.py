from llm.llm_client import call_llm

MAX_QC_ATTEMPTS = 2


def qc_node(state: dict) -> dict:
    """
    Node 5 — Quality Control (LLM-Powered)
    - Checks if the generated doc is complete, accurate, and release-note quality
    - Returns pass/fail with detailed LLM feedback
    - Tracks attempt count to prevent infinite loops
    """
    print("\n🔎 [Node 5] QC: Evaluating documentation quality...")

    doc = state.get("generated_doc", "")
    code = state.get("code_content", "")
    version = state.get("new_version", "")
    attempts = state.get("qc_attempts", 0)

    # Basic structural check first
    if not doc or len(doc.strip()) < 100:
        print("❌ [Node 5] QC FAILED: Document is empty or too short.")
        return {
            "qc_status": "failed",
            "qc_feedback": "Document is empty or too short. Regenerate entirely.",
            "qc_attempts": attempts + 1
        }

    if not version:
        print("❌ [Node 5] QC FAILED: Version is missing.")
        return {
            "qc_status": "failed",
            "qc_feedback": "Version field is missing from the document.",
            "qc_attempts": attempts + 1
        }

    # LLM quality review
    qc_prompt = f"""
You are a documentation quality auditor at a professional software company.

Review the following generated documentation against the source code.

Evaluate strictly on these criteria:
1. COMPLETENESS — Are ALL functions/classes documented?
2. ACCURACY — Do descriptions match what the code actually does?
3. RELEASE_QUALITY — Is it formatted like professional release notes (not a school essay)?
4. STRUCTURE — Does it have Overview, Release Notes, API Reference, Changelog sections?
5. EXAMPLES — Does each function have a usage example?
6. NO_FLUFF — Is it free of filler phrases like "this function adds two numbers"?

Respond STRICTLY in this format:
---
VERDICT: PASS or FAIL
SCORE: X/10
ISSUES:
- issue 1 (if any)
- issue 2 (if any)
FEEDBACK:
One paragraph of specific actionable feedback.
---

Source Code:
```python
{code}
```

Documentation:
{doc}
"""

    print("🤖 [Node 5] LLM reviewing documentation quality...")
    qc_response = call_llm(
        prompt=qc_prompt,
        system="You are a strict documentation QA engineer. Never approve mediocre docs. Hold high standards."
    )

    verdict = "PASS" if "VERDICT: PASS" in qc_response.upper() else "FAIL"

    # Extract feedback
    feedback = ""
    if "FEEDBACK:" in qc_response:
        feedback = qc_response.split("FEEDBACK:")[-1].strip()

    if verdict == "PASS":
        print(f"✅ [Node 5] QC PASSED.")
        return {
            "qc_status": "passed",
            "qc_feedback": feedback,
            "qc_attempts": attempts + 1
        }
    else:
        print(f"⚠️  [Node 5] QC FAILED (attempt {attempts + 1}). Feedback: {feedback[:100]}...")
        # Force pass after max attempts to avoid infinite loop
        if attempts + 1 >= MAX_QC_ATTEMPTS:
            print("⚠️  [Node 5] Max QC attempts reached. Forcing PASS.")
            return {
                "qc_status": "passed",
                "qc_feedback": "Forced pass after max attempts. " + feedback,
                "qc_attempts": attempts + 1
            }
        return {
            "qc_status": "failed",
            "qc_feedback": feedback,
            "qc_attempts": attempts + 1
        }
