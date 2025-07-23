from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Optional
import uuid
from datetime import datetime

from app.models import Motorista, Viagem, Veiculo
from . import schemas

router = APIRouter(
    prefix="/motoristas",
    tags=["Motoristas"]
)

@router.post("/", response_model=schemas.MotoristaOut, status_code=status.HTTP_201_CREATED)
async def criar_motorista(motorista: schemas.MotoristaCreate):
    novo_motorista = await Motorista.create_async(**motorista.dict())
    return novo_motorista

@router.get("/", response_model=List[schemas.MotoristaOut])
async def listar_motoristas(
    cpf: Optional[str] = None,
    cidade: Optional[str] = None,
    limit: int = Query(10, gt=0, description="O número de motoristas a serem retornados não pode ser negativo.")
):
    query = Motorista.all()
    if cpf:
        query = query.filter(cpf=cpf).allow_filtering()
    if cidade:
        query = query.filter(endereco_cidade=cidade).allow_filtering()
    
    motoristas = await query.limit(limit).all_async()
    return motoristas

@router.get("/count/", response_model=int)
async def contar_motoristas():
    return await Motorista.all().allow_filtering().count_async()

@router.get("/{motorista_id}", response_model=schemas.MotoristaOut)
async def obter_motorista(motorista_id: uuid.UUID):
    try:
        motorista = await Motorista.get_async(id=motorista_id)
        return motorista
    except Motorista.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Motorista não encontrado")

@router.put("/{motorista_id}", response_model=schemas.MotoristaOut)
async def atualizar_motorista(motorista_id: uuid.UUID, motorista_data: schemas.MotoristaUpdate):
    try:
        motorista = await Motorista.get_async(id=motorista_id)
    except Motorista.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Motorista não encontrado")

    update_data = motorista_data.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nenhum dado fornecido para atualização")

    await motorista.update_async(**update_data)
    motorista_atualizado = await Motorista.get_async(id=motorista_id)
    return motorista_atualizado

@router.delete("/{motorista_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_motorista(motorista_id: uuid.UUID):
    try:
        motorista = await Motorista.get_async(id=motorista_id)
        await motorista.delete_async()
        return {}
    except Motorista.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Motorista não encontrado")

# CONSULTA COMPLEXA 2: Listar viagens futuras de um motorista com veículo específico
@router.get("/{motorista_id}/viagens_com_veiculo/{veiculo_id}", response_model=List[schemas.ViagemOut])
async def listar_viagens_motorista_veiculo(motorista_id: uuid.UUID, veiculo_id: uuid.UUID):
    try:
        await Motorista.get_async(id=motorista_id)
    except Motorista.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Motorista não encontrado")
    
    try:
        await Veiculo.get_async(id=veiculo_id)
    except Veiculo.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Veículo não encontrado")

    viagens = await Viagem.filter(
        motorista_id=motorista_id,
        veiculo_id=veiculo_id,
        data_viagem__gte=datetime.now() # Usar data_viagem ao invés de hora_partida para filtro de data
    ).allow_filtering().all_async()

    return viagens
