from fastapi import APIRouter, HTTPException, Query
from app.models import Aluno
import uuid
import logging
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter()
PydanticAluno = Aluno.as_pydantic()
PydanticAlunoCreate = Aluno.as_pydantic(exclude=["id"])

logger = logging.getLogger(__name__)

class AlunoUpdate(BaseModel):
    nome_completo: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None

@router.post("/", response_model=PydanticAluno, status_code=201)
async def criar_aluno(aluno: PydanticAlunoCreate):
    logger.info(f"Recebida solicitação para criar aluno: {aluno.nome_completo}")
    try:
        novo_aluno = await Aluno.create_async(**aluno.dict())
        logger.info(f"Aluno {aluno.nome_completo} criado com sucesso com ID: {novo_aluno.id}")
        return novo_aluno
    except Exception as e:
        logger.error(f"Erro ao criar aluno {aluno.nome_completo}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao criar o aluno.")

@router.get("/", response_model=List[PydanticAluno])
async def listar_alunos(
    cpf: Optional[str] = None,
    nome: Optional[str] = None,
    email: Optional[str] = None,
    limit: int = Query(10, gt=0, description="O número de alunos a serem retornados não pode ser negativo.")
):
    logger.info("Recebida solicitação para listar alunos")
    try:
        query = Aluno.all()
        if cpf:
            query = query.filter(cpf=cpf).allow_filtering()
        if nome:
            query = query.filter(nome_completo=nome).allow_filtering()
        if email:
            query = query.filter(email=email).allow_filtering()

        alunos = await query.limit(limit).all_async()
        logger.info(f"{len(alunos)} alunos listados com sucesso")
        return alunos
    except Exception as e:
        logger.error(f"Erro ao listar alunos: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao listar os alunos.")

@router.get("/count/", response_model=int)
async def contar_alunos():
    logger.info("Recebida solicitação para contar alunos")
    try:
        count = await Aluno.all().allow_filtering().count_async()
        logger.info(f"Total de alunos: {count}")
        return count
    except Exception as e:
        logger.error(f"Erro ao contar alunos: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao contar os alunos.")

@router.get("/{aluno_id}", response_model=PydanticAluno)
async def obter_aluno(aluno_id: uuid.UUID):
    logger.info(f"Recebida solicitação para obter aluno com ID: {aluno_id}")
    try:
        aluno = await Aluno.get_async(id=aluno_id)
        if not aluno:
            logger.warning(f"Aluno com ID {aluno_id} não encontrado")
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        logger.info(f"Aluno {aluno.nome_completo} com ID {aluno_id} obtido com sucesso")
        return aluno
    except Exception as e:
        logger.error(f"Erro ao obter aluno com ID {aluno_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao obter o aluno.")

@router.put("/{aluno_id}", response_model=PydanticAluno)
async def atualizar_aluno(aluno_id: uuid.UUID, aluno_data: AlunoUpdate):
    logger.info(f"Recebida solicitação para atualizar aluno com ID: {aluno_id}")
    try:
        aluno = await Aluno.get_async(id=aluno_id)
        if not aluno:
            logger.warning(f"Aluno com ID {aluno_id} não encontrado para atualização")
            raise HTTPException(status_code=404, detail="Aluno não encontrado")

        update_data = aluno_data.dict(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização")

        await aluno.update_async(**update_data)
        logger.info(f"Aluno com ID {aluno_id} atualizado com sucesso")
        return aluno
    except Exception as e:
        logger.error(f"Erro ao atualizar aluno com ID {aluno_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao atualizar o aluno.")

@router.delete("/{aluno_id}", status_code=204)
async def deletar_aluno(aluno_id: uuid.UUID):
    logger.info(f"Recebida solicitação para deletar aluno com ID: {aluno_id}")
    try:
        aluno = await Aluno.get_async(id=aluno_id)
        if not aluno:
            logger.warning(f"Aluno com ID {aluno_id} não encontrado para deleção")
            raise HTTPException(status_code=404, detail="Aluno não encontrado")

        await aluno.delete_async()
        logger.info(f"Aluno com ID {aluno_id} deletado com sucesso")
        return {}
    except Exception as e:
        logger.error(f"Erro ao deletar aluno com ID {aluno_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao deletar o aluno.")