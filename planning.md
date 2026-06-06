# Project 1 Planning: Physics Lab Procedures — RAG System

> Spec and architecture for the Introductory Physics Laboratory RAG assistant.
> This document is written before the pipeline code and is used to direct the
> AI coding tools. Retrieval Approach and Chunking Strategy are updated if the
> approach changes during implementation.

---

## Domain

Introductory **physics laboratory procedures**. The assistant answers
natural-language questions grounded in an *Introductory Physics Laboratory
Manual (Course 20300)* — apparatus, setup, measurement steps, formulas, and
tolerances for a set of classic experiments.

This knowledge is valuable and hard to find through official channels because
lab manuals are dense, sequential, and full of specific numbers (dimensions,
tolerances, formulas) that students must get exactly right. Keyword search
returns a whole page; students instead need a direct, grounded answer to
questions like *"how long should the glider take to cross a level air track?"*
The domain is bounded and factual, which makes grounding both testable and
valuable: a wrong number in a procedure has real consequences, so refusing when
the manual is silent is safer than guessing. (Domain is locked — it replaced an
earlier template domain; see `planning/decisions.md`.)

---

## Documents

The corpus is one integrated 41-page manual,
`documents/PhysicsLabManual.pdf`, which bundles **12 distinct lab sections**.
Each section is an independent procedural "document" covering a different
experiment or instrument, spanning **three subtopics**: instrumentation,
kinematics/dynamics, and fluids/oscillations.

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Measurements and Uncertainty | Recording measurements and estimating/propagating experimental uncertainty. | `documents/PhysicsLabManual.pdf` (p3) |
| 2 | Graphical Representation of Data | Plotting data and extracting results (e.g. slope) from graphs. | `documents/PhysicsLabManual.pdf` (p7) |
| 3 | The Vernier Caliper | Reading a vernier caliper; vernier divisions are 9/10 of the main scale. | `documents/PhysicsLabManual.pdf` (p9) |
| 4 | The Micrometer Caliper | Using a micrometer for fine length measurements. | `documents/PhysicsLabManual.pdf` (p10) |
| 5 | Angle Scale Verniers | Reading angular measurements with a vernier angle scale. | `documents/PhysicsLabManual.pdf` (p11) |
| 6 | Vectors — Equilibrium of a Particle | Force-table equilibrium; resultants and uncertainty (180° = π rad). | `documents/PhysicsLabManual.pdf` (p12) |
| 7 | Air Track | Determining acceleration on a near-frictionless air track (H = 1.27 cm). | `documents/PhysicsLabManual.pdf` (p22) |
| 8 | Atwood's Machine | Measuring acceleration of two masses over a pulley. | `documents/PhysicsLabManual.pdf` (p25) |
| 9 | Centripetal Force | Measuring centripetal force; F = 4π²m f² r. | `documents/PhysicsLabManual.pdf` (p28) |
| 10 | Linear Momentum | Conservation of momentum in collisions. | `documents/PhysicsLabManual.pdf` (p31) |
| 11 | Elasticity and Simple Harmonic Motion | Hooke's-law elongation and the period of an oscillator. | `documents/PhysicsLabManual.pdf` (p34) |
| 12 | Buoyancy and Boyle's Law | Archimedes' principle and gas laws; P = P₀ + ρgh. | `documents/PhysicsLabManual.pdf` (p37) |

> All 12 sections live in one PDF. Each chunk carries a `source` filename tag;
> section-level attribution comes through the chunk text. Splitting into
> per-experiment files is a possible Sprint-2 refinement.

---

## Chunking Strategy

**Chunk size:** 500 characters

**Overlap:** 50 characters (sliding window; stride = 450 characters)

**Reasoning:** The manual is medium-length procedural prose at ~1,768 extracted
characters per page. A 500-character chunk captures roughly one or two complete
procedure steps — enough context to answer a "how do I…" question without
diluting the embedding with unrelated steps. The 50-character (10%) overlap
preserves continuity so a step or formula landing on a boundary keeps its
lead-in, mitigating the risk of procedural steps being split across chunks
(`planning/risks.md` RISK-004). Validated against the real document: the manual
produces **152 chunks**, comfortably inside the required 50–2000 range, so the
provisional values from `DEC-004` need no change yet.

---

## Retrieval Approach

**Embedding model:** `all-MiniLM-L6-v2` via sentence-transformers (384-dim
vectors), stored in ChromaDB (persistent client at `./chroma_db`, collection
`unofficial_guide`, cosine distance).

**Top-k:** 5

**Production tradeoff reflection:** `all-MiniLM-L6-v2` is small, fast, and runs
locally with no API cost — ideal for a prototype — but it trades retrieval
accuracy versus larger hosted embedding models (OpenAI/Cohere, `bge-large`). If
cost weren't a constraint I would weigh: **accuracy on domain-specific text**
(physics/formula vocabulary, where a stronger or fine-tuned model helps most);
**context length** (MiniLM truncates at 256 tokens — fine for 500-char chunks
but limiting if I enlarged them); **latency** (local MiniLM is fast; a hosted
model adds a network round-trip); and **multilingual** support (not needed for
an English manual, so no reason to pay for it). I would also add a cross-encoder
**re-ranker** over the top-k and consider **hybrid dense+BM25 search** so exact
terms like "1.27 cm" or "Atwood" match reliably. k=5 gives the LLM enough
supporting passages to assemble a complete answer while staying small enough to
avoid flooding the prompt with off-topic chunks (RISK-006).

---

## Evaluation Plan

Five test questions with specific, verifiable ground-truth answers taken
directly from the manual, plus one adversarial out-of-scope check.

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | On a properly leveled air track, how long should it take the glider to move across the track? | At least **10 seconds**, regardless of which end it starts from. |
| 2 | What value of H is used when measuring the air track? | **H = 1.27 cm.** |
| 3 | When timing runs, what do you do if two successive time measurements differ by more than 5%? | Take another pair of times and continue **until two successive times agree within 5%**. |
| 4 | What is the formula for hydrostatic pressure P at depth h below a fluid's surface? | **P = P₀ + ρgh** (P₀ = surface pressure, ρ = fluid density). |
| 5 | How does each vernier-scale division compare to the main scale on a vernier caliper? | **Each vernier division is 9/10 of a main-scale division** (least count ≈ 1/10 of a division). |

**Adversarial / grounding check (in addition to the 5, per RISK-003):** Ask a
question the manual cannot answer, e.g. *"What is the boiling point of
nitrogen?"* The system must return the refusal string *"I don't have enough
information on that based on the available documents."* rather than answering
from general knowledge. Pass = refusal, not fabrication. Retrieval is also
tested in isolation at Milestone 4 (distance scores < 0.5 on in-scope queries)
so weak retrieval cannot hide behind a fluent LLM answer (RISK-006).

---

## Anticipated Challenges

1. **PDF extraction artifacts on equation-heavy pages.** pdfplumber emits
   `(cid:NN)` tokens for unmappable glyphs and sometimes drops spaces between
   words (e.g. `if10garetransferred`) on justified/formula text, which hurts
   both readability and retrieval. Mitigation: `clean_text` already strips
   `(cid:NN)` tokens, replacement characters (`�`), and HTML; if formula-dense
   queries suffer, tune `extract_text(x_tolerance=…)` or hand-correct the worst
   pages.

2. **Procedural steps split across chunk boundaries (RISK-004).** A numbered
   sequence (e.g. steps 3–5 of an experiment) can be cut between chunks, so
   retrieval returns incomplete instructions. Mitigation: the 50-char overlap
   preserves boundary context; if needed, switch to paragraph/step-aware
   chunking and log the change in `decisions.md`.

3. **Hallucination on out-of-scope queries (RISK-003).** The Groq LLM may answer
   general physics from its training data instead of the manual. Mitigation: the
   grounding system prompt (`docs/api.md`, DEC-002) instructs refusal when
   context is insufficient, verified by the adversarial eval question above.

---

## Architecture

The five pipeline stages, each labeled with its tool:

```
   documents/PhysicsLabManual.pdf   (.txt / .md / .pdf sources)
                  |
                  v
 [1] INGEST + CHUNK   src/ingest.py  —  Python + pdfplumber
       load -> clean (strip HTML / cid / whitespace) -> 500-char / 50-overlap chunks
                  |   (152 chunk records)
                  v
 [2] EMBED           src/embed.py   —  sentence-transformers (all-MiniLM-L6-v2, 384-dim)
                  |
                  v
 [3] VECTOR STORE    ChromaDB PersistentClient(./chroma_db)
                     collection "unofficial_guide", cosine distance
                  |
                  v
 [4] RETRIEVE        src/query.py   —  top-k = 5 semantic search
       question -> embed -> nearest 5 chunks (+ source names)
                  |
                  v
 [5] GENERATE        src/query.py   —  Groq llama-3.3-70b-versatile (grounded prompt)
       chunks + question -> grounded answer (refuses if context insufficient)
                  |
                  v
   UI               src/app.py     —  Gradio @ localhost:7860  (answer + cited sources)
```

> Stage 1 is complete (Sprint 1). Stages 2–5 are implemented in Sprints 2–3.

---

## AI Tool Plan

AI-generated code (Claude Code / Opus) implements the pipeline; the human author
owns document selection, this spec, and verification.

**Milestone 3 — Ingestion and chunking:** *(done in Sprint 1)* Used Claude Code
to generate `src/ingest.py` from the blueprint's function signatures
(`load_documents`, `clean_text`, `chunk_text`, `build_chunks`, `main`) and the
data-model chunk shape. Input given to the AI: the Sprint-1 Architect Pack
(requirements/blueprint/acceptance), the Chunking Strategy above (500/50), and
the real PDF to test against. Verified by running `python src/ingest.py` and
confirming 152 chunks, all 100–600 chars, free of HTML/`cid`/replacement
artifacts, each tagged with its source filename.

**Milestone 4 — Embedding and retrieval:** Will give Claude the Retrieval
Approach section above plus `docs/api.md` (sentence-transformers + ChromaDB
persistent-client usage) and ask it to implement `src/embed.py` (embed the
`build_chunks` records into collection `unofficial_guide`) and `src/query.py`
(top-k=5 search returning the `docs/data-model.md` output shape). Verify by
checking retrieval in isolation: in-scope queries return relevant chunks with
distance < 0.5 before any LLM is wired in.

**Milestone 5 — Generation and interface:** Will give Claude the exact grounding
system prompt from `docs/api.md` (DO NOT MODIFY, per DEC-002) and the message
format to add grounded generation to `src/query.py`, with programmatic source
attribution (DEC-005). Then ask it to build `src/app.py` as a Gradio UI
(text in → answer + sources out) at localhost:7860. Verify against the 5
evaluation questions plus the adversarial refusal check.
