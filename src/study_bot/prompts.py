"""Prompt templates for the RAG answer generation flow."""

from __future__ import annotations


def build_system_prompt() -> str:
    """Restituisce le istruzioni generali che guidano il modello."""
    return (
        "You are a helpful assistant. Answer only using the provided context. "
        "If the answer is not in the context, say that the information is not available "
        "in the provided documents."
    )


def build_answer_prompt(context: str, question: str) -> str:
    """Inserisce contesto recuperato e domanda nel testo inviato al modello."""
    # La composizione usa solo stringhe Python: separa chiaramente contesto,
    # domanda e punto in cui il modello deve iniziare la risposta.
    return (
        "Answer the question using only the context below.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}\n\n"
        "Answer:"
    )
