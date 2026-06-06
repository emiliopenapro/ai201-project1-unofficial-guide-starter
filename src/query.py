"""
query.py — Sprint 2 / Milestone 4: retrieval (no LLM yet).

Embeds a query and returns the top-k most similar chunks from the ChromaDB
vector store, with their source filenames and distance scores.

Run:  python src/query.py
Runs several in-scope sample queries and checks the Retrieval Quality Gate
(top-result distance < 0.5) from docs/validation.md.

Out of scope for Sprint 2: the "answer" field, grounding prompt, Groq LLM,
Gradio UI — all Sprint 3 / Milestone 5.
"""

import sys

from embed import build_index, embed_texts, get_collection

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TOP_K = 5
GATE_DISTANCE = 0.5  # top-result distance must be below this (docs/validation.md)

# In-scope sample queries (mirror the 5 planning.md evaluation questions).
SAMPLE_QUERIES = [
    "How long should the glider take to move across a level air track?",
    "What value of H is used when measuring the air track?",
    "What do you do if two successive time measurements differ by more than 5%?",
    "What is the formula for hydrostatic pressure below a fluid surface?",
    "How does each vernier-scale division compare to the main scale?",
]


def retrieve(query: str, top_k: int = TOP_K) -> dict:
    """Return the top-k chunks for ``query``.

    Shape: ``{"sources": list[str], "chunks": list[str], "distances": list[float]}``.
    No ``"answer"`` key — grounded generation is added in Sprint 3.
    """
    collection = get_collection()
    result = collection.query(
        query_embeddings=embed_texts([query]),
        n_results=top_k,
    )
    return {
        "sources": [m["source"] for m in result["metadatas"][0]],
        "chunks": result["documents"][0],
        "distances": result["distances"][0],
    }


def _snippet(text: str, n: int = 160) -> str:
    text = text.strip().replace("\n", " ")
    return text if len(text) <= n else text[:n] + "…"


def main() -> None:
    # Ensure the store is populated; build it on first run.
    if get_collection().count() == 0:
        print("Vector store empty — building index first...\n")
        build_index()

    all_passed = True
    for query in SAMPLE_QUERIES:
        result = retrieve(query)
        top_distance = result["distances"][0]
        passed = top_distance < GATE_DISTANCE
        all_passed = all_passed and passed
        flag = "PASS" if passed else "WARN"

        print(f"\n=== Query: {query}")
        print(f"    top distance: {top_distance:.4f}  [{flag} gate < {GATE_DISTANCE}]")
        for rank, (src, chunk, dist) in enumerate(
            zip(result["sources"], result["chunks"], result["distances"]), 1
        ):
            print(f"  {rank}. [{src} | dist={dist:.4f}] {_snippet(chunk)}")

    print("\n" + ("All queries passed the retrieval quality gate."
                  if all_passed else
                  "Some queries exceeded the distance gate — review above."))


if __name__ == "__main__":
    main()
