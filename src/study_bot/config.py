"""Central configuration for the study_bot project.

This module keeps project-wide settings in one place so they can be reused by
multiple modules without hardcoding values in several files.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


# Root of the repository where the package lives.
# For this project it resolves to: C:\My code\study-bot
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Load environment variables from a local .env file if present.
# Place the file at: C:\My code\study-bot\.env
load_dotenv(dotenv_path=PROJECT_ROOT / ".env")


# Path to the folder containing the local documents to ingest.
KB_DOCUMENTS_FOLDER_PATH = os.getenv("KB_DOCUMENTS_FOLDER_PATH", "C:\\My code\\docs-rag")

# Core runtime settings for the project.
STUDY_BOT_MODE = os.getenv("STUDY_BOT_MODE", "tutorial")
STUDY_BOT_NAME = os.getenv("STUDY_BOT_NAME", "study_bot")


def get_documents_folder() -> Path:
    """Return the configured documents folder as a Path object."""
    return Path(KB_DOCUMENTS_FOLDER_PATH)
