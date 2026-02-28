from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_node(state):

    text = state["cleaned_text"]

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,        # characters, not words
        chunk_overlap=200,      # preserves context continuity
        separators=["\n\n", "\n", ".", " ", ""]
    )

    chunks = splitter.split_text(text)

    return {
        "chunks": chunks
    }