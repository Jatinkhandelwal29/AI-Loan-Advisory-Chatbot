import os
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_community.vectorstores import FAISS

from backend.config import EMBEDDING_MODEL, INDEX_DIR, TOP_K

_embeddings = FastEmbedEmbeddings(model_name=EMBEDDING_MODEL)

_vectorstore = None


def _index_path():
    return os.path.join(INDEX_DIR, "index")


def load_vectorstore():
    global _vectorstore
    path = _index_path()
    if os.path.exists(path):
        _vectorstore = FAISS.load_local(
            path, _embeddings, allow_dangerous_deserialization=True
        )
    return _vectorstore


def build_or_update_index(documents):
    global _vectorstore
    if not documents:
        return _vectorstore
    if _vectorstore is None:
        load_vectorstore()
    if _vectorstore is None:
        _vectorstore = FAISS.from_documents(documents, _embeddings)
    else:
        _vectorstore.add_documents(documents)
    _vectorstore.save_local(_index_path())
    return _vectorstore


def rebuild_index_from_scratch(all_documents):
    global _vectorstore
    _vectorstore = FAISS.from_documents(all_documents, _embeddings)
    _vectorstore.save_local(_index_path())
    return _vectorstore


def get_relevant_chunks(query: str, k: int = TOP_K):
    global _vectorstore
    if _vectorstore is None:
        load_vectorstore()
    if _vectorstore is None:
        return []
    return _vectorstore.similarity_search(query, k=k)


def index_is_ready() -> bool:
    global _vectorstore
    if _vectorstore is None:
        load_vectorstore()
    return _vectorstore is not None
