from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Optional
import uuid

from app.models import Veiculo
from . import schemas

router = APIRouter(
    prefix="/veiculos",
    tags=["Veículos"]
)

@router.post("/", response_model=schemas.VeiculoOut, status_code=status.HTTP_201_CREATED)
async def criar_veiculo(veiculo: schemas.VeiculoCreate):
    # O ID agora é passado no body, conforme o schema
    novo_veiculo = await Veiculo.create_async(**veiculo.dict())
    return novo_veiculo

@router.get("/", response_model=List[schemas.VeiculoOut])
async def listar_veiculos(
    placa: Optional[str] = None,
    modelo: Optional[str] = None,
    limit: int = Query(10, gt=0, description="O número de veículos a serem retornados não pode ser negativo.")
):
    query = Veiculo.all()
    if placa:
        query = query.filter(placa=placa).allow_filtering()
    if modelo:
        query = query.filter(modelo=modelo).allow_filtering()
    
    veiculos = await query.limit(limit).all_async()
    return veiculos

@router.get("/count/", response_model=int)
async def contar_veiculos():
    return await Veiculo.all().allow_filtering().count_async()

@router.get("/{veiculo_id}", response_model=schemas.VeiculoOut)
async def obter_veiculo(veiculo_id: uuid.UUID):
    try:
        veiculo = await Veiculo.get_async(id=veiculo_id)
        return veiculo
    except Veiculo.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Veículo não encontrado")

@router.put("/{veiculo_id}", response_model=schemas.VeiculoOut)
async def atualizar_veiculo(veiculo_id: uuid.UUID, veiculo_data: schemas.VeiculoUpdate):
    try:
        veiculo = await Veiculo.get_async(id=veiculo_id)
    except Veiculo.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Veículo não encontrado")

    update_data = veiculo_data.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nenhum dado fornecido para atualização")

    await veiculo.update_async(**update_data)
    veiculo_atualizado = await Veiculo.get_async(id=veiculo_id)
    return veiculo_atualizado

@router.delete("/{veiculo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_veiculo(veiculo_id: uuid.UUID):
    try:
        veiculo = await Veiculo.get_async(id=veiculo_id)
        await veiculo.delete_async()
        return {}
    except Veiculo.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Veículo não encontrado")
