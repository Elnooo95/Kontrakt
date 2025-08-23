# backend/app/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..db import Base, engine, SessionLocal
from ..models import User
from ..schemas import UserCreate, UserLogin, UserOut
from ..security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user_id,   # <-- används för /auth/me
)

router = APIRouter(prefix="/auth", tags=["auth"])

# --- DB dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.on_event("startup")
def init_db():
    Base.metadata.create_all(bind=engine)

# --- Register ---
@router.post("/register", response_model=UserOut)
def register(body: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == body.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="E-post används redan")
    u = User(email=body.email, password_hash=hash_password(body.password))
    db.add(u)
    db.commit()
    db.refresh(u)
    return u

# --- Login ---
@router.post("/login")
def login(body: UserLogin, db: Session = Depends(get_db)):
    u = db.query(User).filter(User.email == body.email).first()
    if not u or not verify_password(body.password, u.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Fel e-post eller lösenord",
        )
    token = create_access_token(u.id)
    return {"access_token": token, "token_type": "bearer"}

# --- Me (kräver Authorization: Bearer <token>) ---
@router.get("/me", response_model=UserOut)
def me(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    u = db.query(User).get(user_id)
    if not u:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return u