"""Document loading helpers for the study_bot project.

The loader module is intentionally simple and explicit. It focuses on the
offline-first path first: local files are supported directly, while cloud-backed
loaders are implemented as placeholders with clear guidance for future
integration. This keeps the package usable in a local development workflow
without requiring credentials or network access.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    from .config import get_documents_folder
except ImportError:  # pragma: no cover - for direct script execution
    from config import get_documents_folder

try:
    from pypdf import PdfReader  # type: ignore
except ImportError:  # pragma: no cover - exercised only when optional dep is absent
    PdfReader = None  # type: ignore[assignment]


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
        RuntimeError: If the PDF dependency is missing.
    """
    document_path = Path(path)
    if not document_path.exists():
        raise FileNotFoundError(f"Document not found: {document_path}")

    suffix = document_path.suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {suffix}")

    if suffix == ".pdf":
        if PdfReader is None:
            raise RuntimeError(
                "PDF support requires the optional dependency 'pypdf'. Install it "
                "with 'pip install pypdf'."
            )

        reader = PdfReader(str(document_path))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(page for page in pages if page).strip()

    return document_path.read_text(encoding="utf-8")


def load_documents_from_folder() -> list[dict[str, Any]]:
    """Load all supported documents from a folder by calling load_local_document per document.

    It scans for supported files and returns a list of dictionaries with the
    content and path for each document. This format is easy to adapt later to
    embeddings or indexing pipelines.

    calls:
        - load_local_document for each supported file
    """
    folder_path = get_documents_folder()
    if not folder_path.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    documents: list[dict[str, Any]] = []
    for document_path in sorted(folder_path.iterdir()):
        if document_path.is_file() and document_path.suffix.lower() in SUPPORTED_EXTENSIONS:
            documents.append(
                {
                    "path": str(document_path),
                    "content": load_local_document(document_path),
                }
            )

    return documents
# Cloud-backed loaders (Google Drive, OneDrive) were removed because they were
# only used by tests in this scaffold. The project remains offline-first and
# uses the configured local `KB_DOCUMENTS_FOLDER_PATH` for ingestion.
