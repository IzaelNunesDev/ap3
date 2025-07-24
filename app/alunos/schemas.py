from pydantic import BaseModel
from typing import Optional
import uuid

class AlunoBase(BaseModel):
    nome_completo: str
    matricula: str
    email: str
    telefone: Optional[str] = None

class AlunoCreate(AlunoBase):
    senha_hash: Optional[str] = None

class AlunoUpdate(BaseModel):
    nome_completo: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    senha_hash: Optional[str] = None

class AlunoOut(AlunoBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
