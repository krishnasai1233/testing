from langgraph.graph import StateGraph, END
from state import GraphState

from nodes.code_analyzer import code_analyzer_node
from nodes.fetch_doc import fetch_doc_node
from nodes.diff_checker import diff_checker_node
from nodes.doc_generator import doc_generator_node
from nodes.qc import qc_node
from nodes.doc_regenerator import doc_regenerator_node
from nodes.save_doc import save_doc_node


# ─── Conditional edge: after diff_checker ───────────────────────────────────
def route_after_diff(state: GraphState) -> str:
    """If no changes detected, skip to save (which will also skip)."""
    if state.get("has_changes"):
        return "doc_generator"
    else:
        return "save_doc"


# ─── Conditional edge: after qc ─────────────────────────────────────────────
def route_after_qc(state: GraphState) -> str:
    """If QC failed and attempts remain, retry via regenerator."""
    if state.get("qc_status") == "passed":
        return "save_doc"
    else:
        return "doc_regenerator"


# ─── Build Graph ─────────────────────────────────────────────────────────────
builder = StateGraph(GraphState)

# Register nodes
builder.add_node("code_analyzer",    code_analyzer_node)
builder.add_node("fetch_doc",        fetch_doc_node)
builder.add_node("diff_checker",     diff_checker_node)
builder.add_node("doc_generator",    doc_generator_node)
builder.add_node("qc",               qc_node)
builder.add_node("doc_regenerator",  doc_regenerator_node)
builder.add_node("save_doc",         save_doc_node)

# Entry point
builder.set_entry_point("code_analyzer")

# Linear edges
builder.add_edge("code_analyzer",   "fetch_doc")
builder.add_edge("fetch_doc",       "diff_checker")

# Conditional: diff_checker → doc_generator OR save_doc
builder.add_conditional_edges(
    "diff_checker",
    route_after_diff,
    {
        "doc_generator": "doc_generator",
        "save_doc":      "save_doc"
    }
)

# Linear: doc_generator → qc
builder.add_edge("doc_generator", "qc")

# Conditional: qc → save_doc OR doc_regenerator
builder.add_conditional_edges(
    "qc",
    route_after_qc,
    {
        "save_doc":        "save_doc",
        "doc_regenerator": "doc_regenerator"
    }
)

# After regeneration, go back to qc
builder.add_edge("doc_regenerator", "qc")

# save_doc → END
builder.add_edge("save_doc", END)

# Compile
graph = builder.compile()


# ─── Runner ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("🚀 AI-Powered Documentation Generator")
    print("=" * 60)

    result = graph.invoke({
        "input_file_path": "data/input_code.py",
        "qc_attempts": 0
    })

    print("\n" + "=" * 60)
    if result.get("final_output_path"):
        print(f"✅ Documentation saved to: {result['final_output_path']}")
        print(f"📋 Version: {result.get('new_version')}")
        print(f"🔎 QC Status: {result.get('qc_status')}")
        if result.get("qc_feedback"):
            print(f"💬 QC Feedback: {result['qc_feedback'][:200]}...")
    elif not result.get("has_changes"):
        print("⚡ No changes detected. Documentation is already up to date.")
    else:
        print("❌ Documentation was not saved. Check QC status.")
    print("=" * 60)
