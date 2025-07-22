from fastapi import APIRouter, HTTPException
from app.models import Admin
import uuid
from typing import List

router = APIRouter()
PydanticAdmin = Admin.as_pydantic()
PydanticAdminCreate = Admin.as_pydantic(exclude=["id"])

@router.post("/", response_model=PydanticAdmin, status_code=201)
async def criar_admin(admin: PydanticAdminCreate):
    return await Admin.create_async(**admin.dict())

@router.get("/", response_model=List[PydanticAdmin])
async def listar_admins():
    return await Admin.all().all_async()

@router.get("/{admin_id}", response_model=PydanticAdmin)
async def obter_admin(admin_id: uuid.UUID):
    admin = await Admin.get_async(id=admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin não encontrado")
    return admin 