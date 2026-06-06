# Validation and Evaluation Plan

## Evaluation Framework
Run all 5 test questions through the system. For each, record:

| Field              | Description                                              |
|--------------------|----------------------------------------------------------|
| Question           | The exact query sent to the system                       |
| Expected Answer    | Ground-truth answer (written before running the system)  |
| System Response    | Exact output from the system                             |
| Retrieved Chunks   | Which chunks were returned (source + snippet)            |
| Accuracy Judgment  | `accurate` / `partially accurate` / `inaccurate`        |
| Failure Analysis   | If inaccurate: specific pipeline reason (not "it was wrong") |

## Retrieval Quality Gate (Milestone 4 Checkpoint)
- Top-3 results for each test query must visually relate to the query.
- Distance scores on top results must be below 0.5.
- If scores exceed 0.6–0.7, retrieval is weak — debug before generation.

## Grounding Test (Milestone 5 Checkpoint)
- Ask one question NOT covered by any document. System must respond with the refusal phrase, not a hallucinated answer.
- Grounded response example: cites a specific document by name.
- Non-grounded response (FAIL): uses general knowledge not traceable to retrieved chunks.

## Chunk Quality Gate (Milestone 3 Checkpoint)
- Print 5 random chunks. Each must be:
  - Readable and self-contained
  - Free of HTML artifacts
  - Between 100–600 characters
  - Tagged with correct source filename

## Success Metrics Summary
| Metric                          | Pass Threshold                   |
|---------------------------------|----------------------------------|
| Total chunks                    | 50–2000                          |
| Retrieval distance (top result) | < 0.5                            |
| Source attribution              | Present in every response        |
| Out-of-scope refusal            | Correctly declines                |
| Failure cases documented        | At least 1, with specific cause  |
