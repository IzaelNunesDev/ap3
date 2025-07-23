from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

# Schema base para ViagemAlunos (contém as chaves)
class ViagemAlunosBase(BaseModel):
    viagem_id: uuid.UUID
    aluno_id: uuid.UUID

# Schema para criação (herda as chaves)
class ViagemAlunosCreate(ViagemAlunosBase):
    pass

# Schema para atualização
class ViagemAlunosUpdate(BaseModel):
    status_embarque: Optional[str] = None

# Schema de saída (mostra todos os campos do modelo)
class ViagemAlunosOut(ViagemAlunosBase):
    data_inscricao: datetime
    status_embarque: str

    class Config:
        orm_mode = True
