# Decisions Log

All significant technical choices are logged here to prevent relitigating them in future sprints.

---

## DEC-001: Stack Selection
**Date:** Sprint 1  
**Decision:** Use `sentence-transformers (all-MiniLM-L6-v2)` + ChromaDB + Groq `llama-3.3-70b-versatile` + Gradio.  
**Reason:** Required by course spec. Free tier, no credit card, runs locally.  
**Locked:** Yes — do not substitute components without updating this log.

## DEC-002: Grounding Enforcement Strategy
**Date:** Sprint 1  
**Decision:** Enforce grounding via system prompt (see `docs/api.md`). LLM is explicitly instructed to answer only from retrieved context and to refuse if context is insufficient.  
**Reason:** Pipeline-level grounding is more reliable than post-hoc filtering.  
**Locked:** Yes — do not soften the system prompt.

## DEC-003: ChromaDB Persistence
**Date:** Sprint 1  
**Decision:** Use `PersistentClient(path="./chroma_db")` so the vector store survives between Python sessions.  
**Reason:** Without persistence, re-embedding is required on every run, which is slow and wasteful.  
**Locked:** Yes.

## DEC-004: Chunk Parameters (Provisional)
**Date:** Sprint 1  
**Decision:** Start with chunk size 500 chars, overlap 50 chars.  
**Reason:** Suitable for medium-length review text. To be validated against actual documents in Milestone 3.  
**Locked:** No — revisit after printing 5 sample chunks. Log any change here.

**UPDATE (Sprint 2):** Switched from fixed-character windows to **sentence-aware
chunking** — sentences are packed greedily up to 500 chars (never broken
mid-sentence), with a 50-char tail overlap; max chunk ≤ 600 chars. A retrieval
sweep showed fixed 500/50 left one eval query (hydrostatic pressure) at distance
0.502 because the formula `P = P₀ + ρgh` was split from its prose. Sentence-aware
chunking keeps the formula sentence intact and brought **all 5 evaluation
queries under the 0.5 gate** (0.31 / 0.44 / 0.39 / 0.39 / 0.26) with 157 chunks,
all 100–600 chars. This directly mitigates RISK-004.

## DEC-005: Source Attribution Method
**Date:** Sprint 1  
**Decision:** Append source filenames programmatically after LLM generation (do not rely solely on LLM to cite sources).  
**Reason:** LLMs can omit citations even when instructed. Programmatic attribution from retrieved chunk metadata is reliable.  
**Locked:** Yes.

## DEC-006: Dependency Versions for Python 3.14
**Date:** Sprint 2  
**Decision:** Bump `sentence-transformers` to 5.5.1 and `chromadb` to 1.5.9 (from the original `==3.4.1` / `>=0.6.0`). The locked DEC-001 *components* are unchanged — still all-MiniLM-L6-v2 + ChromaDB; only versions moved to ones with prebuilt wheels for Python 3.14.3.  
**Reason:** The original `sentence-transformers==3.4.1` predates Python 3.14 and has no compatible wheel; pinning the newer versions keeps the install reproducible. ChromaDB now uses cosine distance explicitly (`hnsw:space: cosine`) per docs/data-model.md.  
**Locked:** Versions only — revisit if the environment's Python version changes. Components remain locked under DEC-001.

## DEC-007: Sprint 2 Retrieval Output Shape
**Date:** Sprint 2  
**Decision:** `query.retrieve()` returns `{"sources", "chunks", "distances"}` — omitting the `"answer"` key from docs/data-model.md's full shape until the LLM exists.  
**Reason:** Generation is Sprint 3 / Milestone 5. Returning distances now supports the Retrieval Quality Gate (< 0.5). The `"answer"` key is added when grounded generation lands.  
**Locked:** No — supersede in Sprint 3.
