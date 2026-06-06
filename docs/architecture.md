# Architecture

## Pipeline Overview
```
Raw Documents (.txt / .pdf)
        ↓
[Milestone 3] Ingestion + Cleaning (ingest.py)
        ↓
[Milestone 3] Chunking (chunk size: 500 chars, overlap: 50 chars)
        ↓
[Milestone 4] Embedding (all-MiniLM-L6-v2 via sentence-transformers)
        ↓
[Milestone 4] Vector Store (ChromaDB, local, collection: "unofficial_guide")
        ↓
[Milestone 5] Retrieval (top-k=5 semantic search)
        ↓
[Milestone 5] Grounded Generation (Groq llama-3.3-70b-versatile)
        ↓
[Milestone 5] Gradio Interface (app.py → localhost:7860)
```

## Component Responsibilities

| Component     | File          | Responsibility                                              |
|---------------|---------------|-------------------------------------------------------------|
| Ingestion     | `src/ingest.py` | Load raw docs, clean HTML/boilerplate, output clean text  |
| Chunking      | `src/ingest.py` | Split cleaned text into chunks with overlap               |
| Embedding     | `src/embed.py`  | Embed chunks via sentence-transformers, store in ChromaDB |
| Retrieval     | `src/query.py`  | Accept query string, return top-k chunks + source names   |
| Generation    | `src/query.py`  | Pass chunks to Groq LLM with grounding prompt, return answer |
| Interface     | `src/app.py`    | Gradio UI: text input → answer + sources output           |

## Constraints
- Runs entirely locally except for Groq API calls (LLM generation only).
- No user authentication required (local prototype).
- No database other than ChromaDB.
- API key stored in `.env`, never committed to git.
