import uuid
from datetime import datetime
from caspyorm import Model, fields

class Rota(Model):
    __table_name__ = "rotas"
    id = fields.UUID(primary_key=True)
    nome = fields.Text(required=True, index=True)
    origem = fields.Text(required=True)
    destino = fields.Text(required=True)
    paradas = fields.Map(fields.Text(), fields.Text())
    ativo = fields.Boolean(default=True)

class Veiculo(Model):
    __table_name__ = "veiculos"
    id = fields.UUID(primary_key=True)
    placa = fields.Text(required=True, index=True)
    modelo = fields.Text(required=True)
    capacidade = fields.Integer(required=True)
    acessivel = fields.Boolean(default=False)
    ano_fabricacao = fields.Integer()

class Motorista(Model):
    __table_name__ = "motoristas"
    id = fields.UUID(primary_key=True)
    nome_completo = fields.Text(required=True)
    cpf = fields.Text(required=True, index=True)
    cnh = fields.Text(required=True)
    data_nascimento = fields.Timestamp()
    telefone = fields.Text()

class Aluno(Model):
    __table_name__ = "alunos"
    id = fields.UUID(primary_key=True)
    nome_completo = fields.Text(required=True)
    matricula = fields.Text(required=True, index=True)
    email = fields.Text(required=True)
    telefone = fields.Text()
    senha_hash = fields.Text()

class Admin(Model):
    __table_name__ = "admins"
    id = fields.UUID(primary_key=True)
    nome = fields.Text(required=True)
    email = fields.Text(required=True, index=True)
    senha_hash = fields.Text(required=True)
    nivel_permissao = fields.Integer(default=1)

class Viagem(Model):
    __table_name__ = "viagens"
    rota_id = fields.UUID(partition_key=True)
    data_viagem = fields.Timestamp(partition_key=True)
    id = fields.UUID(clustering_key=True, default=uuid.uuid4)
    veiculo_id = fields.UUID(index=True)
    motorista_id = fields.UUID(index=True)
    hora_partida = fields.Timestamp(required=True)
    vagas_disponiveis = fields.Integer(required=True)
    status = fields.Text(default="agendada")

class ViagemAlunos(Model):
    __table_name__ = "viagem_alunos"
    viagem_id = fields.UUID(partition_key=True)
    aluno_id = fields.UUID(clustering_key=True)
    data_inscricao = fields.Timestamp(default=datetime.now)
    status_embarque = fields.Text(default="pendente")

# Função para sincronizar todas as tabelas de forma assíncrona
async def sync_all_tables_async():
    await Rota.sync_table_async()
    await Veiculo.sync_table_async()
    await Motorista.sync_table_async()
    await Aluno.sync_table_async()
    await Admin.sync_table_async()
    await Viagem.sync_table_async()
    await ViagemAlunos.sync_table_async()