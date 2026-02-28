def retrieve_node(state):

    retriever = state["retriever"]
    question = state["question"]

    docs = retriever.invoke(question)

    context = "\n\n".join([doc.page_content for doc in docs])

    return {
        "retrieved_docs": context
    }