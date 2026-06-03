import os
from langchain_community.vectorstores import FAISS
from src.embeddings import get_embeddings
from src.config import settings

def save_to_vector_store(documents):
    embeddings = get_embeddings()
    # Check if index already exists
    index_path = os.path.join(settings.faiss_index_dir, "index.faiss")
    if os.path.exists(index_path):
        vector_store = FAISS.load_local(
            settings.faiss_index_dir, 
            embeddings,
            allow_dangerous_deserialization=True
        )
        vector_store.add_documents(documents)
    else:
        vector_store = FAISS.from_documents(documents, embeddings)
    
    vector_store.save_local(settings.faiss_index_dir)

def get_retriever():
    embeddings = get_embeddings()
    index_path = os.path.join(settings.faiss_index_dir, "index.faiss")
    if not os.path.exists(index_path):
        return None
        
    vector_store = FAISS.load_local(
        settings.faiss_index_dir, 
        embeddings,
        allow_dangerous_deserialization=True
    )
    return vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 4,
            "fetch_k": 10
        }
    )
