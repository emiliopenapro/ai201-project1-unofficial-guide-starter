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
tolerances for 12 classic experiments (air track, Atwood's machine, centripetal
force, vernier caliper, buoyancy, and more).

**On the "unofficial guide" framing.** The project pattern targets knowledge
that is *hard to find or use* through official channels. This corpus is an
official manual, but the accessibility problem is real and the angle is honest:
the knowledge students actually need mid-lab is *procedural and situational* —
"what exactly do I do at this step, which formula applies, what tolerance counts
as a pass" — and it is **buried and scattered** across a dense 41-page PDF. A
student at the bench can't skim 41 pages to find that the air track must be level
enough for the glider to take *at least 10 seconds* to cross, or that timing runs
must agree within *5%*. The official document exists; extracting the right
sentence at the right moment is the unmet need. This system acts like a TA who
has read the whole manual and answers a specific question instantly, **with a
citation** so the student can verify it against the source.

**Why it's a good RAG fit.** The domain is bounded and factual, which makes
grounding both testable and valuable: a wrong number in a procedure has real
consequences, so refusing when the manual is silent is safer than guessing. The
12 experiments give natural document boundaries and varied subtopics
(instrumentation, kinematics/dynamics, fluids/oscillations) for retrieval to
discriminate between. (Domain is locked — it replaced an earlier template
domain; see `planning/decisions.md`.)

---

## Documents

The corpus is **13 `.txt` documents** in `documents/`, one per section of the
*Introductory Physics Laboratory Manual (Course 20300)*. The manual was split by
section so each document has a meaningful source filename — retrieval can then
cite the specific experiment a fact came from. The set spans **three subtopics**:
instrumentation, kinematics/dynamics, and fluids/oscillations. (Original PDF kept
for provenance at `raw_sources/PhysicsLabManual.pdf`; the splitter is
`split_manual.py`.)

| # | Source file (`documents/`) | Description |
|---|-----------------------------|-------------|
| 1 | `physlab_00_introduction.txt` | Lab aims, manners/safety, and general procedure expectations. |
| 2 | `physlab_01_measurements_uncertainty.txt` | Recording measurements and estimating/propagating uncertainty. |
| 3 | `physlab_02_graphical_representation.txt` | Plotting data and extracting results (e.g. slope) from graphs. |
| 4 | `physlab_03_vernier_caliper.txt` | Reading a vernier caliper; vernier divisions are 9/10 of the main scale. |
| 5 | `physlab_04_micrometer_caliper.txt` | Using a screw micrometer for fine length measurements. |
| 6 | `physlab_05_angle_scale_verniers.txt` | Reading angular measurements with a vernier angle scale. |
| 7 | `physlab_06_vectors_equilibrium.txt` | Force-table equilibrium; resultants and uncertainty (180° = π rad). |
| 8 | `physlab_07_air_track.txt` | Acceleration on a near-frictionless air track (H = 1.27 cm; ≥10 s to cross). |
| 9 | `physlab_08_atwoods_machine.txt` | Measuring acceleration of two masses over a pulley. |
| 10 | `physlab_09_centripetal_force.txt` | Measuring centripetal force; F = 4π²m f² r. |
| 11 | `physlab_10_linear_momentum.txt` | Conservation of momentum in collisions. |
| 12 | `physlab_11_elasticity_shm.txt` | Hooke's-law elongation and the period of an oscillator. |
| 13 | `physlab_12_buoyancy_boyles_law.txt` | Archimedes' principle and gas laws; P = P₀ + ρgh. |

> Each chunk carries its `source` filename in metadata, so an answer about the
> air track cites `physlab_07_air_track.txt`, not a generic source.

---

## Chunking Strategy

**Chunk size:** 500 characters (max per chunk; sentence-aware, never split mid-sentence)

**Overlap:** 50-character tail of the previous chunk, prepended for continuity

**Reasoning:** The manual is medium-length procedural prose at ~1,768 extracted
characters per page. Chunks are built **sentence-aware**: whole sentences are
packed greedily up to 500 characters and never broken mid-sentence, with a
50-character tail of the prior chunk prepended for continuity (every chunk stays
within 100–600 chars). This keeps a procedure step or a formula together with
its surrounding prose. It is a deliberate change from the initial
fixed-character window (`DEC-004`): a Sprint-2 retrieval sweep showed fixed
500/50 split the formula `P = P₀ + ρgh` from its prose, leaving the
hydrostatic-pressure eval query at distance 0.502 (just over the 0.5 gate).
Sentence-aware chunking brought **all 5 evaluation-style queries under 0.5**
(see Retrieval Approach) and directly mitigates `planning/risks.md` RISK-004.
The corpus produces **157 chunks**, comfortably inside the required 50–2000 range.

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

**Validation (Milestone 4):** All 5 evaluation questions were run through
`src/query.py` against the 157-vector store. Every query returned chunks from the
correct section file (e.g. air-track questions cite `physlab_07_air_track.txt`,
the pressure formula cites `physlab_12_buoyancy_boyles_law.txt`) with top-result
cosine distance **below the 0.5 quality gate** (0.31 / 0.44 / 0.39 / 0.39 / 0.26),
so retrieval is verified in isolation before any LLM is wired in.

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
   documents/physlab_*.txt   (13 section files; .txt / .md / .pdf supported)
                  |
                  v
 [1] INGEST + CHUNK   src/ingest.py  —  Python + pdfplumber
       load -> clean (strip HTML / cid / whitespace) -> sentence-aware <=500-char chunks
                  |   (157 chunk records)
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
confirming 157 chunks, all 100–600 chars, free of HTML/`cid`/replacement
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
