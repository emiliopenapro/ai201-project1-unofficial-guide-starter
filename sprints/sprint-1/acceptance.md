# Sprint 1 — Acceptance Criteria

## Definition of Done

The Builder must verify ALL of the following before Sprint 1 is complete:

### AC-1: Document Collection
- [ ] `documents/` folder exists with ≥10 `.txt` files
- [ ] Each file has a meaningful name following `{domain}_{source}_{id}.txt`
- [ ] Files cover ≥2 different subtopics within the chosen domain

### AC-2: planning.md
- [ ] All 7 sections are filled with substantive content (no placeholders, no "TBD")
- [ ] Chunking strategy states chunk size and overlap in numbers and justifies them
- [ ] Evaluation plan includes exactly 5 questions, each with a specific verifiable expected answer
- [ ] Architecture diagram is present and labels all 5 stages with tool names
- [ ] AI Tool Plan names specific pipeline components, not generic statements

### AC-3: src/ingest.py
- [ ] Script runs without errors: `python src/ingest.py`
- [ ] Prints total chunk count (must be between 50 and 2000)
- [ ] Prints 5 random chunks to terminal
- [ ] Each printed chunk:
  - Is ≥100 characters and ≤600 characters
  - Contains no HTML tags or entities
  - Is tagged with its correct source filename

### AC-4: Git Commits
- [ ] At least 1 commit after Milestone 1 (document collection)
- [ ] At least 1 commit after Milestone 2 (planning.md complete)
- [ ] At least 1 commit after Milestone 3 (ingest.py verified)

## Out-of-Scope Verification
The Builder must NOT have produced:
- Any embedding code
- Any ChromaDB setup
- Any Groq API calls
- Any Gradio UI code
