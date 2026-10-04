"""Caricamento dei documenti locali supportati dal progetto."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pypdf import PdfReader

try:
    from .config import get_documents_folder
except ImportError:  # pragma: no cover - for direct script execution
    from config import get_documents_folder


SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf"}


def load_local_document(path: str | Path) -> str:
    """Load a local text or PDF document into a single string.

    Args:
        path: Path to a local file.

    Returns:
        The document content as a string.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file type is unsupported.
    """
    # Path rappresenta un percorso del filesystem e offre metodi per interrogarlo
    # e leggerlo. Accetta sia una stringa sia un Path già creato dal chiamante.
    document_path = Path(path)

    # exists() è un metodo di Path: restituisce True se il percorso esiste.
    if not document_path.exists():
        raise FileNotFoundError(f"Document not found: {document_path}")

    # suffix è una proprietà di Path (non una funzione): contiene l'estensione,
    # ad esempio ".PDF". lower() la uniforma a minuscolo prima del confronto.
    suffix = document_path.suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {suffix}")

    if suffix == ".pdf":
        # PdfReader apre il PDF e rende disponibili le sue pagine in reader.pages.
        reader = PdfReader(str(document_path))

        # extract_text() è un metodo di pypdf: restituisce il testo della pagina
        # come str, oppure None se non riesce a estrarlo. In quel caso usiamo "".
        pages = [page.extract_text() or "" for page in reader.pages]

        # join() unisce le stringhe delle pagine con un a capo; strip() rimuove
        # spazi e a capo superflui all'inizio e alla fine. Il risultato è str.
        return "\n".join(page for page in pages if page).strip()

    # read_text() è un metodo di pathlib.Path, disponibile su document_path.
    # Legge il file e restituisce il contenuto come stringa (str); encoding indica
    # che i byte del file vanno decodificati come UTF-8.
    return document_path.read_text(encoding="utf-8")


def load_documents_from_folder(
    folder_path: str | Path | None = None,
) -> list[dict[str, Any]]:
    """Load all supported documents from a folder by calling load_local_document per document.

    It scans the provided folder, or the configured folder when omitted, for
    supported files and returns dictionaries containing each document's path
    and content. This format is easy to pass to chunking and indexing stages.

    calls:
        - load_local_document for each supported file
    """
    # Il parametro può essere una stringa, un Path o None. Se è None, usiamo
    # la cartella predefinita definita nella configurazione del progetto.
    folder_path = Path(folder_path) if folder_path is not None else get_documents_folder()

    # iterdir() enumera gli elementi contenuti direttamente nella cartella;
    # sorted() li mette in ordine stabile per rendere ripetibile il caricamento.
    if not folder_path.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    # La lista conterrà un dizionario per ogni documento: path e content sono
    # stringhe, mentre il valore complessivo restituito è list[dict[str, Any]].
    documents: list[dict[str, Any]] = []
    for document_path in sorted(folder_path.iterdir()):
        # is_file() esclude le sottocartelle; controlliamo poi l'estensione per
        # ignorare file che questo loader non sa leggere.
        if document_path.is_file() and document_path.suffix.lower() in SUPPORTED_EXTENSIONS:
            documents.append(
                {
                    # Convertiamo Path in str per conservare un valore semplice
                    # da stampare o serializzare insieme al testo del documento.
                    "path": str(document_path),
                    # Riutilizziamo la funzione precedente: sceglie come leggere
                    # il singolo file e restituisce sempre il contenuto in str.
                    "content": load_local_document(document_path),
                }
            )

    return documents
# Cloud-backed loaders (Google Drive, OneDrive) were removed because they were
# only used by tests in this scaffold. The project remains offline-first and
# uses the configured local `KB_DOCUMENTS_FOLDER_PATH` for ingestion.
