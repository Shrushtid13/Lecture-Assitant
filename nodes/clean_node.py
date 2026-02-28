
def clean_node(state):
    text = " ".join([seg["text"] for seg in state["raw_segments"]])
    llm = state["llm"]

    prompt = f"""
    Clean the following lecture transcript:
    - Remove filler words
    - Remove unrelated personal stories
    - Convert Hinglish to formal English
    - Preserve academic content

    Transcript:
    {text}
    """

    response = llm.invoke(prompt)

    return {
        "cleaned_text": response.content,
        "global_context": response.content[:1000]
    }