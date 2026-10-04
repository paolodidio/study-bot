"""Minimal LLM adapter for grounding answers in retrieved context."""

from __future__ import annotations

from typing import Any

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from study_bot.prompts import build_answer_prompt, build_system_prompt


def build_local_llm(
    *,
    model_name: str = "google/flan-t5-small",
    max_new_tokens: int = 128,
) -> dict[str, Any]:
    """Build a lightweight local seq2seq model for the tutorial pipeline."""
    # PyTorch sceglie GPU se CUDA è disponibile, altrimenti CPU. Il tokenizer
    # converte testo in token e il modello genera token di risposta.
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)
    # eval() mette il modello in modalità inferenza (non addestramento), adatta
    # alle risposte e più stabile per l'esecuzione.
    model.eval()
    return {
        "tokenizer": tokenizer,
        "model": model,
        "device": device,
        "max_new_tokens": max_new_tokens,
    }


def answer_question(
    vector_store: Any,
    question: str,
    *,
    k: int = 2,
    model_name: str = "google/flan-t5-small",
    llm: dict[str, Any] | None = None,
) -> str:
    """Retrieve context from the vector store and answer using a local model."""
    from study_bot.retriever import get_relevant_documents

    # Prima recuperiamo i passaggi più pertinenti; poi li uniamo in un unico
    # testo da affiancare alla domanda nel prompt.
    docs = get_relevant_documents(vector_store, question, k=k)
    context = "\n\n".join(doc.page_content for doc in docs)

    system_prompt = build_system_prompt()
    prompt = build_answer_prompt(context, question)
    full_prompt = f"{system_prompt}\n\n{prompt}"

    if llm is None:
        llm = build_local_llm(model_name=model_name)
    tokenizer = llm["tokenizer"]
    model = llm["model"]
    device = llm["device"]
    max_new_tokens = llm["max_new_tokens"]

    # Il tokenizer prepara tensori PyTorch; li spostiamo sullo stesso dispositivo
    # del modello. inference_mode() evita di conservare dati per il training.
    inputs = tokenizer(full_prompt, return_tensors="pt").to(device)
    with torch.inference_mode():
        outputs = model.generate(**inputs, max_new_tokens=max_new_tokens)
    return tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
