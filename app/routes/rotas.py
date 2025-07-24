from fastapi import APIRouter, HTTPException
from app.models import Rota, Viagem, ViagemAlunos, Aluno
import uuid
import logging
from typing import List, Optional
from pydantic import BaseModel
import asyncio
from fastapi import Query

router = APIRouter()
PydanticRota = Rota.as_pydantic()
PydanticRotaCreate = Rota.as_pydantic(exclude=["id"])
PydanticAluno = Aluno.as_pydantic()

logger = logging.getLogger(__name__)

class RotaUpdate(BaseModel):
    nome: Optional[str] = None
    origem: Optional[str] = None
    destino: Optional[str] = None
    paradas: Optional[dict] = None
    ativo: Optional[bool] = None

@router.post("/", response_model=PydanticRota, status_code=201)
async def criar_rota(rota: PydanticRotaCreate):
    logger.info(f"Recebida solicitação para criar rota: {rota.nome}")
    try:
        nova_rota = await Rota.create_async(**rota.dict())
        logger.info(f"Rota {rota.nome} criada com sucesso com ID: {nova_rota.id}")
        return nova_rota
    except Exception as e:
        logger.error(f"Erro ao criar rota {rota.nome}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao criar a rota.")

@router.get("/", response_model=List[PydanticRota])
async def listar_rotas(
    nome: Optional[str] = None,
    origem: Optional[str] = None,
    destino: Optional[str] = None,
    limit: int = Query(10, gt=0, description="O número de rotas a serem retornadas não pode ser negativo.")
):
    logger.info("Recebida solicitação para listar rotas")
    try:
        query = Rota.all()
        if nome:
            query = query.filter(nome=nome).allow_filtering()
        if origem:
            query = query.filter(origem=origem).allow_filtering()
        if destino:
            query = query.filter(destino=destino).allow_filtering()
        
        rotas = await query.limit(limit).all_async()
        logger.info(f"{len(rotas)} rotas listadas com sucesso")
        return rotas
    except Exception as e:
        logger.error(f"Erro ao listar rotas: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao listar as rotas.")

@router.get("/count/", response_model=int)
async def contar_rotas():
    logger.info("Recebida solicitação para contar rotas")
    try:
        count = await Rota.all().allow_filtering().count_async()
        logger.info(f"Total de rotas: {count}")
        return count
    except Exception as e:
        logger.error(f"Erro ao contar rotas: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao contar as rotas.")

@router.get("/{rota_id}", response_model=PydanticRota)
async def obter_rota(rota_id: uuid.UUID):
    logger.info(f"Recebida solicitação para obter rota com ID: {rota_id}")
    try:
        rota = await Rota.get_async(id=rota_id)
        if not rota:
            logger.warning(f"Rota com ID {rota_id} não encontrada")
            raise HTTPException(status_code=404, detail="Rota não encontrada")
        logger.info(f"Rota {rota.nome} com ID {rota_id} obtida com sucesso")
        return rota
    except Exception as e:
        logger.error(f"Erro ao obter rota com ID {rota_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao obter a rota.")

@router.put("/{rota_id}", response_model=PydanticRota)
async def atualizar_rota(rota_id: uuid.UUID, rota_data: RotaUpdate):
    logger.info(f"Recebida solicitação para atualizar rota com ID: {rota_id}")
    try:
        rota = await Rota.get_async(id=rota_id)
        if not rota:
            logger.warning(f"Rota com ID {rota_id} não encontrada para atualização")
            raise HTTPException(status_code=404, detail="Rota não encontrada")

        update_data = rota_data.dict(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização")

        await rota.update_async(**update_data)
        logger.info(f"Rota com ID {rota_id} atualizada com sucesso")
        return rota
    except Exception as e:
        logger.error(f"Erro ao atualizar rota com ID {rota_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao atualizar a rota.")

@router.delete("/{rota_id}", status_code=204)
async def deletar_rota(rota_id: uuid.UUID):
    logger.info(f"Recebida solicitação para deletar rota com ID: {rota_id}")
    try:
        rota = await Rota.get_async(id=rota_id)
        if not rota:
            logger.warning(f"Rota com ID {rota_id} não encontrada para deleção")
            raise HTTPException(status_code=404, detail="Rota não encontrada")

        await rota.delete_async()
        logger.info(f"Rota com ID {rota_id} deletada com sucesso")
        return {}
    except Exception as e:
        logger.error(f"Erro ao deletar rota com ID {rota_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao deletar a rota.")

@router.get("/{rota_id}/alunos", response_model=List[PydanticAluno])
async def listar_alunos_na_rota(rota_id: uuid.UUID):
    logger.info(f"Listando alunos para a rota {rota_id}")
    try:
        viagens = await Viagem.filter(rota_id=rota_id).all_async()
        if not viagens:
            return []

        aluno_ids = set()
        viagem_ids = [v.id for v in viagens]

        tasks_viagem_alunos = [ViagemAlunos.filter(viagem_id=vid).all_async() for vid in viagem_ids]
        resultados_inscricoes = await asyncio.gather(*tasks_viagem_alunos)

        for inscricoes in resultados_inscricoes:
            for inscricao in inscricoes:
                aluno_ids.add(inscricao.aluno_id)

        if not aluno_ids:
            return []

        tasks_alunos = [Aluno.get_async(id=aid) for aid in aluno_ids]
        alunos_result = await asyncio.gather(*tasks_alunos)

        alunos_finais = [aluno for aluno in alunos_result if aluno is not None]
        logger.info(f"{len(alunos_finais)} alunos encontrados para a rota {rota_id}")
        return alunos_finais
    except Exception as e:
        logger.error(f"Erro ao listar alunos da rota {rota_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro ao processar a solicitação")