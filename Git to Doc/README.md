# 📦 AI-Powered Documentation Generator

An intelligent, LangGraph-based pipeline that automatically generates and versions **professional release-note style documentation** for your Python code — powered by **Gemini 2.0 Flash**.

---

## ✨ Features

- 🤖 **LLM at every stage** — Gemini 2.0 Flash analyses, diffs, generates, and reviews
- 🔍 **Intelligent diff detection** — not just hash comparison, LLM checks if doc is actually outdated
- 📋 **Release-note quality docs** — structured like Stripe/GitHub release notes, not school essays
- 🔄 **Auto-versioning** — Version_1, Version_2, ... saved as separate `.md` files
- ✅ **LLM-powered QC** — reviews doc completeness and accuracy against actual code
- 🔁 **Auto-retry on QC fail** — regenerates with feedback, up to 2 attempts
- ⚡ **Smart skip** — if nothing changed, no LLM calls are wasted

---

## 🗂️ Project Structure

```
doc_gen/
├── main.py                  ← LangGraph entry point
├── state.py                 ← Shared GraphState (TypedDict)
├── requirements.txt
├── .env                     ← Your Gemini API key
│
├── llm/
│   └── llm_client.py        ← Gemini 2.0 Flash client
│
├── nodes/
│   ├── code_analyzer.py     ← Node 1: Read file + LLM code analysis
│   ├── fetch_doc.py         ← Node 2: Load existing doc + last hash
│   ├── diff_checker.py      ← Node 3: LLM-powered diff (hash + semantic)
│   ├── doc_generator.py     ← Node 4: Generate release-note docs
│   ├── qc.py                ← Node 5: LLM quality review
│   ├── doc_regenerator.py   ← Node 6: Fix doc using QC feedback
│   └── save_doc.py          ← Node 7: Save versioned .md + hash
│
├── utils/
│   ├── hash_utils.py        ← MD5 hashing
│   └── version_utils.py     ← Version tracking helpers
│
└── data/
    ├── input_code.py        ← ✏️  PUT YOUR CODE HERE
    └── docs/                ← Generated docs appear here
        ├── doc_Version_1.md
        ├── doc_Version_2.md
        └── .last_hash
```

---

## 🔀 LangGraph Flow

```
[code_analyzer]
      │  reads file, LLM analyses structure
      ▼
[fetch_doc]
      │  loads existing doc + saved hash
      ▼
[diff_checker]
      │  hash check → LLM semantic diff
      │
      ├─── has_changes=False ──────────────► [save_doc] → END
      │                                       (skips save, prints "up to date")
      └─── has_changes=True
                │
                ▼
        [doc_generator]
                │  generates release-note Markdown
                ▼
              [qc]
                │  LLM reviews doc vs code
                │
                ├─── PASS ───────────────────► [save_doc] → END
                │
                └─── FAIL
                          │
                          ▼
                  [doc_regenerator]
                          │  fixes using QC feedback
                          └──────────────► back to [qc]
                                           (max 2 retries, then force PASS)
```

---

## ▶️ How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Add your code
Put the Python file you want to document in:
```
data/input_code.py
```

### 3. Run
```bash
python main.py
```

### 4. Find your docs
```
data/docs/doc_Version_1.md   ← first run
data/docs/doc_Version_2.md   ← after code changes
...
```

---

## 🔁 What Happens on Each Run

| Scenario | Result |
|---|---|
| First run, no docs exist | Generates `Version_1` |
| Run again, code unchanged | Prints "up to date", nothing saved |
| Code changed, doc outdated | Generates new version (Version_2, 3, ...) |
| Code changed, doc still valid | LLM confirms no update needed |
| QC fails | Auto-regenerates with feedback, retries |

---

## 📄 Output Doc Format

Each generated `.md` file looks like a professional release note:

```
# 📦 Project Documentation
Version: Version_2 | Release Date: 2025-01-15 | Status: Updated Release

## 🚀 Overview
## 📋 Release Notes — Version_2
   ✅ What's New | 🔄 What Changed | ❌ What Was Removed
## 🔧 API Reference  (tables + examples per function)
## ⚙️ Dependencies
## 🧠 Technical Notes
## 📌 Known Limitations
## 📜 Changelog
```

---

## ⚙️ Configuration

Edit `.env` to change the API key:
```
GEMINI_API_KEY=your_key_here
```

Edit `nodes/qc.py` to change max retry attempts:
```python
MAX_QC_ATTEMPTS = 2  # increase for more retries
```

Edit `main.py` to point to a different input file:
```python
"input_file_path": "data/your_file.py"
```
