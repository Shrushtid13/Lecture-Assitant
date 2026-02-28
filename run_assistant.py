from graph_builder import build_graph
from formatter import DocumentFormatter

def run_langgraph_assistant(audio_path):

    graph = build_graph()

    result = graph.invoke({
        "audio_path": audio_path
    })

    formatter = DocumentFormatter()
    file_buffer = formatter.generate_docx(result["structured_notes"])

    return result["structured_notes"], file_buffer