import logging
import os
from dotenv import load_dotenv
from caspyorm import connection

# Carrega as variáveis de ambiente
load_dotenv()

# Variáveis de ambiente para conexão com o AstraDB
ASTRA_CLIENT_ID = os.getenv("ASTRA_CLIENT_ID")
ASTRA_CLIENT_SECRET = os.getenv("ASTRA_CLIENT_SECRET")
ASTRA_BUNDLE_PATH = os.getenv("ASTRA_BUNDLE_PATH")
ASTRA_KEYSPACE = os.getenv("ASTRA_KEYSPACE")

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def connect_to_db_async():
    try:
        logging.info("Iniciando conexão com o AstraDB via caspyorm...")

        # Conecta usando a função nativa do caspyorm, passando os parâmetros necessários
        await connection.connect_async(
            secure_connect_bundle=ASTRA_BUNDLE_PATH,
            username=ASTRA_CLIENT_ID,
            password=ASTRA_CLIENT_SECRET,
            keyspace=ASTRA_KEYSPACE,
            schema_metadata_enabled=False,  # Chave para resolver o erro de permissão
            protocol_version=4
        )

        logging.info("Conexão com o banco de dados estabelecida com sucesso!")

    except Exception as e:
        logging.error(f"Erro fatal ao conectar ao Cassandra: {e}", exc_info=True)
        raise

async def disconnect_from_db_async():
    logging.info("Fechando a conexão com o banco de dados...")
    await connection.disconnect_async()
    logging.info("Conexão com o banco de dados fechada.")
