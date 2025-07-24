from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

class ViagemAlunosBase(BaseModel):
    viagem_id: uuid.UUID
    aluno_id: uuid.UUID

class ViagemAlunosCreate(ViagemAlunosBase):
    pass

class ViagemAlunosUpdate(BaseModel):
    status_embarque: Optional[str] = None

class ViagemAlunosOut(ViagemAlunosBase):
    data_inscricao: datetime
    status_embarque: str

    class Config:
        orm_mode = True
