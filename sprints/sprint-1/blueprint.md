# Sprint 1 — Blueprint

## Implementation Plan

### Step 1: Collect Documents (Human task — no code)
- Create a `documents/` folder in the repo root.
- Save each source document as a `.txt` file (e.g., `rmp_prof_smith.txt`, `reddit_housing_thread_1.txt`).
- Naming convention: `{domain}_{source}_{id}.txt` — lowercase, underscores, no spaces.
- Target: ≥10 files. More is better; aim for variety of subtopics.

### Step 2: Write planning.md (Human task — no code)
Fill all sections of `planning.md`:
- **Domain:** What and why.
- **Documents:** List every file in `documents/` with a one-line description.
- **Chunking Strategy:** State chunk size, overlap, and justify based on document structure.
- **Retrieval Approach:** Embedding model, top-k value, production tradeoff reflection.
- **Evaluation Plan:** 5 test questions + expected ground-truth answers.
- **Anticipated Challenges:** ≥2 specific risks.
- **AI Tool Plan:** Which pipeline parts will use AI-generated code and what input you'll give the AI.
- **Architecture Diagram:** ASCII or Mermaid diagram showing the 5 pipeline stages with tool labels.

### Step 3: Build src/ingest.py (Builder task)

```
src/ingest.py
├── load_documents(data_dir: str) → list[dict]
│     Reads all .txt and .pdf files from data_dir.
│     Returns: [{"source": filename, "text": raw_text}, ...]
│
├── clean_text(text: str) → str
│     Removes HTML tags, entities (&amp;, &nbsp;), extra whitespace.
│     Keeps: review text, ratings, names, course numbers.
│
├── chunk_text(text: str, chunk_size: int, overlap: int) → list[str]
│     Splits cleaned text into overlapping chunks.
│     Default: chunk_size=500, overlap=50 (chars).
│
├── build_chunks(documents: list[dict]) → list[dict]
│     Applies clean_text + chunk_text to each document.
│     Returns: [{"id": "filename_0", "text": chunk, "source": filename, "chunk_index": int}, ...]
│
└── main()
      Calls load → clean → chunk → prints 5 random chunks + total count.
```

### File Layout After Sprint 1
```
/
├── documents/
│   ├── rmp_prof_jones.txt
│   ├── reddit_housing_1.txt
│   └── ... (≥10 files)
├── planning.md
├── src/
│   └── ingest.py
```

### Chunk Size Validation Logic
```python
assert 50 <= total_chunks <= 2000, f"Chunk count {total_chunks} is out of expected range."
```
