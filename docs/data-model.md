# Data Model

## Core Entity: Chunk

Each chunk stored in ChromaDB has the following structure:

| Field         | Type    | Description                                              |
|---------------|---------|----------------------------------------------------------|
| `id`          | string  | Unique ID: `{source_filename}_{chunk_index}`            |
| `text`        | string  | The chunk content (500 chars, ~50 char overlap)         |
| `source`      | string  | Original filename (e.g., `physlab_07_air_track.txt`)    |
| `chunk_index` | int     | Position of this chunk within the source document       |
| `domain`      | string  | Domain tag (e.g., `lab_procedure`)       |

## ChromaDB Collection
- **Collection name:** `unofficial_guide`
- **Embedding model:** `all-MiniLM-L6-v2` (384-dimensional vectors)
- **Distance metric:** cosine (default)

## Source Documents (Target)
- Minimum 10 documents
- Formats accepted: `.txt`, `.pdf` (via pdfplumber)
- Expected total chunks: 50–2000 (flag if outside this range)

## Retrieval Output Shape
```python
{
  "answer": str,         # LLM-generated grounded response
  "sources": list[str],  # List of source filenames cited
  "chunks": list[str]    # Raw retrieved chunk texts (for debugging)
}
```
