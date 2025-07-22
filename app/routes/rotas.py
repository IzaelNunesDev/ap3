from fastapi import APIRouter, HTTPException
from app.models import Rota
import uuid
from typing import List

router = APIRouter()
PydanticRota = Rota.as_pydantic()
PydanticRotaCreate = Rota.as_pydantic(exclude=["id"])

@router.post("/", response_model=PydanticRota, status_code=201)
async def criar_rota(rota: PydanticRotaCreate):
    return await Rota.create_async(**rota.dict())

@router.get("/", response_model=List[PydanticRota])
async def listar_rotas():
    return await Rota.all().all_async()

@router.get("/{rota_id}", response_model=PydanticRota)
async def obter_rota(rota_id: uuid.UUID):
    rota = await Rota.get_async(id=rota_id)
    if not rota:
        raise HTTPException(status_code=404, detail="Rota não encontrada")
    return rota 