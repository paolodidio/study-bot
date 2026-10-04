"""Load and preview the local documents configured for study_bot.

Run from repository root with:

    python scripts/ingest.py

"""
from __future__ import annotations

import sys
from pathlib import Path

# Make sure the package can be imported from the local `src` folder.
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from study_bot.config import get_documents_folder
from study_bot.loaders import load_documents_from_folder


def main() -> int:
    folder = get_documents_folder()
    print(f"Configured documents folder -> {folder}")

    try:
        docs = load_documents_from_folder()
    except Exception as exc:
        print("load_documents_from_folder() raised:", repr(exc))
        return 2

    print(f"Loaded {len(docs)} document(s)")
    for index, document in enumerate(docs, 1):
        print(f"{index}. {document['path']} — {len(document['content'])} chars")

    if docs:
        print("\nContent preview (first document):\n", docs[0]["content"][:200])

    print("Done")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
