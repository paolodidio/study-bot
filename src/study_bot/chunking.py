"""Utilities for splitting loaded documents into searchable text chunks."""

from __future__ import annotations

from typing import Any


def split_text(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> list[str]:
    """Divide una stringa in blocchi di caratteri che possono sovrapporsi."""
    # chunk_size è il numero massimo di caratteri presi per ciascun blocco.
    # chunk_overlap è quanti caratteri finali di un blocco vogliamo ripetere
    # all'inizio del successivo, così il contesto non si interrompe al confine.
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")
    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be between zero and chunk_size - 1")
    if not text:
        return []

    # step è quanto spostiamo in avanti l'inizio del blocco a ogni iterazione.
    # Sottraiamo overlap da chunk_size: ad esempio 6 - 2 = 4. Il blocco legge
    # 6 caratteri, ma il successivo parte dopo 4, quindi riprende gli ultimi 2.
    step = chunk_size - chunk_overlap
    chunks: list[str] = []
    start = 0
    while start < len(text):
        # remaining conta i caratteri da start fino alla fine. Se ne restano
        # solo overlap, quei caratteri sono già nel blocco precedente: fermiamo
        # il ciclo per non aggiungere un frammento composto solo da duplicati.
        remaining = len(text) - start
        if chunks and remaining <= chunk_overlap:
            break

        # Lo slicing text[start:end] restituisce una nuova stringa: qui end è
        # start + chunk_size, quindi il blocco contiene al massimo chunk_size
        # caratteri. append() aggiunge proprio questa stringa alla lista chunks.
        chunks.append(text[start : start + chunk_size])

        # Non partiamo dalla fine del blocco: avanziamo solo di step. Siccome
        # step = chunk_size - overlap, quando overlap > 0 l'inizio si sposta
        # meno della lunghezza letta e i blocchi condividono quei caratteri.
        start += step
    return chunks


def chunk_documents(
    documents: list[dict[str, Any]],
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> list[dict[str, Any]]:
    """Split loaded documents and preserve their source in each chunk.

    Each item in ``documents`` is expected to have this shape::

        {"path": "notes.md", "content": "abcdefghij"}

    ``split_text()`` returns a list of strings for each document. For example,
    with ``chunk_size=6`` and ``chunk_overlap=2``::

        ["abcdef", "efghij"]

    The loop uses ``enumerate()`` to read both the position and the value of
    each chunk. On the example above, its iterations are::

        index=0, content="abcdef"
        index=1, content="efghij"

    ``index`` becomes the ``chunk_index`` metadata, while ``content`` becomes
    the text stored in that chunk. The resulting items are::

        {"source": "notes.md", "chunk_index": 0, "content": "abcdef"}
        {"source": "notes.md", "chunk_index": 1, "content": "efghij"}

    Args:
        documents: Loaded documents containing ``path`` and ``content``.
        chunk_size: Maximum number of characters in each chunk.
        chunk_overlap: Number of characters shared by neighboring chunks.
    """
    # Per ogni documento split_text() produce stringhe. enumerate() dà a ciascuna
    # stringa il suo indice; append() aggiunge alla lista un dizionario con il
    # testo del chunk e i suoi metadati (file sorgente e posizione nel file).
    chunks: list[dict[str, Any]] = []
    for document in documents:
        source = document["path"]
        for index, content in enumerate(
            split_text(document["content"], chunk_size, chunk_overlap)
        ):
            chunks.append(
                {
                    "source": source,
                    "chunk_index": index,
                    "content": content,
                }
            )
    return chunks