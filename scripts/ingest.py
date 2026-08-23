"""Simple ingestion test script.

Creates temporary documents, points the configured documents folder at them,
then calls `load_documents_from_folder()` and `load_local_document()` to
exercise the loader functionality.

Run from repository root with:

    python scripts/ingest.py

"""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

# Make sure the package can be imported from the local `src` folder.
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from study_bot.loaders import load_documents_from_folder, load_local_document
from study_bot.config import get_documents_folder


def write_sample_files(folder: Path) -> None:
    (folder / "notes.txt").write_text("hello from a text document", encoding="utf-8")
    (folder / "guide.md").write_text("# Study guide\n\nUse this note to revise.", encoding="utf-8")



def main() -> int:
    print("Ingest test script — exercising loaders")

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        write_sample_files(tmp)

        # `study_bot.config` loads the `.env` and exposes the configured folder.
        print(f"Configured documents folder -> {get_documents_folder()}")

        try:
            docs = load_documents_from_folder()
        except Exception as exc:
            print("load_documents_from_folder() raised:", repr(exc))
            return 2

        print(f"Loaded {len(docs)} document(s)")
        for i, d in enumerate(docs, 1):
            print(f"{i}. {d['path']} — {len(d['content'])} chars")

        # Call single-file loader on the first document (if present)
        if docs:
            first_path = Path(docs[0]["path"])
            try:
                content = load_local_document(first_path)
                print("\nContent preview (first document):\n", content[:200])
            except Exception as exc:
                print("load_local_document() raised:", repr(exc))
                return 3

        # PDF support is expected to be provided by the environment if needed.

    print("Done")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
