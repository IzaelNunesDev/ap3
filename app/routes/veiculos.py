from fastapi import APIRouter, HTTPException, Query
from app.models import Veiculo
import uuid
import logging
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter()
PydanticVeiculo = Veiculo.as_pydantic()
PydanticVeiculoCreate = Veiculo.as_pydantic(exclude=["id"])

logger = logging.getLogger(__name__)

class VeiculoUpdate(BaseModel):
    modelo: Optional[str] = None
    capacidade: Optional[int] = None
    acessivel: Optional[bool] = None
    ano_fabricacao: Optional[int] = None

@router.post("/", response_model=PydanticVeiculo, status_code=201)
async def criar_veiculo(veiculo: PydanticVeiculoCreate):
    logger.info(f"Recebida solicitação para criar veículo: {veiculo.placa}")
    try:
        novo_veiculo = await Veiculo.create_async(**veiculo.dict())
        logger.info(f"Veículo {veiculo.placa} criado com sucesso com ID: {novo_veiculo.id}")
        return novo_veiculo
    except Exception as e:
        logger.error(f"Erro ao criar veículo {veiculo.placa}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao criar o veículo.")

@router.get("/", response_model=List[PydanticVeiculo])
async def listar_veiculos(
    placa: Optional[str] = None,
    modelo: Optional[str] = None,
    limit: int = Query(10, gt=0, description="O número de veículos a serem retornados não pode ser negativo.")
):
    logger.info("Recebida solicitação para listar veículos")
    try:
        query = Veiculo.all()
        if placa:
            query = query.filter(placa=placa).allow_filtering()
        if modelo:
            query = query.filter(modelo=modelo).allow_filtering()
        
        veiculos = await query.limit(limit).all_async()
        logger.info(f"{len(veiculos)} veículos listados com sucesso")
        return veiculos
    except Exception as e:
        logger.error(f"Erro ao listar veículos: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao listar os veículos.")

@router.get("/count/", response_model=int)
async def contar_veiculos():
    logger.info("Recebida solicitação para contar veículos")
    try:
        count = await Veiculo.all().allow_filtering().count_async()
        logger.info(f"Total de veículos: {count}")
        return count
    except Exception as e:
        logger.error(f"Erro ao contar veículos: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao contar os veículos.")

@router.get("/{veiculo_id}", response_model=PydanticVeiculo)
async def obter_veiculo(veiculo_id: uuid.UUID):
    logger.info(f"Recebida solicitação para obter veículo com ID: {veiculo_id}")
    try:
        veiculo = await Veiculo.get_async(id=veiculo_id)
        if not veiculo:
            logger.warning(f"Veículo com ID {veiculo_id} não encontrado")
            raise HTTPException(status_code=404, detail="Veículo não encontrado")
        logger.info(f"Veículo {veiculo.placa} com ID {veiculo_id} obtido com sucesso")
        return veiculo
    except Exception as e:
        logger.error(f"Erro ao obter veículo com ID {veiculo_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao obter o veículo.")

@router.put("/{veiculo_id}", response_model=PydanticVeiculo)
async def atualizar_veiculo(veiculo_id: uuid.UUID, veiculo_data: VeiculoUpdate):
    logger.info(f"Recebida solicitação para atualizar veículo com ID: {veiculo_id}")
    try:
        veiculo = await Veiculo.get_async(id=veiculo_id)
        if not veiculo:
            logger.warning(f"Veículo com ID {veiculo_id} não encontrado para atualização")
            raise HTTPException(status_code=404, detail="Veículo não encontrado")

        update_data = veiculo_data.dict(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização")

        await veiculo.update_async(**update_data)
        logger.info(f"Veículo com ID {veiculo_id} atualizado com sucesso")
        return veiculo
    except Exception as e:
        logger.error(f"Erro ao atualizar veículo com ID {veiculo_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao atualizar o veículo.")

@router.delete("/{veiculo_id}", status_code=204)
async def deletar_veiculo(veiculo_id: uuid.UUID):
    logger.info(f"Recebida solicitação para deletar veículo com ID: {veiculo_id}")
    try:
        veiculo = await Veiculo.get_async(id=veiculo_id)
        if not veiculo:
            logger.warning(f"Veículo com ID {veiculo_id} não encontrado para deleção")
            raise HTTPException(status_code=404, detail="Veículo não encontrado")

        await veiculo.delete_async()
        logger.info(f"Veículo com ID {veiculo_id} deletado com sucesso")
        return {}
    except Exception as e:
        logger.error(f"Erro ao deletar veículo com ID {veiculo_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao deletar o veículo.")