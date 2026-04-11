import faiss
import numpy as np

dimension = 384
index = faiss.IndexFlatL2(dimension)
documents = []

def add_documents(chunks, embeddings):
    global documents
    index.add(np.array(embeddings))
    documents.extend(chunks)

def search(query_embedding, k=3):
    D, I = index.search(np.array([query_embedding]), k)
    return [documents[i] for i in I[0]]