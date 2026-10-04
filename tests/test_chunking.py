from study_bot.chunking import chunk_documents, split_text


def test_split_text_preserves_overlap_without_tiny_trailing_chunk() -> None:
    assert split_text("abcdefghij", chunk_size=6, chunk_overlap=2) == [
        "abcdef",
        "efghij",
    ]


def test_chunk_documents_preserves_source_and_index() -> None:
    chunks = chunk_documents(
        [{"path": "notes.md", "content": "abcdefghij"}],
        chunk_size=6,
        chunk_overlap=2,
    )

    assert chunks == [
        {"source": "notes.md", "chunk_index": 0, "content": "abcdef"},
        {"source": "notes.md", "chunk_index": 1, "content": "efghij"},
    ]


def test_split_text_rejects_invalid_chunk_settings() -> None:
    for chunk_size, chunk_overlap in ((0, 0), (5, 5), (5, -1)):
        try:
            split_text("text", chunk_size, chunk_overlap)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid chunk settings were accepted")