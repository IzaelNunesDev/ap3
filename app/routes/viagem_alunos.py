from fastapi import APIRouter, HTTPException, Query
from app.models import ViagemAlunos
import uuid
import logging
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()
PydanticViagemAlunos = ViagemAlunos.as_pydantic()
PydanticViagemAlunosCreate = ViagemAlunos.as_pydantic(exclude=[])

logger = logging.getLogger(__name__)

class ViagemAlunosUpdate(BaseModel):
    status_embarque: Optional[str] = None

@router.post("/", response_model=PydanticViagemAlunos, status_code=201)
async def criar_viagem_aluno(viagem_aluno: PydanticViagemAlunosCreate):
    logger.info(f"Recebida solicitação para criar inscrição de aluno em viagem: {viagem_aluno}")
    try:
        nova_inscricao = await ViagemAlunos.create_async(**viagem_aluno.dict())
        logger.info(f"Inscrição de aluno em viagem criada com sucesso: {nova_inscricao}")
        return nova_inscricao
    except Exception as e:
        logger.error(f"Erro ao criar inscrição de aluno em viagem: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao criar a inscrição.")

@router.get("/", response_model=List[PydanticViagemAlunos])
async def listar_viagem_alunos(
    viagem_id: Optional[uuid.UUID] = None,
    aluno_id: Optional[uuid.UUID] = None,
    status_embarque: Optional[str] = None,
    limit: int = Query(10, gt=0, description="O número de inscrições a serem retornadas não pode ser negativo.")
):
    logger.info("Recebida solicitação para listar inscrições de alunos em viagens")
    try:
        query = ViagemAlunos.all()
        if viagem_id:
            query = query.filter(viagem_id=viagem_id).allow_filtering()
        if aluno_id:
            query = query.filter(aluno_id=aluno_id).allow_filtering()
        if status_embarque:
            query = query.filter(status_embarque=status_embarque).allow_filtering()
        
        inscricoes = await query.limit(limit).all_async()
        logger.info(f"{len(inscricoes)} inscrições listadas com sucesso")
        return inscricoes
    except Exception as e:
        logger.error(f"Erro ao listar inscrições: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao listar as inscrições.")

@router.get("/count/", response_model=int)
async def contar_viagem_alunos():
    logger.info("Recebida solicitação para contar inscrições de alunos em viagens")
    try:
        count = await ViagemAlunos.all().allow_filtering().count_async()
        logger.info(f"Total de inscrições: {count}")
        return count
    except Exception as e:
        logger.error(f"Erro ao contar inscrições: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao contar as inscrições.")

@router.get("/{viagem_id}/{aluno_id}", response_model=PydanticViagemAlunos)
async def obter_viagem_aluno(viagem_id: uuid.UUID, aluno_id: uuid.UUID):
    logger.info(f"Recebida solicitação para obter inscrição com viagem ID {viagem_id} e aluno ID {aluno_id}")
    try:
        viagem_aluno = await ViagemAlunos.get_async(viagem_id=viagem_id, aluno_id=aluno_id)
        if not viagem_aluno:
            logger.warning(f"Inscrição com viagem ID {viagem_id} e aluno ID {aluno_id} não encontrada")
            raise HTTPException(status_code=404, detail="Inscrição não encontrada")
        logger.info(f"Inscrição obtida com sucesso: {viagem_aluno}")
        return viagem_aluno
    except Exception as e:
        logger.error(f"Erro ao obter inscrição: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao obter a inscrição.")

@router.put("/{viagem_id}/{aluno_id}", response_model=PydanticViagemAlunos)
async def atualizar_viagem_aluno(
    viagem_id: uuid.UUID, 
    aluno_id: uuid.UUID, 
    viagem_aluno_data: ViagemAlunosUpdate
):
    logger.info(f"Recebida solicitação para atualizar inscrição com viagem ID {viagem_id} e aluno ID {aluno_id}")
    try:
        viagem_aluno = await ViagemAlunos.get_async(viagem_id=viagem_id, aluno_id=aluno_id)
        if not viagem_aluno:
            logger.warning(f"Inscrição com viagem ID {viagem_id} e aluno ID {aluno_id} não encontrada para atualização")
            raise HTTPException(status_code=404, detail="Inscrição não encontrada")

        update_data = viagem_aluno_data.dict(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização")

        await viagem_aluno.update_async(**update_data)
        logger.info(f"Inscrição atualizada com sucesso: {viagem_aluno}")
        return viagem_aluno
    except Exception as e:
        logger.error(f"Erro ao atualizar inscrição: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao atualizar a inscrição.")

@router.delete("/{viagem_id}/{aluno_id}", status_code=204)
async def deletar_viagem_aluno(viagem_id: uuid.UUID, aluno_id: uuid.UUID):
    logger.info(f"Recebida solicitação para deletar inscrição com viagem ID {viagem_id} e aluno ID {aluno_id}")
    try:
        viagem_aluno = await ViagemAlunos.get_async(viagem_id=viagem_id, aluno_id=aluno_id)
        if not viagem_aluno:
            logger.warning(f"Inscrição com viagem ID {viagem_id} e aluno ID {aluno_id} não encontrada para deleção")
            raise HTTPException(status_code=404, detail="Inscrição não encontrada")

        await viagem_aluno.delete_async()
        logger.info(f"Inscrição deletada com sucesso")
        return {}
    except Exception as e:
        logger.error(f"Erro ao deletar inscrição: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao deletar a inscrição.")