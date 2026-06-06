"""
app.py — Milestone 5 Gradio interface for the Physics Lab Procedures RAG system.

A user types a question about the introductory physics lab experiments and gets
a grounded, source-cited answer (or a refusal if the manual doesn't cover it).

Run:  python src/app.py   ->  http://localhost:7860
"""
import gradio as gr

from query import ask

TITLE = "Physics Lab Procedures — Unofficial Guide"
DESCRIPTION = (
    "Ask a question about the introductory physics lab experiments — air track, "
    "Atwood's machine, vernier caliper, buoyancy, and more. Answers are grounded "
    "**only** in the lab manual and cite the document they came from. If the "
    "manual doesn't cover it, the system says so instead of guessing."
)
EXAMPLES = [
    "How long should the glider take to cross a level air track?",
    "What is the formula for hydrostatic pressure below a fluid surface?",
    "How does each vernier-scale division compare to the main scale?",
    "What do you do if two successive time measurements differ by more than 5%?",
]


def respond(question: str):
    """Gradio handler: question -> (answer, formatted sources)."""
    if not question or not question.strip():
        return "Please enter a question.", ""
    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"]) or "— (not found in the documents)"
    return result["answer"], sources


def build_demo() -> gr.Blocks:
    with gr.Blocks(title=TITLE) as demo:
        gr.Markdown(f"# {TITLE}\n\n{DESCRIPTION}")
        question = gr.Textbox(
            label="Your question",
            placeholder="e.g. What value of H is used when measuring the air track?",
        )
        ask_btn = gr.Button("Ask", variant="primary")
        answer = gr.Textbox(label="Answer", lines=6)
        sources = gr.Textbox(label="Sources (retrieved documents)", lines=3)

        ask_btn.click(respond, inputs=question, outputs=[answer, sources])
        question.submit(respond, inputs=question, outputs=[answer, sources])
        gr.Examples(EXAMPLES, inputs=question)
    return demo


if __name__ == "__main__":
    build_demo().launch(server_name="127.0.0.1", server_port=7860)
