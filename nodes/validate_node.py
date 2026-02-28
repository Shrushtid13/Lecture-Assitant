def validate_node(state):
    llm = state["llm"]
    prompt = f"""
    Evaluate coherence of these lecture summaries:

    {state['summaries']}

    Are there:
    - Topic overlaps?
    - Redundancy?
    - Poor segmentation?

    Answer only YES or NO.
    """

    response = llm.invoke(prompt)

    if "NO" in response.content.upper():
        return {"validation_passed": True}
    else:
        return {"validation_passed": False}