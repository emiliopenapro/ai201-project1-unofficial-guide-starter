# Week 1 Project — The Unofficial Guide
**Course:** AI201 | Applications of AI Engineering  
**Due:** Monday, June 8th at 2:59AM EDT

---

## Overview

Colleges have two kinds of knowledge: the official kind (course catalogs, housing handbooks, university websites) and the real kind — the stuff students actually share with each other to survive. Rate My Professor reviews. Subreddit threads about which dining hall is worth the walk. Anonymous posts about which off-campus apartments have mold problems. Discord servers where seniors tell freshmen what professors actually want on exams.

In this project, you'll build **The Unofficial Guide**: a RAG (Retrieval-Augmented Generation) system that makes this kind of student-generated knowledge searchable and answerable. A user asks a plain-language question — "Is the housing lottery actually random?" or "Which CS professor gives the most useful feedback?" — and gets a grounded, cited answer drawn from real documents you collected.

This is your first production AI project. More structure is provided here than in later projects — use it to build the habits (spec first, evaluate honestly, document completely) that you'll need when that structure is gone.

---

## Why This Matters

RAG is now one of the most common patterns in production AI engineering. Almost every company building AI features is using some version of it — to ground models on internal documentation, to answer questions from proprietary data, to reduce hallucination in high-stakes contexts. The specific skills you're building this week (chunking strategy, semantic search, grounded generation, honest evaluation) appear in job descriptions for AI engineers at companies of every size. More importantly, you're learning to build systems that are honest about their limitations — a skill that's increasingly in demand as organizations realize that confident-but-wrong AI is a liability.

---

## 🎯 Goals

By completing this project, you will be able to:

- Build an end-to-end document processing pipeline: ingestion, chunking, and embedding.
- Set up and query a vector store for semantic search.
- Generate grounded responses using retrieved context.
- Design and run an evaluation framework to measure how well your system actually works.
- Document your design decisions so someone else could understand and extend your system.

---

## ✅ Features

### Required Features

**Document Ingestion Pipeline:**  
Collect and process at least 10 documents from your chosen domain. Your pipeline must: load the raw documents, clean or preprocess them as needed (remove navigation text, ads, etc.), and produce structured text ready for chunking. Describe this process in your README.

**Chunking Strategy:**  
Split your documents into chunks using a deliberate strategy — not just "split every 500 characters." Your `planning.md` must explain your chunk size, overlap, and why those choices fit your documents. For example, review-style text may warrant smaller chunks than long-form guides.

**Vector Store and Semantic Search:**  
Embed your chunks and store them in a vector database. Given a user query, retrieve the top relevant chunks using semantic similarity search. Your README should name the embedding model you used and reflect on what tradeoffs you'd consider if you were choosing for a production system (cost, context length, multilingual support, local vs. API).

**Grounded Response Generation:**  
Use an LLM to generate an answer to the user's query using only the retrieved chunks as context. Responses should not rely on the model's general knowledge — they should be grounded in what was retrieved. Include source attribution (which document(s) the answer draws from) in every response.

**Query Interface:**  
Build a basic interface for querying your system. This can be a simple web UI, a command-line tool, or a notebook — but it must be usable enough to demonstrate in your video without explaining how to navigate it.

**Evaluation Report:**  
Design 5 test questions with ground-truth answers, then run your system on each and evaluate the results. For each question, your report should document: the question, the correct answer, what your system returned, which chunks were retrieved, and whether the retrieval and response were accurate, partially accurate, or inaccurate. Identify at least one failure case and explain why it happened.

---

### Stretch Features

Complete any of these for extra credit. Update your `planning.md` before starting each one.

**Hybrid Search:**  
Combine semantic search with keyword (BM25) search and compare results to semantic-only.

**Chunking Strategy Comparison:**  
Test 2+ chunking approaches on the same query set and report which performed better and why.

**Metadata Filtering:**  
Allow users to filter by document source, date, or rating (e.g., only show reviews from the past year).

**Conversational Memory:**  
Support multi-turn queries where the system remembers context from the previous question.

---

## 💡 Hints

- Collect your documents before you write any pipeline code. You'll make better chunking decisions once you've read what you're working with.
- Test retrieval before you add generation. A lot of RAG failures are retrieval failures — the LLM can't generate a good answer from bad chunks.
- Your evaluation should surface a failure. If all 5 test questions come back perfect, either your test questions are too easy or your evaluation criteria are too lenient. Make it harder.
- Source citations are not optional. A system that can't tell users where its answers came from isn't production-ready.
- If your system hallucinates (makes up something not in the documents), that's a valuable failure to document in your README — not something to hide.

**If your documents are PDFs** (housing guides, syllabi, handbooks, etc.), use `pdfplumber` to extract text:

```bash
pip install pdfplumber
```

```python
import pdfplumber
pdf = pdfplumber.open("file.pdf")
text = "\n\n".join(p.extract_text() for p in pdf.pages if p.extract_text())
```

Note that `pdfplumber` does not perform OCR — scanned image-only PDFs will produce empty text. Digitally-created PDFs (anything you can select text in) work fine.

---

## 🛠️ Tools and Setup

This project uses a free tool stack — no paid subscriptions or API credits required.

### Recommended Stack

| Component   | Tool                                      | Notes                                      |
|-------------|-------------------------------------------|--------------------------------------------|
| Embeddings  | `sentence-transformers` (`all-MiniLM-L6-v2`) | Runs locally — no API key, no rate limits |
| Vector store | ChromaDB                                 | Runs locally — no account needed           |
| LLM         | Groq (`llama-3.3-70b-versatile`)          | Free tier — sign up at console.groq.com    |

### Getting Started

1. **Fork** the Unofficial Guide starter repo, then **clone your fork** locally.

2. **Create and activate a virtual environment** from inside your cloned repo:

```bash
python -m venv .venv
source .venv/bin/activate        # Mac/Linux
source .venv/Scripts/activate    # Windows (Git Bash)
# or: .venv\Scripts\activate     # Windows (Command Prompt)
```

You should see `(.venv)` in your terminal prompt. Do this before installing anything — it keeps this project's dependencies isolated from the rest of your system.

3. **Install dependencies** — `requirements.txt` is already in the repo:

```bash
pip install -r requirements.txt
```

4. **Set up your API key.** Copy `.env.example` to `.env` in your repo root:

```bash
cp .env.example .env
```

Then replace `your_key_here` with your Groq API key. This file is already listed in `.gitignore` — never commit it. Get a free key at console.groq.com — no credit card required.

---

## Milestone 1: Choose Your Domain and Collect Documents
⏰ ~30 min

Before touching any code, decide what kind of student knowledge your system will make searchable and collect the raw material. Your documents are the foundation of everything — retrieval quality, chunking decisions, and evaluation design all depend on what you're actually working with. Read them before you build anything.

1. **Choose one domain** for your Unofficial Guide. A domain is a *topic or category of knowledge* — not a specific website. For example, "student reviews of CS professors at [university]" is a domain; Rate My Professors is a *source* you'd use to gather documents within that domain. Similarly, "off-campus housing experiences" is a domain; Reddit is a source. Keeping this distinction clear will help you stay focused when collecting documents.

   Strong domain options: course and professor reviews, off-campus housing, campus dining, campus survival guides, or your own campus community. For each, sources might include Rate My Professors, department subreddits, housing forums, Yelp reviews, orientation wikis, or unofficial FAQs.

2. **Identify at least 10 specific source documents, pages, or threads.** Write down each source URL or file path. More sources means better coverage — aim for sources that together answer a range of different questions, not 10 pages that all say the same thing.

3. **Skim your documents before you do anything else.** Notice how they're structured: Are they short reviews or long guides? Are the key facts concentrated in one sentence or spread across paragraphs? This will directly inform your chunking decisions in Milestone 2.

4. **Write a 2–3 sentence summary** of your domain and what makes this knowledge hard to find otherwise. You'll use this in your `planning.md` and README.

### 📍 Checkpoint

You have at least 10 source documents identified (with URLs or file paths) and can describe in plain language what kinds of questions your system will be able to answer. If you can't describe 5 specific questions your system should handle, your domain may be too vague — narrow it down.

Make at least one commit before moving to Milestone 2.

---

## Milestone 2: Write Your Spec Before Any Code
⏰ ~1 hour

Write your `planning.md` before you write a single line of pipeline code. This isn't busywork — the decisions you make here shape every implementation choice downstream, and your spec is what you'll hand to an AI tool to generate code from. A clear spec produces useful AI-generated code. A vague one produces generic code that doesn't fit your system.

> ⚠️ **AI usage guardrail:** Do not ask your AI tool to fill in `planning.md` for you. Use it to understand concepts, pressure-test your decisions, and answer specific questions — not to generate the entire plan. A spec written by AI will produce a system you can't debug. Use the guiding questions and example prompts embedded in each section as starting points for those conversations.

Open the `planning.md` already in your cloned repo. The section headers are pre-populated — fill them in with real content, not placeholders or "TBD."

```markdown
## Domain
[What domain did you choose? Why is this knowledge valuable and hard to find through official channels?]

## Documents
[List your specific sources: URLs, subreddit names, forum threads, or file descriptions. Aim for variety — sources that together cover different subtopics or perspectives within your domain.]

## Chunking Strategy
[How will you split documents into chunks? State your chunk size (in tokens or characters), overlap size, and explain why those numbers fit the structure of your documents.

Guiding questions:
- Are your documents short reviews (1–3 sentences) or long guides (many paragraphs)? How does that affect the right chunk size?
- If a key fact spans two adjacent chunks, will either chunk be retrievable on its own? What does overlap help with?
- How would you know if your chunks are too small? Too large?

Useful AI prompts:
- "Explain how chunk size affects retrieval quality for short, opinion-based reviews."
- "What are the tradeoffs between chunking by paragraph vs. fixed character count for [my document type]?"
- "If I use 200-character chunks for review text, what kinds of queries might this fail for?"]

## Retrieval Approach
[Which embedding model are you using? How many chunks will you retrieve per query (top-k)? What tradeoffs would you weigh in choosing a different embedding model for production?

Guiding questions:
- How many retrieved chunks is enough to give the LLM useful context?
- Why does semantic search find relevant chunks even when the query doesn't share exact words with the document?

Useful AI prompts:
- "What are different strategies for structuring embeddings for short, opinion-based text?"
- "What does top-k mean in a retrieval system, and what are the tradeoffs of setting it too high vs. too low?"]

## Evaluation Plan
[List your 5 test questions with their expected correct answers. Questions should be specific enough that you can judge whether the system's response is right or wrong.]

## Anticipated Challenges
[What could go wrong? Name at least two specific risks.]

## AI Tool Plan
[Which parts of the pipeline do you plan to use AI tools to help implement? For each part, describe what you'll give the AI as input and what you expect it to produce. Be specific.]
```

Additionally:
- **Draw a simple pipeline diagram** and add it to your `planning.md` under a `## Architecture` header. Your diagram should show the five stages: Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation. Label each stage with the tool or library you're using.
- **Review your evaluation plan questions** — each one should have a specific, verifiable expected answer.
- **Update `planning.md`** before starting any stretch features later.

### 📍 Checkpoint

`planning.md` contains all sections with substantive content, including an AI Tool Plan that names specific pipeline components you'll prompt AI to implement. Your pipeline diagram labels each stage with the tool you're using. Your evaluation plan includes 5 specific test questions, each with a clear expected answer that a grader could check a system response against.

Make at least one commit before moving to Milestone 3.

---

## Milestone 3: Build the Document Pipeline
⏰ ~2–3 hours

Your pipeline has two jobs: load your documents into memory and split them into chunks your embedding model can work with. Most RAG failures trace back to bad chunks — chunks that are too large dilute the relevant information, chunks that are too small lose context. Build this carefully and verify the output before moving on. Don't skip the chunk inspection step.

**Start simple.** If you haven't collected your documents yet, begin with plain `.txt` files rather than live web scraping. Some sources (like Rate My Professors) are difficult to scrape due to JavaScript rendering or blocked requests — you may need to copy text manually, use PDFs, or export to a structured format. This is normal and expected.

The 2–3 hour estimate reflects a careful, incremental process. If you find yourself finishing in 20 minutes by having AI generate everything at once, you're moving too fast. Verify each stage before relying on it in the next.

**Steps:**

1. Use your `planning.md` as a prompt to an AI tool to generate your ingestion and chunking code. Share your Documents section, Chunking Strategy section, and pipeline diagram. Ask the AI to implement a script that loads your documents, cleans them, and produces chunks matching your specified chunk size and overlap. Review what it generates: does it match your spec?

2. Write a script that loads all your documents. Save the raw text to a consistent format before you start cleaning.

3. **Clean each document.** Remove anything that isn't the substantive content you want your system to use:
   - **Remove:** HTML tags, navigation menus, cookie banners, ads, footers, repeated site headers, "Read more" links, share buttons, comment counts, and boilerplate.
   - **Keep:** The actual review text, opinions, ratings, descriptions, and any context needed to understand the content (e.g., the professor's name or course number in a review).
   
   After cleaning, print one document and read it. If you still see nav text, leftover HTML entities (`&amp;`, `&nbsp;`), or content that doesn't belong to your domain, clean further before continuing.

4. Implement your chunking strategy from `planning.md`. If you're changing those numbers, update `planning.md` to reflect why.

5. **Print 5 representative chunks and inspect them.** For each, ask: does this make sense on its own? Could someone answer a question from this chunk alone?

   - ✅ **Good chunk** — a complete, retrievable thought: *"Professor Smith's exams are heavily based on lecture slides, not the textbook. Students consistently mention that attending every class is more important than doing the readings. Midterms are curved; finals are not."*
   - ❌ **Bad chunk (too small)** — a fragment: *"Professor Smith's exams are heavily"*
   - ❌ **Bad chunk (too large)** — multiple unrelated topics merged, too diluted to match any specific query
   - ❌ **Bad chunk (HTML artifact)** — `<div class="review-body">Professor Smith&#39;s exams are`

6. Count your total chunks. If you have fewer than 50 chunks across 10 documents, your chunks may be too large. If you have more than 2,000, your chunks may be too small.

### 📍 Checkpoint

Print 5 random chunks. Each one should be readable, substantive, and self-contained. If you see fragments, HTML, or empty strings, debug before embedding — bad chunks cannot be fixed by tuning retrieval later.

Common issues and how to diagnose them:
- **Empty chunks:** Add a `len(chunk) > 0` filter, or check if your documents loaded correctly.
- **HTML artifacts:** Print a raw document before cleaning and compare.
- **All chunks the same length:** Consider whether paragraph or sentence splitting fits your documents better.
- **Chunks from the wrong document:** Check that your metadata (source filename) is attached correctly to each chunk.

Make at least one commit before moving to Milestone 4.

---

## Milestone 4: Embed Your Chunks and Test Retrieval
⏰ ~1–2 hours

Embed your chunks and load them into a vector store, then test retrieval before you layer on generation. This step is where most retrieval bugs surface — and they're far easier to debug here than after you've wired in an LLM. Don't move to Milestone 5 until retrieval is returning relevant results.

**Steps:**

1. Use your `planning.md` Retrieval Approach section and pipeline diagram to prompt an AI tool to generate your embedding and retrieval code. Ask it to implement the embedding step (loading chunks, embedding with `all-MiniLM-L6-v2`, storing in ChromaDB with source metadata) and a retrieval function. If the generated code uses a ChromaDB API call you don't recognize, ask the AI to explain it.

2. Set up your embedding model. Load it with `SentenceTransformer("all-MiniLM-L6-v2")`.

3. Embed all your chunks and load them into ChromaDB along with metadata for each chunk: at minimum, the source document name and the chunk's position in that document.

4. Write a retrieval function that accepts a query string and returns the top-k most relevant chunks along with their source information. Start with k=4 or k=5.

5. **Test retrieval with at least 3 of your 5 evaluation plan queries.** For each, print the returned chunks and their distance scores. Ask: are these actually relevant to the question?

   - ✅ **Good retrieval:** *Query: "What do students say about Professor Smith's exams?" → Top result: "Professor Smith's midterms are heavily curved and focus on lecture slides…" (distance: 0.18)*
   - ❌ **Bad retrieval:** *Top result: "The parking situation near the CS building has gotten worse since construction started." (distance: 0.61)*

6. If retrieval is returning chunks that seem unrelated, debug before moving on:
   - Print a retrieved chunk in full — does it actually contain relevant content?
   - Check distance scores — scores above 0.6–0.7 indicate weak matches.
   - Check chunk content — if chunks look like fragments or HTML leftovers, the cleaning/chunking stage didn't finish correctly.
   - Check metadata — if results are coming from the wrong source, verify each chunk was stored with the correct source filename.
   - Adjust chunk size — if retrieval consistently pulls loosely related content, try larger chunks.

### 📍 Checkpoint

Querying your vector store with 3 of your test questions returns chunks that visibly relate to each question. Distance scores on your top results are below 0.5. If retrieval doesn't feel right, this is the time to fix it — generation won't compensate for poor retrieval.

Make at least one commit before moving to Milestone 5.

---

## Milestone 5: Wire Up Generation and Build Your Interface
⏰ ~1–2 hours

Connect retrieval to an LLM to generate grounded answers, then build a usable interface. The key engineering challenge here is grounding: your prompt must instruct the LLM to answer from the retrieved context only — not from its general training knowledge.

**Steps:**

1. Use your `planning.md` and pipeline diagram to prompt an AI tool to generate the generation and interface code. Your prompt should include: your grounding requirement (answers from retrieved context only, with source attribution), the output format you want (answer + source list), and the Gradio skeleton structure if you're using it. Before running the generated code, read through it — make sure the system prompt actually enforces grounding, not just suggests it.

2. **Connect to your LLM.** Use Groq's `llama-3.3-70b-versatile`. Write a prompt template that passes the retrieved chunks as context and explicitly instructs the model to answer only from that context. Example:

   > "Answer the question using only the information in the provided documents. If the documents don't contain enough information to answer, say 'I don't have enough information on that.'"

3. **Add source attribution** to your response format. The LLM's response should name which document(s) the answer came from — either by instructing the model to cite sources in its response, or by appending retrieved source names programmatically after generation.

4. **Test grounded generation end-to-end on 2–3 queries.** The test: could this response have come from anywhere other than your retrieved chunks?

   - ✅ **Grounded response:** *"According to student reviews of Professor Smith (source: rmp_smith_reviews.txt), exams are heavily curved and focus on lecture material rather than the textbook."*
   - ❌ **Non-grounded response:** *"Professor Smith likely structures exams similarly to most CS professors, emphasizing core concepts and problem-solving skills…"* (This sounds authoritative but came from the model's training data, not your documents.)

   Also ask a question your documents don't cover. The system should explicitly say it doesn't have enough information.

5. **Build your query interface.** The recommended approach is a Gradio web UI:

```bash
pip install gradio
```

```python
import gradio as gr
from query import ask  # or wherever your end-to-end function lives

def handle_query(question):
    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources

with gr.Blocks() as demo:
    inp = gr.Textbox(label="Your question")
    btn = gr.Button("Ask")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=4)
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

demo.launch()
```

Run it with `python app.py` and open `http://localhost:7860`. You can also use Streamlit or a simple CLI — the requirement is that a viewer can understand how to use it from your demo video without narration explaining basic operation.

### 📍 Checkpoint

End-to-end: you enter a query, the system retrieves relevant chunks, and the response cites which document(s) it drew from. When you ask something your documents don't cover, the system declines to answer rather than generating something plausible but unfounded.

Make at least one commit before moving to Milestone 6.

---

## Milestone 6: Evaluate, Document, and Record
⏰ ~1.5–2 hours

Run your evaluation plan, write your README, and record your demo. Identifying and honestly explaining a failure case is more valuable than having a system that appears to work perfectly. Graders are looking for evidence that you understand your system's limitations, not just that it runs.

**Steps:**

1. **Run your system on all 5 test questions** from `planning.md`. For each question, record in your README: the question, the expected answer, the system's actual response, and your accuracy judgment: `accurate`, `partially accurate`, or `inaccurate`.

2. **Identify at least one failure case** — a question where retrieval or generation didn't work as expected. Write a specific explanation of *why* it failed, tied to a part of the pipeline. "The answer was wrong" is not an explanation. "The relevant information was split across a chunk boundary, so the retrieval returned only half the context" is an explanation.

3. **Complete your `README.md`** using the template already in the starter repo. Every section has a guiding prompt — replace the prompts with your actual content. Every section is required; one-liners will not receive full credit.

4. **Write your spec reflection** in the README: describe one way the spec helped guide your implementation and one way your implementation diverged from it and why.

5. **Add the AI usage section** to your README. Describe at least 2 specific instances: what you asked the AI tool to do, what it produced, and what you changed, overrode, or directed differently.

6. **Record a 3–5 minute demo video.** Show:
   - At least 3 different queries with source citations visible in the response
   - One query where retrieval and generation both work well
   - One query where the system struggles or fails (narrate what went wrong)
   - A brief walkthrough of your evaluation report

### 📍 Checkpoint

All 5 evaluation questions are documented with accuracy judgments in your README. At least one failure is explained with a specific cause tied to the pipeline. README covers all required sections. Demo video is recorded and shows all required moments.

Make a final commit with your completed README and evaluation results before submitting.

---

## 📬 Submitting Your Project

Submit all of the following through the Course Portal:

- Link to your forked GitHub repository
- `planning.md` in your repo root (written before implementation, updated before stretch features)
- `README.md` including:
  - Domain and document sources (with specific names/URLs)
  - Chunking strategy and reasoning (chunk size, overlap, why it fits your documents)
  - Sample chunks: at least 5 labeled sample chunks, each with its source document name
  - Embedding model used, and a brief reflection on production tradeoffs
  - Retrieval test results: at least 3 queries, each showing the query and the top returned chunks; for at least 2, a written explanation of why the returned chunks are relevant
  - How grounded generation is enforced in your system (prompt design or pipeline structure)
  - Example responses: at least 2 responses with source attribution visible, plus one out-of-scope query showing the system's refusal response
  - Query interface: a description of the input and output fields, and a sample interaction transcript
  - Evaluation report: all 5 test questions with expected answers, system responses, and accuracy judgments
  - At least one honest failure case with a specific explanation of why it happened
  - Spec reflection: one way the spec helped you, one way implementation diverged from it and why
  - AI usage section: at least 2 specific instances describing what you directed the AI to do and what you revised or overrode
- Demo video (3–5 minutes) showing:
  - At least 3 different queries answered with source citations visible in the response
  - One query where retrieval works well (briefly narrate why the retrieved chunks are relevant)
  - One query where the system struggles or fails (narrate what went wrong)
  - A walkthrough of the evaluation report

---

## 🗺️ How It's Graded

A detailed breakdown of graded features and points can be found on the course grading page.
