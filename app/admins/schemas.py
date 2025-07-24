from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid

class AdminBase(BaseModel):
    nome: str
    email: EmailStr
    nivel_permissao: int = 1

class AdminCreate(AdminBase):
    senha_hash: str

class AdminUpdate(BaseModel):
    nome: Optional[str] = None
    nivel_permissao: Optional[int] = None

class AdminOut(AdminBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
