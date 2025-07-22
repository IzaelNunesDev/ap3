from fastapi import FastAPI
from app.models import sync_all_tables_async
from app.database import connect_to_db_async
from caspyorm import connection
import os

from app.routes import alunos, veiculos, motoristas, admins, rotas, viagens, viagem_alunos

app = FastAPI(title="Transporter API")

@app.on_event("startup")
async def startup_event():
    await connect_to_db_async()
    await sync_all_tables_async()

@app.on_event("shutdown")
async def shutdown_event():
    await connection.disconnect_async()

app.include_router(alunos.router, prefix="/alunos", tags=["Alunos"])
app.include_router(veiculos.router, prefix="/veiculos", tags=["Veículos"])
app.include_router(motoristas.router, prefix="/motoristas", tags=["Motoristas"])
app.include_router(admins.router, prefix="/admins", tags=["Admins"])
app.include_router(rotas.router, prefix="/rotas", tags=["Rotas"])
app.include_router(viagens.router, prefix="/viagens", tags=["Viagens"])
app.include_router(viagem_alunos.router, prefix="/viagem_alunos", tags=["ViagemAlunos"]) 