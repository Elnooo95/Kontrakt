# AI-kontraktsförklarare – MVP (2 veckor) + Kodstomme

## ⚠️ Viktigt
- Denna app **ersätter inte juridisk rådgivning**. Visa alltid tydlig ansvarsfriskrivning.
- Hantera personuppgifter varsamt (GDPR): dataminimera, kryptera, radera filer enligt policy.

---

## 🚧 2-veckors MVP-plan (dag-för-dag)

### Vecka 1
**Dag 1 – Projekt & ramverk**
- Sätt upp monorepo: `/backend` (FastAPI + SQLite) och `/frontend` (Next.js + Tailwind).
- Grundläggande sidor: Landningssida, Login, Register.
- Miljöfiler (.env-exempel).
- Juridisk ansvarsfriskrivning på landningssidan.

**Dag 2 – Databas & Auth**
- Skapa User- och Document-modeller (SQLite via SQLAlchemy).
- Implementera registrering/inloggning (bcrypt + JWT).
- Skydda `/documents/*`-endpoints (Bearer-token).

**Dag 3 – Uppladdning & Extraktion**
- Endpoint `/documents/upload` tar emot PDF/JPG/PNG/TXT.
- Extraktion: PyMuPDF (PDF) + enkel TXT-stöd. Lägg stub för OCR.
- Spara originalfil till tmp och radera efter bearbetning.

**Dag 4 – Pipeline v1 (sammanfattning)**
- Dela kontrakt i klausuler (rubriker/punktlistor).
- Heuristisk extraktion av nyckeldata (belopp, datum, uppsägning).
- LLM-sammanfattning på enkel svenska. (OpenAI-adapter, temp 0.2)

**Dag 5 – Riskflaggor & Rapport API**
- Enkla regler + LLM-bedömning för Risk/Bevaka/Ofarlig.
- Bygg JSON-rapport med TL;DR, skyldigheter, viktiga datum/belopp, flaggor, citat.
- Endpoint `/documents/{id}` returnerar rapport.

**Dag 6 – Frontend Dashboard**
- Uppladdningsformulär, rapportvy (kort, tabeller, badges).
- Spara JWT i localStorage och använd på API-anrop.
- Visa varningsbanderoll (”ej juridisk rådgivning”).

**Dag 7 – Test & Hårdning**
- Enhetstester av pipeline (dummykontrakt).
- Begränsa filtyper/storlek. CORS. Loggning utan PII.
- Prestanda: Synchronous v1 (enkelt).

### Vecka 2
**Dag 8 – Stripe-prenumeration**
- Backend-endpoint för Checkout-session.
- Webhook för subscription events (created/updated/deleted).
- Knyt Stripe customer till User.

**Dag 9 – Gating & Kundportal**
- Frontend: ”Prenumerera”-knapp → redirect till Stripe Checkout.
- Visa ”Pro-funktioner” endast om `subscription_status='active'`.
- Länk till customer portal.

**Dag 10 – Q&A (RAG-läge light)**
- Endpoint `/documents/{id}/ask` som endast svarar med citat från dokumentet.
- Implementera enkel sökning i klausuler (string match / pgvector-stub).

**Dag 11 – Export & Delning**
- Generera PDF/print-vänlig rapport (HTML → PDF).
- Explicita tidsstämplar och versionsnummer.

**Dag 12 – OCR & Scans (valfritt)**
- Hook för Tesseract eller Google Vision (env-toggle).

**Dag 13 – Säkerhet & Integritet**
- Retentionspolicy (t.ex. radera originalfil direkt och endast spara analys-JSON).
- Kryptering i DB för känsliga fält (om behövs).

**Dag 14 – Go-Live**
- Deploy: Backend (Railway/Fly/Render), Frontend (Vercel/Netlify).
- Minimi-analys (Plausible/Umami), support-mail, onboarding-mail.

---

## 🧪 Acceptanskriterier (MVP)
- Kan registrera/inlogga, ladda upp kontrakt, få rapport på enkel svenska med minst 5 delar:
  TL;DR, skyldigheter, motpartens skyldigheter, viktiga belopp/datum, varningsflaggor med citat.
- Prenumeration via Stripe fungerar i testläge och gate:ad till Pro-funktioner.
- Q&A svarar endast utifrån kontraktet (”Framgår ej i dokumentet” om saknas).

## 🔧 Lokal utveckling
Backend:
```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # lägg in dina nycklar
uvicorn app.main:app --reload
```
Frontend:
```bash
cd frontend
npm i
cp .env.example .env.local
npm run dev
```

## 🌍 Miljövariabler
Se `.env.example` filer i respektive katalog.
