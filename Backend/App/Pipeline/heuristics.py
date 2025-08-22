import re
from typing import Dict, List

MONEY_RE = re.compile(r"(\d+[\s\,\.]?\d*)\s*(kr|SEK)", re.IGNORECASE)
DATE_RE = re.compile(r"(\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}[\./-]\d{1,2}[\./-]\d{2,4}\b)")
BINDING_RE = re.compile(r"(bindningstid|minsta bindning|bindning)", re.IGNORECASE)
TERMINATION_RE = re.compile(r"(uppsägning|uppsägningstid|säga upp)", re.IGNORECASE)
AUTO_RENEW_RE = re.compile(r"(automatisk förlängning|förlängs automatiskt|förlängs med)", re.IGNORECASE)
LATE_FEE_RE = re.compile(r"(påminnelseavgift|förseningsavgift|dröjsmålsränta)", re.IGNORECASE)
UNILATERAL_RE = re.compile(r"(ensidig|ändra villkor utan|leverantören får ändra)", re.IGNORECASE)
DATA_SHARE_RE = re.compile(r"(dela personuppgifter|tredje part|marknadsföringssyften)", re.IGNORECASE)

def extract_facts(text: str) -> Dict:
    moneys = MONEY_RE.findall(text)
    dates = DATE_RE.findall(text)
    return {
        "belopp": list(set([" ".join(m).strip() if isinstance(m, tuple) else m for m in moneys]))[:10],
        "datum": list(set(dates))[:10]
    }

def detect_risks(text: str) -> List[Dict]:
    rules = [
        ("Bindningstid", BINDING_RE),
        ("Uppsägning", TERMINATION_RE),
        ("Automatisk förlängning", AUTO_RENEW_RE),
        ("Avgifter/försening", LATE_FEE_RE),
        ("Ensida ändringar", UNILATERAL_RE),
        ("Delning av personuppgifter", DATA_SHARE_RE),
    ]
    findings = []
    for label, rx in rules:
        for m in rx.finditer(text):
            snippet = text[max(0, m.start()-80): m.end()+80].replace("\n", " ")
            findings.append({"typ": label, "klass": "Bevaka", "varför": f"Hittade nyckelord för {label.lower()}.", "citat": snippet})
    return findings[:20]
