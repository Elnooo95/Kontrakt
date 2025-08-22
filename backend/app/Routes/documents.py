from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..models import Document, User
from ..security import get_current_user_id
from ..schemas import DocumentOut
from ..pipeline.extract import extract_text_from_pdf
from ..pipeline.report import build_report
import os, tempfile

router = APIRouter(prefix="/documents", tags=["documents"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload", response_model=DocumentOut)
async def upload(file: UploadFile = File(...), user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    ext = os.path.splitext(file.filename)[-1].lower()
    if ext not in [".pdf", ".txt"]:
        raise HTTPException(status_code=400, detail="Endast PDF eller TXT i denna kodstomme")
    # Spara temporärt
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    # Extrahera text
    if ext == ".pdf":
        text = extract_text_from_pdf(tmp_path)
    else:
        text = content.decode("utf-8", errors="ignore")

    # Bygg rapport
    report = build_report(text)

    # Spara i DB
    doc = Document(user_id=user_id, filename=file.filename, report_json=json_dumps(report))
    db.add(doc); db.commit(); db.refresh(doc)

    try:
        os.remove(tmp_path)
    except Exception:
        pass

    return {"id": doc.id, "filename": doc.filename, "report": report}

def json_dumps(obj):
    import json
    return json.dumps(obj, ensure_ascii=False)
