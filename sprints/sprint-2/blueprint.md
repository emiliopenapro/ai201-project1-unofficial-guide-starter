# Sprint 2 — Blueprint

## Implementation Plan

### Step 0: Verify dependencies install (Python 3.14)
- Install `sentence-transformers` and `chromadb` into `.venv`.
- First run downloads the `all-MiniLM-L6-v2` model (~80 MB) from Hugging Face.
- **Risk:** PyTorch may lack prebuilt wheels for Python 3.14. If install fails,
  STOP and report options (new venv on 3.11/3.12, or a lighter embedding stack).

### Step 1: Build src/embed.py

```
src/embed.py
├── get_collection() → chromadb collection
│     PersistentClient(path="./chroma_db"); get_or_create_collection("unofficial_guide").
│
├── embed_texts(texts: list[str]) → list[list[float]]
│     SentenceTransformer("all-MiniLM-L6-v2").encode(texts) → 384-dim vectors.
│
├── build_index(rebuild: bool = False) → int
│     Loads chunks via ingest.build_chunks(load_documents(DATA_DIR)).
│     Adds documents=text, ids=id, metadatas={source, chunk_index, domain}.
│     Returns the number of vectors stored.
│
└── main()
      Builds the index and prints the stored vector count.
```

### Step 2: Build src/query.py

```
src/query.py
├── retrieve(query: str, top_k: int = 5) → dict
│     Embeds the query, runs collection.query(n_results=top_k).
│     Returns: {"sources": list[str], "chunks": list[str], "distances": list[float]}
│     (No "answer" key yet — that is Sprint 3 / Milestone 5.)
│
└── main()
      Runs ≥3 in-scope sample queries, prints each query + top chunks
      (source + snippet) + distance scores, and flags any top distance ≥ 0.5.
```

### File Layout After Sprint 2
```
src/
├── ingest.py     (Sprint 1)
├── embed.py      (new)
└── query.py      (new)
chroma_db/        (generated, git-ignored)
```

### Retrieval Quality Gate (from docs/validation.md)
- Top-3 results for each query must visually relate to the query.
- Top-result distance must be < 0.5 (warn/debug if > 0.6–0.7).

### Decisions to honor
- DEC-001 stack (all-MiniLM-L6-v2 + ChromaDB) — do not substitute.
- DEC-003 persistence — use `PersistentClient(path="./chroma_db")`.
