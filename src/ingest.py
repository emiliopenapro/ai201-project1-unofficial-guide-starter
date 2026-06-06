"""
ingest.py — Sprint 1 ingestion + chunking pipeline.

Loads raw source documents (.txt, .md, .pdf), cleans them, and splits them into
overlapping character chunks ready for embedding in a later sprint.

Run:  python src/ingest.py
Outputs the total chunk count and 5 random sample chunks for verification.

Out of scope for Sprint 1: embedding, ChromaDB, Groq generation, Gradio UI.
"""

import html
import random
import re
import sys
from pathlib import Path

import pdfplumber

# Physics text contains glyphs (e.g. U+2212 minus) that the default Windows
# console codec (cp1252) cannot encode. Force UTF-8 output where supported.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# --- Configuration -----------------------------------------------------------
# Chunk parameters per docs/architecture.md and DEC-004 (provisional).
CHUNK_SIZE = 500
OVERLAP = 50

# Domain tag per docs/data-model.md (Chunk.domain).
DOMAIN = "lab_procedure"

# Folder holding the raw source documents.
DATA_DIR = "documents"

# File types we know how to read.
SUPPORTED_SUFFIXES = {".txt", ".md", ".pdf"}

# Acceptable total-chunk range per docs/data-model.md.
MIN_CHUNKS = 50
MAX_CHUNKS = 2000


# --- Loading -----------------------------------------------------------------
def _read_pdf(path: Path) -> str:
    """Extract text from a (text-based) PDF, one page at a time."""
    pages = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            pages.append(page.extract_text() or "")
    return "\n".join(pages)


def load_documents(data_dir: str) -> list[dict]:
    """Read all supported files in ``data_dir``.

    Returns a list of ``{"source": filename, "text": raw_text}`` dicts.
    """
    directory = Path(data_dir)
    if not directory.is_dir():
        raise FileNotFoundError(f"Data directory not found: {directory}")

    documents = []
    for path in sorted(directory.iterdir()):
        if path.suffix.lower() not in SUPPORTED_SUFFIXES:
            continue
        if path.suffix.lower() == ".pdf":
            text = _read_pdf(path)
        else:
            text = path.read_text(encoding="utf-8", errors="replace")
        documents.append({"source": path.name, "text": text})

    if not documents:
        raise ValueError(
            f"No supported documents ({', '.join(sorted(SUPPORTED_SUFFIXES))}) "
            f"found in {directory}/"
        )
    return documents


# --- Cleaning ----------------------------------------------------------------
_HTML_TAG_RE = re.compile(r"<[^>]+>")
_CID_RE = re.compile(r"\(cid:\d+\)")  # pdfplumber's unmapped-glyph tokens
_WHITESPACE_RE = re.compile(r"\s+")


def clean_text(text: str) -> str:
    """Strip HTML tags/entities and collapse whitespace.

    Keeps the underlying review/procedure text, names, ratings, and course
    numbers intact; only markup and excess whitespace are removed.
    """
    text = _HTML_TAG_RE.sub(" ", text)   # drop <tags>
    text = html.unescape(text)           # &amp; &nbsp; -> & (space)
    text = text.replace("\xa0", " ")     # stray non-breaking spaces
    text = text.replace("�", "")    # PDF replacement chars (bad glyphs)
    text = _CID_RE.sub(" ", text)        # pdfplumber (cid:NN) glyph tokens
    text = _WHITESPACE_RE.sub(" ", text)  # collapse runs of whitespace
    return text.strip()


# --- Chunking ----------------------------------------------------------------
def chunk_text(text: str, chunk_size: int = CHUNK_SIZE,
               overlap: int = OVERLAP) -> list[str]:
    """Split ``text`` into overlapping character chunks.

    Consecutive chunks advance by ``chunk_size - overlap`` characters so that
    each chunk shares ``overlap`` characters with the previous one.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and < chunk_size")

    text = text.strip()
    if not text:
        return []

    step = chunk_size - overlap
    chunks = []
    for start in range(0, len(text), step):
        chunk = text[start:start + chunk_size].strip()
        if chunk:
            chunks.append(chunk)
        if start + chunk_size >= len(text):
            break
    return chunks


# --- Assembly ----------------------------------------------------------------
def build_chunks(documents: list[dict]) -> list[dict]:
    """Clean and chunk every document into the Chunk record shape.

    Returns ``{"id", "text", "source", "chunk_index", "domain"}`` dicts per
    docs/data-model.md.
    """
    records = []
    for doc in documents:
        source = doc["source"]
        cleaned = clean_text(doc["text"])
        for index, chunk in enumerate(chunk_text(cleaned)):
            records.append({
                "id": f"{source}_{index}",
                "text": chunk,
                "source": source,
                "chunk_index": index,
                "domain": DOMAIN,
            })
    return records


# --- Entry point -------------------------------------------------------------
def main() -> None:
    documents = load_documents(DATA_DIR)
    print(f"Loaded {len(documents)} document(s) from {DATA_DIR}/:")
    for doc in documents:
        print(f"  - {doc['source']} ({len(doc['text'])} raw chars)")

    chunks = build_chunks(documents)
    total = len(chunks)
    print(f"\nTotal chunks: {total}")

    assert MIN_CHUNKS <= total <= MAX_CHUNKS, (
        f"Chunk count {total} is out of expected range "
        f"[{MIN_CHUNKS}, {MAX_CHUNKS}]."
    )

    print("\n--- 5 random sample chunks ---")
    sample = random.sample(chunks, k=min(5, total))
    for record in sample:
        text = record["text"]
        print(
            f"\n[{record['source']} | chunk_index={record['chunk_index']} | "
            f"{len(text)} chars]"
        )
        print(text)


if __name__ == "__main__":
    main()
