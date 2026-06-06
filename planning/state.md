# State — Current Project Status

## Active Sprint
**Sprint 1:** Document Collection + planning.md + Ingestion Pipeline (Milestones 1–3)

## Status
- [x] Scaffold created
- [x] Architect Pack for Sprint 1 generated
- [x] Domain chosen — locked to "Physics Lab Procedures" (RMP/Reddit refs in docs are stale template artifacts)
- [x] Source documents collected — `PhysicsLabManual.pdf`, a 41-page manual integrating 12 lab sections (satisfies ≥10 docs / ≥2 subtopics)
- [x] `planning.md` written — all 8 template sections filled, no placeholders
- [x] Ingestion + chunking script (`src/ingest.py`) complete and runs clean
- [x] 5 sample chunks printed and verified (152 total chunks, all 100–600 chars, no HTML/cid/replacement artifacts)

## Recently Completed
- Scaffold initialized (agents.md, docs/, planning/, sprints/)
- `.venv` created; `pdfplumber==0.11.9` installed and added to `requirements.txt`
- `src/ingest.py` built per blueprint: load (.txt/.md/.pdf) → clean → chunk; verified against PhysicsLabManual.pdf (152 chunks, in 50–2000 range)

## Currently Blocked
- Nothing blocked. Milestones 1–3 code/artifacts complete and verified.
- Remaining: git commits for Milestones 1/2/3 (AC-4) — awaiting user go-ahead.

## Next Up (Sprint 2)
- Embedding + ChromaDB setup (`src/embed.py`) — Milestone 4
- Retrieval function + testing (`src/query.py`) — Milestone 4

## Deadline Tracker
| Milestone | Est. Hours | Status      |
|-----------|------------|-------------|
| 1 — Domain + Docs  | 0.5h | ✅ Done (manual = 12 lab sections) |
| 2 — planning.md    | 1.0h | ✅ Done (8 sections filled) |
| 3 — Pipeline       | 2.5h | ✅ Code done & verified (against 1 doc) |
| 4 — Embed + Retrieval | 1.5h | ⬜ Not started |
| 5 — Generation + UI | 1.5h | ⬜ Not started |
| 6 — Eval + README + Video | 2.0h | ⬜ Not started |
| **Total**          | **9.0h** | |
