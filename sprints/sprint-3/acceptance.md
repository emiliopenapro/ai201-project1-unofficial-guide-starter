# Sprint 3 — Acceptance Criteria

## Definition of Done

The Builder must verify ALL of the following before Sprint 3 is complete:

### AC-1: Grounded Generation (src/query.py)
- [ ] `answer(query, top_k=5)` returns `{"answer", "sources", "chunks"}`
- [ ] Uses Groq `llama-3.3-70b-versatile` via the `groq` SDK with the key from `.env`
- [ ] System prompt is the EXACT text from `docs/api.md` (DEC-002), unmodified
- [ ] In-scope questions produce answers grounded in the manual
- [ ] `sources` is derived programmatically from retrieved chunk metadata (DEC-005),
      not parsed from the LLM output

### AC-2: Out-of-Scope Refusal (RISK-003)
- [ ] An out-of-scope question (e.g. "What is the boiling point of nitrogen?")
      returns the refusal phrase: "I don't have enough information on that based
      on the available documents."
- [ ] The system does NOT answer out-of-scope questions from general knowledge

### AC-3: Query Interface (src/app.py)
- [ ] `python src/app.py` launches a Gradio app on localhost:7860
- [ ] Has a question input field and an answer + sources output
- [ ] A sample interaction returns an answer with the source filename visible

### AC-4: Git Commit
- [ ] At least 1 commit after Milestone 5 (generation + UI verified)

## Out-of-Scope Verification
The Builder must NOT have:
- Modified the grounding system prompt from `docs/api.md`
- Changed the embedding model, chunking, or retrieval logic
- Added authentication or deployment configuration
