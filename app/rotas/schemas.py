from pydantic import BaseModel
from typing import Optional, Dict, Any
import uuid

# Schema base para Rota
class RotaBase(BaseModel):
    nome: str
    origem: str
    destino: str
    paradas: Optional[Dict[str, Any]] = None
    ativo: bool = True

# Schema para criação de Rota
class RotaCreate(RotaBase):
    pass

# Schema para atualização de Rota
class RotaUpdate(BaseModel):
    nome: Optional[str] = None
    origem: Optional[str] = None
    destino: Optional[str] = None
    paradas: Optional[Dict[str, Any]] = None
    ativo: Optional[bool] = None

# Schema de saída para Rota
class RotaOut(RotaBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
