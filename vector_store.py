from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
import os


def build_vector_store(structured_notes, embeddings, lecture_id):

    docs = []

    for i, section in enumerate(structured_notes):

        content = f"""
Topic: {section['topic']}

Summary:
{section['summary']}

Keywords:
{", ".join(section['keywords'])}
"""

        docs.append(
            Document(
                page_content=content,
                metadata={
                    "topic": section["topic"],
                    "index": i
                }
            )
        )

    # Persist directory
    persist_dir = "chroma_db"
    os.makedirs(persist_dir, exist_ok=True)

    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=persist_dir,
        collection_name= lecture_id
    )

    return vectorstore