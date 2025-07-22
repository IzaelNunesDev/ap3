from fastapi import APIRouter, HTTPException
from app.models import Veiculo
import uuid
from typing import List

router = APIRouter()
PydanticVeiculo = Veiculo.as_pydantic()
PydanticVeiculoCreate = Veiculo.as_pydantic(exclude=["id"])

@router.post("/", response_model=PydanticVeiculo, status_code=201)
async def criar_veiculo(veiculo: PydanticVeiculoCreate):
    return await Veiculo.create_async(**veiculo.dict())

@router.get("/", response_model=List[PydanticVeiculo])
async def listar_veiculos():
    return await Veiculo.all().all_async()

@router.get("/{veiculo_id}", response_model=PydanticVeiculo)
async def obter_veiculo(veiculo_id: uuid.UUID):
    veiculo = await Veiculo.get_async(id=veiculo_id)
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    return veiculo 