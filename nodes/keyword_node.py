
def keyword_node(state):
    keywords = []
    used_terms = set()
    llm = state["llm"]

    for summary in state["summaries"]:
        prompt = f"""
        Extract 6 academic key terms from:

        {summary}

        Avoid repeating previously used terms:
        {list(used_terms)}
        """

        response = llm.invoke(prompt)
        terms = [k.strip("-• ") for k in response.content.split("\n") if k]

        cleaned = []
        for t in terms:
            if t.lower() not in used_terms:
                cleaned.append(t)
                used_terms.add(t.lower())

        keywords.append(cleaned[:6])

    return {"keywords": keywords}