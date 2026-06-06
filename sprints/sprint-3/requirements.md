# Sprint 3 — Requirements

## What Is Being Built
Milestone 5: grounded answer generation and a query interface. The retrieval
layer from Sprint 2 is wired to the Groq LLM with a strict grounding prompt, and
a Gradio UI exposes the system to a user.

## Business Justification
Retrieval returns chunks; users need answers. This sprint turns retrieved
context into a grounded, source-cited answer — and, critically, makes the system
*refuse* when the documents don't contain the answer (the whole point of a RAG
system over a raw LLM).

## Scope
| In Scope                                                        | Out of Scope                         |
|-----------------------------------------------------------------|--------------------------------------|
| Grounded generation in `src/query.py` (Groq llama-3.3-70b-versatile) | Changing the embedding/retrieval stack |
| The exact grounding system prompt from `docs/api.md` (DEC-002)  | Re-chunking / re-embedding           |
| `answer(query)` returning `{answer, sources, chunks}` (DEC-007 → full shape) | Auth / multi-user (local prototype) |
| Programmatic source attribution (DEC-005)                       | Deployment / hosting                 |
| Out-of-scope refusal behavior + test (RISK-003)                 | The evaluation report / README / video (final submission) |
| `src/app.py`: Gradio UI (text in → answer + sources), localhost:7860 |                                 |
| Git commit after Milestone 5                                    |                                      |

## Deliverables
1. `answer(query, top_k=5)` in `src/query.py` returning `{"answer", "sources", "chunks"}`.
2. Grounded answers that cite source filename(s); refusal string when context is insufficient.
3. `src/app.py` — a Gradio app at localhost:7860 with a question box and an
   answer + sources output.
4. Demonstrated: ≥2 in-scope answers with sources, and ≥1 out-of-scope query
   that returns the refusal phrase.

## Success Definition
A user types a physics-lab question into the Gradio UI and gets a correct answer
grounded in the manual with the source filename shown; an out-of-scope question
returns "I don't have enough information on that based on the available documents."
