from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Optional
import uuid

from app.models import Admin
from . import schemas

router = APIRouter(
    prefix="/admins",
    tags=["Admins"]
)

@router.post("/", response_model=schemas.AdminOut, status_code=status.HTTP_201_CREATED)
async def criar_admin(admin: schemas.AdminCreate):
    novo_admin = await Admin.create_async(**admin.dict())
    return novo_admin

@router.get("/", response_model=List[schemas.AdminOut])
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
    
    admins = await query.limit(limit).all_async()
    return admins

@router.get("/count/", response_model=int)
async def contar_admins():
    return await Admin.all().allow_filtering().count_async()

@router.get("/{admin_id}", response_model=schemas.AdminOut)
async def obter_admin(admin_id: uuid.UUID):
    try:
        admin = await Admin.get_async(id=admin_id)
        return admin
    except Admin.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin não encontrado")

@router.put("/{admin_id}", response_model=schemas.AdminOut)
async def atualizar_admin(admin_id: uuid.UUID, admin_data: schemas.AdminUpdate):
    try:
        admin = await Admin.get_async(id=admin_id)
    except Admin.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin não encontrado")

    update_data = admin_data.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nenhum dado fornecido para atualização")

    await admin.update_async(**update_data)
    admin_atualizado = await Admin.get_async(id=admin_id)
    return admin_atualizado

@router.delete("/{admin_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_admin(admin_id: uuid.UUID):
    try:
        admin = await Admin.get_async(id=admin_id)
        await admin.delete_async()
        return {}
    except Admin.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin não encontrado")
