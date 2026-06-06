# API Integrations

## Groq LLM API

- **Endpoint:** `https://api.groq.com/openai/v1/chat/completions`
- **Model:** `llama-3.3-70b-versatile`
- **Auth:** `GROQ_API_KEY` from `.env`
- **Client:** `groq` Python SDK (`from groq import Groq`)

### System Prompt Template (Grounding Rule — DO NOT MODIFY without logging in decisions.md)
```
You are a helpful assistant for college students. Answer the user's question using ONLY the information provided in the documents below. If the documents do not contain enough information to answer the question, respond with: "I don't have enough information on that based on the available documents." Do not use your general training knowledge. Always cite which document(s) your answer comes from.
```

### Input Format
```python
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": f"Documents:\n{context}\n\nQuestion: {query}"}
]
```

### Output
- Plain text answer with inline source citations.

---

## sentence-transformers (Local — No API Key)
- **Model:** `all-MiniLM-L6-v2`
- **Usage:** `SentenceTransformer("all-MiniLM-L6-v2").encode(texts)`
- **Output:** 384-dim float vectors

---

## ChromaDB (Local — No API Key)
- **Client:** `chromadb.Client()` (ephemeral) or `chromadb.PersistentClient(path="./chroma_db")` (persistent)
- **Use persistent client** so the vector store survives between runs.
