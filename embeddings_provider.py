from langchain_mistralai import MistralAIEmbeddings

def get_embeddings():
    return MistralAIEmbeddings(model="mistral-embed")