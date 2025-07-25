from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import connect_to_db_async, disconnect_from_db_async
from app.models import Rota, Veiculo, Motorista, Aluno, Admin, Viagem, ViagemAlunos
from app.logging_config import setup_logging
from app.alunos import routes as alunos_routes
from app.motoristas import routes as motoristas_routes
from app.rotas import routes as rotas_routes
from app.veiculos import routes as veiculos_routes
from app.admins import routes as admins_routes
from app.viagens import routes as viagens_routes
from app.viagem_alunos import routes as viagem_alunos_routes

setup_logging()
app = FastAPI(
    title="Rota Fácil API",
    description="API para gerenciamento de rotas, veículos, motoristas e alunos.",
    version="1.0.0"
)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await connect_to_db_async()
    await Rota.sync_table_async(auto_apply=True)
    await Veiculo.sync_table_async(auto_apply=True)
    await Motorista.sync_table_async(auto_apply=True)
    await Aluno.sync_table_async(auto_apply=True)
    await Admin.sync_table_async(auto_apply=True)
    await Viagem.sync_table_async(auto_apply=True)
    await ViagemAlunos.sync_table_async(auto_apply=True)

@app.on_event("shutdown")
async def shutdown_event():
    await disconnect_from_db_async()

app.include_router(alunos_routes.router)
app.include_router(motoristas_routes.router)
app.include_router(rotas_routes.router)
app.include_router(veiculos_routes.router)
app.include_router(admins_routes.router)
app.include_router(viagens_routes.router)
app.include_router(viagem_alunos_routes.router)
