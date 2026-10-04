from study_bot.retriever import get_relevant_documents
from study_bot.llm import answer_question
from study_bot.vectorstore import build_faiss_index


def test_get_relevant_documents_returns_matching_chunk() -> None:
    chunks = [
        {"source": "notes.md", "chunk_index": 0, "content": "The cat sleeps on the sofa."},
        {"source": "notes.md", "chunk_index": 1, "content": "The dog barks loudly at night."},
    ]

    vector_store = build_faiss_index(chunks)
    docs = get_relevant_documents(vector_store, "What is the cat doing?")

    assert len(docs) == 2
    assert "cat" in docs[0].page_content.lower()


def test_answer_question_uses_context() -> None:
    chunks = [
        {"source": "notes.md", "chunk_index": 0, "content": "The cat sleeps on the sofa."},
        {"source": "notes.md", "chunk_index": 1, "content": "The dog barks loudly at night."},
    ]

    vector_store = build_faiss_index(chunks)
    answer = answer_question(vector_store, "What is the cat doing?")

    assert isinstance(answer, str)
    assert len(answer) > 0
