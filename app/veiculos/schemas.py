from pydantic import BaseModel
from typing import Optional
import uuid

# Schema base para Veiculo
class VeiculoBase(BaseModel):
    placa: str
    modelo: str
    capacidade: int
    acessivel: bool = False
    ano_fabricacao: Optional[int] = None

# Schema para criação de Veiculo
class VeiculoCreate(VeiculoBase):
    id: uuid.UUID # O ID é obrigatório no modelo CaspyORM

# Schema para atualização de Veiculo
class VeiculoUpdate(BaseModel):
    modelo: Optional[str] = None
    capacidade: Optional[int] = None
    acessivel: Optional[bool] = None
    ano_fabricacao: Optional[int] = None

# Schema de saída para Veiculo
class VeiculoOut(VeiculoBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
