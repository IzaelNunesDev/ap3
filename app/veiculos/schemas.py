from pydantic import BaseModel
from typing import Optional
import uuid

class VeiculoBase(BaseModel):
    placa: str
    modelo: str
    capacidade: int
    acessivel: bool = False
    ano_fabricacao: Optional[int] = None

class VeiculoCreate(VeiculoBase):
    id: uuid.UUID

class VeiculoUpdate(BaseModel):
    modelo: Optional[str] = None
    capacidade: Optional[int] = None
    acessivel: Optional[bool] = None
    ano_fabricacao: Optional[int] = None

class VeiculoOut(VeiculoBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
