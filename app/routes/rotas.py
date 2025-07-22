from fastapi import APIRouter, HTTPException
from app.models import Rota, Viagem, ViagemAlunos, Aluno
import uuid
from typing import List, Optional
from pydantic import BaseModel
import asyncio

router = APIRouter()
PydanticRota = Rota.as_pydantic()
PydanticRotaCreate = Rota.as_pydantic(exclude=["id"])
PydanticAluno = Aluno.as_pydantic()

class RotaUpdate(BaseModel):
    nome: Optional[str] = None
    origem: Optional[str] = None
    destino: Optional[str] = None
    paradas: Optional[dict] = None
    ativo: Optional[bool] = None

@router.post("/", response_model=PydanticRota, status_code=201)
async def criar_rota(rota: PydanticRotaCreate):
    return await Rota.create_async(**rota.dict())

@router.get("/", response_model=List[PydanticRota])
async def listar_rotas(
    nome: Optional[str] = None,
    origem: Optional[str] = None,
    destino: Optional[str] = None,
    limit: int = 10
):
    query = Rota.all()
    if nome:
        query = query.filter(nome=nome)
    if origem:
        query = query.filter(origem=origem).allow_filtering()
    if destino:
        query = query.filter(destino=destino).allow_filtering()
    
    return await query.limit(limit).all_async()

@router.get("/count/", response_model=int)
async def contar_rotas():
    return await Rota.all().allow_filtering().count_async()

@router.get("/{rota_id}", response_model=PydanticRota)
async def obter_rota(rota_id: uuid.UUID):
    rota = await Rota.get_async(id=rota_id)
    if not rota:
        raise HTTPException(status_code=404, detail="Rota não encontrada")
    return rota

@router.put("/{rota_id}", response_model=PydanticRota)
async def atualizar_rota(rota_id: uuid.UUID, rota_data: RotaUpdate):
    rota = await Rota.get_async(id=rota_id)
    if not rota:
        raise HTTPException(status_code=404, detail="Rota não encontrada")

    update_data = rota_data.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização")

    await rota.update_async(**update_data)
    return rota

@router.delete("/{rota_id}", status_code=204)
async def deletar_rota(rota_id: uuid.UUID):
    rota = await Rota.get_async(id=rota_id)
    if not rota:
        raise HTTPException(status_code=404, detail="Rota não encontrada")

    await rota.delete_async()
    return {}

# CONSULTA COMPLEXA 1: Listar todos os alunos de uma rota específica
# Entidades envolvidas: Rota -> Viagem -> ViagemAlunos -> Aluno (4 entidades)
@router.get("/{rota_id}/alunos", response_model=List[PydanticAluno])
async def listar_alunos_na_rota(rota_id: uuid.UUID):
    """
    Consulta complexa que envolve 4 entidades:
    Rota -> Viagem -> ViagemAlunos -> Aluno
    """
    # 1. Encontrar todas as viagens para a rota especificada
    viagens = await Viagem.filter(rota_id=rota_id).all_async()
    if not viagens:
        return []

    # 2. Para cada viagem, buscar os IDs dos alunos inscritos
    aluno_ids = set()
    viagem_ids = [v.id for v in viagens]

    tasks_viagem_alunos = [ViagemAlunos.filter(viagem_id=vid).all_async() for vid in viagem_ids]
    resultados_inscricoes = await asyncio.gather(*tasks_viagem_alunos)

    for inscricoes in resultados_inscricoes:
        for inscricao in inscricoes:
            aluno_ids.add(inscricao.aluno_id)

    if not aluno_ids:
        return []

    # 3. Buscar os detalhes de cada aluno de forma concorrente
    tasks_alunos = [Aluno.get_async(id=aid) for aid in aluno_ids]
    alunos_result = await asyncio.gather(*tasks_alunos)

    # Filtrar resultados nulos caso algum aluno tenha sido deletado
    alunos_finais = [aluno for aluno in alunos_result if aluno is not None]

    return alunos_finais