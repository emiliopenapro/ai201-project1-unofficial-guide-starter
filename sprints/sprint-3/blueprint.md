# Sprint 3 — Blueprint

## Implementation Plan

### Step 0: Install the UI dependency
- Add `gradio` to `.venv` and uncomment it in `requirements.txt`.
- `groq` and `python-dotenv` are already installed and verified.

### Step 1: Grounded generation in src/query.py

```
src/query.py  (extend, do not rewrite retrieval)
├── SYSTEM_PROMPT   = exact text from docs/api.md (DEC-002 — DO NOT MODIFY)
├── REFUSAL         = "I don't have enough information on that based on the
│                      available documents."
│
├── generate(query, chunks) → str
│     Builds messages per docs/api.md:
│       system = SYSTEM_PROMPT
│       user   = f"Documents:\n{context}\n\nQuestion: {query}"
│     Calls Groq llama-3.3-70b-versatile (temperature low). Returns answer text.
│
└── answer(query, top_k=5) → dict
      retrieve(query, top_k) → chunks/sources/distances.
      generate(query, chunks) → answer text.
      Programmatic source attribution (DEC-005): unique source filenames from the
      retrieved chunks, appended/returned alongside the answer.
      Returns: {"answer": str, "sources": list[str], "chunks": list[str]}
```

- **Grounding (DEC-002):** the system prompt instructs the model to answer only
  from the provided documents and to emit the refusal phrase otherwise. Do not
  soften it.
- **Attribution (DEC-005):** sources come from retrieved chunk metadata, not from
  trusting the LLM to cite.

### Step 2: src/app.py (Gradio UI)

```
src/app.py
├── respond(query: str) → (answer_text, sources_text)
│     Calls query.answer(query); formats the answer and a sources list.
└── Gradio Blocks/Interface
      Input:  textbox (question)
      Output: answer textbox + sources textbox
      Launch on localhost:7860.
```

### File Layout After Sprint 3
```
src/
├── ingest.py   (Sprint 1)
├── embed.py    (Sprint 2)
├── query.py    (Sprint 2 retrieval + Sprint 3 generation)
└── app.py      (new)
```

### Validation (docs/validation.md — Milestone 5 Checkpoint)
- Grounded response cites a specific document by name.
- One out-of-scope question must return the refusal phrase, not a hallucination.

### Decisions to honor
- DEC-002 grounding prompt — exact text, do not modify.
- DEC-005 programmatic source attribution.
- DEC-007 — `answer()` now returns the full `{answer, sources, chunks}` shape.
