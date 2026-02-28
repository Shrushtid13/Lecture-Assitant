def relevance_node(state):

    llm = state["llm"]
    sentences = state["sentences"]

    filtered = []

    for s in sentences:

        prompt = f"""
You are analyzing a university-level lecture transcript.

Definitions:
ACADEMIC_CONTENT = teaching theory, definitions, formulas
EXAMPLE_SUPPORTING = example explaining a concept
PERSONAL_ANECDOTE = personal life stories not needed for understanding
FILLER = greetings, hesitation, apologies

Classify strictly.

Sentence:
{s}

Return only one label.
"""

        response = llm.invoke(prompt)
        label = response.content.strip()

        if label in ["ACADEMIC_CONTENT", "EXAMPLE_SUPPORTING"]:
            filtered.append(s)

    return {
        "filtered_sentences": filtered
    }