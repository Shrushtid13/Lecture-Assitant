def structure_node(state):
    structured = []

    for i in range(len(state["topics"])):
        structured.append({
            "topic": state["topics"][i],
            "summary": state["summaries"][i],
            "keywords": state["keywords"][i]
        })

    return {"structured_notes": structured}