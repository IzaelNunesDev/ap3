from fastapi import APIRouter, HTTPException
from app.models import Veiculo
import uuid
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter()
PydanticVeiculo = Veiculo.as_pydantic()
PydanticVeiculoCreate = Veiculo.as_pydantic(exclude=["id"])

class VeiculoUpdate(BaseModel):
    modelo: Optional[str] = None
    capacidade: Optional[int] = None
    acessivel: Optional[bool] = None
    ano_fabricacao: Optional[int] = None

@router.post("/", response_model=PydanticVeiculo, status_code=201)
async def criar_veiculo(veiculo: PydanticVeiculoCreate):
    return await Veiculo.create_async(**veiculo.dict())

@router.get("/", response_model=List[PydanticVeiculo])
async def listar_veiculos(
    placa: Optional[str] = None,
    modelo: Optional[str] = None,
    limit: int = 10
):
    query = Veiculo.all()
    if placa:
        query = query.filter(placa=placa)
    if modelo:
        query = query.filter(modelo=modelo).allow_filtering()
    
    return await query.limit(limit).all_async()

@router.get("/count/", response_model=int)
async def contar_veiculos():
    return await Veiculo.all().allow_filtering().count_async()

@router.get("/{veiculo_id}", response_model=PydanticVeiculo)
async def obter_veiculo(veiculo_id: uuid.UUID):
    veiculo = await Veiculo.get_async(id=veiculo_id)
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    return veiculo

@router.put("/{veiculo_id}", response_model=PydanticVeiculo)
async def atualizar_veiculo(veiculo_id: uuid.UUID, veiculo_data: VeiculoUpdate):
    veiculo = await Veiculo.get_async(id=veiculo_id)
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")

    update_data = veiculo_data.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização")

    await veiculo.update_async(**update_data)
    return veiculo

@router.delete("/{veiculo_id}", status_code=204)
async def deletar_veiculo(veiculo_id: uuid.UUID):
    veiculo = await Veiculo.get_async(id=veiculo_id)
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")

    await veiculo.delete_async()
    return {}