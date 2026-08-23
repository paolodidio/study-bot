"""Entrypoint module for the study_bot scaffold.

This module is intentionally simple and tutorial-friendly. It runs directly
without requiring command-line arguments and can load small configuration
values from a local .env file or use sensible hardcoded defaults.
"""

from __future__ import annotations

from pathlib import Path

try:
    from .config import STUDY_BOT_MODE, STUDY_BOT_NAME, get_documents_folder
except ImportError:  # pragma: no cover - for direct script execution
    from config import STUDY_BOT_MODE, STUDY_BOT_NAME, get_documents_folder


def build_project_intro() -> str:
    """Return a short explanatory startup string for the scaffold.

    This message acts like a mini tutorial for a new contributor:
    it explains what the project is, why the architecture matters,
    and what each stage of the RAG pipeline will do.
    """
    return (
        "study_bot is an offline-first RAG chatbot scaffold.\n"
        "The idea is simple: collect documents, turn them into searchable context,\n"
        "and use that context to answer questions more reliably.\n"
        "In future steps, you will add loaders, embeddings, a vector store,\n"
        "a retriever, and an LLM interface."
    )


def load_settings() -> dict[str, str | Path]:
    """Load the runtime settings from the shared config module."""
    return {
        "STUDY_BOT_MODE": STUDY_BOT_MODE,
        "STUDY_BOT_NAME": STUDY_BOT_NAME,
        "STUDY_BOT_DOCUMENTS_FOLDER": str(get_documents_folder()),
    }


def main() -> int:
    """Run the tutorial-style startup flow without any arguments.

    This entrypoint is designed to be executed directly with:
    python src/study_bot/main.py
    """
    settings = load_settings()

    print(build_project_intro())
    print()
    print("What you are looking at:")
    print("- a minimal package structure for a chatbot project")
    print("- a starting point for future RAG components")
    print("- a simple direct-run entrypoint for learning and experimentation")
    print()
    print("Configuration:")
    print(f"- mode: {settings['STUDY_BOT_MODE']}")
    print(f"- name: {settings['STUDY_BOT_NAME']}")
    print(f"- documents folder: {settings['STUDY_BOT_DOCUMENTS_FOLDER']}")
    print()
    print("Project source package:", Path(__file__).resolve().parent)
    print("Next step: add a loader, retriever, or LLM adapter.")
    return 0


def run_demo() -> str:
    """Return the demo string for programmatic use and tests."""
    return build_project_intro()


if __name__ == "__main__":
    raise SystemExit(main())
