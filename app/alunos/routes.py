from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Optional
import uuid

from app.models import Aluno
from . import schemas

router = APIRouter(
    prefix="/alunos",
    tags=["Alunos"]
)

@router.post("/", response_model=schemas.AlunoOut, status_code=status.HTTP_201_CREATED)
async def criar_aluno(aluno: schemas.AlunoCreate):
    novo_aluno = await Aluno.create_async(**aluno.dict())
    return novo_aluno

@router.get("/", response_model=List[schemas.AlunoOut])
async def listar_alunos(
    matricula: Optional[str] = None,
    nome: Optional[str] = None,
    email: Optional[str] = None,
    limit: int = Query(10, gt=0, description="O número de alunos a serem retornados não pode ser negativo.")
):
    query = Aluno.all()
    if matricula:
        query = query.filter(matricula=matricula).allow_filtering()
    if nome:
        # Supondo que você queira uma busca 'contém', o que não é direto no Cassandra.
        # Mantendo o filtro de igualdade por simplicidade.
        query = query.filter(nome_completo=nome).allow_filtering()
    if email:
        query = query.filter(email=email).allow_filtering()

    alunos = await query.limit(limit).all_async()
    return alunos

@router.get("/count/", response_model=int)
async def contar_alunos():
    return await Aluno.all().allow_filtering().count_async()

@router.get("/{aluno_id}", response_model=schemas.AlunoOut)
async def obter_aluno(aluno_id: uuid.UUID):
    try:
        aluno = await Aluno.get_async(id=aluno_id)
        return aluno
    except Aluno.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado")

@router.put("/{aluno_id}", response_model=schemas.AlunoOut)
async def atualizar_aluno(aluno_id: uuid.UUID, aluno_data: schemas.AlunoUpdate):
    try:
        aluno = await Aluno.get_async(id=aluno_id)
    except Aluno.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado")

    update_data = aluno_data.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nenhum dado fornecido para atualização")

    await aluno.update_async(**update_data)
    # Re-fetch para obter os dados atualizados, já que update_async não os retorna
    aluno_atualizado = await Aluno.get_async(id=aluno_id)
    return aluno_atualizado

@router.delete("/{aluno_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_aluno(aluno_id: uuid.UUID):
    try:
        aluno = await Aluno.get_async(id=aluno_id)
        await aluno.delete_async()
        return {}
    except Aluno.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado")
