import asyncio
import uuid
from datetime import datetime, timedelta

from app.database import connect_to_db_async, disconnect_from_db_async
from app.models import Rota, Veiculo, Motorista, Aluno, Admin, Viagem, ViagemAlunos

def print_header(title):
    """Imprime um cabeçalho formatado."""
    print("\n" + "="*80)
    print(f" {title.upper()} ".center(80, "="))
    print("="*80)

def print_subheader(title):
    """Imprime um subcabeçalho."""
    print(f"\n--- {title} ---")

def print_result(item):
    """Imprime um item de resultado de forma legível."""
    if item is None:
        print("   -> Nenhum resultado encontrado.")
        return
    if isinstance(item, list):
        if not item:
            print("   -> Nenhum resultado encontrado.")
            return
        for i in item:
            if hasattr(i, 'dict'):
                 print(f"   -> {i.dict()}")
            else:
                 print(f"   -> {i}")
    else:
        if hasattr(item, 'dict'):
             print(f"   -> {item.dict()}")
        else:
             print(f"   -> {item}")

async def populate_database():
    """Limpa e popula o banco de dados com dados de teste interligados."""
    print_header("Iniciando a População do Banco de Dados")

    print_subheader("Limpando tabelas existentes...")
    from caspyorm.connection import get_async_session

    session = get_async_session()
    tables_to_truncate = ["rotas", "veiculos", "motoristas", "alunos", "admins", "viagens", "viagem_alunos"]
    for table in tables_to_truncate:
        await asyncio.to_thread(session.execute, f"TRUNCATE TABLE {table}")
    print("Tabelas limpas com sucesso.")

    print_subheader("Criando Rotas, Veículos, Motoristas, Alunos e Admins...")

    rota1 = await Rota.create_async(nome="Rota UFC - Terminal", origem="UFC Pici", destino="Terminal Papicu")
    rota2 = await Rota.create_async(nome="Rota Noturna - Centro", origem="Benfica", destino="Praça do Ferreira")

    veiculo1_id = uuid.uuid4()
    veiculo1 = await Veiculo.create_async(id=veiculo1_id, placa="ABC-1234", modelo="Ônibus", capacidade=40)
    veiculo2_id = uuid.uuid4()
    veiculo2 = await Veiculo.create_async(id=veiculo2_id, placa="XYZ-5678", modelo="Micro-ônibus", capacidade=25, acessivel=True)

    motorista1 = await Motorista.create_async(nome_completo="Carlos Souza", cpf="111.222.333-44", cnh="123456789")
    motorista2 = await Motorista.create_async(nome_completo="Ana Pereira", cpf="555.666.777-88", cnh="987654321")

    alunos_data = [
        {"nome_completo": "Beatriz Lima", "matricula": "500001", "email": "bia@ufc.br"},
        {"nome_completo": "Davi Costa", "matricula": "500002", "email": "davi@ufc.br"},
        {"nome_completo": "Helena Dias", "matricula": "500003", "email": "helena@ufc.br"},
        {"nome_completo": "Lucas Martins", "matricula": "500004", "email": "lucas@ufc.br"},
        {"nome_completo": "Sofia Ribeiro", "matricula": "500005", "email": "sofia@ufc.br"},
    ]
    alunos_instances = [Aluno(**data) for data in alunos_data]
    alunos = await Aluno.bulk_create_async(alunos_instances)

    admin1 = await Admin.create_async(nome="Admin Principal", email="admin@rotafacil.com", senha_hash="hash_segura_123", nivel_permissao=5)

    print("Entidades independentes criadas.")

    print_subheader("Criando Viagens...")
    viagem1 = await Viagem.create_async(
        rota_id=rota1.id,
        veiculo_id=veiculo1.id,
        motorista_id=motorista1.id,
        hora_partida=datetime.now() + timedelta(hours=2),
        vagas_disponiveis=veiculo1.capacidade
    )
    viagem2 = await Viagem.create_async(
        rota_id=rota1.id,
        veiculo_id=veiculo2.id,
        motorista_id=motorista2.id,
        hora_partida=datetime.now() + timedelta(days=1),
        vagas_disponiveis=veiculo2.capacidade
    )
    viagem3 = await Viagem.create_async(
        rota_id=rota2.id,
        veiculo_id=veiculo1.id,
        motorista_id=motorista1.id,
        hora_partida=datetime.now() + timedelta(days=2),
        vagas_disponiveis=veiculo1.capacidade
    )
    print("Viagens criadas.")

    print_subheader("Inscrevendo Alunos nas Viagens...")
    await ViagemAlunos.create_async(viagem_id=viagem1.id, aluno_id=alunos[0].id)
    await ViagemAlunos.create_async(viagem_id=viagem1.id, aluno_id=alunos[1].id)
    await ViagemAlunos.create_async(viagem_id=viagem2.id, aluno_id=alunos[2].id)
    await ViagemAlunos.create_async(viagem_id=viagem2.id, aluno_id=alunos[3].id)
    await ViagemAlunos.create_async(viagem_id=viagem3.id, aluno_id=alunos[0].id) # Aluno 0 em duas viagens
    await ViagemAlunos.create_async(viagem_id=viagem3.id, aluno_id=alunos[4].id)
    print("Inscrições de alunos criadas.")
    
    print("\nPopulação do banco de dados concluída!")
    
    return {
        "rota1_id": rota1.id,
        "motorista1_id": motorista1.id,
        "veiculo1_id": veiculo1.id,
        "aluno1_id": alunos[0].id,
        "admin1_id": admin1.id
    }

async def run_simple_queries(ids: dict):
    """Executa e exibe o resultado de consultas simples."""
    print_header("Executando Consultas Simples")

    print_subheader("Listando todos os Veículos (F2)")
    veiculos = await Veiculo.all().all_async()
    print_result(veiculos)

    print_subheader("Obtendo um Aluno por ID (F3 - Read)")
    aluno = await Aluno.get_async(id=ids["aluno1_id"])
    print_result(aluno)
    
    print_subheader("Atualizando o nome do Aluno (F3 - Update)")
    if aluno:
        await aluno.update_async(nome_completo="Beatriz Lima Silva")
        aluno_atualizado = await Aluno.get_async(id=ids["aluno1_id"])
        print_result(aluno_atualizado)

    print_subheader("Deletando o Aluno (F3 - Delete)")
    if aluno:
        await aluno.delete_async()
        try:
            aluno_deletado = await Aluno.get_async(id=ids["aluno1_id"])
        except Aluno.DoesNotExist:
            aluno_deletado = None
        print("   -> Verificando se o aluno foi deletado...")
        print_result(aluno_deletado) # Deve retornar "Nenhum resultado"

    print_subheader("Contando o total de Motoristas (F4)")
    total_motoristas = await Motorista.all().allow_filtering().count_async()
    print(f"   -> Total: {total_motoristas}")

    print_subheader("Listando os 2 primeiros Alunos (F5 - Limitação)")
    alunos_limitados = await Aluno.all().limit(2).all_async()
    print_result(alunos_limitados)
    
    print_subheader("Filtrando Rotas pelo nome 'Rota UFC - Terminal' (F6)")
    rota_filtrada = await Rota.filter(nome="Rota UFC - Terminal").allow_filtering().all_async()
    print_result(rota_filtrada)

    print_subheader("Listando todos os Admins")
    admins = await Admin.all().allow_filtering().all_async()
    print_result(admins)

async def run_complex_queries(ids: dict):
    """Executa e exibe o resultado das consultas complexas."""
    print_header("Executando Consultas Complexas (F7)")

    print_subheader("Consulta 1: Listar todos os alunos da rota 'UFC - Terminal'")
    rota_id = ids["rota1_id"]

    viagens_da_rota = await Viagem.filter(rota_id=rota_id).allow_filtering().all_async()
    print(f"   Passo 1: Encontradas {len(viagens_da_rota)} viagens para a rota.")

    if not viagens_da_rota:
        print("   -> Nenhuma viagem encontrada para esta rota.")
        return

    aluno_ids = set()
    viagem_ids = [v.id for v in viagens_da_rota]
    tasks_viagem_alunos = [ViagemAlunos.filter(viagem_id=vid).allow_filtering().all_async() for vid in viagem_ids]
    resultados_inscricoes = await asyncio.gather(*tasks_viagem_alunos, return_exceptions=True)
    for resultado in resultados_inscricoes:
         if isinstance(resultado, Exception):
              print(f"   Erro ao buscar inscrições: {resultado}")
              continue
         for inscricao in resultado:
             aluno_ids.add(inscricao.aluno_id)
    print(f"   Passo 2: Encontrados {len(aluno_ids)} IDs de alunos únicos inscritos nessas viagens.")

    if not aluno_ids:
        print("   -> Nenhum aluno encontrado para as viagens desta rota.")
        return

    tasks_alunos = []
    for aid in aluno_ids:
        task = asyncio.create_task(safe_get_aluno(aid))
        tasks_alunos.append(task)

    alunos_result = await asyncio.gather(*tasks_alunos, return_exceptions=True)
    alunos_finais = [aluno for aluno in alunos_result if aluno is not None and not isinstance(aluno, Exception)]
    print("   Passo 3: Detalhes dos alunos recuperados.")
    
    print("\n   Resultado Final (Alunos na Rota):")
    print_result(alunos_finais)

    print_subheader("Consulta 2: Listar viagens futuras do Motorista 1 com o Veículo 1")
    motorista_id = ids["motorista1_id"]
    veiculo_id = ids["veiculo1_id"]
    
    viagens = await Viagem.filter(
        motorista_id=motorista_id,
        veiculo_id=veiculo_id,
        data_viagem__gte=datetime.now().date() # Filtrar por data >= hoje
    ).allow_filtering().all_async()

    print("\n   Resultado Final (Viagens do Motorista/Veículo):")
    print_result(viagens)

async def safe_get_aluno(aluno_id: uuid.UUID):
    try:
        return await Aluno.get_async(id=aluno_id)
    except Aluno.DoesNotExist:
        return None
    except Exception as e:
        print(f"   Erro ao buscar aluno {aluno_id}: {e}")
        return None

async def main():
    """Função principal para orquestrar a execução do script."""
    try:
        await connect_to_db_async()
        created_ids = await populate_database()
        await run_simple_queries(created_ids)
        await run_complex_queries(created_ids)
    except Exception as e:
        print(f"\nOcorreu um erro durante a execução: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await disconnect_from_db_async()

if __name__ == "__main__":
    asyncio.run(main())