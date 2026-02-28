from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict, Any



# STATE DEFINITION

class NoteState(TypedDict, total=False):
    audio_path: str
    sentences: List[str]
    filtered_sentences: List[str]
    cleaned_text: str
    chunks: List[str]
    topics: List[str]
    summaries: List[str]
    keywords: List[List[str]]
    structured_notes: List[Dict]
    validation_passed: bool
    llm: Any



# NODE IMPORTS


from nodes.asr_node import asr_node
from nodes.relevance_node import relevance_node
from nodes.normalize_node import normalize_node
from nodes.chunk_node import chunk_node
from nodes.topic_node import topic_node
from nodes.summarizer_node import summarize_node
from nodes.keyword_node import keyword_node
from nodes.validate_node import validate_node
from nodes.structure_node import structure_node



# GRAPH BUILDER


def build_note_graph():

    workflow = StateGraph(NoteState)

    # Add nodes
    workflow.add_node("asr", asr_node)
    workflow.add_node("relevance", relevance_node)
    workflow.add_node("normalize", normalize_node)
    workflow.add_node("chunk", chunk_node)
    workflow.add_node("topic", topic_node)
    workflow.add_node("summarize", summarize_node)
    workflow.add_node("keywords", keyword_node)
    workflow.add_node("validate", validate_node)
    workflow.add_node("structure", structure_node)

    # Entry point
    workflow.set_entry_point("asr")

    # Proper pipeline flow
    workflow.add_edge("asr", "relevance")
    workflow.add_edge("relevance", "normalize")
    workflow.add_edge("normalize", "chunk")
    workflow.add_edge("chunk", "topic")
    workflow.add_edge("topic", "summarize")
    workflow.add_edge("summarize", "keywords")
    workflow.add_edge("keywords", "validate")

    # Validation loop
    workflow.add_conditional_edges(
        "validate",
        lambda state: "structure" if state.get("validation_passed") else "chunk",
        {
            "structure": "structure",
            "chunk": "chunk"
        }
    )

    workflow.add_edge("structure", END)

    return workflow.compile()