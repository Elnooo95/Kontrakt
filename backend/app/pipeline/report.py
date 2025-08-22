from typing import Dict, List
from .extract import split_into_clauses
from .heuristics import extract_facts, detect_risks
from ..llm_provider import summarize_clauses

def build_report(full_text: str) -> Dict:
    clauses = split_into_clauses(full_text)
    tldr = summarize_clauses(clauses)
    facts = extract_facts(full_text)
    risks = detect_risks(full_text)

    # Naiv skyldighetsutvinning (heuristik)
    skyld_du = [c for c in clauses if "du ska" in c.lower() or "kunden ska" in c.lower()][:6]
    skyld_mot = [c for c in clauses if "vi ska" in c.lower() or "leverantören ska" in c.lower()][:6]

    viktiga_poster = [{"nyckel": "Belopp", "värden": facts.get("belopp", [])},
                      {"nyckel": "Datum", "värden": facts.get("datum", [])}]

    citat = []
    for i, c in enumerate(clauses[:10], start=1):
        citat.append({"klausul": i, "text": c[:400] + ("..." if len(c) > 400 else "")})

    return {
        "tldr": tldr,
        "skyldigheter_du": skyld_du or ["Framgår ej tydligt."],
        "skyldigheter_motpart": skyld_mot or ["Framgår ej tydligt."],
        "viktiga_poster": viktiga_poster,
        "varningsflaggor": risks,
        "citat": citat,
    }
