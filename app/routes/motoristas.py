from fastapi import APIRouter, HTTPException
from app.models import Motorista
import uuid
from typing import List

router = APIRouter()
PydanticMotorista = Motorista.as_pydantic()
PydanticMotoristaCreate = Motorista.as_pydantic(exclude=["id"])

@router.post("/", response_model=PydanticMotorista, status_code=201)
async def criar_motorista(motorista: PydanticMotoristaCreate):
    return await Motorista.create_async(**motorista.dict())

@router.get("/", response_model=List[PydanticMotorista])
async def listar_motoristas():
    return await Motorista.all().all_async()

@router.get("/{motorista_id}", response_model=PydanticMotorista)
async def obter_motorista(motorista_id: uuid.UUID):
    motorista = await Motorista.get_async(id=motorista_id)
    if not motorista:
        raise HTTPException(status_code=404, detail="Motorista não encontrado")
    return motorista 