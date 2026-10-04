"""Utilities for embedding text chunks and persisting them in a FAISS index."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


def get_embedding_device() -> str:
    """Return the preferred device for embeddings.

    If CUDA is available, use it to accelerate local embeddings. Otherwise, fall
    back to CPU for reliable execution on standard machines.
    """
    try:
        import torch
        if torch.cuda.is_available():
            return "cuda"
    except Exception:
        pass
    return "cpu"


def build_faiss_index(
    chunks: list[dict[str, Any]],
    *,
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    index_path: str | Path | None = None,
) -> FAISS:
    """Create a FAISS vector store from chunk dictionaries.

    Each chunk is expected to match the output of ``chunk_documents()`` and must
    contain ``content``. The vector store stores the text in memory and can be
    serialized to disk if ``index_path`` is passed.
    """
    # FAISS indicizza il testo; i metadati vengono memorizzati accanto a ogni
    # testo, così la ricerca può restituire anche sorgente e indice del chunk.
    texts = [chunk["content"] for chunk in chunks]
    metadatas = [
        {"source": chunk["source"], "chunk_index": chunk["chunk_index"]}
        for chunk in chunks
    ]
    if not texts:
        raise ValueError("No chunks provided to create a vector store index.")

    device = get_embedding_device()
    # HuggingFaceEmbeddings trasforma ogni testo in un vettore numerico;
    # quel vettore permette a FAISS di confrontare il significato delle query.
    embeddings_model = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={"device": device},
    )

    # from_texts() abbina ogni testo al dizionario metadati nella stessa
    # posizione, calcola gli embedding e crea l'indice FAISS.
    vector_store = FAISS.from_texts(texts, embeddings_model, metadatas=metadatas)
    # Se richiesto, salva l'indice e i Document (testo più metadati) su disco.
    if index_path is not None:
        vector_store.save_local(str(index_path))
    return vector_store
