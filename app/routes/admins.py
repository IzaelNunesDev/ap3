from fastapi import APIRouter, HTTPException
from app.models import Admin
import uuid
import logging
from typing import List, Optional
from pydantic import BaseModel
from fastapi import Query

router = APIRouter()
PydanticAdmin = Admin.as_pydantic()
PydanticAdminCreate = Admin.as_pydantic(exclude=["id"])

logger = logging.getLogger(__name__)

class AdminUpdate(BaseModel):
    nome: Optional[str] = None
    nivel_permissao: Optional[int] = None

@router.post("/", response_model=PydanticAdmin, status_code=201)
async def criar_admin(admin: PydanticAdminCreate):
    logger.info(f"Recebida solicitação para criar admin: {admin.nome}")
    try:
        novo_admin = await Admin.create_async(**admin.dict())
        logger.info(f"Admin {admin.nome} criado com sucesso com ID: {novo_admin.id}")
        return novo_admin
    except Exception as e:
        logger.error(f"Erro ao criar admin {admin.nome}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao criar o admin.")

@router.get("/", response_model=List[PydanticAdmin])
async def listar_admins(
    email: Optional[str] = None,
    nivel_permissao: Optional[int] = None,
    limit: int = Query(10, gt=0, description="O número de administradores a serem retornados não pode ser negativo.")
):
    logger.info("Recebida solicitação para listar admins")
    try:
        query = Admin.all()
        if email:
            query = query.filter(email=email).allow_filtering()
        if nivel_permissao is not None:
            query = query.filter(nivel_permissao=nivel_permissao).allow_filtering()
        
        admins = await query.limit(limit).all_async()
        logger.info(f"{len(admins)} admins listados com sucesso")
        return admins
    except Exception as e:
        logger.error(f"Erro ao listar admins: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao listar os admins.")

@router.get("/count/", response_model=int)
async def contar_admins():
    logger.info("Recebida solicitação para contar admins")
    try:
        count = await Admin.all().allow_filtering().count_async()
        logger.info(f"Total de admins: {count}")
        return count
    except Exception as e:
        logger.error(f"Erro ao contar admins: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao contar os admins.")

@router.get("/{admin_id}", response_model=PydanticAdmin)
async def obter_admin(admin_id: uuid.UUID):
    logger.info(f"Recebida solicitação para obter admin com ID: {admin_id}")
    try:
        admin = await Admin.get_async(id=admin_id)
        if not admin:
            logger.warning(f"Admin com ID {admin_id} não encontrado")
            raise HTTPException(status_code=404, detail="Admin não encontrado")
        logger.info(f"Admin {admin.nome} com ID {admin_id} obtido com sucesso")
        return admin
    except Exception as e:
        logger.error(f"Erro ao obter admin com ID {admin_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao obter o admin.")

@router.put("/{admin_id}", response_model=PydanticAdmin)
async def atualizar_admin(admin_id: uuid.UUID, admin_data: AdminUpdate):
    logger.info(f"Recebida solicitação para atualizar admin com ID: {admin_id}")
    try:
        admin = await Admin.get_async(id=admin_id)
        if not admin:
            logger.warning(f"Admin com ID {admin_id} não encontrado para atualização")
            raise HTTPException(status_code=404, detail="Admin não encontrado")

        update_data = admin_data.dict(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização")

        await admin.update_async(**update_data)
        logger.info(f"Admin com ID {admin_id} atualizado com sucesso")
        return admin
    except Exception as e:
        logger.error(f"Erro ao atualizar admin com ID {admin_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao atualizar o admin.")

@router.delete("/{admin_id}", status_code=204)
async def deletar_admin(admin_id: uuid.UUID):
    logger.info(f"Recebida solicitação para deletar admin com ID: {admin_id}")
    try:
        admin = await Admin.get_async(id=admin_id)
        if not admin:
            logger.warning(f"Admin com ID {admin_id} não encontrado para deleção")
            raise HTTPException(status_code=404, detail="Admin não encontrado")

        await admin.delete_async()
        logger.info(f"Admin com ID {admin_id} deletado com sucesso")
        return {}
    except Exception as e:
        logger.error(f"Erro ao deletar admin com ID {admin_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao deletar o admin.")