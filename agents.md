# agents.md — Main Router

## Purpose
This file is the first file the Builder reads. It defines the operating model, reading order, and workflow rules for every sprint.

## Project Identity
- **Project:** Physics Lab Procedures — RAG System
- **Course:** AI201 | Applications of AI Engineering
- **Due:** Monday, June 8th, 2:59AM EDT
- **Type:** Local prototype (no deployment required)

## Reading Order (Builder must read in this sequence before any sprint)
1. `agents.md` (this file)
2. `docs/architecture.md`
3. `docs/data-model.md`
4. `docs/api.md`
5. `planning/state.md`
6. `planning/decisions.md`
7. Current sprint folder: `sprints/sprint-N/requirements.md` → `blueprint.md` → `acceptance.md`

## Builder Rules (Non-Negotiable)
- DO NOT write source code until a Dry Run summary has been reviewed and approved.
- DO NOT deviate from the stack defined in `docs/architecture.md`.
- DO NOT invent permissions, business rules, or chunking parameters not in the spec.
- ALL source code goes into `src/`.
- After each milestone, update `planning/state.md` with what was completed and what is next.
- If a contradiction is found between files, STOP and flag it — do not resolve it silently.

## Workflow Per Sprint
1. Read all files in reading order above.
2. Read the current sprint's Architect Pack (requirements → blueprint → acceptance).
3. Produce a Dry Run summary: what is being built, what is OUT OF SCOPE, and any ambiguities found.
4. Wait for Architect approval.
5. Write code into `src/`.
