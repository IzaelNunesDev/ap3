from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid

# Schema base para Admin
class AdminBase(BaseModel):
    nome: str
    email: EmailStr
    nivel_permissao: int = 1

# Schema para criação de Admin
class AdminCreate(AdminBase):
    senha_hash: str

# Schema para atualização de Admin
class AdminUpdate(BaseModel):
    nome: Optional[str] = None
    nivel_permissao: Optional[int] = None

# Schema de saída para Admin
class AdminOut(AdminBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
