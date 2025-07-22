from fastapi import APIRouter, HTTPException
from app.models import Admin
import uuid
from typing import List, Optional
from pydantic import BaseModel
from fastapi import Query

router = APIRouter()
PydanticAdmin = Admin.as_pydantic()
PydanticAdminCreate = Admin.as_pydantic(exclude=["id"])

class AdminUpdate(BaseModel):
    nome: Optional[str] = None
    nivel_permissao: Optional[int] = None

@router.post("/", response_model=PydanticAdmin, status_code=201)
async def criar_admin(admin: PydanticAdminCreate):
    return await Admin.create_async(**admin.dict())

@router.get("/", response_model=List[PydanticAdmin])
async def listar_admins(
    email: Optional[str] = None,
    nivel_permissao: Optional[int] = None,
    limit: int = Query(10, gt=0, description="O número de administradores a serem retornados não pode ser negativo.")
):
    query = Admin.all()
    if email:
        query = query.filter(email=email).allow_filtering()
    if nivel_permissao is not None:
        query = query.filter(nivel_permissao=nivel_permissao).allow_filtering()
    
    return await query.limit(limit).all_async()

@router.get("/count/", response_model=int)
async def contar_admins():
    return await Admin.all().allow_filtering().count_async()

@router.get("/{admin_id}", response_model=PydanticAdmin)
async def obter_admin(admin_id: uuid.UUID):
    admin = await Admin.get_async(id=admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin não encontrado")
    return admin

@router.put("/{admin_id}", response_model=PydanticAdmin)
async def atualizar_admin(admin_id: uuid.UUID, admin_data: AdminUpdate):
    admin = await Admin.get_async(id=admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin não encontrado")

    update_data = admin_data.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização")

    await admin.update_async(**update_data)
    return admin

@router.delete("/{admin_id}", status_code=204)
async def deletar_admin(admin_id: uuid.UUID):
    admin = await Admin.get_async(id=admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin não encontrado")

    await admin.delete_async()
    return {}