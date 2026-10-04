"""Retriever utilities for selecting the most relevant chunks from a FAISS index."""

from __future__ import annotations

from typing import Any

from langchain_core.documents import Document


def get_relevant_documents(
    vector_store: Any,
    question: str,
    *,
    k: int = 2,
) -> list[Document]:
    """Restituisce i k chunk più simili semanticamente alla domanda."""
    # similarity_search è il metodo del vector store LangChain che confronta
    # la domanda con gli embedding e restituisce Document con il testo trovato.
    return vector_store.similarity_search(question, k=k)
