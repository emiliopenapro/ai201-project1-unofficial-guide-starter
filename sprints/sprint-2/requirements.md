# Sprint 2 — Requirements

## What Is Being Built
Milestone 4 of the RAG system: turn the Sprint 1 chunks into a searchable vector
store, and build a retrieval function that returns the most relevant chunks for a
query. This is the "memory" of the system — no LLM generation yet.

## Business Justification
Chunks alone are inert. Embedding them and storing them in a vector database is
what makes semantic search possible. Retrieval quality is the single biggest
driver of final answer quality, so it must be built and tested *in isolation*
(before the LLM can mask weak retrieval — see `planning/risks.md` RISK-006).

## Scope
| In Scope                                                   | Out of Scope                              |
|------------------------------------------------------------|-------------------------------------------|
| `src/embed.py`: embed chunks, persist to ChromaDB          | Groq LLM generation (Sprint 3)            |
| `src/query.py`: `retrieve(query, top_k=5)` returning chunks + sources + distances | The `"answer"` field / grounding prompt (Sprint 3) |
| Retrieval Quality Gate testing (distance < 0.5)            | Gradio UI / `app.py` (Sprint 3)           |
| Persisting the store to `./chroma_db` (DEC-003)            | Out-of-scope refusal logic (Sprint 3)     |
| Git commit after Milestone 4                               | README / evaluation report / video        |

## Deliverables
1. `src/embed.py` that embeds all chunks and persists them to ChromaDB
   (collection `unofficial_guide`).
2. `src/query.py` exposing `retrieve(query, top_k=5)` and a runnable `main()`
   that prints results for sample queries.
3. Terminal output for ≥3 test queries showing the query, top returned chunks
   (source + snippet), and distance scores.
4. Evidence the Retrieval Quality Gate passes: top-result distance < 0.5 on
   in-scope queries.

## Success Definition
Running `python src/query.py` answers in-scope physics questions by returning
relevant chunks from the correct manual sections, with distance scores below
0.5, and without any LLM involved.
