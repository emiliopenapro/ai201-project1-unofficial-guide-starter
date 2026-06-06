# Sprint 2 — Acceptance Criteria

## Definition of Done

The Builder must verify ALL of the following before Sprint 2 is complete:

### AC-1: Embedding + Vector Store (src/embed.py)
- [ ] `python src/embed.py` runs without errors
- [ ] Uses `all-MiniLM-L6-v2` via sentence-transformers (DEC-001)
- [ ] Persists to ChromaDB `PersistentClient(path="./chroma_db")`, collection
      `unofficial_guide` (DEC-003)
- [ ] Prints the number of vectors stored; count equals the Sprint 1 chunk count
      (157, ± any re-chunk) and is within 50–2000
- [ ] Each stored record carries metadata: `source`, `chunk_index`, `domain`

### AC-2: Retrieval (src/query.py)
- [ ] `retrieve(query, top_k=5)` returns `{"sources", "chunks", "distances"}`
- [ ] `python src/query.py` prints results for ≥3 in-scope test queries
- [ ] Each result shows source filename, a chunk snippet, and a distance score
- [ ] Top-result distance is < 0.5 for in-scope queries (Retrieval Quality Gate)
- [ ] No `"answer"` field and no LLM call (deferred to Sprint 3)

### AC-3: Persistence
- [ ] The `./chroma_db` store survives between runs (a second `query.py` run does
      not require re-embedding)
- [ ] `chroma_db/` is git-ignored (never committed)

### AC-4: Git Commit
- [ ] At least 1 commit after Milestone 4 (embed.py + query.py verified)

## Out-of-Scope Verification
The Builder must NOT have produced:
- Any Groq API calls or `"answer"` generation
- Any grounding/refusal prompt logic
- Any Gradio UI code
