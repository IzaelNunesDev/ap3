from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Optional
import uuid

from app.models import ViagemAlunos
from . import schemas

router = APIRouter(
    prefix="/viagem_alunos",
    tags=["ViagemAlunos"]
)

@router.post("/", response_model=schemas.ViagemAlunosOut, status_code=status.HTTP_201_CREATED)
async def criar_viagem_aluno(viagem_aluno: schemas.ViagemAlunosCreate):
    try:
        # Checar se a inscrição já existe para evitar duplicatas
        await ViagemAlunos.get_async(viagem_id=viagem_aluno.viagem_id, aluno_id=viagem_aluno.aluno_id)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Aluno já inscrito nesta viagem")
    except ViagemAlunos.DoesNotExist:
        # Se não existe, podemos criar
        nova_inscricao = await ViagemAlunos.create_async(**viagem_aluno.dict())
        return nova_inscricao

@router.get("/", response_model=List[schemas.ViagemAlunosOut])
async def listar_viagem_alunos(
    viagem_id: Optional[uuid.UUID] = None,
    aluno_id: Optional[uuid.UUID] = None,
    status_embarque: Optional[str] = None,
    limit: int = Query(10, gt=0, description="O número de inscrições a serem retornadas não pode ser negativo.")
):
    query = ViagemAlunos.all()
    if viagem_id:
        query = query.filter(viagem_id=viagem_id).allow_filtering()
    if aluno_id:
        query = query.filter(aluno_id=aluno_id).allow_filtering()
    if status_embarque:
        query = query.filter(status_embarque=status_embarque).allow_filtering()
    
    inscricoes = await query.limit(limit).all_async()
    return inscricoes

@router.get("/count/", response_model=int)
async def contar_viagem_alunos():
    return await ViagemAlunos.all().allow_filtering().count_async()

@router.get("/{viagem_id}/{aluno_id}", response_model=schemas.ViagemAlunosOut)
async def obter_viagem_aluno(viagem_id: uuid.UUID, aluno_id: uuid.UUID):
    try:
        inscricao = await ViagemAlunos.get_async(viagem_id=viagem_id, aluno_id=aluno_id)
        return inscricao
    except ViagemAlunos.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inscrição não encontrada")

@router.put("/{viagem_id}/{aluno_id}", response_model=schemas.ViagemAlunosOut)
async def atualizar_viagem_aluno(
    viagem_id: uuid.UUID, 
    aluno_id: uuid.UUID, 
    viagem_aluno_data: schemas.ViagemAlunosUpdate
):
    try:
        inscricao = await ViagemAlunos.get_async(viagem_id=viagem_id, aluno_id=aluno_id)
    except ViagemAlunos.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inscrição não encontrada")

    update_data = viagem_aluno_data.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nenhum dado fornecido para atualização")

    await inscricao.update_async(**update_data)
    inscricao_atualizada = await ViagemAlunos.get_async(viagem_id=viagem_id, aluno_id=aluno_id)
    return inscricao_atualizada

@router.delete("/{viagem_id}/{aluno_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_viagem_aluno(viagem_id: uuid.UUID, aluno_id: uuid.UUID):
    try:
        inscricao = await ViagemAlunos.get_async(viagem_id=viagem_id, aluno_id=aluno_id)
        await inscricao.delete_async()
        return {}
    except ViagemAlunos.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inscrição não encontrada")
