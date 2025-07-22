from fastapi import APIRouter, HTTPException
from app.models import Motorista, Viagem, Veiculo
import uuid
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from fastapi import Query

router = APIRouter()
PydanticMotorista = Motorista.as_pydantic()
PydanticMotoristaCreate = Motorista.as_pydantic(exclude=["id"])
PydanticViagem = Viagem.as_pydantic()

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
    return await Motorista.create_async(**motorista.dict())

@router.get("/", response_model=List[PydanticMotorista])
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
    
    return await query.limit(limit).all_async()

@router.get("/count/", response_model=int)
async def contar_motoristas():
    return await Motorista.all().allow_filtering().count_async()

@router.get("/{motorista_id}", response_model=PydanticMotorista)
async def obter_motorista(motorista_id: uuid.UUID):
    motorista = await Motorista.get_async(id=motorista_id)
    if not motorista:
        raise HTTPException(status_code=404, detail="Motorista não encontrado")
    return motorista

@router.put("/{motorista_id}", response_model=PydanticMotorista)
async def atualizar_motorista(motorista_id: uuid.UUID, motorista_data: MotoristaUpdate):
    motorista = await Motorista.get_async(id=motorista_id)
    if not motorista:
        raise HTTPException(status_code=404, detail="Motorista não encontrado")

    update_data = motorista_data.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização")

    await motorista.update_async(**update_data)
    return motorista

@router.delete("/{motorista_id}", status_code=204)
async def deletar_motorista(motorista_id: uuid.UUID):
    motorista = await Motorista.get_async(id=motorista_id)
    if not motorista:
        raise HTTPException(status_code=404, detail="Motorista não encontrado")

    await motorista.delete_async()
    return {}

# CONSULTA COMPLEXA 2: Listar viagens futuras de um motorista com veículo específico
# Entidades envolvidas: Motorista, Veiculo, Viagem (3 entidades)
@router.get("/{motorista_id}/viagens_com_veiculo/{veiculo_id}", response_model=List[PydanticViagem])
async def listar_viagens_motorista_veiculo(motorista_id: uuid.UUID, veiculo_id: uuid.UUID):
    """
    Consulta complexa que envolve 3 entidades:
    Motorista, Veiculo, Viagem
    Lista viagens futuras de um motorista específico usando um veículo específico
    """
    # Verificar se motorista e veículo existem
    motorista = await Motorista.get_async(id=motorista_id)
    if not motorista:
        raise HTTPException(status_code=404, detail="Motorista não encontrado")
    
    veiculo = await Veiculo.get_async(id=veiculo_id)
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")

    # Buscar viagens futuras com a combinação motorista + veículo
    viagens = await Viagem.filter(
        motorista_id=motorista_id,
        veiculo_id=veiculo_id,
        hora_partida__gte=datetime.now()
    ).allow_filtering().all_async()

    if not viagens:
        return []

    return viagens