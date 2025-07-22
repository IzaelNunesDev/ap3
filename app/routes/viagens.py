from fastapi import APIRouter, HTTPException
from app.models import Viagem
import uuid
from typing import List

router = APIRouter()
PydanticViagem = Viagem.as_pydantic()
PydanticViagemCreate = Viagem.as_pydantic(exclude=["id"])

@router.post("/", response_model=PydanticViagem, status_code=201)
async def criar_viagem(viagem: PydanticViagemCreate):
    return await Viagem.create_async(**viagem.dict())

@router.get("/", response_model=List[PydanticViagem])
async def listar_viagens():
    return await Viagem.all().all_async()

@router.get("/{viagem_id}", response_model=PydanticViagem)
async def obter_viagem(viagem_id: uuid.UUID):
    viagem = await Viagem.get_async(id=viagem_id)
    if not viagem:
        raise HTTPException(status_code=404, detail="Viagem não encontrada")
    return viagem 