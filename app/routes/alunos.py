from fastapi import APIRouter, HTTPException
from app.models import Aluno
import uuid
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter()
PydanticAluno = Aluno.as_pydantic()
PydanticAlunoCreate = Aluno.as_pydantic(exclude=["id"])

class AlunoUpdate(BaseModel):
    nome_completo: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None

@router.post("/", response_model=PydanticAluno, status_code=201)
async def criar_aluno(aluno: PydanticAlunoCreate):
    return await Aluno.create_async(**aluno.dict())

@router.get("/", response_model=List[PydanticAluno])
async def listar_alunos(limit: int = 10):
    return await Aluno.all().limit(limit).all_async()

@router.get("/count/", response_model=int)
async def contar_alunos():
    return await Aluno.all().allow_filtering().count_async()

@router.get("/{aluno_id}", response_model=PydanticAluno)
async def obter_aluno(aluno_id: uuid.UUID):
    aluno = await Aluno.get_async(id=aluno_id)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno

@router.put("/{aluno_id}", response_model=PydanticAluno)
async def atualizar_aluno(aluno_id: uuid.UUID, aluno_data: AlunoUpdate):
    aluno = await Aluno.get_async(id=aluno_id)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    update_data = aluno_data.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização")

    await aluno.update_async(**update_data)
    return aluno

@router.delete("/{aluno_id}", status_code=204)
async def deletar_aluno(aluno_id: uuid.UUID):
    aluno = await Aluno.get_async(id=aluno_id)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    await aluno.delete_async()
    return {}