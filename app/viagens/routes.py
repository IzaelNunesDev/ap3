from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Optional
import uuid
from datetime import datetime

from app.models import Viagem
from . import schemas

router = APIRouter(
    prefix="/viagens",
    tags=["Viagens"]
)

@router.post("/", response_model=schemas.ViagemOut, status_code=status.HTTP_201_CREATED)
async def criar_viagem(viagem: schemas.ViagemCreate):
    nova_viagem = await Viagem.create_async(**viagem.dict())
    return nova_viagem

@router.get("/", response_model=List[schemas.ViagemOut])
async def listar_viagens(
    rota_id: Optional[uuid.UUID] = None,
    motorista_id: Optional[uuid.UUID] = None,
    veiculo_id: Optional[uuid.UUID] = None,
    status: Optional[str] = None,
    limit: int = Query(10, gt=0, description="O número de viagens a serem retornadas não pode ser negativo.")
):
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
    return viagens

@router.get("/count/", response_model=int)
async def contar_viagens():
    return await Viagem.all().allow_filtering().count_async()

@router.get("/{rota_id}/{data_viagem}/{viagem_id}", response_model=schemas.ViagemOut)
async def obter_viagem(rota_id: uuid.UUID, data_viagem: datetime, viagem_id: uuid.UUID):
    try:
        viagem = await Viagem.get_async(rota_id=rota_id, data_viagem=data_viagem, id=viagem_id)
        return viagem
    except Viagem.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Viagem não encontrada")

@router.put("/{rota_id}/{data_viagem}/{viagem_id}", response_model=schemas.ViagemOut)
async def atualizar_viagem(
    rota_id: uuid.UUID, 
    data_viagem: datetime, 
    viagem_id: uuid.UUID, 
    viagem_data: schemas.ViagemUpdate
):
    try:
        viagem = await Viagem.get_async(rota_id=rota_id, data_viagem=data_viagem, id=viagem_id)
    except Viagem.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Viagem não encontrada")

    update_data = viagem_data.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nenhum dado fornecido para atualização")

    await viagem.update_async(**update_data)
    viagem_atualizada = await Viagem.get_async(rota_id=rota_id, data_viagem=data_viagem, id=viagem_id)
    return viagem_atualizada

@router.delete("/{rota_id}/{data_viagem}/{viagem_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_viagem(rota_id: uuid.UUID, data_viagem: datetime, viagem_id: uuid.UUID):
    try:
        viagem = await Viagem.get_async(rota_id=rota_id, data_viagem=data_viagem, id=viagem_id)
        await viagem.delete_async()
        return {}
    except Viagem.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Viagem não encontrada")
