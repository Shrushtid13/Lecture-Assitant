from langgraph.graph import StateGraph, END
from typing import TypedDict, Any


class QAState(TypedDict, total=False):
    question: str
    retriever: Any
    retrieved_docs: str
    answer: str
    llm: Any

from nodes.retrieve_node import retrieve_node
from nodes.answer_node import answer_node


def build_qa_graph():

    workflow = StateGraph(QAState)

    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("answer", answer_node)

    workflow.set_entry_point("retrieve")

    workflow.add_edge("retrieve", "answer")
    workflow.add_edge("answer", END)

    return workflow.compile()