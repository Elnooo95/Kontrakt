from pydantic import BaseModel, EmailStr
from typing import Optional, List, Any, Dict

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    subscription_status: Optional[str] = None
    class Config:
        from_attributes = True

class Report(BaseModel):
    tldr: list[str]
    skyldigheter_du: list[str]
    skyldigheter_motpart: list[str]
    viktiga_poster: list[dict]
    varningsflaggor: list[dict]
    citat: list[dict]

class DocumentOut(BaseModel):
    id: int
    filename: str
    report: Dict[str, Any]
