# The Unofficial Guide — Project 1

A Retrieval-Augmented Generation (RAG) system that answers natural-language
questions about introductory physics lab procedures, grounded only in an
*Introductory Physics Laboratory Manual (Course 20300)* and citing its sources.

**Run it:**
```bash
python -m venv .venv && .venv\Scripts\activate      # Windows
pip install -r requirements.txt
cp .env.example .env                                 # add your Groq API key
python src/embed.py        # build the vector store (one-time)
python src/app.py          # launch the UI at http://localhost:7860
```

---

## Domain

**Introductory physics laboratory procedures** — apparatus, setup, measurement
steps, formulas, and tolerances for 12 classic experiments (air track, Atwood's
machine, centripetal force, vernier caliper, buoyancy, and more).

The project pattern targets knowledge that is *hard to find or use* through
official channels. This corpus is an official manual, but the accessibility
problem is real: the knowledge a student needs mid-lab is **procedural and
situational** — "what exactly do I do at this step, which formula applies, what
tolerance counts as a pass" — and it is buried and scattered across a dense
41-page PDF. A student at the bench can't skim 41 pages to learn that the air
track must be level enough for the glider to take *at least 10 seconds* to cross,
or that timing runs must agree within *5%*. The document exists; extracting the
right sentence at the right moment is the unmet need. This system acts like a TA
who has read the whole manual and answers a specific question instantly, **with a
citation** so the student can verify it against the source.

---

## Document Sources

The source is a single official manual, *Introductory Physics Laboratory Manual,
Course 20300* (`raw_sources/PhysicsLabManual.pdf`). It was **split by section
into 13 `.txt` documents** (via `split_manual.py`) so each chunk carries a
meaningful source filename and answers can cite the specific experiment.

| # | Source | Type | File path |
|---|--------|------|-----------|
| 1 | Introduction (aims, lab manners) | manual section | `documents/physlab_00_introduction.txt` |
| 2 | Measurements and Uncertainty | manual section | `documents/physlab_01_measurements_uncertainty.txt` |
| 3 | Graphical Representation of Data | manual section | `documents/physlab_02_graphical_representation.txt` |
| 4 | The Vernier Caliper | manual section | `documents/physlab_03_vernier_caliper.txt` |
| 5 | The Micrometer Caliper | manual section | `documents/physlab_04_micrometer_caliper.txt` |
| 6 | Angle Scale Verniers | manual section | `documents/physlab_05_angle_scale_verniers.txt` |
| 7 | Vectors — Equilibrium of a Particle | manual section | `documents/physlab_06_vectors_equilibrium.txt` |
| 8 | Air Track | manual section | `documents/physlab_07_air_track.txt` |
| 9 | Atwood's Machine | manual section | `documents/physlab_08_atwoods_machine.txt` |
| 10 | Centripetal Force | manual section | `documents/physlab_09_centripetal_force.txt` |
| 11 | Linear Momentum | manual section | `documents/physlab_10_linear_momentum.txt` |
| 12 | Elasticity and Simple Harmonic Motion | manual section | `documents/physlab_11_elasticity_shm.txt` |
| 13 | Buoyancy and Boyle's Law | manual section | `documents/physlab_12_buoyancy_boyles_law.txt` |

Subtopics span three areas: **instrumentation** (calipers, verniers), **kinematics/
dynamics** (air track, Atwood, centripetal, momentum), and **fluids/oscillations**
(buoyancy, SHM).

---

## Chunking Strategy

**Chunk size:** 500 characters maximum (sentence-aware — never split mid-sentence)

**Overlap:** a 50-character tail of the previous chunk is prepended to each chunk

**Preprocessing before chunking:** load `.txt`/`.md`/`.pdf` (`pdfplumber` for PDF),
then clean — strip HTML tags/entities, pdfplumber `(cid:NN)` glyph tokens, `�`
replacement characters, and collapse whitespace (`src/ingest.py`).

**Why these choices fit the documents:** the manual is medium-length procedural
prose (~1,768 chars/page). Sentences are packed greedily up to 500 characters and
never broken, so a procedure step or a formula stays with its surrounding prose;
the 50-char overlap preserves continuity across chunk boundaries. This is a
deliberate, evidence-driven choice: an early fixed-character version split the
formula `P = P₀ + ρgh` away from its prose, leaving the hydrostatic-pressure query
just over the retrieval gate (distance 0.502). Switching to sentence-aware
chunking fixed it (0.382) and improved every test query (logged as DEC-004).

**Final chunk count:** **157 chunks** across the 13 documents (within the 50–2000
target). Every chunk is 100–600 characters.

### 5 sample chunks (each labeled with its source)

```
[physlab_07_air_track.txt | chunk_index=12 | 541 chars]
...Compare your value with the standard value by calculating the Uncertainty
Ratio: |g−g_standard|/∆g. Values less than 1 indicate excellent agreement,
greater than 4, disagreement and possible mistakes... Draw a free-body diagram
showing the forces on the glider sitting on an airtrack at an angle θ.

[physlab_02_graphical_representation.txt | chunk_index=8 | 290 chars]
9.81 m/s2, we calculate the uncertainty ratio, UR. UR=(9.81−9.60)/0.64=0.21/0.64
=0.33, so the agreement is very good. [Note: Making the uncertainty too large
(lower precision) can make the result appear in better agreement... but makes the
measurement less meaningful.]

[physlab_09_centripetal_force.txt | chunk_index=0 | 130 chars]
Centripetal Force APPARATUS 1. Centripetal force apparatus 2. Set of slotted
weights 3. Equal-arm balance with standard weights 4.

[physlab_01_measurements_uncertainty.txt | chunk_index=4 | 361 chars]
...Six repetitions are reasonable. Since range increases with repetitions, we
must note the number used. Uncertainty - How far from the correct value our
result might be... We will take the larger of range and sensitivity as our
measure of uncertainty.

[physlab_01_measurements_uncertainty.txt | chunk_index=10 | 545 chars]
=ab when a and b have uncertainties of Δa and Δb. Then ΔR=(a+Δa)(b+Δb)−ab=
aΔb+bΔa+(Δb)(Δa)... The RULE for combining uncertainties is given in terms of
fractional uncertainties, Δx/x. It is simply that each factor contributes equally
to the fractional uncertainty of the result.
```

---

## Embedding Model

**Model used:** `all-MiniLM-L6-v2` (sentence-transformers), producing 384-dim
vectors, stored in **ChromaDB** (persistent client at `./chroma_db`, collection
`unofficial_guide`, **cosine** distance). Retrieval returns the **top-k = 5**
chunks.

**Production tradeoff reflection:** `all-MiniLM-L6-v2` is small, fast, and runs
locally with no API cost — ideal for a prototype. If deploying for real users with
cost no object, I'd weigh: **accuracy on domain-specific text** (physics/formula
vocabulary, where a stronger or fine-tuned model helps most — and would likely
have improved the failure case below); **context length** (MiniLM truncates at
256 tokens — fine for 500-char chunks, limiting if I enlarged them); **latency**
(local MiniLM is fast; a hosted model adds a network round-trip); and
**multilingual** support (unnecessary for an English manual). I would also add a
cross-encoder **re-ranker** over the top-k and consider **hybrid dense + BM25
search** so exact terms like `1.27 cm` or `Atwood` match reliably.

---

## Grounded Generation

The LLM is **Groq `llama-3.3-70b-versatile`** (`src/query.py`, `temperature=0.2`).

**System prompt grounding instruction** (used verbatim, `docs/api.md` / DEC-002):

> You are a helpful assistant for college students. Answer the user's question
> using ONLY the information provided in the documents below. If the documents do
> not contain enough information to answer the question, respond with: "I don't
> have enough information on that based on the available documents." Do not use
> your general training knowledge. Always cite which document(s) your answer comes
> from.

**Structural choices:** the retrieved chunks are passed as the only context, each
labelled `[Source: <filename>]`, in a user message of the form
`Documents:\n{context}\n\nQuestion: {query}`. Grounding is enforced at the prompt
level (the model is told to use only the context and to refuse otherwise), not by
post-hoc filtering.

**How source attribution is surfaced:** `ask()` returns the unique source
filenames taken **programmatically from the retrieved chunks' metadata** (DEC-005)
— not parsed from the model's text, which can omit citations. On a refusal, no
sources are listed (the answer isn't drawn from any document).

**Example responses:**

- *Q: "How long should the glider take to cross a level air track?"* →
  "…it should take the glider **at least 10 seconds** to move across the track, no
  matter at which end it is placed." **Sources:** `physlab_07_air_track.txt`
- *Q: "How does a vernier division compare to the main scale?"* →
  "…each vernier division is **9/10 of the divisions on the main scale**."
  **Sources:** `physlab_03_vernier_caliper.txt`
- *Out-of-scope — Q: "What is the boiling point of nitrogen?"* →
  "I don't have enough information on that based on the available documents."
  **Sources:** *(none)*

**Query interface:** a **Gradio** web UI (`src/app.py`, `http://localhost:7860`).
Input: a single "Your question" text box. Outputs: an "Answer" box and a
"Sources (retrieved documents)" box. Sample interaction:

```
Your question:  What value of H is used when measuring the air track?
Answer:         The value of H used when measuring the air track is 1.27 cm.
                (Source: physlab_07_air_track.txt)
Sources:        • physlab_07_air_track.txt
```

---

## Evaluation Report

All 5 questions from `planning.md` were run end-to-end through `ask()`
(reproducible via `python evaluate.py`). Distances are the top-result cosine
distance from retrieval.

| # | Question | Expected answer | System response (summarized) | Retrieval | Accuracy |
|---|----------|-----------------|------------------------------|-----------|----------|
| 1 | How long should the glider take to cross a level air track? | At least 10 seconds | "at least 10 seconds, no matter at which end it is placed" (d=0.28) | Relevant | Accurate |
| 2 | What value of H is used for the air track? | H = 1.27 cm | "1.27 cm" (d=0.45) | Relevant | Accurate |
| 3 | What if two successive times differ by more than 5%? | Take another pair until within 5% | "take another pair… until two successive times are within 5%" (d=0.34) | Relevant | Accurate |
| 4 | Formula for hydrostatic pressure at depth h? | P = P₀ + ρgh | "P = P₀ + ρgh, where P₀ is surface pressure and ρ is density" (d=0.41) | Relevant | Accurate |
| 5 | How does a vernier division compare to the main scale? | 9/10 of a main-scale division | "each vernier division is 9/10 of the divisions on the main scale" (d=0.19) | Relevant | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target
**Response accuracy:** Accurate / Partially accurate / Inaccurate

These five are deliberately verifiable factual lookups, and the system answers all
five accurately with correct citations. Because a clean 5/5 can hide weaknesses, I
stress-tested further; that surfaced the genuine failure documented below.

---

## Failure Case Analysis

**Question that failed:** "What is the density of methyl alcohol?"

**What the system returned:** "I don't have enough information on that based on the
available documents." — a **false refusal**. The answer *is* in the corpus: the
density table in `physlab_12_buoyancy_boyles_law.txt` contains the line
`Aluminum 2.7 Alcohol, Methyl 0.80` (methyl alcohol = 0.80). (For contrast, the
system *does* correctly answer "density of granite" and "density of limestone",
both 2.7, from the same table.)

**Root cause (tied to a specific pipeline stage):** the failure is in
**ingestion → retrieval**, caused by **PDF table extraction**. `pdfplumber`
flattens the two-column density table into merged rows like
`Aluminum 2.7 Alcohol, Methyl 0.80` and `Zinc - wrought 7.2 Granite 2.7`, where a
material and its value are interleaved with an unrelated material. This mangled,
structure-less text embeds poorly against a clean query, so "density of methyl
alcohol" retrieved at distance **0.693** — well above the 0.5 quality gate and
into the "weak retrieval" zone. The density-table chunk wasn't retrieved strongly
enough, so the grounded model correctly refused given the weak context it saw.
Granite/limestone happen to work because their value (2.7) is common and appears
in stronger-matching contexts.

**What I would change to fix it:** detect and reshape tables at ingestion (e.g.,
`pdfplumber`'s `extract_tables()` to emit one clean `material: value` line per
entry), and/or add **hybrid dense + BM25 keyword search** so an exact term like
"Methyl" matches even when the dense embedding of the mangled row is weak. A
cross-encoder re-ranker would also help promote the table chunk.

---

## Spec Reflection

**One way the spec helped me during implementation:** `planning.md` and
`docs/validation.md` defined a concrete retrieval quality gate (top-result cosine
distance < 0.5) *before* any LLM was wired in. Testing retrieval against that
number — rather than eyeballing answers — is exactly what exposed the
hydrostatic-pressure formula being split across a chunk boundary (distance 0.502).
Without that measurable target I'd likely have shipped fixed-character chunking and
only noticed the weakness as vaguely worse answers later. The decisions log also
kept the grounding prompt and embedding model fixed, so I never relitigated them.

**One way my implementation diverged from the spec, and why:** the spec
(`docs/architecture.md` and DEC-004) initially specified **fixed 500/50-character**
chunking. Implementation diverged to **sentence-aware** chunking because real
retrieval testing showed fixed windows split a formula from its explanatory prose,
pushing one evaluation query above the gate. DEC-004 was explicitly marked
"revisit after seeing real chunks," so I changed the approach and logged the
before/after evidence (0.502 → 0.382) as a DEC-004 update. A second divergence:
the corpus started as one PDF and was split into 13 per-section files so source
attribution could name the specific experiment.

---

## AI Usage

**Instance 1 — Chunking strategy (directed a change after measuring)**

- *What I gave the AI:* the `planning.md` Chunking Strategy section and the
  blueprint function signatures, asking it to implement `src/ingest.py`
  (load → clean → chunk) with the specified 500/50 parameters.
- *What it produced:* a working pipeline using **fixed-character** sliding-window
  chunking, exactly as the initial spec described.
- *What I changed or overrode:* after running a retrieval sweep, I found the
  hydrostatic-pressure formula was split across a boundary (distance 0.502, over
  the gate). I directed a switch to **sentence-aware** chunking (pack whole
  sentences ≤ 500 chars, 50-char tail overlap), verified it beat the fixed
  approach on all 5 queries, and logged it as a DEC-004 update — overriding the
  AI's spec-faithful first version with an evidence-based design.

**Instance 2 — Splitting the corpus into per-section documents**

- *What I gave the AI:* the goal of satisfying the "≥10 documents with meaningful
  source attribution" requirement from a single 41-page PDF, plus the section list
  from the manual's table of contents.
- *What it produced:* `split_manual.py`, which extracts the PDF text and splits it
  on section headings into 13 `.txt` files.
- *What I changed or overrode:* the first version failed on two sections because
  `re.escape` turned an intended `.` wildcard into a literal dot (so it couldn't
  match the curly apostrophe in "Atwood's"/"Boyle's") and headings that wrapped
  across PDF line breaks weren't matched. I corrected it to make whitespace
  flexible (`\s+`) and to match either straight or curly apostrophes, then
  verified all 13 files start at the correct heading.
