import uuid
from datetime import datetime
from caspyorm import Model, fields

class Rota(Model):
    __table_name__ = "rotas"
    id = fields.UUID(primary_key=True, default=uuid.uuid4)
    nome = fields.Text(required=True, index=True)
    origem = fields.Text(required=True)
    destino = fields.Text(required=True)
    paradas = fields.Map(key_field=fields.Text(), value_field=fields.Text())
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
    # Relacionamento 1:1 (embedding) - Endereço
    endereco_rua = fields.Text()
    endereco_numero = fields.Text()
    endereco_cidade = fields.Text()
    endereco_cep = fields.Text()
    endereco_estado = fields.Text()

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

# Em /home/izael/Projetos/Python/ap3/app/models.py

class Viagem(Model):
    __table_name__ = "viagens"
    
    # --- Início da Correção ---
    # A ordem aqui define a chave primária.
    # O primeiro campo vira a "partition key". Os seguintes, "clustering keys".
    data_viagem = fields.Timestamp(primary_key=True, default=datetime.now)
    id = fields.UUID(primary_key=True, default=uuid.uuid4)
    rota_id = fields.UUID(primary_key=True)
    # --- Fim da Correção ---

    veiculo_id = fields.UUID(index=True)
    motorista_id = fields.UUID(index=True)
    hora_partida = fields.Timestamp()
    vagas_disponiveis = fields.Integer()
    status = fields.Text(default="Agendada")

class ViagemAlunos(Model):
    __table_name__ = "viagem_alunos"
    # Garante a ordem correta da chave primária
    aluno_id = fields.UUID(primary_key=True)
    viagem_id = fields.UUID(primary_key=True)
    data_inscricao = fields.Timestamp(default=datetime.now)
    status_embarque = fields.Text(default="pendente")