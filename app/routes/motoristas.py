from fastapi import APIRouter, HTTPException
from app.models import Motorista, Viagem, Veiculo
import uuid
import logging
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from fastapi import Query

router = APIRouter()
PydanticMotorista = Motorista.as_pydantic()
PydanticMotoristaCreate = Motorista.as_pydantic(exclude=["id"])
PydanticViagem = Viagem.as_pydantic()

logger = logging.getLogger(__name__)

class MotoristaUpdate(BaseModel):
    nome_completo: Optional[str] = None
    telefone: Optional[str] = None
    endereco_rua: Optional[str] = None
    endereco_numero: Optional[str] = None
    endereco_cidade: Optional[str] = None
    endereco_cep: Optional[str] = None
    endereco_estado: Optional[str] = None

@router.post("/", response_model=PydanticMotorista, status_code=201)
async def criar_motorista(motorista: PydanticMotoristaCreate):
    logger.info(f"Recebida solicitação para criar motorista: {motorista.nome_completo}")
    try:
        novo_motorista = await Motorista.create_async(**motorista.dict())
        logger.info(f"Motorista {motorista.nome_completo} criado com sucesso com ID: {novo_motorista.id}")
        return novo_motorista
    except Exception as e:
        logger.error(f"Erro ao criar motorista {motorista.nome_completo}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao criar o motorista.")

@router.get("/", response_model=List[PydanticMotorista])
async def listar_motoristas(
    cpf: Optional[str] = None,
    cidade: Optional[str] = None,
    limit: int = Query(10, gt=0, description="O número de motoristas a serem retornados não pode ser negativo.")
):
    logger.info("Recebida solicitação para listar motoristas")
    try:
        query = Motorista.all()
        if cpf:
            query = query.filter(cpf=cpf).allow_filtering()
        if cidade:
            query = query.filter(endereco_cidade=cidade).allow_filtering()
        
        motoristas = await query.limit(limit).all_async()
        logger.info(f"{len(motoristas)} motoristas listados com sucesso")
        return motoristas
    except Exception as e:
        logger.error(f"Erro ao listar motoristas: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao listar os motoristas.")

@router.get("/count/", response_model=int)
async def contar_motoristas():
    logger.info("Recebida solicitação para contar motoristas")
    try:
        count = await Motorista.all().allow_filtering().count_async()
        logger.info(f"Total de motoristas: {count}")
        return count
    except Exception as e:
        logger.error(f"Erro ao contar motoristas: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao contar os motoristas.")

@router.get("/{motorista_id}", response_model=PydanticMotorista)
async def obter_motorista(motorista_id: uuid.UUID):
    logger.info(f"Recebida solicitação para obter motorista com ID: {motorista_id}")
    try:
        motorista = await Motorista.get_async(id=motorista_id)
        if not motorista:
            logger.warning(f"Motorista com ID {motorista_id} não encontrado")
            raise HTTPException(status_code=404, detail="Motorista não encontrado")
        logger.info(f"Motorista {motorista.nome_completo} com ID {motorista_id} obtido com sucesso")
        return motorista
    except Exception as e:
        logger.error(f"Erro ao obter motorista com ID {motorista_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao obter o motorista.")

@router.put("/{motorista_id}", response_model=PydanticMotorista)
async def atualizar_motorista(motorista_id: uuid.UUID, motorista_data: MotoristaUpdate):
    logger.info(f"Recebida solicitação para atualizar motorista com ID: {motorista_id}")
    try:
        motorista = await Motorista.get_async(id=motorista_id)
        if not motorista:
            logger.warning(f"Motorista com ID {motorista_id} não encontrado para atualização")
            raise HTTPException(status_code=404, detail="Motorista não encontrado")

        update_data = motorista_data.dict(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização")

        await motorista.update_async(**update_data)
        logger.info(f"Motorista com ID {motorista_id} atualizado com sucesso")
        return motorista
    except Exception as e:
        logger.error(f"Erro ao atualizar motorista com ID {motorista_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao atualizar o motorista.")

@router.delete("/{motorista_id}", status_code=204)
async def deletar_motorista(motorista_id: uuid.UUID):
    logger.info(f"Recebida solicitação para deletar motorista com ID: {motorista_id}")
    try:
        motorista = await Motorista.get_async(id=motorista_id)
        if not motorista:
            logger.warning(f"Motorista com ID {motorista_id} não encontrado para deleção")
            raise HTTPException(status_code=404, detail="Motorista não encontrado")

        await motorista.delete_async()
        logger.info(f"Motorista com ID {motorista_id} deletado com sucesso")
        return {}
    except Exception as e:
        logger.error(f"Erro ao deletar motorista com ID {motorista_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao deletar o motorista.")

# CONSULTA COMPLEXA 2: Listar viagens futuras de um motorista com veículo específico
# Entidades envolvidas: Motorista, Veiculo, Viagem (3 entidades)
@router.get("/{motorista_id}/viagens_com_veiculo/{veiculo_id}", response_model=List[PydanticViagem])
async def listar_viagens_motorista_veiculo(motorista_id: uuid.UUID, veiculo_id: uuid.UUID):
    logger.info(f"Listando viagens para o motorista {motorista_id} com o veículo {veiculo_id}")
    try:
        motorista = await Motorista.get_async(id=motorista_id)
        if not motorista:
            raise HTTPException(status_code=404, detail="Motorista não encontrado")
        
        veiculo = await Veiculo.get_async(id=veiculo_id)
        if not veiculo:
            raise HTTPException(status_code=404, detail="Veículo não encontrado")

        viagens = await Viagem.filter(
            motorista_id=motorista_id,
            veiculo_id=veiculo_id,
            hora_partida__gte=datetime.now()
        ).allow_filtering().all_async()

        logger.info(f"{len(viagens)} viagens encontradas.")
        return viagens
    except Exception as e:
        logger.error(f"Erro ao listar viagens: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro ao processar a solicitação")