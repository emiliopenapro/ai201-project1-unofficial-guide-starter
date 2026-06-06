# State — Current Project Status

## Active Sprint
**Sprint 2:** Embedding + Vector Store + Retrieval (Milestone 4). Sprint 1 (Milestones 1–3) complete and pushed to `main`.

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

## Currently Blocked
- Nothing blocked. Milestone 4 code complete and verified.
- Remaining: git commit for Milestone 4 (AC-4) — awaiting user go-ahead.

## Next Up (Sprint 3 — Milestone 5)
- Grounded generation in `src/query.py` — Groq llama-3.3-70b-versatile + grounding prompt (DEC-002), add `"answer"` key + programmatic source attribution (DEC-005).
- Gradio UI (`src/app.py`) at localhost:7860.
- Out-of-scope refusal test (RISK-003).

## Deadline Tracker
| Milestone | Est. Hours | Status      |
|-----------|------------|-------------|
| 1 — Domain + Docs  | 0.5h | ✅ Done (manual = 12 lab sections) |
| 2 — planning.md    | 1.0h | ✅ Done (8 sections filled) |
| 3 — Pipeline       | 2.5h | ✅ Code done & verified (against 1 doc) |
| 4 — Embed + Retrieval | 1.5h | ✅ Done (157 vectors; gate 5/5 < 0.5) |
| 5 — Generation + UI | 1.5h | ⬜ Not started |
| 6 — Eval + README + Video | 2.0h | ⬜ Not started |
| **Total**          | **9.0h** | |
