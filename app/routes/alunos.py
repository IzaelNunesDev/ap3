from fastapi import APIRouter, HTTPException
from app.models import Aluno
import uuid
from typing import List

router = APIRouter()
PydanticAluno = Aluno.as_pydantic()
PydanticAlunoCreate = Aluno.as_pydantic(exclude=["id"])

@router.post("/", response_model=PydanticAluno, status_code=201)
async def criar_aluno(aluno: PydanticAlunoCreate):
    return await Aluno.create_async(**aluno.dict())

@router.get("/", response_model=List[PydanticAluno])
async def listar_alunos():
    return await Aluno.all().all_async()

@router.get("/{aluno_id}", response_model=PydanticAluno)
async def obter_aluno(aluno_id: uuid.UUID):
    aluno = await Aluno.get_async(id=aluno_id)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno 