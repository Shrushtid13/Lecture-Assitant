def normalize_node(state):

    llm = state["llm"]

    text = " ".join(state["filtered_sentences"])

    prompt = f"""
The following lecture contains English mixed with Hindi.

Convert it into clear academic English.
Preserve technical meaning.
Do NOT summarize.
Do NOT remove content.

Text:
{text}
"""

    response = llm.invoke(prompt)

    return {
        "cleaned_text": response.content
    }