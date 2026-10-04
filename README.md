# study-bot

Questa repository è pensata come un progetto reale e come un tutorial pratico per costruire un chatbot RAG.

## Cosa stai imparando qui

Questo progetto mostra, passo per passo, come costruire un sistema di studio basato su RAG:

1. raccogliere documenti;
2. prepararli e dividerli in blocchi;
3. trasformarli in embedding;
4. recuperare il contenuto più rilevante;
5. usare un modello linguistico per rispondere in modo informato.

## Stato attuale del progetto (sintesi)

- Il progetto è focalizzato su un flusso offline-first: carica file locali (`.txt`, `.md`, `.pdf`), li divide in chunk, crea un indice FAISS e permette di rispondere usando un modello locale.
- La CLI interattiva orchestra i componenti RAG; i parametri di esecuzione si configurano nel file `.env`, senza argomenti da riga di comando.
- Le integrazioni cloud e un'interfaccia frontend non sono incluse. Sono presenti test automatici in `tests/`.
- `scripts/ingest.py` carica e mostra un'anteprima dei documenti nella cartella configurata.

## Struttura del progetto

- `src/` - cartella dei sorgenti del progetto
 - `src/study_bot/main.py` - entrypoint semplice e didattico
- `src/study_bot/config.py` - configurazione (carica `.env`, espone `get_documents_folder()`)
- `src/study_bot/loaders.py` - funzioni per caricare documenti locali
- `src/study_bot/chunking.py` - suddivide i documenti caricati in blocchi con metadati
- `src/study_bot/vectorstore.py` e `src/study_bot/retriever.py` - indicizzazione FAISS e ricerca semantica
- `src/study_bot/prompts.py` e `src/study_bot/llm.py` - prompt e generazione della risposta con un modello locale
- `tests/` - test per chunking, vector store e pipeline RAG
- `scripts/ingest.py` - script per caricare e mostrare un'anteprima dei documenti configurati
- `requirements.txt` - dipendenze per il progetto


## Come iniziare

1. Crea un ambiente virtuale:

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

2. Installa le dipendenze:

```cmd
pip install -r requirements.txt
```

3. Copia `.env.example` in `.env` e imposta `KB_DOCUMENTS_FOLDER_PATH` sulla cartella che contiene i tuoi documenti. Poi avvia la CLI interattiva:

```cmd
copy .env.example .env
python src/study_bot/main.py
```

Al primo avvio i modelli Hugging Face potrebbero essere scaricati. In `.env` puoi configurare:

- `KB_DOCUMENTS_FOLDER_PATH`: cartella dei documenti `.txt`, `.md` e `.pdf`.
- `RAG_CHUNK_SIZE`: dimensione massima dei chunk in caratteri (default `500`).
- `RAG_CHUNK_OVERLAP`: caratteri condivisi fra chunk adiacenti (default `50`; deve essere minore di `RAG_CHUNK_SIZE`).
- `RAG_TOP_K`: numero di chunk recuperati per domanda (default `2`).
- `RAG_EMBEDDING_MODEL`: modello Hugging Face degli embedding.
- `RAG_LLM_MODEL`: modello Hugging Face che genera le risposte.

Il template `.env.example` contiene i valori predefiniti. `.env` è escluso da Git: non inserire lì segreti se in futuro ne aggiungerai.

Scrivi una domanda nella chat; per uscire digita `exit` o `quit` (anche `Ctrl+C` chiude la sessione).

4. Per controllare separatamente il caricamento dei documenti:

```cmd
python scripts/ingest.py
```

## Note operative

- La cartella dei documenti è risolta tramite `study_bot.config.get_documents_folder()`, che legge `KB_DOCUMENTS_FOLDER_PATH` dall'ambiente o dal file `.env`.
- I loader locali espongono due funzioni principali:
  - `load_local_document(path)` → legge un singolo file e restituisce il contenuto come `str`.
  - `load_documents_from_folder()` → legge la cartella configurata e restituisce una lista di dizionari `{ "path": str, "content": str }`;
    internamente chiama `load_local_document()` per ogni file.
  - `split_text(text, chunk_size=500, chunk_overlap=50)` → divide un testo in blocchi sovrapposti.
  - `chunk_documents(documents, chunk_size=500, chunk_overlap=50)` → crea blocchi con `source`, `chunk_index` e `content`.

  I chunk possono essere trasformati in embedding e indicizzati con `build_faiss_index()`; `answer_question()` usa l'indice per recuperare contesto e generare una risposta locale.

## Leggi in questo ordine

- `src/study_bot/main.py` per vedere il punto di partenza del codice
- `src/study_bot/loaders.py` per l'implementazione del caricamento locale
- `src/study_bot/chunking.py` per la suddivisione in blocchi
