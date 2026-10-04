"""Central configuration for the study_bot project.

This module keeps project-wide settings in one place so they can be reused by
multiple modules without hardcoding values in several files.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


# __file__ è il percorso di questo file. Path.resolve() lo rende assoluto e
# parents[2] risale dalla cartella del package alla radice del repository.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# python-dotenv legge le coppie NOME=valore da .env e le rende disponibili
# tramite os.getenv(). Il file non è obbligatorio: sotto ci sono valori predefiniti.
load_dotenv(dotenv_path=PROJECT_ROOT / ".env")


# Questa cartella contiene i documenti da caricare; os.getenv() usa il valore
# di .env o, se manca, il percorso predefinito indicato qui.
KB_DOCUMENTS_FOLDER_PATH = os.getenv("KB_DOCUMENTS_FOLDER_PATH", "C:\\My code\\docs-rag")

# Core runtime settings for the project.
STUDY_BOT_MODE = os.getenv("STUDY_BOT_MODE", "tutorial")
STUDY_BOT_NAME = os.getenv("STUDY_BOT_NAME", "study_bot")

# I parametri numerici arrivano da .env come testo, quindi int() li converte
# in interi prima che chunking e retrieval li usino.
RAG_CHUNK_SIZE = int(os.getenv("RAG_CHUNK_SIZE", "500"))
RAG_CHUNK_OVERLAP = int(os.getenv("RAG_CHUNK_OVERLAP", "50"))
RAG_TOP_K = int(os.getenv("RAG_TOP_K", "2"))
RAG_EMBEDDING_MODEL = os.getenv(
    "RAG_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
)
RAG_LLM_MODEL = os.getenv("RAG_LLM_MODEL", "google/flan-t5-small")


def get_documents_folder() -> Path:
    """Restituisce come Path la cartella documenti scelta nella configurazione."""
    return Path(KB_DOCUMENTS_FOLDER_PATH)
