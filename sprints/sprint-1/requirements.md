# Sprint 1 — Requirements

## What Is Being Built
The foundation of the RAG system: document collection, the `planning.md` spec, and the ingestion + chunking pipeline.

## Business Justification
Without clean, chunked documents, no other milestone is possible. Retrieval quality depends entirely on chunk quality. This sprint produces the two required graded artifacts before any code sprint: `planning.md` and the ingestion pipeline.

## Scope
| In Scope                                              | Out of Scope                          |
|-------------------------------------------------------|---------------------------------------|
| Choosing a domain                                     | Embedding (Sprint 2)                  |
| Collecting ≥10 source documents as `.txt` files       | ChromaDB setup (Sprint 2)             |
| Writing `planning.md` (all sections, including eval plan) | Groq LLM integration (Sprint 3)  |
| Writing `src/ingest.py`: load, clean, chunk documents | Gradio UI (Sprint 3)                  |
| Printing + verifying 5 sample chunks                  | Evaluation report (Sprint 4)          |
| Git commit after Milestone 1, 2, and 3                |                                       |

## Deliverables
1. `documents/` folder containing ≥10 `.txt` source documents
2. `planning.md` in repo root (all sections filled, no placeholders)
3. `src/ingest.py` that loads, cleans, and chunks all documents
4. Terminal output showing 5 sample chunks (printed, verified)
5. Total chunk count printed and within 50–2000 range

## Success Definition
The Builder can print 5 random chunks from the pipeline. Each chunk is readable, self-contained, free of HTML artifacts, and tagged with its source filename.
