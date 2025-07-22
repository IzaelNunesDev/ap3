from fastapi import FastAPI
from app.database import connect_to_db_async, disconnect_from_db_async
from app.models import Rota, Veiculo, Motorista, Aluno, Admin, Viagem, ViagemAlunos

# Importa todos os seus arquivos de rota
from app.routes import alunos, veiculos, motoristas, admins, rotas, viagens, viagem_alunos

app = FastAPI(
    title="Rota Fácil API",
    description="API para gerenciamento de rotas, veículos, motoristas e alunos.",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    await connect_to_db_async()
    # Sincroniza todas as tabelas para garantir que o schema esteja correto
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

# Inclui todos os routers na aplicação
app.include_router(alunos.router, prefix="/alunos", tags=["Alunos"])
app.include_router(veiculos.router, prefix="/veiculos", tags=["Veículos"])
app.include_router(motoristas.router, prefix="/motoristas", tags=["Motoristas"])
app.include_router(admins.router, prefix="/admins", tags=["Admins"])
app.include_router(rotas.router, prefix="/rotas", tags=["Rotas"])
app.include_router(viagens.router, prefix="/viagens", tags=["Viagens"])
app.include_router(viagem_alunos.router, prefix="/viagem_alunos", tags=["ViagemAlunos"])
