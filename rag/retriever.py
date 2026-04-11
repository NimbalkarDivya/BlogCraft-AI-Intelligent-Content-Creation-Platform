from rag.embedder import get_embedding
from rag.vector_store import search

def retrieve_context(query):
    query_embedding = get_embedding(query)
    docs = search(query_embedding)
    return "\n".join(docs)