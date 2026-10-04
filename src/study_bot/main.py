"""Interactive command-line entrypoint for the local study chatbot."""

from __future__ import annotations

import sys
from collections.abc import Callable
from pathlib import Path

# Quando lo script è lanciato direttamente, Python aggiunge al percorso di
# ricerca la cartella che contiene study_bot, così gli import del package funzionano.
if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from study_bot.config import (
    RAG_CHUNK_OVERLAP,
    RAG_CHUNK_SIZE,
    RAG_EMBEDDING_MODEL,
    RAG_LLM_MODEL,
    RAG_TOP_K,
    get_documents_folder,
)


Answerer = Callable[[str], str]


def build_chatbot(
    *,
    documents_folder: str | Path | None = None,
    chunk_size: int = RAG_CHUNK_SIZE,
    chunk_overlap: int = RAG_CHUNK_OVERLAP,
    top_k: int = RAG_TOP_K,
    embedding_model: str = RAG_EMBEDDING_MODEL,
    llm_model: str = RAG_LLM_MODEL,
) -> tuple[Answerer, int, int]:
    """Load documents, build the search index and initialize the local LLM once."""
    # Importiamo i componenti qui, quando si costruisce davvero la chat: così
    # questo modulo può definire il loop CLI senza caricare subito i modelli pesanti.
    from study_bot.chunking import chunk_documents
    from study_bot.llm import answer_question, build_local_llm
    from study_bot.loaders import load_documents_from_folder
    from study_bot.vectorstore import build_faiss_index

    # Fase di preparazione, eseguita una sola volta all'avvio: carica i file,
    # li divide, crea l'indice per la ricerca e carica il modello generativo.
    documents = load_documents_from_folder(documents_folder)
    if not documents:
        raise ValueError(
            f"Nessun documento .txt, .md o .pdf trovato in {documents_folder or get_documents_folder()}"
        )

    chunks = chunk_documents(documents, chunk_size, chunk_overlap)
    if not chunks:
        raise ValueError("I documenti trovati non contengono testo indicizzabile.")

    vector_store = build_faiss_index(chunks, model_name=embedding_model)
    llm = build_local_llm(model_name=llm_model)

    # La funzione chiusa conserva indice e modello in memoria: ogni domanda
    # riusa gli stessi oggetti invece di ricostruirli.
    def answer(question: str) -> str:
        return answer_question(vector_store, question, k=top_k, llm=llm)

    return answer, len(documents), len(chunks)


def run_chat_loop(
    answerer: Answerer,
    *,
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
) -> None:
    """Read questions until the user enters an exit command or sends EOF."""
    # Il ciclo gestisce una domanda per volta, permette righe vuote e termina
    # con un comando esplicito oppure con Ctrl+C/fine input.
    output_fn("Chat pronta. Scrivi 'exit' o 'quit' per terminare.")
    while True:
        try:
            question = input_fn("Tu: ").strip()
        except (EOFError, KeyboardInterrupt):
            output_fn("\nSessione terminata.")
            return

        if question.lower() in {"exit", "quit", "/exit", "/quit"}:
            output_fn("Alla prossima!")
            return
        if not question:
            continue

        try:
            answer = answerer(question)
        except Exception as exc:
            output_fn(f"Errore durante la risposta: {exc}")
            continue
        output_fn(f"Bot: {answer}")


def main() -> int:
    """Initialize the RAG pipeline and start an interactive chat session."""
    # Verifica i parametri prima di inizializzare modelli e indice, così gli
    # errori di configurazione vengono segnalati subito e senza lavoro inutile.
    if RAG_TOP_K < 1:
        print("Configurazione non valida: RAG_TOP_K deve essere almeno 1.", file=sys.stderr)
        return 2
    if RAG_CHUNK_SIZE < 1 or not 0 <= RAG_CHUNK_OVERLAP < RAG_CHUNK_SIZE:
        print(
            "Configurazione non valida: RAG_CHUNK_SIZE deve essere positivo e "
            "RAG_CHUNK_OVERLAP tra 0 e RAG_CHUNK_SIZE - 1.",
            file=sys.stderr,
        )
        return 2

    documents_folder = get_documents_folder()
    print(f"Cartella documenti: {documents_folder}")
    print("Caricamento documenti, indice e modello (al primo avvio può richiedere tempo)...")
    try:
        answerer, document_count, chunk_count = build_chatbot(
            documents_folder=documents_folder,
            chunk_size=RAG_CHUNK_SIZE,
            chunk_overlap=RAG_CHUNK_OVERLAP,
            top_k=RAG_TOP_K,
            embedding_model=RAG_EMBEDDING_MODEL,
            llm_model=RAG_LLM_MODEL,
        )
    except Exception as exc:
        print(f"Impossibile avviare la chat: {exc}", file=sys.stderr)
        return 1

    print(f"Pronto: {document_count} documenti, {chunk_count} chunk indicizzati.")
    run_chat_loop(answerer)
    return 0


if __name__ == "__main__":
    # Converte il codice di uscita di main() nel codice di uscita del processo.
    raise SystemExit(main())