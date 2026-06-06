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

## DEC-005: Source Attribution Method
**Date:** Sprint 1  
**Decision:** Append source filenames programmatically after LLM generation (do not rely solely on LLM to cite sources).  
**Reason:** LLMs can omit citations even when instructed. Programmatic attribution from retrieved chunk metadata is reliable.  
**Locked:** Yes.
