def answer_node(state):

    llm = state["llm"]
    question = state["question"]
    context = state["retrieved_docs"]

    prompt = f"""
You are a lecture Q&A assistant.

Answer the question strictly using the provided lecture context.
Always base your answer on the context. Do not use any outside knowledge.
Always answer in clear, simple English suitable for university students.
If the answer is not in the context, say:
"Answer not found in lecture material."

Lecture Context:
{context}

Question:
{question}

Answer clearly and academically.
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content.strip()
    }