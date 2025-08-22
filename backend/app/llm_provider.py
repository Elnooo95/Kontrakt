import os
from .config import settings

# Stub adapter – byta enkelt till annan leverantör.
def summarize_clauses(clauses: list[str]) -> list[str]:
    # I MVP-stubben använder vi enkla heuristiker. Byt till riktig LLM vid behov.
    res = []
    for c in clauses[:8]:
        s = c.strip()
        if len(s) > 220:
            s = s[:200] + "..."
        res.append(s)
    if not res:
        res = ["Kunde inte generera sammanfattning."]
    return res

def explain_plain_swedish(text: str) -> str:
    # Stub: returnera texten rakt av (i riktig version: ring LLM).
    return text

# OBS: här skulle man anropa OpenAI API med settings.OPENAI_API_KEY
# men lämnas som stub i denna kodstomme för enkel körning lokalt utan nyckel.
