from fastapi import APIRouter, HTTPException
from app.models import Viagem
import uuid
import logging
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from fastapi import Query

router = APIRouter()
PydanticViagem = Viagem.as_pydantic()
PydanticViagemCreate = Viagem.as_pydantic(exclude=["id"])

logger = logging.getLogger(__name__)

class ViagemUpdate(BaseModel):
    veiculo_id: Optional[uuid.UUID] = None
    motorista_id: Optional[uuid.UUID] = None
    hora_partida: Optional[datetime] = None
    vagas_disponiveis: Optional[int] = None
    status: Optional[str] = None

@router.post("/", response_model=PydanticViagem, status_code=201)
async def criar_viagem(viagem: PydanticViagemCreate):
    logger.info(f"Recebida solicitação para criar viagem: {viagem}")
    try:
        nova_viagem = await Viagem.create_async(**viagem.dict())
        logger.info(f"Viagem criada com sucesso com ID: {nova_viagem.id}")
        return nova_viagem
    except Exception as e:
        logger.error(f"Erro ao criar viagem: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao criar a viagem.")

@router.get("/", response_model=List[PydanticViagem])
async def listar_viagens(
    rota_id: Optional[uuid.UUID] = None,
    motorista_id: Optional[uuid.UUID] = None,
    veiculo_id: Optional[uuid.UUID] = None,
    status: Optional[str] = None,
    limit: int = Query(10, gt=0, description="O número de viagens a serem retornadas não pode ser negativo.")
):
    logger.info("Recebida solicitação para listar viagens")
    try:
        query = Viagem.all()
        if rota_id:
            query = query.filter(rota_id=rota_id).allow_filtering()
        if motorista_id:
            query = query.filter(motorista_id=motorista_id).allow_filtering()
        if veiculo_id:
            query = query.filter(veiculo_id=veiculo_id).allow_filtering()
        if status:
            query = query.filter(status=status).allow_filtering()
        
        viagens = await query.limit(limit).all_async()
        logger.info(f"{len(viagens)} viagens listadas com sucesso")
        return viagens
    except Exception as e:
        logger.error(f"Erro ao listar viagens: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao listar as viagens.")

@router.get("/count/", response_model=int)
async def contar_viagens():
    logger.info("Recebida solicitação para contar viagens")
    try:
        count = await Viagem.all().allow_filtering().count_async()
        logger.info(f"Total de viagens: {count}")
        return count
    except Exception as e:
        logger.error(f"Erro ao contar viagens: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao contar as viagens.")

@router.get("/{rota_id}/{data_viagem}/{viagem_id}", response_model=PydanticViagem)
async def obter_viagem(rota_id: uuid.UUID, data_viagem: datetime, viagem_id: uuid.UUID):
    logger.info(f"Recebida solicitação para obter viagem com ID {viagem_id}")
    try:
        viagem = await Viagem.get_async(rota_id=rota_id, data_viagem=data_viagem, id=viagem_id)
        if not viagem:
            logger.warning(f"Viagem com ID {viagem_id} não encontrada")
            raise HTTPException(status_code=404, detail="Viagem não encontrada")
        logger.info(f"Viagem obtida com sucesso: {viagem}")
        return viagem
    except Exception as e:
        logger.error(f"Erro ao obter viagem: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao obter a viagem.")

@router.put("/{rota_id}/{data_viagem}/{viagem_id}", response_model=PydanticViagem)
async def atualizar_viagem(
    rota_id: uuid.UUID, 
    data_viagem: datetime, 
    viagem_id: uuid.UUID, 
    viagem_data: ViagemUpdate
):
    logger.info(f"Recebida solicitação para atualizar viagem com ID {viagem_id}")
    try:
        viagem = await Viagem.get_async(rota_id=rota_id, data_viagem=data_viagem, id=viagem_id)
        if not viagem:
            logger.warning(f"Viagem com ID {viagem_id} não encontrada para atualização")
            raise HTTPException(status_code=404, detail="Viagem não encontrada")

        update_data = viagem_data.dict(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização")

        await viagem.update_async(**update_data)
        logger.info(f"Viagem atualizada com sucesso: {viagem}")
        return viagem
    except Exception as e:
        logger.error(f"Erro ao atualizar viagem: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao atualizar a viagem.")

@router.delete("/{rota_id}/{data_viagem}/{viagem_id}", status_code=204)
async def deletar_viagem(rota_id: uuid.UUID, data_viagem: datetime, viagem_id: uuid.UUID):
    logger.info(f"Recebida solicitação para deletar viagem com ID {viagem_id}")
    try:
        viagem = await Viagem.get_async(rota_id=rota_id, data_viagem=data_viagem, id=viagem_id)
        if not viagem:
            logger.warning(f"Viagem com ID {viagem_id} não encontrada para deleção")
            raise HTTPException(status_code=404, detail="Viagem não encontrada")

        await viagem.delete_async()
        logger.info(f"Viagem deletada com sucesso")
        return {}
    except Exception as e:
        logger.error(f"Erro ao deletar viagem: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao deletar a viagem.")