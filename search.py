import faiss
from embedder import model

def create_faiss_index(pdf_embeddings, question, dimension):
    index = faiss.IndexFlatL2(dimension)
    index.is_trained = True
    index.add(pdf_embeddings.astype("float32"))

    query_vector = model.encode([question]).astype("float32")
    D, I = index.search(query_vector.reshape(1, -1), k=5)
    return I
    

    
