"""Minimal study_bot package scaffold.

This package is the entrypoint for the project. It exposes a simple
version and the main startup helpers. Future modules will add loaders,
embeddings, retrievers, and LLM adapters.
"""

__version__ = "0.1.0"

from .main import main, run_demo

__all__ = ["__version__", "main", "run_demo"]
