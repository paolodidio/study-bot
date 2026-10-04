from study_bot.vectorstore import build_faiss_index, get_embedding_device


def test_get_embedding_device_uses_cpu_when_cuda_is_unavailable() -> None:
    device = get_embedding_device()
    assert device in {"cuda", "cpu"}


def test_build_faiss_index_returns_relevant_matches() -> None:
    chunks = [
        {"source": "notes.md", "chunk_index": 0, "content": "The cat sleeps on the sofa."},
        {"source": "notes.md", "chunk_index": 1, "content": "The dog barks loudly at night."},
    ]

    index = build_faiss_index(chunks)
    results = index.similarity_search("cat", k=1)

    assert len(results) == 1
    assert "cat" in results[0].page_content.lower()
    assert results[0].metadata == {"source": "notes.md", "chunk_index": 0}
