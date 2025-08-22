from typing import Tuple, List
import fitz  # PyMuPDF

def extract_text_from_pdf(path: str) -> str:
    doc = fitz.open(path)
    texts = []
    for page in doc:
        texts.append(page.get_text())
    return "\n".join(texts)

def split_into_clauses(text: str) -> List[str]:
    # Enkel split: dela vid rubriker/punktlistor
    import re
    parts = re.split(r"\n\s*(§|\d+\.|[A-ZÅÄÖ ].{0,60}:)\s*", text)
    # Faller tillbaka till stycke-split om inget hittas
    if len(parts) <= 1:
        return [p for p in text.split("\n\n") if p.strip()]
    # Återbygg ungefärliga klausuler
    clauses = []
    buf = []
    for line in text.split("\n"):
        if line.strip().endswith(":") or line.strip().startswith("§"):
            if buf:
                clauses.append("\n".join(buf))
                buf = []
        buf.append(line)
    if buf:
        clauses.append("\n".join(buf))
    return [c for c in clauses if c.strip()]
