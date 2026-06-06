"""
embed.py — Sprint 2 / Milestone 4: embedding + vector store.

Embeds the Sprint 1 chunks with all-MiniLM-L6-v2 and persists them to a local
ChromaDB collection so they can be searched semantically.

Run:  python src/embed.py
Builds (or refreshes) the vector store and prints the number of vectors stored.

Out of scope for Sprint 2: LLM generation, grounding prompts, Gradio UI.
"""

import sys

import chromadb
from sentence_transformers import SentenceTransformer

from ingest import DATA_DIR, build_chunks, load_documents

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# --- Configuration (DEC-001 / DEC-003 / docs/data-model.md) ------------------
EMBED_MODEL = "all-MiniLM-L6-v2"   # 384-dim, sentence-transformers
CHROMA_PATH = "./chroma_db"        # persistent store (DEC-003)
COLLECTION = "unofficial_guide"
# ChromaDB defaults to L2; data-model specifies cosine, so set it explicitly.
COLLECTION_METADATA = {"hnsw:space": "cosine"}

MIN_VECTORS = 50
MAX_VECTORS = 2000

# Lazily-loaded singleton so the model is only built once per process.
_model: SentenceTransformer | None = None


def get_model() -> SentenceTransformer:
    """Return the (cached) sentence-transformers embedding model."""
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBED_MODEL)
    return _model


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed a list of strings into 384-dim vectors."""
    return get_model().encode(texts, show_progress_bar=False).tolist()


def get_collection():
    """Open (or create) the persistent ChromaDB collection."""
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    return client.get_or_create_collection(
        COLLECTION, metadata=COLLECTION_METADATA
    )


def build_index(rebuild: bool = False) -> int:
    """Embed all chunks and upsert them into the collection.

    ``upsert`` keyed on each chunk's stable ``id`` makes re-runs idempotent, so
    the persisted store is refreshed rather than duplicated. Pass
    ``rebuild=True`` to drop and recreate the collection first.
    """
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    if rebuild:
        try:
            client.delete_collection(COLLECTION)
        except Exception:
            pass  # collection may not exist yet
    collection = client.get_or_create_collection(
        COLLECTION, metadata=COLLECTION_METADATA
    )

    records = build_chunks(load_documents(DATA_DIR))
    collection.upsert(
        ids=[r["id"] for r in records],
        documents=[r["text"] for r in records],
        metadatas=[
            {
                "source": r["source"],
                "chunk_index": r["chunk_index"],
                "domain": r["domain"],
            }
            for r in records
        ],
        embeddings=embed_texts([r["text"] for r in records]),
    )
    return collection.count()


def main() -> None:
    print(f"Embedding chunks with {EMBED_MODEL} -> ChromaDB '{COLLECTION}' ...")
    count = build_index()
    print(f"Vectors stored: {count}")
    assert MIN_VECTORS <= count <= MAX_VECTORS, (
        f"Vector count {count} is out of expected range "
        f"[{MIN_VECTORS}, {MAX_VECTORS}]."
    )
    print(f"Persisted to {CHROMA_PATH}/ (survives between runs).")


if __name__ == "__main__":
    main()
