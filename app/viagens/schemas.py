from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

class ViagemBase(BaseModel):
    rota_id: uuid.UUID
    data_viagem: datetime
    veiculo_id: uuid.UUID
    motorista_id: uuid.UUID
    hora_partida: datetime
    vagas_disponiveis: int
    status: str = "Agendada"

class ViagemCreate(ViagemBase):
    pass

class ViagemUpdate(BaseModel):
    veiculo_id: Optional[uuid.UUID] = None
    motorista_id: Optional[uuid.UUID] = None
    hora_partida: Optional[datetime] = None
    vagas_disponiveis: Optional[int] = None
    status: Optional[str] = None

class ViagemOut(ViagemBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
