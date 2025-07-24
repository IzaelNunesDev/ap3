from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Optional
import uuid
import asyncio

from app.models import Rota, Viagem, ViagemAlunos, Aluno
from . import schemas
from app.alunos.schemas import AlunoOut

router = APIRouter(
    prefix="/rotas",
    tags=["Rotas"]
)

@router.post("/", response_model=schemas.RotaOut, status_code=status.HTTP_201_CREATED)
async def criar_rota(rota: schemas.RotaCreate):
    nova_rota = await Rota.create_async(**rota.dict())
    return nova_rota

@router.get("/", response_model=List[schemas.RotaOut])
async def listar_rotas(
    nome: Optional[str] = None,
    origem: Optional[str] = None,
    destino: Optional[str] = None,
    limit: int = Query(10, gt=0, description="O número de rotas a serem retornadas não pode ser negativo.")
):
    query = Rota.all()
    if nome:
        query = query.filter(nome=nome).allow_filtering()
    if origem:
        query = query.filter(origem=origem).allow_filtering()
    if destino:
        query = query.filter(destino=destino).allow_filtering()
    
    rotas = await query.limit(limit).all_async()
    return rotas

@router.get("/count/", response_model=int)
async def contar_rotas():
    return await Rota.all().allow_filtering().count_async()

@router.get("/{rota_id}", response_model=schemas.RotaOut)
async def obter_rota(rota_id: uuid.UUID):
    try:
        rota = await Rota.get_async(id=rota_id)
        return rota
    except Rota.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rota não encontrada")

@router.put("/{rota_id}", response_model=schemas.RotaOut)
async def atualizar_rota(rota_id: uuid.UUID, rota_data: schemas.RotaUpdate):
    try:
        rota = await Rota.get_async(id=rota_id)
    except Rota.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rota não encontrada")

    update_data = rota_data.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nenhum dado fornecido para atualização")

    await rota.update_async(**update_data)
    rota_atualizada = await Rota.get_async(id=rota_id)
    return rota_atualizada

@router.delete("/{rota_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_rota(rota_id: uuid.UUID):
    try:
        rota = await Rota.get_async(id=rota_id)
        await rota.delete_async()
        return {}
    except Rota.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rota não encontrada")

# CONSULTA COMPLEXA 1: Listar todos os alunos de uma rota específica    
@router.get("/{rota_id}/alunos", response_model=List[AlunoOut])
async def listar_alunos_na_rota(rota_id: uuid.UUID):
    viagens = await Viagem.filter(rota_id=rota_id).all_async()
    if not viagens:
        return []

    viagem_ids = [v.id for v in viagens]
    
    tasks_viagem_alunos = [ViagemAlunos.filter(viagem_id=vid).all_async() for vid in viagem_ids]
    resultados_inscricoes = await asyncio.gather(*tasks_viagem_alunos)

    aluno_ids = set()
    for inscricoes in resultados_inscricoes:
        for inscricao in inscricoes:
            aluno_ids.add(inscricao.aluno_id)

    if not aluno_ids:
        return []

    tasks_alunos = [Aluno.get_async(id=aid) for aid in aluno_ids]
    alunos = await asyncio.gather(*tasks_alunos)
    
    return [aluno for aluno in alunos if aluno is not None]
