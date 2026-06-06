"""
query.py — retrieval (Milestone 4) + grounded generation (Milestone 5).

`retrieve()` returns the top-k most similar chunks from ChromaDB. `ask()` then
passes them to the Groq LLM with the grounding prompt and returns a cited answer.

Run:  python src/query.py
Runs the in-scope sample queries and checks the Retrieval Quality Gate
(top-result distance < 0.5) from docs/validation.md.
"""

import os
import sys

from dotenv import load_dotenv
from groq import Groq

from embed import build_index, embed_texts, get_collection

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

load_dotenv()

TOP_K = 5
GATE_DISTANCE = 0.5  # top-result distance must be below this (docs/validation.md)

# --- Generation config (DEC-002: grounding prompt is verbatim from docs/api.md) ---
LLM_MODEL = "llama-3.3-70b-versatile"
TEMPERATURE = 0.2
REFUSAL = "I don't have enough information on that based on the available documents."
SYSTEM_PROMPT = (
    "You are a helpful assistant for college students. Answer the user's "
    "question using ONLY the information provided in the documents below. If "
    "the documents do not contain enough information to answer the question, "
    "respond with: \"I don't have enough information on that based on the "
    "available documents.\" Do not use your general training knowledge. Always "
    "cite which document(s) your answer comes from."
)

_client: Groq | None = None


def _groq() -> Groq:
    """Return the (cached) Groq client, keyed from GROQ_API_KEY in .env."""
    global _client
    if _client is None:
        _client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    return _client

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


def generate(query: str, sources: list[str], chunks: list[str]) -> str:
    """Generate a grounded answer from retrieved chunks via Groq (DEC-002).

    Each chunk is labelled with its source filename so the model can cite it;
    the system prompt restricts the model to this context and instructs refusal
    when it is insufficient.
    """
    context = "\n\n".join(
        f"[Source: {src}]\n{chunk}" for src, chunk in zip(sources, chunks)
    )
    response = _groq().chat.completions.create(
        model=LLM_MODEL,
        temperature=TEMPERATURE,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",
             "content": f"Documents:\n{context}\n\nQuestion: {query}"},
        ],
    )
    return response.choices[0].message.content.strip()


def ask(query: str, top_k: int = TOP_K) -> dict:
    """End-to-end: retrieve -> grounded generation -> cited answer.

    Returns ``{"answer", "sources", "chunks"}`` (docs/data-model.md). Sources are
    the unique retrieved source filenames — programmatic attribution per DEC-005,
    not parsed from the LLM. On a refusal (out-of-scope query), no sources are
    listed since the answer is not drawn from any document.
    """
    retrieved = retrieve(query, top_k)
    answer = generate(query, retrieved["sources"], retrieved["chunks"])
    if "don't have enough information" in answer.lower():
        sources = []
    else:
        sources = list(dict.fromkeys(retrieved["sources"]))  # dedupe, keep order
    return {"answer": answer, "sources": sources, "chunks": retrieved["chunks"]}


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
