from pydantic import BaseModel
from typing import Optional
import uuid

# Schema base com os campos comuns
class AlunoBase(BaseModel):
    nome_completo: str
    matricula: str
    email: str  # Alterado de EmailStr para str para depuração
    telefone: Optional[str] = None

# Schema para a criação de um novo aluno (não inclui o ID)
class AlunoCreate(AlunoBase):
    senha_hash: Optional[str] = None # Senha pode ser opcional na criação inicial

# Schema para a atualização de um aluno (todos os campos são opcionais)
class AlunoUpdate(BaseModel):
    nome_completo: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    senha_hash: Optional[str] = None

# Schema para a representação de um aluno na saída da API (inclui o ID)
class AlunoOut(AlunoBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
