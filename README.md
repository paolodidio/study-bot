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

- Il progetto è focalizzato su un flusso offline-first: i loader supportano il caricamento locale di file (`.txt`, `.md`, `.pdf`).
- Le integrazioni cloud (Google Drive, OneDrive) e i test automatici non sono presenti in questa copia semplificata.
- Aggiunto: `scripts/ingest.py` — script di prova per esercitare i loader locali e verificare il comportamento di base.

## Struttura del progetto

- `src/` - cartella dei sorgenti del progetto
 - `src/study_bot/main.py` - entrypoint semplice e didattico
- `src/study_bot/config.py` - configurazione (carica `.env`, espone `get_documents_folder()`)
- `src/study_bot/loaders.py` - funzioni per caricare documenti locali
- `scripts/ingest.py` - script semplice per creare file d'esempio e chiamare i loader
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

3. Esegui il demo (entrypoint package):

```cmd
python src/study_bot/main.py
```

4. Esegui lo script di ingestione (esercita i loader locali):

```cmd
python scripts/ingest.py
```

## Note operative

- La cartella dei documenti è risolta tramite `study_bot.config.get_documents_folder()`, che legge la variabile `KB_DOCUMENTS_FOLDER_PATH` (eventualmente definita in `.env`), si trova nel .env
- I loader locali espongono due funzioni principali:
  - `load_local_document(path)` → legge un singolo file e restituisce il contenuto come `str`.
  - `load_documents_from_folder()` → legge la cartella configurata e restituisce una lista di dizionari `{ "path": str, "content": str }`;
    internamente chiama `load_local_document()` per ogni file.

## Leggi in questo ordine

- `src/study_bot/main.py` per vedere il punto di partenza del codice
- `src/study_bot/loaders.py` per l'implementazione del caricamento locale
