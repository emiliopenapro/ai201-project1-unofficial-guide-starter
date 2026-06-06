"""Run the 5-question evaluation plan end-to-end through the RAG system.

Prints, for each question: the question, expected answer, system response, the
retrieved source(s) + top distance. Used to produce the README evaluation report.

Run from repo root:  python evaluate.py
"""
import sys

sys.path.insert(0, "src")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from query import ask, retrieve  # noqa: E402

# (question, expected ground-truth answer) — from planning.md Evaluation Plan.
EVAL = [
    ("On a properly leveled air track, how long should it take the glider to move across the track?",
     "At least 10 seconds, regardless of which end it starts from."),
    ("What value of H is used when measuring the air track?",
     "H = 1.27 cm."),
    ("When timing runs, what do you do if two successive time measurements differ by more than 5%?",
     "Take another pair of times and continue until two successive times agree within 5%."),
    ("What is the formula for hydrostatic pressure P at depth h below a fluid's surface?",
     "P = P0 + rho*g*h (P0 = surface pressure, rho = fluid density)."),
    ("How does each vernier-scale division compare to the main scale on a vernier caliper?",
     "Each vernier division is 9/10 of a main-scale division."),
]


def run(question: str) -> None:
    ret = retrieve(question)
    res = ask(question)
    print(f"Q: {question}")
    print(f"  retrieved top: {ret['sources'][0]}  (distance {ret['distances'][0]:.3f})")
    print(f"  sources: {res['sources']}")
    print(f"  ANSWER: {res['answer']}")


def main() -> None:
    for i, (q, expected) in enumerate(EVAL, 1):
        print(f"\n===== EVAL {i} =====")
        print(f"  EXPECTED: {expected}")
        run(q)


if __name__ == "__main__":
    main()
