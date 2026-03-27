from llm.llm_client import call_llm
from utils.version_utils import next_version


def doc_generator_node(state: dict) -> dict:
    """
    Node 4 — Doc Generator
    - Skips if has_changes is False
    - Generates release-note style Markdown documentation
    - For Version_1: full initial documentation
    - For Version_N: incremental release notes with changelog
    """
    print("\n✍️  [Node 4] Doc Generator: Generating documentation...")

    # Skip if no changes
    if not state.get("has_changes", True):
        print("⚡ [Node 4] No changes. Reusing existing doc.")
        return {
            "generated_doc": state.get("existing_doc"),
            "new_version": state.get("existing_version")
        }

    code = state.get("code_content", "")
    code_analysis = state.get("code_analysis", "")
    change_summary = state.get("change_summary", "")
    existing_doc = state.get("existing_doc")
    existing_version = state.get("existing_version")

    # Version calculation
    if not existing_doc:
        new_version = "Version_1"
    else:
        new_version = next_version(existing_version)

    print(f"📝 [Node 4] Generating {new_version}...")

    # ---- INITIAL DOCUMENTATION (Version_1) ----
    if not existing_doc:
        prompt = f"""
You are a world-class technical documentation engineer.

Generate professional, release-note style Markdown documentation for this Python code.

This is VERSION 1 — the initial release documentation.

STRICT FORMAT TO FOLLOW:

---
# 📦 Project Documentation

**Version:** {new_version}
**Release Date:** {__import__('datetime').date.today()}
**Status:** Initial Release

---

## 🚀 Overview
Describe clearly what this project/module does, its purpose, and who would use it.

---

## 📋 Release Notes — {new_version}
### What's New
- Bullet list of everything introduced in this version

---

## 🔧 API Reference

For each function or class:

### `function_name(params)`
| Field | Detail |
|---|---|
| **Description** | What it does |
| **Parameters** | param: type — description |
| **Returns** | type — description |
| **Raises** | Any exceptions |

**Example:**
```python
# usage example
```

---

## ⚙️ Dependencies
List all imports and external packages used.

---

## 🧠 Technical Notes
- Any important implementation details, edge cases, or warnings

---

## 📌 Known Limitations
- What this version does NOT handle

---

Code Analysis:
{code_analysis}

Source Code:
```python
{code}
```

Generate ONLY clean professional Markdown. No filler. No generic boilerplate. Be precise and technical.
"""
    # ---- INCREMENTAL UPDATE ----
    else:
        prompt = f"""
You are a world-class technical documentation engineer.

Update the existing documentation to produce a new version with proper release notes.

New Version: {new_version}
Previous Version: {existing_version}

Change Analysis:
{change_summary}

STRICT FORMAT TO FOLLOW:

---
# 📦 Project Documentation

**Version:** {new_version}
**Release Date:** {__import__('datetime').date.today()}
**Status:** Updated Release
**Previous Version:** {existing_version}

---

## 🚀 Overview
(Update if the overall purpose changed, otherwise keep concise.)

---

## 📋 Release Notes — {new_version}
### ✅ What's New
- List NEW functions/features added

### 🔄 What Changed
- List MODIFIED functions/behaviour

### ❌ What Was Removed
- List anything deprecated or removed

### 🐛 Bug Fixes / Improvements
- Any improvements (if applicable)

---

## 🔧 API Reference
(Full updated API reference — include ALL functions, updated or not)

For each function or class:

### `function_name(params)`
| Field | Detail |
|---|---|
| **Description** | What it does |
| **Parameters** | param: type — description |
| **Returns** | type — description |
| **Raises** | Any exceptions |

**Example:**
```python
# usage example
```

---

## ⚙️ Dependencies
Updated list.

---

## 🧠 Technical Notes
Updated notes.

---

## 📌 Known Limitations
Updated limitations.

---

## 📜 Changelog
| Version | Date | Summary |
|---|---|---|
| {new_version} | {__import__('datetime').date.today()} | (summarise this update in one line) |
(copy previous changelog rows here if they exist in old doc)

---

Code Analysis:
{code_analysis}

Source Code:
```python
{code}
```

Existing Documentation for reference:
{existing_doc}

Generate ONLY clean professional Markdown. Precise, technical, release-note quality.
"""

    generated_doc = call_llm(
        prompt=prompt,
        system="You are a senior technical writer at a software company. Your documentation reads like professional release notes from companies like Stripe, GitHub, or AWS. Always be precise, structured, and developer-friendly."
    )

    print(f"✅ [Node 4] Documentation generated for {new_version}.")

    return {
        "generated_doc": generated_doc.strip(),
        "new_version": new_version
    }
