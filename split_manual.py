"""One-off: split PhysicsLabManual.pdf into per-section .txt source documents.

Run once from repo root:  python split_manual.py
Produces documents/physlab_*.txt (one per lab section) so each chunk has a
meaningful source filename for attribution. Not part of the runtime pipeline.
"""
import re
import sys
from pathlib import Path

import pdfplumber

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PDF = "documents/PhysicsLabManual.pdf"

# Ordered (filename, heading text). Heading spaces become flexible whitespace
# so headings that wrap across PDF line breaks still match.
RAW = [
    ("physlab_00_introduction", "Introduction"),
    ("physlab_01_measurements_uncertainty", "Measurements and Uncertainty"),
    ("physlab_02_graphical_representation", "Graphical Representation"),
    ("physlab_03_vernier_caliper", "The Vernier Caliper"),
    ("physlab_04_micrometer_caliper", "The Micrometer Caliper"),
    ("physlab_05_angle_scale_verniers", "Angle Scale Verniers"),
    ("physlab_06_vectors_equilibrium", "Vectors - Equilibrium of a Particle"),
    ("physlab_07_air_track", "Air Track APPARATUS"),
    ("physlab_08_atwoods_machine", "Atwood's Machine"),
    ("physlab_09_centripetal_force", "Centripetal Force APPARATUS"),
    ("physlab_10_linear_momentum", "Linear Momentum APPARATUS"),
    ("physlab_11_elasticity_shm", "Elasticity and Simple Harmonic Motion"),
    ("physlab_12_buoyancy_boyles_law", "Buoyancy and Boyle's Law Part A"),
]


def pattern(heading: str) -> str:
    """Escape a heading into a regex; spaces match any whitespace and
    apostrophes match either straight (') or curly (’) variants."""
    words = []
    for word in heading.split(" "):
        chars = "".join("['’]" if c in "'’" else re.escape(c) for c in word)
        words.append(chars)
    return r"\s+".join(words)


def main() -> None:
    with pdfplumber.open(PDF) as pdf:
        pages = [(p.extract_text() or "") for p in pdf.pages]
    full = "\n".join(pages[1:])  # skip the table-of-contents page
    full = re.sub(r"\(cid:\d+\)", " ", full).replace("�", "")

    sections = [(name, pattern(h)) for name, h in RAW]
    positions = []
    cursor = 0
    for name, pat in sections:
        match = re.search(pat, full[cursor:])
        if match:
            start = cursor + match.start()
            positions.append(start)
            cursor = start + 1
        else:
            positions.append(None)
            print("NOT FOUND:", name)

    docs = Path("documents")
    written = 0
    for i, (name, _) in enumerate(sections):
        if positions[i] is None:
            continue
        start = positions[i]
        end = next(
            (positions[j] for j in range(i + 1, len(sections))
             if positions[j] is not None),
            len(full),
        )
        seg = full[start:end]
        seg = re.sub(r"[ \t]+\n", "\n", seg)
        seg = re.sub(r"\n{3,}", "\n\n", seg).strip() + "\n"
        (docs / f"{name}.txt").write_text(seg, encoding="utf-8")
        print(f"{name}.txt: {len(seg):5d} chars | {seg[:48]!r}")
        written += 1
    print(f"\nwrote {written} files")


if __name__ == "__main__":
    main()
