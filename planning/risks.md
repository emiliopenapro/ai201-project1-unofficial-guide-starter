# Risks — Known Traps

## RISK-001: Scanned PDF lab manuals won't extract
**Risk:** pdfplumber cannot OCR scanned/image-only PDFs — they produce empty text.  
**Mitigation:** Test each PDF by selecting text in a PDF viewer. If you can select text, it works. If not, retype or find a digital version.  
**Status:** Open — validate each document before Milestone 3.

## RISK-002: Too few chunks (< 50)
**Risk:** Lab procedure documents tend to be short and structured. With large chunk sizes, total chunk count may fall below 50.  
**Mitigation:** Use smaller chunk size (300–400 chars) for structured procedural text. Count chunks after Milestone 3.  
**Status:** Open — validate at Milestone 3 checkpoint.

## RISK-003: Hallucination on out-of-scope queries
**Risk:** Groq LLM may answer from general physics knowledge instead of the retrieved lab documents.  
**Mitigation:** System prompt explicitly instructs refusal if context is insufficient. Test with at least one out-of-scope query in Milestone 5.  
**Status:** Open — validate at Milestone 5 checkpoint.

## RISK-004: Procedural steps split across chunk boundaries
**Risk:** A numbered procedure (e.g., steps 3–5 of an experiment) may be split across chunks, causing retrieval to return incomplete instructions.  
**Mitigation:** Consider paragraph-based chunking rather than fixed-character chunking for step-by-step documents. Log decision in decisions.md.  
**Status:** Open — decide at Milestone 2.

## RISK-005: Deadline pressure causing spec-skipping
**Risk:** Due June 8th — with time pressure, temptation is to skip planning.md and go straight to code.  
**Mitigation:** planning.md is a graded deliverable required before any code (Milestone 2). Do not skip.  
**Status:** Active warning — enforce at Sprint 1.

## RISK-006: Weak retrieval masked by strong LLM
**Risk:** Groq LLM may generate a plausible-sounding physics answer from its training data even when retrieved chunks are irrelevant.  
**Mitigation:** Test retrieval in isolation (Milestone 4) before wiring in the LLM. Check distance scores < 0.5.  
**Status:** Open — validate at Milestone 4 checkpoint.
