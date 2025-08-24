# backend/app/routes/documents.py
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import os, tempfile, json

from ..db import SessionLocal
from ..models import Document
from ..security import get_current_user_id
from ..schemas import DocumentOut
from ..pipeline.extract import extract_text_from_pdf
from ..pipeline.report import build_report

router = APIRouter(prefix="/documents", tags=["documents"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def json_dumps(obj):
    return json.dumps(obj, ensure_ascii=False)

def json_loads(s):
    try:
        return json.loads(s) if isinstance(s, str) else s
    except Exception:
        return {}

@router.get("", response_model=List[DocumentOut])  # GET /documents
def list_documents(user_id: int = Depends(get_current_user_id),
                   db: Session = Depends(get_db)):
    rows = (
        db.query(Document)
        .filter(Document.user_id == user_id)
        .order_by(Document.created_at.desc())
        .all()
    )
    # Mappa till schemaformat
    return [
        {"id": d.id, "filename": d.filename, "report": json_loads(d.report_json)}
        for d in rows
    ]

@router.post("/upload", response_model=DocumentOut)  # POST /documents/upload
async def upload(file: UploadFile = File(...),
                 user_id: int = Depends(get_current_user_id),
                 db: Session = Depends(get_db)):
    ext = os.path.splitext(file.filename or "")[-1].lower()
    if ext not in [".pdf", ".txt"]:
        raise HTTPException(status_code=400, detail="Endast PDF eller TXT i denna kodstomme")

    # Spara temporärt
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    # Extrahera text
    try:
        if ext == ".pdf":
            text = extract_text_from_pdf(tmp_path)
        else:
            text = content.decode("utf-8", errors="ignore")
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass

    # Bygg r

