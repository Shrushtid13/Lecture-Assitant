def topic_node(state):

    llm = state["llm"]
    topics = []

    for chunk in state["chunks"]:

        prompt = f"""
You are analyzing university-level lecture content.

Generate a concise academic topic title (maximum 8 words)
based strictly on the content below.

Rules:
- Do not explain
- Do not include quotation marks
- Do not include introductory text
- Return only the title

Lecture Content:
{chunk}
"""

        response = llm.invoke(prompt)
        topics.append(response.content.strip())

    return {
        "topics": topics
    }