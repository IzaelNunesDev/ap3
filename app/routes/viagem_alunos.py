from fastapi import APIRouter, HTTPException, Query
from app.models import ViagemAlunos
import uuid
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()
PydanticViagemAlunos = ViagemAlunos.as_pydantic()
PydanticViagemAlunosCreate = ViagemAlunos.as_pydantic(exclude=[])

class ViagemAlunosUpdate(BaseModel):
    status_embarque: Optional[str] = None

@router.post("/", response_model=PydanticViagemAlunos, status_code=201)
async def criar_viagem_aluno(viagem_aluno: PydanticViagemAlunosCreate):
    return await ViagemAlunos.create_async(**viagem_aluno.dict())

@router.get("/", response_model=List[PydanticViagemAlunos])
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
    
    return await query.limit(limit).all_async()

@router.get("/count/", response_model=int)
async def contar_viagem_alunos():
    return await ViagemAlunos.all().allow_filtering().count_async()

@router.get("/{viagem_id}/{aluno_id}", response_model=PydanticViagemAlunos)
async def obter_viagem_aluno(viagem_id: uuid.UUID, aluno_id: uuid.UUID):
    viagem_aluno = await ViagemAlunos.get_async(viagem_id=viagem_id, aluno_id=aluno_id)
    if not viagem_aluno:
        raise HTTPException(status_code=404, detail="Inscrição não encontrada")
    return viagem_aluno

@router.put("/{viagem_id}/{aluno_id}", response_model=PydanticViagemAlunos)
async def atualizar_viagem_aluno(
    viagem_id: uuid.UUID, 
    aluno_id: uuid.UUID, 
    viagem_aluno_data: ViagemAlunosUpdate
):
    viagem_aluno = await ViagemAlunos.get_async(viagem_id=viagem_id, aluno_id=aluno_id)
    if not viagem_aluno:
        raise HTTPException(status_code=404, detail="Inscrição não encontrada")

    update_data = viagem_aluno_data.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização")

    await viagem_aluno.update_async(**update_data)
    return viagem_aluno

@router.delete("/{viagem_id}/{aluno_id}", status_code=204)
async def deletar_viagem_aluno(viagem_id: uuid.UUID, aluno_id: uuid.UUID):
    viagem_aluno = await ViagemAlunos.get_async(viagem_id=viagem_id, aluno_id=aluno_id)
    if not viagem_aluno:
        raise HTTPException(status_code=404, detail="Inscrição não encontrada")

    await viagem_aluno.delete_async()
    return {}