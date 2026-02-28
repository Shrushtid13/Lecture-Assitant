from langgraph.graph import StateGraph, END
from graph_state import LectureState

from nodes.asr_node import asr_node
from nodes.clean_node import clean_node
from nodes.chunk_node import chunk_node
from nodes.topic_node import topic_node
from nodes.summarizer_node import summarize_node
from nodes.keyword_node import keyword_node
from nodes.validate_node import validate_node
from nodes.structure_node import structure_node

def build_graph():
    workflow = StateGraph(LectureState)

    workflow.add_node("asr", asr_node)
    workflow.add_node("clean", clean_node)
    workflow.add_node("chunk", chunk_node)
    workflow.add_node("topic", topic_node)
    workflow.add_node("summarize", summarize_node)
    workflow.add_node("keywords", keyword_node)
    workflow.add_node("validate", validate_node)
    workflow.add_node("structure", structure_node)

    workflow.set_entry_point("asr")

    workflow.add_edge("asr", "clean")
    workflow.add_edge("clean", "chunk")
    workflow.add_edge("chunk", "topic")
    workflow.add_edge("topic", "summarize")
    workflow.add_edge("summarize", "keywords")
    workflow.add_edge("keywords", "validate")

    workflow.add_conditional_edges(
        "validate",
        lambda state: "structure" if state["validation_passed"] else "chunk",
        {
            "structure": "structure",
            "chunk": "chunk"
        }
    )

    workflow.add_edge("structure", END)

    return workflow.compile()