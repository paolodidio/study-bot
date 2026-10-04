import importlib

from study_bot.main import run_chat_loop


def test_run_chat_loop_answers_questions_and_skips_blank_input() -> None:
    questions = iter(["  ", "What is RAG?", "quit"])
    asked: list[str] = []
    output: list[str] = []

    def answerer(question: str) -> str:
        asked.append(question)
        return "Retrieval-augmented generation."

    run_chat_loop(
        answerer,
        input_fn=lambda _prompt: next(questions),
        output_fn=output.append,
    )

    assert asked == ["What is RAG?"]
    assert "Bot: Retrieval-augmented generation." in output
    assert output[-1] == "Alla prossima!"


def test_run_chat_loop_handles_end_of_input() -> None:
    output: list[str] = []

    def end_input(_prompt: str) -> str:
        raise EOFError

    run_chat_loop(lambda _question: "unused", input_fn=end_input, output_fn=output.append)

    assert output[-1] == "\nSessione terminata."


def test_main_builds_chat_from_environment_configuration(monkeypatch) -> None:
    cli = importlib.import_module("study_bot.main")
    captured: dict[str, object] = {}

    def fake_build_chatbot(**kwargs):
        captured.update(kwargs)
        return lambda _question: "answer", 3, 7

    monkeypatch.setattr(cli, "get_documents_folder", lambda: "docs")
    monkeypatch.setattr(cli, "build_chatbot", fake_build_chatbot)
    monkeypatch.setattr(cli, "run_chat_loop", lambda _answerer: None)

    assert cli.main() == 0
    assert captured == {
        "documents_folder": "docs",
        "chunk_size": cli.RAG_CHUNK_SIZE,
        "chunk_overlap": cli.RAG_CHUNK_OVERLAP,
        "top_k": cli.RAG_TOP_K,
        "embedding_model": cli.RAG_EMBEDDING_MODEL,
        "llm_model": cli.RAG_LLM_MODEL,
    }