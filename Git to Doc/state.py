from typing import TypedDict, Optional


class GraphState(TypedDict):
    # Input
    input_file_path: str

    # Code analysis
    code_content: Optional[str]
    current_hash: Optional[str]

    # Existing doc
    existing_doc: Optional[str]
    existing_version: Optional[str]
    last_hash: Optional[str]

    # LLM diff analysis
    has_changes: Optional[bool]           # True if LLM detects code changed
    change_summary: Optional[str]         # LLM summary of what changed
    code_analysis: Optional[str]          # LLM deep analysis of the code

    # Doc generation
    generated_doc: Optional[str]
    new_version: Optional[str]

    # QC
    qc_status: Optional[str]             # "passed" or "failed"
    qc_feedback: Optional[str]           # LLM feedback on the doc quality
    qc_attempts: Optional[int]           # retry counter

    # Output
    final_output_path: Optional[str]
