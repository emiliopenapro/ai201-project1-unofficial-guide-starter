# State — Current Project Status

## Active Sprint
**Sprint 3:** Grounded Generation + Gradio UI (Milestone 5) — complete, pending commit. Sprints 1–2 (Milestones 1–4) on `main`.

## Status
- [x] Scaffold created
- [x] Architect Pack for Sprint 1 generated
- [x] Domain chosen — locked to "Physics Lab Procedures" (RMP/Reddit refs in docs are stale template artifacts)
- [x] Source documents collected — manual split into **13 `.txt` files** in `documents/` (one per section; original PDF kept in `raw_sources/`). Satisfies ≥10 docs / ≥2 subtopics with meaningful per-file source attribution.
- [x] `planning.md` written — all 8 template sections filled, no placeholders
- [x] Ingestion + chunking script (`src/ingest.py`) complete and runs clean
- [x] 5 sample chunks printed and verified (157 total chunks, all 100–600 chars, no HTML/cid/replacement artifacts)

## Recently Completed
- Scaffold initialized (agents.md, docs/, planning/, sprints/)
- `.venv` created; `pdfplumber==0.11.9` installed and added to `requirements.txt`
- `src/ingest.py` built per blueprint: load (.txt/.md/.pdf) → clean → chunk; corpus split into 13 section .txt files (157 chunks, in 50–2000 range)

## Sprint 2 — Completed (Milestone 4)
- `sprints/sprint-2/` Architect Pack generated (requirements/blueprint/acceptance).
- ML stack verified on Python 3.14: torch 2.12.0, sentence-transformers 5.5.1, chromadb 1.5.9 (see DEC-006).
- `src/ingest.py` — chunking switched to **sentence-aware** (DEC-004 update) to fix a formula split across a boundary; 157 chunks across 13 files, all 100–600 chars.
- `src/embed.py` — embeds 157 chunks via all-MiniLM-L6-v2, persists to ChromaDB `unofficial_guide` (cosine); 157 vectors stored.
- `src/query.py` — `retrieve(query, top_k=5)` returns `{sources, chunks, distances}` (DEC-007); tests all 5 eval queries; sources now cite specific section files.
- Retrieval Quality Gate: **5/5 eval queries pass** top-distance < 0.5 (0.31 / 0.44 / 0.39 / 0.39 / 0.26). RISK-004 mitigated.

## Sprint 3 — Completed (Milestone 5)
- `src/query.py` — added `generate()` + `ask()`. Uses Groq llama-3.3-70b-versatile with the verbatim grounding prompt (DEC-002); `ask()` returns `{answer, sources, chunks}` (closes DEC-007). Programmatic source attribution from chunk metadata (DEC-005); no sources listed on refusal.
- `src/app.py` — Gradio UI at http://127.0.0.1:7860 (question box → answer + sources). Verified serving (HTTP 200).
- Verified: in-scope questions answered with citations (e.g. air track → physlab_07_air_track.txt); out-of-scope ("boiling point of nitrogen?") returns the exact refusal phrase with no sources (RISK-003 mitigated).
- `gradio==6.16.0` installed (Python 3.14 OK) and added to requirements.txt.

## Currently Blocked
- Nothing blocked. Milestone 5 complete and verified.
- Remaining: git commit for Milestone 5 (AC-4) — awaiting user go-ahead.

## Next Up (Milestone 6 — Eval + README + Video)
- Run all 5 eval questions end-to-end through `ask()`; record answers + accuracy judgments.
- Complete `README.md` (all required sections; see docs/week1_project_unofficial_guide.md).
- Document ≥1 honest failure case with a pipeline-specific cause.
- Record 3–5 min demo video.

## Deadline Tracker
| Milestone | Est. Hours | Status      |
|-----------|------------|-------------|
| 1 — Domain + Docs  | 0.5h | ✅ Done (manual = 12 lab sections) |
| 2 — planning.md    | 1.0h | ✅ Done (8 sections filled) |
| 3 — Pipeline       | 2.5h | ✅ Code done & verified (against 1 doc) |
| 4 — Embed + Retrieval | 1.5h | ✅ Done (157 vectors; gate 5/5 < 0.5) |
| 5 — Generation + UI | 1.5h | ✅ Done (grounded + refusal; Gradio @7860) |
| 6 — Eval + README + Video | 2.0h | ⬜ Not started |
| **Total**          | **9.0h** | |
