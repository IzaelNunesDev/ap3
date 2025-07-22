from fastapi import APIRouter, HTTPException
from app.models import ViagemAlunos
import uuid
from typing import List

router = APIRouter()
PydanticViagemAlunos = ViagemAlunos.as_pydantic()
PydanticViagemAlunosCreate = ViagemAlunos.as_pydantic()

@router.post("/", response_model=PydanticViagemAlunos, status_code=201)
async def criar_viagem_aluno(viagem_aluno: PydanticViagemAlunosCreate):
    return await ViagemAlunos.create_async(**viagem_aluno.dict())

@router.get("/", response_model=List[PydanticViagemAlunos])
async def listar_viagem_alunos():
    return await ViagemAlunos.all().all_async()

@router.get("/{viagem_id}/{aluno_id}", response_model=PydanticViagemAlunos)
async def obter_viagem_aluno(viagem_id: uuid.UUID, aluno_id: uuid.UUID):
    viagem_aluno = await ViagemAlunos.get_async(viagem_id=viagem_id, aluno_id=aluno_id)
    if not viagem_aluno:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    return viagem_aluno 