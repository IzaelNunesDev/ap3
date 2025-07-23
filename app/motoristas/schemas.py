from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

# Schemas para Motorista
class MotoristaBase(BaseModel):
    nome_completo: str
    cpf: str
    cnh: str
    data_nascimento: Optional[datetime] = None
    telefone: Optional[str] = None
    endereco_rua: Optional[str] = None
    endereco_numero: Optional[str] = None
    endereco_cidade: Optional[str] = None
    endereco_cep: Optional[str] = None
    endereco_estado: Optional[str] = None

class MotoristaCreate(MotoristaBase):
    pass

class MotoristaUpdate(BaseModel):
    nome_completo: Optional[str] = None
    telefone: Optional[str] = None
    endereco_rua: Optional[str] = None
    endereco_numero: Optional[str] = None
    endereco_cidade: Optional[str] = None
    endereco_cep: Optional[str] = None
    endereco_estado: Optional[str] = None

class MotoristaOut(MotoristaBase):
    id: uuid.UUID

    class Config:
        orm_mode = True

# Schema para a saída da consulta complexa de Viagem
# O ideal é que este schema fique em app/viagens/schemas.py no futuro
class ViagemOut(BaseModel):
    id: uuid.UUID
    data_viagem: datetime
    rota_id: uuid.UUID
    veiculo_id: uuid.UUID
    motorista_id: uuid.UUID
    hora_partida: Optional[datetime] = None
    vagas_disponiveis: Optional[int] = None
    status: Optional[str] = None

    class Config:
        orm_mode = True
