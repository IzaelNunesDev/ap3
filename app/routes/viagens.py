from fastapi import APIRouter, HTTPException
from app.models import Viagem
import uuid
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from fastapi import Query

router = APIRouter()
PydanticViagem = Viagem.as_pydantic()
PydanticViagemCreate = Viagem.as_pydantic(exclude=["id"])

class ViagemUpdate(BaseModel):
    veiculo_id: Optional[uuid.UUID] = None
    motorista_id: Optional[uuid.UUID] = None
    hora_partida: Optional[datetime] = None
    vagas_disponiveis: Optional[int] = None
    status: Optional[str] = None

@router.post("/", response_model=PydanticViagem, status_code=201)
async def criar_viagem(viagem: PydanticViagemCreate):
    return await Viagem.create_async(**viagem.dict())

@router.get("/", response_model=List[PydanticViagem])
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
    
    return await query.limit(limit).all_async()

@router.get("/count/", response_model=int)
async def contar_viagens():
    return await Viagem.all().allow_filtering().count_async()

@router.get("/{rota_id}/{data_viagem}/{viagem_id}", response_model=PydanticViagem)
async def obter_viagem(rota_id: uuid.UUID, data_viagem: datetime, viagem_id: uuid.UUID):
    viagem = await Viagem.get_async(rota_id=rota_id, data_viagem=data_viagem, id=viagem_id)
    if not viagem:
        raise HTTPException(status_code=404, detail="Viagem não encontrada")
    return viagem

@router.put("/{rota_id}/{data_viagem}/{viagem_id}", response_model=PydanticViagem)
async def atualizar_viagem(
    rota_id: uuid.UUID, 
    data_viagem: datetime, 
    viagem_id: uuid.UUID, 
    viagem_data: ViagemUpdate
):
    viagem = await Viagem.get_async(rota_id=rota_id, data_viagem=data_viagem, id=viagem_id)
    if not viagem:
        raise HTTPException(status_code=404, detail="Viagem não encontrada")

    update_data = viagem_data.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização")

    await viagem.update_async(**update_data)
    return viagem

@router.delete("/{rota_id}/{data_viagem}/{viagem_id}", status_code=204)
async def deletar_viagem(rota_id: uuid.UUID, data_viagem: datetime, viagem_id: uuid.UUID):
    viagem = await Viagem.get_async(rota_id=rota_id, data_viagem=data_viagem, id=viagem_id)
    if not viagem:
        raise HTTPException(status_code=404, detail="Viagem não encontrada")

    await viagem.delete_async()
    return {}