def summarize_node(state):

    llm = state["llm"]
    summaries = []
    rolling_context = ""

    for chunk in state["chunks"]:

        prompt = f"""
You are converting lecture content into clear and simple student notes.

Guidelines:
- Use plain and easy English.
- Keep explanations short and clear.
- Do NOT sound like a textbook.
- Do NOT add extra theory.
- Maintain continuity with previous notes.
- Do NOT repeat previous content.
- Keep important technical terms exactly as they appear

Previous notes:
{rolling_context}

New lecture section:
{chunk}

Return only the notes for this section.
"""

        response = llm.invoke(prompt)
        summary = response.content.strip()

        summaries.append(summary)

        # Keep rolling context limited to avoid token explosion
        rolling_context = "\n".join(summaries[-3:])

    return {
        "summaries": summaries
    }